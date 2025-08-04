# src/nodes/data_validator.py
from src.state.state import State
from src.LLMs.groq import GroqLLM

class DataValidator:
    def __init__(self, llm_agent=None):
        self.llm_agent = llm_agent
    
    async def process(self, state: State) -> dict:
        """
        Clean validation process - LLM handles everything with bound tools
        """
        
        # Get data from state
        areas_with_increases = state["messages"][-1]
        print(f"DATAVALIDATOR, -----Areas with Increases-----: {areas_with_increases}")
        print(f"DATAVALIDATOR, *********END*********")
        original_data = state["messages"][0] if state["messages"] else ""
        
        validation_prompt = f"""
            Search the web for reasons for tyre cost increase in india for the categories in {areas_with_increases} and keep the response specific to them. 
            
        """

        try:
            # With bind_tools(), you invoke directly on the model
            response = await self.llm_agent.ainvoke(validation_prompt)
            
            print(f"DATAVALIDATOR, -----Validation Response-----:", response)
            
            # The response structure might be different - check what's returned
            content = response.content if hasattr(response, 'content') else str(response)
            
            return {
                "messages": state["messages"] + ["Data validation completed"],
                "validation_results": content
            }
            
        except Exception as e:
            return {
                "messages": state["messages"] + [f"Validation error: {str(e)}"],
                "validation_results": None
            }
