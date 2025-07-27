import json, os
from src.state.state import State

class categoryClassifier:
    def __init__(self, model):
        self.llm = model
        config_path = "/Users/surya/Developer/AI-Negotiator/src/config/config.json"
        with open(config_path, 'r') as f:
            self.config = json.load(f)

    def process(self, state: State) -> dict:
        """
        Use LLM to classify data and identify areas with increases
        """
        if not state["messages"]:
            return {"messages": ["No data to classify"],
                    "areas_with_increases": []}

        text = state["messages"][-1]
        
        # Convert config to string for prompt
        config_string = json.dumps(self.config, indent=2)
        
        classification_prompt = f"""
        You are given the following configuration with business categories and increment indicators:
        
        {config_string}
        
        Analyze the following parsed data and classify it:
        
        {text}
        
        Instructions:
        - Look for data points that match the category keywords
        - Check if those data points show any increment indicators
        - Return only categories that have BOTH matching keywords AND increment indicators
        
        Return response as JSON:
        {{
            "areas_with_increases": ["CATEGORY1", "CATEGORY2"],
            "details": "Brief explanation"
        }}
        """
        
        print(f"-----Classification Prompt------: {classification_prompt}")  # Debugging output
        
        try:
            response = self.llm.invoke(classification_prompt)
            print(f"-----LLM Response-----: {response}")  # Debugging output
            
            try:
                parsed_response = json.loads(response)
                areas_with_increases = parsed_response.get("areas_with_increases", [])
                details = parsed_response.get("details", "")
                
                print(f"-----Classification Details-----:", {
                    "messages": state["messages"] + [f"Areas with increments: {areas_with_increases}\nDetails: {details}"],
                    "areas_with_increases": areas_with_increases
                })
                
                return {
                    "messages": state["messages"] + [f"Areas with increments: {areas_with_increases}\nDetails: {details}"],
                    "areas_with_increases": areas_with_increases
                }
                
            except json.JSONDecodeError:
                return {
                    "messages": state["messages"] + [f"Classification: {response}"],
                    "areas_with_increases": []
                }
                
        except Exception as e:
            return {
                "messages": state["messages"] + [f"Classification error: {str(e)}"],
                "areas_with_increases": []
            }
