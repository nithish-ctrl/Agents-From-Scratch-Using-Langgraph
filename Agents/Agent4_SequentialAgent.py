from typing import TypedDict, List
from langgraph.graph import StateGraph

class SequentialState(TypedDict):
    name : str
    age : int
    skill : List[str]
    final : str

def nameNode(state : SequentialState) -> SequentialState:
    state["final"] = f'Hi {state["name"]}, Welcome to the system !!.'
    return state

def ageNode(state: SequentialState) -> SequentialState:
    state["final"] += f'You age is {state["age"]}.'
    return state

def skillNode(state: SequentialState) -> SequentialState:
    state["final"] += f'Your skills are {",".join(state["skill"])}. You are pretty talented!!'
    return state

graph = StateGraph(SequentialState)
graph.add_node("NameNode", nameNode)
graph.add_node("AgeNode", ageNode)
graph.add_node("SkillNode", skillNode)

graph.set_entry_point("NameNode")
graph.add_edge("NameNode", "AgeNode")
graph.add_edge("AgeNode", "SkillNode")
graph.set_finish_point("SkillNode")

app = graph.compile()

state : SequentialState = {"name": "Snigdha", "age": 27, "skill": ["Python", "C++", "Full Stack Dev"], "final": ""}
answer = app.invoke(state)
print(answer['final'])
