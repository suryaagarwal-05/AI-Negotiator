#This file will have state to be used in graph

from typing_extensions import TypedDict, List
from typing import Annotated
from langgraph.graph import add_messages

class State(TypedDict):
    """
    Represents the state of the graph.
    """
    
    messages : Annotated[List, add_messages]
    
    
    