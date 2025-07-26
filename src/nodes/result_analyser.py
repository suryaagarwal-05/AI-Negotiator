from src.state.state import State

class resultAnalyser:
    def __init__(self,model):
        self.llm = model

    def process(self, state:State) -> dict:
        """Invoke llm model"""
        return {"messages":self.llm.invoke(state["messages"])}