from agent import graph
from langchain_core.messages import HumanMessage
import sys

def run_workflow(user_input: str):
    """Run the workflow with the given input and return the result."""
    final_step = {}
    
    # Configure with recursion limit as safety measure
    config = {"recursion_limit": 15}
    step_count = 0
    try:
        for step in graph.stream({"messages": [HumanMessage(content=user_input)]}, config=config):
            node_name = list(step.keys())[0]
            step_data = list(step.values())[0]
            step_count += 1
            
            # Optional: Uncomment for debugging
            # print(f"Step {step_count} - Agent: {node_name}")
                
            # Keep track of the latest step
            final_step = step
        
        # Workflow completed successfully
        
    except Exception as e:
        print(f"Error during workflow execution: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    return final_step

def get_user_input(prompt: str) -> str:
    """Get input from user with a prompt."""
    return input(f"\n{prompt}\nYour response: ").strip()

def main(user_input: str):
    print(f"Starting trip planning for: {user_input}")
    
    # Run the workflow
    final_step = run_workflow(user_input)
    
    if not final_step:
        print("Workflow failed to execute.")
        return
    
    # Check if we need more information
    final_state = list(final_step.values())[0]
    missing_info = final_state.get("missing_info")
    

    
    if missing_info:
        print(f"\n{final_state['messages'][-1].content}")
        
        # Get the missing information from user
        extracted_info = final_state.get("extracted_info", {})
        updated_info = extracted_info.copy()
        
        for missing_item in missing_info:
            if "departure" in missing_item.lower():
                departure = get_user_input("Please provide the departure city (e.g., Mumbai, New York, London):")
                # Convert city name to IATA code (simplified mapping)
                city_to_iata = {
                    "mumbai": "BOM", "new york": "JFK", "london": "LHR", "paris": "CDG",
                    "tokyo": "NRT", "delhi": "DEL", "bangalore": "BLR", "dubai": "DXB",
                    "singapore": "SIN", "sydney": "SYD", "melbourne": "MEL", "toronto": "YYZ",
                    "vancouver": "YVR", "montreal": "YUL", "berlin": "BER", "madrid": "MAD",
                    "rome": "FCO", "amsterdam": "AMS", "barcelona": "BCN", "milan": "MXP",
                    "vienna": "VIE", "prague": "PRG", "zurich": "ZUR", "geneva": "GVA"
                }
                updated_info["departure"] = city_to_iata.get(departure.lower(), departure.upper()[:3])
                
            elif "arrival" in missing_item.lower():
                arrival = get_user_input("Please provide the destination city (e.g., Paris, London, Tokyo):")
                city_to_iata = {
                    "mumbai": "BOM", "new york": "JFK", "london": "LHR", "paris": "CDG",
                    "tokyo": "NRT", "delhi": "DEL", "bangalore": "BLR", "dubai": "DXB",
                    "singapore": "SIN", "sydney": "SYD", "melbourne": "MEL", "toronto": "YYZ",
                    "vancouver": "YVR", "montreal": "YUL", "berlin": "BER", "madrid": "MAD",
                    "rome": "FCO", "amsterdam": "AMS", "barcelona": "BCN", "milan": "MXP",
                    "vienna": "VIE", "prague": "PRG", "zurich": "ZUR", "geneva": "GVA"
                }
                updated_info["arrival"] = city_to_iata.get(arrival.lower(), arrival.upper()[:3])
                
            elif "date" in missing_item.lower():
                date = get_user_input("Please provide the travel date (e.g., 2024-12-25, December 25, 2024, or 'next month'):")
                # Try to parse the date
                try:
                    from dateutil.parser import parse
                    parsed_date = parse(date, fuzzy=True)
                    updated_info["date"] = parsed_date.strftime("%Y-%m-%d")
                except:
                    updated_info["date"] = date
                    
            elif "city" in missing_item.lower():
                city = get_user_input("Please provide the destination city for hotel booking:")
                city_to_iata = {
                    "mumbai": "BOM", "new york": "NYC", "london": "LON", "paris": "PAR",
                    "tokyo": "TYO", "delhi": "DEL", "bangalore": "BLR", "dubai": "DXB",
                    "singapore": "SIN", "sydney": "SYD", "melbourne": "MEL", "toronto": "YTO",
                    "vancouver": "YVR", "montreal": "YMQ", "berlin": "BER", "madrid": "MAD",
                    "rome": "ROM", "amsterdam": "AMS", "barcelona": "BCN", "milan": "MIL",
                    "vienna": "VIE", "prague": "PRG", "zurich": "ZUR", "geneva": "GVA"
                }
                updated_info["city_code"] = city_to_iata.get(city.lower(), city.upper()[:3])
                
            elif "checkin" in missing_item.lower():
                checkin = get_user_input("Please provide the check-in date (e.g., 2024-12-25, December 25, 2024):")
                try:
                    from dateutil.parser import parse
                    parsed_date = parse(checkin, fuzzy=True)
                    updated_info["checkin_date"] = parsed_date.strftime("%Y-%m-%d")
                except:
                    updated_info["checkin_date"] = checkin
                    
            elif "checkout" in missing_item.lower():
                checkout = get_user_input("Please provide the check-out date (e.g., 2024-12-30, December 30, 2024):")
                try:
                    from dateutil.parser import parse
                    parsed_date = parse(checkout, fuzzy=True)
                    updated_info["checkout_date"] = parsed_date.strftime("%Y-%m-%d")
                except:
                    updated_info["checkout_date"] = checkout
        
        # Create updated query with the new information
        updated_query = f"Plan a trip from {updated_info.get('departure', '')} to {updated_info.get('arrival', '')} on {updated_info.get('date', '')}"
        if updated_info.get('checkin_date') and updated_info.get('checkout_date'):
            updated_query += f" with check-in on {updated_info['checkin_date']} and check-out on {updated_info['checkout_date']}"
        
        print(f"\nThank you! Now planning your trip with the updated information...")
        print(f"Updated query: {updated_query}")
        
        # Run the workflow again with updated information
        final_step = run_workflow(updated_query)
        
        if not final_step:
            print("Workflow failed to execute with updated information.")
            return
        
        # Check if the second run also needs more information
        final_state = list(final_step.values())[0]
        missing_info_2 = final_state.get("missing_info")
        

        
        if missing_info_2:
            print(f"\nI still need more information: {', '.join(missing_info_2)}")
            print("Let me ask for the remaining details...")
            
            # Get the additional missing information
            extracted_info_2 = final_state.get("extracted_info", {})
            updated_info_2 = extracted_info_2.copy()
            
            for missing_item in missing_info_2:
                if "checkin" in missing_item.lower():
                    checkin = get_user_input("Please provide the check-in date for your hotel (e.g., 2025-12-25, December 25, 2025):")
                    try:
                        from dateutil.parser import parse
                        parsed_date = parse(checkin, fuzzy=True)
                        updated_info_2["checkin_date"] = parsed_date.strftime("%Y-%m-%d")
                    except:
                        updated_info_2["checkin_date"] = checkin
                        
                elif "checkout" in missing_item.lower():
                    checkout = get_user_input("Please provide the check-out date for your hotel (e.g., 2025-12-30, December 30, 2025):")
                    try:
                        from dateutil.parser import parse
                        parsed_date = parse(checkout, fuzzy=True)
                        updated_info_2["checkout_date"] = parsed_date.strftime("%Y-%m-%d")
                    except:
                        updated_info_2["checkout_date"] = checkout
            
            # Create final updated query
            final_query = f"Plan a trip from {updated_info.get('departure', '')} to {updated_info.get('arrival', '')} on {updated_info.get('date', '')}"
            if updated_info_2.get('checkin_date') and updated_info_2.get('checkout_date'):
                final_query += f" with check-in on {updated_info_2['checkin_date']} and check-out on {updated_info_2['checkout_date']}"
            
            print(f"\nPerfect! Now planning your complete trip...")
            print(f"Final query: {final_query}")
            
            # Run the workflow one more time with all information
            final_step = run_workflow(final_query)
            
            if not final_step:
                print("Workflow failed to execute with complete information.")
                return
    
    # --- Final summary ---
    if final_step:
        final_state = list(final_step.values())[0]
        final_data = final_state.get("final_data")
        
        if final_data:
            print(final_data)
        else:
            print("No final trip plan was generated.")
    else:
        print("No steps were executed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main2.py '<your travel query>'")
        sys.exit(1)
        
    query = " ".join(sys.argv[1:])
    main(query)
