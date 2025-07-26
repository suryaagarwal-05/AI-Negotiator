import pandas as pd
from src.langgraph.graph_builder import GraphBuilder

from dotenv import load_dotenv
load_dotenv()

def run_negotiator(csv_path):
    # Step 1: Read CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"Loaded file with columns: {list(df.columns)}")
    
       # Step 2: Call langgraph function to start the negotiation process
    graph_builder = GraphBuilder()
    
    # Convert DataFrame to string representation for LLM processing
    csv_data = df.to_string(index=False)
    
    # Pass the actual data instead of a hardcoded message
    result = graph_builder.negotiator_graph(csv_data)
    print("Negotiation Result:", result)

    
 
