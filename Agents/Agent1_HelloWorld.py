from typing import TypedDict
from langgraph.graph import StateGraph

class HelloWorldState(TypedDict):
    message : str


def greeter(state : HelloWorldState) -> HelloWorldState:
    """Simple function to greet the world."""
    #return {"message": "Hello, World!!"}
    state["message"] = "Hello " + state["message"] + ", Hows it going?"
    return state

graph = StateGraph(HelloWorldState)
graph.add_node("greet", greeter)
graph.set_entry_point("greet")
graph.set_finish_point("greet")
app = graph.compile()

'''
# Visualize the graph
from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))
'''

result = app.invoke({"message": "Bob"})
print(result["message"])