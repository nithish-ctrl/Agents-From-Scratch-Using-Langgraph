from langgraph.graph import START, END, StateGraph
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from model import load_model

llm = load_model()

class MemoryState(TypedDict):
    messages : List[Union[HumanMessage, AIMessage]]

def MemoryAgent(state : MemoryState)-> MemoryState:
    """Invokes the model and also saves the AIMessage"""
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print(f'Response : {response.content}\n')
    return state

graph = StateGraph(MemoryState)
graph.add_node("MemoryAgent",MemoryAgent)
graph.add_edge(START,"MemoryAgent")
graph.add_edge("MemoryAgent", END)

agent = graph.compile()
convo_history = []
user_input = input("Enter the query : ")
while user_input.lower() != "exit" and user_input.lower() != "quit":
    convo_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages" : convo_history})
    convo_history = result["messages"]
    user_input = input("Enter the query : ")



with open("Conversation_history.txt", "w") as convo:
    convo.write(f'Conversation History :')
    
    for text in convo_history:
        if isinstance(text, HumanMessage):
            convo.write(f'You : {text.content}\n')
        elif isinstance(text, AIMessage):
            convo.write(f'AI : {text.content}\n')
    convo.write("End of conversation")

print("Conversation Saved in log")


