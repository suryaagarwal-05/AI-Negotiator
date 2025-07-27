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
        if not state.get("areas_with_increases") or not state["messages"]:
            return {
                "messages": state["messages"] + ["No data to validate"],
                "validation_results": None
            }
        
        # Get data from state
        areas_with_increases = state["areas_with_increases"]
        original_data = state["messages"][0] if state["messages"] else ""
        
        # Simple, comprehensive prompt
        validation_prompt = f"""
        Validate these areas showing increases by searching for current information:

        AREAS WITH INCREASES: {areas_with_increases}
        ORIGINAL CONTEXT: {original_data}

        Please search for and analyze:
        1. Recent news about these areas to verify the increases
        2. Competitor pricing and market data for comparison  
        3. Industry trends and market context

        Provide a comprehensive validation report with your findings and recommendations.
        """
        
        try:
            # Let the agent handle everything
            response = await self.llm_agent.ainvoke({
                "messages": [{"role": "user", "content": validation_prompt}]
            })
            
            return {
                "messages": state["messages"] + ["Data validation completed"],
                "validation_results": response['messages'][-1].content
            }
            
        except Exception as e:
            return {
                "messages": state["messages"] + [f"Validation error: {str(e)}"],
                "validation_results": None
            }