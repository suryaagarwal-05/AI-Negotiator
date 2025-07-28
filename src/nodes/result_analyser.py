from src.state.state import State
from langchain_core.messages import SystemMessage, HumanMessage


class resultAnalyser:
    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Analyze validator output and generate negotiation strategies for price increases
        """
        # Extract the last message from validator
        validator_output = state["messages"][-1].content if state["messages"] else ""
        
        # Create analysis prompt
        analysis_prompt = self._create_analysis_prompt(validator_output)
        
        # Prepare messages for LLM
        messages = [
            SystemMessage(content=self._get_system_prompt()),
            HumanMessage(content=analysis_prompt)
        ]
        
        # Invoke LLM for analysis
        response = self.llm.invoke(messages)
        
        # Add the analysis to state messages and return the updated state
        updated_messages = state["messages"] + [response]
        
        # Return the state format
        return {"messages": updated_messages}

    def _get_system_prompt(self) -> str:
        """System prompt for negotiation strategy analysis"""
        return """
        You are an expert business negotiation strategist specializing in price increase scenarios. 
        Your role is to analyze validated data about price increases and provide actionable negotiation strategies.
        
        Key responsibilities:
        1. Analyze the validated price increase data and trends
        2. Identify leverage points and negotiation opportunities
        3. Provide specific, actionable negotiation strategies
        4. Consider both supplier and buyer perspectives
        5. Suggest alternative approaches and compromise solutions
        
        Always structure your response with:
        - Executive Summary
        - Key Findings from Analysis
        - Negotiation Strategies
        - Risk Assessment
        - Recommended Actions
        """

    def _create_analysis_prompt(self, validator_output: str) -> str:
        """Create detailed analysis prompt based on validator output"""
        return f"""
        Please analyze the following validated price increase data and provide comprehensive negotiation strategies:

        VALIDATED DATA:
        {validator_output}

        ANALYSIS REQUIREMENTS:
        1. **Data Analysis**:
           - Identify the most significant price increases by category/item
           - Determine patterns and trends in the price changes
           - Calculate overall impact and percentage increases
           - Highlight any anomalies or unusual increases

        2. **Market Context Assessment**:
           - Evaluate if increases align with market trends
           - Identify potential external factors (inflation, supply chain, etc.)
           - Assess reasonableness of proposed increases

        3. **Negotiation Strategy Development**:
           - **Immediate Actions**: What to do first in negotiations
           - **Leverage Points**: Areas where you have negotiating power
           - **Alternative Solutions**: Creative approaches to minimize impact
           - **Compromise Scenarios**: Win-win propositions
           - **Timeline Strategies**: Phased implementation options

        4. **Risk Assessment**:
           - **High Risk Areas**: Categories with excessive increases
           - **Supplier Relationship Impact**: How to maintain partnerships
           - **Budget Impact**: Financial implications and mitigation

        5. **Tactical Recommendations**:
           - Specific talking points for negotiations
           - Data-driven arguments to present
           - Potential counteroffers and alternatives
           - Long-term relationship preservation strategies

        Please provide a structured, actionable response that a procurement professional can immediately implement.
        """