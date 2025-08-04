import pandas as pd
from src.langgraph.graph_builder import run_negotiator_graph  # Import the wrapper
from dotenv import load_dotenv

load_dotenv()

def extract_pdf_path_from_messages(result):
    # Search messages from the end for the PDF file path message.
    if not result or 'messages' not in result:
        return None
    messages = result['messages']
    for msg in reversed(messages):
        # Each message can be an object (with attribute 'content') or dict with 'content', or a plain string
        content = None
        if isinstance(msg, dict):
            content = msg.get('content')
        elif hasattr(msg, 'content'):
            content = getattr(msg, 'content')
        elif isinstance(msg, str):
            content = msg
        if content and 'PDF report generated at:' in content:
            return content.split('PDF report generated at:')[-1].strip()
    return None

async def run_negotiator(csv_path):
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"Loaded file with columns: {list(df.columns)}")
    csv_data = df.to_string(index=False)
    result = await run_negotiator_graph(csv_data)
    print("Negotiation Result:", result)

    pdf_path = extract_pdf_path_from_messages(result)
    print("Extracted PDF Path:", pdf_path)
    return {"pdf_path": pdf_path}
