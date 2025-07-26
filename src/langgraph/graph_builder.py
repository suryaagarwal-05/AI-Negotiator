#This file be responsible for building the graph

from langgraph.graph import StateGraph, START, END
from src.nodes.data_parser import dataParser
from src.nodes.category_classifier import categoryClassifier
from src.nodes.data_validator import dataValidator
from src.nodes.result_analyser import resultAnalyser
from src.nodes.output_generator import outputGenerator

from src.LLMs.groq import GroqLLM
from src.state.state import State

class GraphBuilder:
  def __init__(self):
    
    self.graph_builder = StateGraph(State)
    self.llm = GroqLLM.get_llm_model()
    
  def negotiator_graph(self, csv_data):
    #tools
    
    #nodes
    ##TODO: remove hardcoded strings and implement real functions to use
    self.graph_builder.add_node("parser", dataParser(self.llm).process)
    self.graph_builder.add_node("classifier", categoryClassifier(self.llm).process)
    self.graph_builder.add_node("validator", dataValidator(self.llm).process)
    # self.graph_builder.add_node("analyzer", resultAnalyser(self.llm))
    # self.graph_builder.add_node("generator", outputGenerator(self.llm))
    
    
    #edges
    self.graph_builder.add_edge(START, "parser")
    self.graph_builder.add_edge("parser", "classifier")
    self.graph_builder.add_edge("classifier", "validator")
    # self.graph_builder.add_edge("validator", "analyzer")
    # self.graph_builder.add_edge("analyzer", "generator")
    # self.graph_builder.add_edge("generator", END)
    self.graph_builder.add_edge("validator", END)
    
    compiled_graph = self.graph_builder.compile()
  
    
    initial_state = {
            "messages": [f"Please parse this CSV data and classify the sections or areas in which the values are increased:\n\n{csv_data}"]
        }
        
    return compiled_graph.invoke(initial_state)