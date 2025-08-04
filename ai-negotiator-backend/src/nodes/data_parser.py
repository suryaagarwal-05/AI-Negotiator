from src.state.state import State

class dataParser:
    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """Parse and analyze the CSV data"""
        
        # Get the last message (which should contain the CSV data)
        if state["messages"]:
            csv_data_message = state["messages"][-1]
            
            # Create a more specific prompt for data parsing
            parsing_prompt = f"""
            You are an expert data summarizer. 
            Read the following CSV data.
            Return ONLY a concise summary listing each specific area mentioned in the proposal_text where a price increase is stated, including the reason and the exact percentage increase for each.
            Do NOT include any explanation, classification, column names, or any information not explicitly present in the CSV.
            Summarize only the price increases, mentioning the precise cause and percent as provided in the CSV proposal_text. 
            Do not combine, change, or omit any details from the original entries.

            Data to analyze:
            {csv_data_message}
            """

            
            # Invoke the LLM with the parsing prompt
            response = self.llm.invoke(parsing_prompt)
            print("111111111111111111111111111111111111111111", response)
            
            # Return the updated state
            return {"messages": [response]}
        else:
            return {"messages": ["No data provided for parsing"]}
