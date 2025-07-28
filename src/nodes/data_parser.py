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
            You are a data analyst. Please analyze the following CSV data and:
            1. Identify the structure and columns
            2. Classify different sections or categories
            3. Identify areas where values have increased
            4. Provide a summary of your findings
            5. Keep the response concise and focused on the increases(do not mention useless things.)
            
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
