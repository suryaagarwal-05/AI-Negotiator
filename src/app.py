import pandas as pd
from src.langgraph.graph_builder import run_negotiator_graph  # Import the wrapper
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
    
    # Step 2: Use the synchronous wrapper
    csv_data = df.to_string(index=False)
    result = run_negotiator_graph(csv_data)  # This handles async internally
    print("Negotiation Result:", result)
