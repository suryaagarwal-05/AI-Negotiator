from src.state.state import State

class categoryClassifier:
    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """Classify the parsed data into standard business categories"""
        
        if not state["messages"]:
            return {"messages": ["No data received from parser for classification"]}
        
        # Get the parsed data
        parsed_data = state["messages"][-1]
        
        # Simple classification prompt
        classification_prompt = f"""
        Based on the following parsed data, classify the information into these standard business categories:

        1. FINANCIAL (revenue, costs, profits, budgets)
        2. OPERATIONAL (efficiency, productivity, quality)
        3. CUSTOMER (satisfaction, acquisition, retention)
        4. MARKET (share, growth, competition)
        5. HUMAN RESOURCES (headcount, salaries, training)
        6. TECHNOLOGY (systems, automation, digital)

        Parsed Data:
        {parsed_data}

        Please classify each data point and identify which categories show increases. 
        Format your response clearly with category headers and bullet points.
        """
        
        try:
            classification_result = self.llm.invoke(classification_prompt)
            return {"messages": state["messages"] + [f"CLASSIFICATION:\n{classification_result}"]}
        
        except Exception as e:
            return {"messages": state["messages"] + [f"Classification error: {str(e)}"]}
