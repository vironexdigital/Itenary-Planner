from dotenv import load_dotenv
from amadeus import Client, ResponseError
from geopy.geocoders import Nominatim
import os, requests, time

load_dotenv()

#AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
#OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")  Not useful for free tier
# Direct Amadeus client to bypass SDK issues
class AmadeusDirectClient:
    def __init__(self, client_id, client_secret, environment='test'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = environment
        self.base_url = f"https://{environment}.api.amadeus.com" if environment == 'test' else "https://api.amadeus.com"
        self.access_token = None
        self.token_expires_at = 0
    
    def get_access_token(self):
        """Get OAuth access token."""
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        url = f"{self.base_url}/v1/security/oauth2/token"
        
        response = requests.post(url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
        )
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.token_expires_at = time.time() + token_data['expires_in'] - 60
            return self.access_token
        else:
            raise Exception(f"OAuth failed: {response.status_code} - {response.text}")
    
    def search_flights(self, origin, destination, departure_date, adults=1, max_results=3):
        """Search for flights using direct HTTP calls."""
        token = self.get_access_token()
        
        url = f"{self.base_url}/v2/shopping/flight-offers"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': departure_date,
            'adults': adults,
            'max': max_results
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Flight search failed: {response.status_code} - {response.text}")

# Initialize the direct client
amadeus_direct = AmadeusDirectClient(AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET, 'test')

# Keep the original client for hotel searches (they might work)
amadeus = Client(
        client_id=AMADEUS_CLIENT_ID,
        client_secret=AMADEUS_CLIENT_SECRET,
        hostname='test'
                )

# --------- FLIGHT API ----------
# Uncomment the following lines if you want to use AviationStack API (but unreliable for future flights and limited calls)
# def get_flights_data(departure, arrival, date=None):
#     url = "http://api.aviationstack.com/v1/flights"
#     params = {
#         "access_key": AVIATIONSTACK_API_KEY,
#         "dep_iata": departure,
#         "arr_iata": arrival,
#         "flight_status": "scheduled",
#         "flight_date": date  # if needed
#     }
#     try:
#         res = requests.get(url, params=params)
#         res.raise_for_status()
#         return res.json().get("data", [])[:3]
#     except Exception as e:
#         return [{"error": str(e)}]
def get_flights_data(departure, arrival, date=None):
    try:
        # Use the direct client instead of the SDK
        response = amadeus_direct.search_flights(
            origin=departure.upper(),
            destination=arrival.upper(),
            departure_date=date,
            adults=1,
            max_results=3
        )

        flights = response.get('data', [])
        top_flights = []

        for flight in flights:
            itinerary = flight['itineraries'][0]
            segments = itinerary['segments']
            duration = itinerary['duration']
            price = flight['price']['total']
            currency = flight['price']['currency']

            top_flights.append({
                "price": f"{price} {currency}",
                "duration": duration,
                "segments": [
                    {
                        "from": seg['departure']['iataCode'],
                        "to": seg['arrival']['iataCode'],
                        "airline": seg['carrierCode'],
                        "flightNumber": seg['number'],
                        "departureTime": seg['departure']['at'],
                        "arrivalTime": seg['arrival']['at']
                    } for seg in segments
                ]
            })

        return top_flights

    except Exception as e:
        return [{"error": str(e)}]

# --------- HOTEL API (Amadeus) ----------
def get_hotels_data(city_code: str, checkin_date: str, checkout_date: str, adults: int = 1):
    """
    Implements the two-phase hotel search to fetch offers for a given city.

    This function first uses the Hotel List API to find hotel IDs for a city,
    and then uses the Hotel Search API to get real-time offers for those hotels.

    Args:
        amadeus: An initialized Amadeus API client instance.
        city_code: The IATA code for the city (e.g., 'PAR').
        checkin_date: The check-in date in 'YYYY-MM-DD' format.
        checkout_date: The check-out date in 'YYYY-MM-DD' format.
        adults: The number of adults per room.

    Returns:
        A list of hotel offer dictionaries, or an error dictionary if an issue occurs.
    """
    # --- Phase 1: Get Hotel IDs from City Code ---
    # This call translates the city code into a list of specific hotel properties.
    try:
        hotel_list_response = amadeus.reference_data.locations.hotels.by_city.get(
            cityCode=city_code
        )
        hotels = hotel_list_response.data
    except ResponseError as e:
        return [{"error": f"Hotel List API Error: {e}"}]

    # --- Edge Case Handling for Phase 1 ---
    # If the Hotel List API returns no hotels, there is nothing to search for.
    if not hotels:
        return [{"message": f"No hotels found for city code: {city_code}"}]

    # Extract the hotel IDs from the response. The Hotel Search API requires these.
    hotel_ids = [hotel['hotelId'] for hotel in hotels]

    # --- Phase 2: Get Hotel Offers from Hotel IDs ---
    # This call uses the collected hotel IDs to find real-time offers.
    try:
        hotel_offers_response = amadeus.shopping.hotel_offers_search.get(
            hotelIds=','.join(hotel_ids[:20]),  # Using a slice to respect API limits
            adults=adults,
            checkInDate=checkin_date,
            checkOutDate=checkout_date,
            roomQuantity=1,
            bestRateOnly=True # This valid parameter can be used
        )
        offers = hotel_offers_response.data
    except ResponseError as e:
        # Handle API errors during the offer search.
        return [{"error": f"Hotel Offers API Error: {e}"}]

    # --- Edge Case Handling for Phase 2 ---
    # If hotels were found but no offers are available for the given dates.
    if not offers:
        return [{"message": f"No offers available for the hotels in {city_code} on the selected dates."}]

    return offers
# --------- WEATHER API ----------
# def get_weather_data(city):
#     url = "https://api.openweathermap.org/data/2.5/weather"
#     params = {
#         "q": city,
#         "appid": OPENWEATHER_API_KEY,
#         "units": "metric"
#     }
#     try:
#         res = requests.get(url, params=params)
#         res.raise_for_status()
#         return res.json()
#     except Exception as e:
#         return {"error": str(e)}

# --------- RESTAURANTS ----------
def get_city_coordinates(city):
    """
    Returns the latitude and longitude of a city using Nominatim with fallback support.
    Includes comprehensive error handling for SSL and network issues.
    """
    # First try hardcoded coordinates for common cities
    fallback_coords = get_fallback_coordinates(city)
    if fallback_coords:
        return fallback_coords
    
    # Try geocoding with error handling
    try:
        geolocator = Nominatim(user_agent="restaurant_agent")
        location = geolocator.geocode(city, timeout=5)
        if location:
            return location.latitude, location.longitude
        else:
            # Return default coordinates (London) as last resort
            return 51.5074, -0.1278
            
    except Exception as e:
        # Return default coordinates (London) as last resort
        return 51.5074, -0.1278

def get_fallback_coordinates(city):
    """
    Returns hardcoded coordinates for common cities as fallback.
    """
    city_lower = city.lower().strip()
    
    fallback_coords = {
        'paris': (48.8566, 2.3522),
        'london': (51.5074, -0.1278),
        'new york': (40.7128, -74.0060),
        'nyc': (40.7128, -74.0060),
        'tokyo': (35.6762, 139.6503),
        'madrid': (40.4168, -3.7038),
        'rome': (41.9028, 12.4964),
        'berlin': (52.5200, 13.4050),
        'amsterdam': (52.3676, 4.9041),
        'barcelona': (41.3851, 2.1734),
        'milan': (45.4642, 9.1900),
        'vienna': (48.2082, 16.3738),
        'prague': (50.0755, 14.4378),
        'zurich': (47.3769, 8.5417),
        'geneva': (46.2044, 6.1432),
        'dubai': (25.2048, 55.2708),
        'singapore': (1.3521, 103.8198),
        'hong kong': (22.3193, 114.1694),
        'sydney': (-33.8688, 151.2093),
        'melbourne': (-37.8136, 144.9631),
        'los angeles': (34.0522, -118.2437),
        'san francisco': (37.7749, -122.4194),
        'chicago': (41.8781, -87.6298),
        'mumbai': (19.0760, 72.8777),
        'delhi': (28.7041, 77.1025),
        'bangalore': (12.9716, 77.5946),
        'toronto': (43.6532, -79.3832),
        'vancouver': (49.2827, -123.1207),
        'montreal': (45.5017, -73.5673)
    }
    
    return fallback_coords.get(city_lower)
    
def get_restaurants_data(lat, lon, radius=1000, limit=5):
    """
    Fetch nearby restaurants using Overpass API with coordinates.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.
        radius (int): Radius in meters.
        limit (int): Number of restaurants.

    Returns:
        List of restaurants or error dict.
    """
    try:
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        node
          ["amenity"="restaurant"]
          (around:{radius},{lat},{lon});
        out body;
        """
        res = requests.post(overpass_url, data={"data": query})
        res.raise_for_status()
        data = res.json()

        restaurants = []
        for element in data.get("elements", [])[:limit]:
            tags = element.get("tags", {})
            restaurants.append({
                "name": tags.get("name", "Unnamed Restaurant"),
                "cuisine": tags.get("cuisine", "Unknown"),
                "lat": element.get("lat"),
                "lon": element.get("lon"),
                "address": tags.get("addr:full") or f"{tags.get('addr:street', '')} {tags.get('addr:housenumber', '')}".strip()
            })

        return restaurants

    except Exception as e:
        return {"error": str(e)}

