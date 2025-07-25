#This file be responsible for building the graph

from langgraph.graph import StateGraph

from src.LLMs import GroqLLM
from src.state import State

class GraphBuilder:
  def __init__(self):
    self.graph_builder = StateGraph(State)
    self.llm = GroqLLM.get_llm_model()