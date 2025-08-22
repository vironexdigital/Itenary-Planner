from agent import graph
from langchain_core.messages import HumanMessage
import sys

def main(user_input: str):
    final_step = {}

    print(f"Starting trip planning for: {user_input}")
    
    # Configure with recursion limit as safety measure
    config = {"recursion_limit": 15}
    for step in graph.stream({"messages": [HumanMessage(content=user_input)]}, config=config):
        node_name = list(step.keys())[0]
        step_data = list(step.values())[0]

       # if node_name != "TripAgent":
       #     print(f"Current Agent: {node_name}")
        # Show current agent working
       # print(f"Current Agent: {node_name}")
            
        # Keep track of the latest step
        final_step = step
    
    # --- Final summary ---
    if final_step:
        final_state = list(final_step.values())[0]
        final_data = final_state.get("final_data")
        
        if final_data:
           # print("\n" + "="*50)
           # print("FINAL TRIP PLAN")
           # print("="*50)
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
