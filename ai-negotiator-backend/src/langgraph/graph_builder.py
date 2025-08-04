# graph_builder.py
from langgraph.graph import StateGraph, START, END
from src.nodes.data_parser import dataParser
from src.nodes.category_classifier import categoryClassifier
from src.nodes.data_validator import DataValidator
from src.nodes.result_analyser import resultAnalyser
from src.nodes.output_generator import outputGenerator

from src.LLMs.groq import GroqLLM
from src.state.state import State
import asyncio

csv_data = "/Users/surya/Developer/AI-Negotiator/ai-negotiator-backend/data.csv"

class GraphBuilder:
    def __init__(self):
        self.graph_builder = StateGraph(State)
        self.llm = GroqLLM.get_llm_model()  # Basic LLM for parsing/classification
        self.llm_with_tools = None  # Will be initialized async
        
    async def _initialize_tools(self):
        """Initialize LLM with tools for validation"""
        if self.llm_with_tools is None:
            self.llm_with_tools = await GroqLLM.get_llm_with_tools()
    
    async def negotiator_graph(self, csv_data):
        # Initialize tools if needed
        await self._initialize_tools()
        
        # Build graph
        self.graph_builder.add_node("parser", dataParser(self.llm).process)
        self.graph_builder.add_node("classifier", categoryClassifier(self.llm).process)
        self.graph_builder.add_node("validator", DataValidator(self.llm_with_tools).process)
        self.graph_builder.add_node("analyzer", resultAnalyser(self.llm).process)
        self.graph_builder.add_node("generator", outputGenerator(self.llm).process)
        
        # Add edges
        self.graph_builder.add_edge(START, "parser")
        self.graph_builder.add_edge("parser", "classifier") 
        self.graph_builder.add_edge("classifier", "validator")
        self.graph_builder.add_edge("validator", "analyzer")
        self.graph_builder.add_edge("analyzer", "generator")
        self.graph_builder.add_edge("generator", END)
        # self.graph_builder.add_edge("analyzer", END)
        
        compiled_graph = self.graph_builder.compile()
        
        initial_state = {
            "messages": [f"Please parse this CSV data and classify the sections or areas in which the values are increased:\n\n{csv_data}"]
        }
        
        # Use ainvoke for async execution
        return await compiled_graph.ainvoke(initial_state)

# Usage wrapper to handle async
async def run_negotiator_graph(csv_data):
    """Synchronous wrapper for the async graph"""
    # async def _run():
    builder = GraphBuilder()
    return await builder.negotiator_graph(csv_data)
    
    # return asyncio.run(_run())
    
run_negotiator_graph(csv_data)