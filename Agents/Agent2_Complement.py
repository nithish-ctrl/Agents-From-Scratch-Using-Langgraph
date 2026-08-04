from typing import TypedDict
from langgraph.graph import StateGraph

class ComplementState(TypedDict):
    name : str
    result : str

def complementNode(state : ComplementState) -> ComplementState:
    """Simple function to complement the name add to the state."""
    state["result"] = "Hi " + state["name"] + ", you look great today!!. You look stunning!!"
    return state

graph = StateGraph(ComplementState)
graph.add_node("complement", complementNode)
graph.set_entry_point("complement")
graph.set_finish_point("complement")

app = graph.compile()



result = app.invoke({"name": "Snigdha", "result":""})
print(result["result"])

