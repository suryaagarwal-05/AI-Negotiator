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
        print(f"DATAVALIDATOR, -----Areas with Increases-----: {areas_with_increases}")  # Debugging output
        print(f"DATAVALIDATOR, *********END*********")  # Debugging output
        original_data = state["messages"][0] if state["messages"] else ""
        
        # AREAS WITH INCREASES: {areas_with_increases}
        
        # Optimized prompt for Tavily MCP tools
        validation_prompt = f"""
You have access to Tavily search tools that can search the web, news, and provide real-time information. You must make only **one tool call** to fetch all required information for price increase for tyres in india.

Your task:
- Conduct a **single search operation** that gathers concise, high-quality insights for each area listed.
Respond with only the necessary, actionable content. Be direct, structured, and avoid filler.
"""


        try:
            # Let the agent handle everything
            response = await self.llm_agent.ainvoke({
                "messages": [{"role": "user", "content": validation_prompt}]
            })
            
            print(f"DATAVALIDATOR, -----Validation Response-----:",response)  # Debugging output
            
            return {
                "messages": state["messages"] + ["Data validation completed"],
                "validation_results": response['messages'][-1].content
            }
            
        except Exception as e:
            return {
                "messages": state["messages"] + [f"Validation error: {str(e)}"],
                "validation_results": None
            }