from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class ConditionalState(TypedDict):
    name : str
    age : int
    skill : str
    role : str
    final : str

def nameNode(state: ConditionalState) -> ConditionalState:
    state["final"] = f'Hi {state["name"]}, Welcome to the community !!.'
    return state

def childNode(state: ConditionalState) -> ConditionalState:
    state["final"] += f' You are a child, you can explore the kids learning section.'
    return state

def adultNode(state: ConditionalState) -> ConditionalState:
    state["final"] += f' You are an adult, you can join the community meetings. '
    return state

def deciderNode(state: ConditionalState):
    if state["age"] < 18 : return "childNode"
    else : return "adultNode"

def skillNode(state : ConditionalState) -> ConditionalState:
    state["final"] += f'Your skill is {state["skill"]}.'
    return state

def internNode(state: ConditionalState) -> ConditionalState:
    state["final"] += f'Your role is {state["role"]}. You can explore your role specific resources.'
    return state

def FteNode(state: ConditionalState) -> ConditionalState:
    state["final"] += f'Your role is {state["role"]}. You can explore all the resources and community features.'
    return state

def role_deciderNode(state : ConditionalState): 
    if state["role"] == "intern" : return "internNode"
    else : return "FteNode"

graph = StateGraph(ConditionalState)
graph.add_node("nameNode", nameNode)
graph.add_node("deciderNode", lambda state : state)
graph.add_node("childNode", childNode)
graph.add_node("adultNode", adultNode)
graph.add_node("skillNode", skillNode)
graph.add_node("role_deciderNode", lambda state : state)
graph.add_node("internNode", internNode)
graph.add_node("FteNode", FteNode)

graph.add_edge(START, "nameNode")
graph.add_edge("nameNode", "deciderNode")
graph.add_conditional_edges(
    "deciderNode",
    deciderNode,
    {
        "childNode" : "childNode",
        "adultNode" : "adultNode"
    }
)
graph.add_edge("childNode", "skillNode")
graph.add_edge("adultNode", "skillNode")
graph.add_edge("skillNode", "role_deciderNode")
graph.add_conditional_edges(
    "role_deciderNode",
    role_deciderNode,
    {
        "internNode" : "internNode",
        "FteNode" : "FteNode"
    }
)
graph.add_edge("internNode", END)
graph.add_edge("FteNode", END)

app = graph.compile()
input_state = ConditionalState(name="Snigdha", age=23, skill="Python", role="FTE", final="")
answer = app.invoke(input_state)
print(answer["final"])


input_state = ConditionalState(name="Nithish", age=17, skill="Python", role="intern", final="")
answer = app.invoke(input_state)
print(answer["final"])


