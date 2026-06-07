from typing import TypedDict, List, Any
from langchain_core.messages import HumanMessage # Didn't use beacuse didnt need a type to tell inside list
from langgraph.graph import StateGraph, START, END
from langchain_core.output_parsers import StrOutputParser # Didnt use because the format is right
from model import load_model 
from prompt_template import prompt_template

llm = load_model()
prompt_template = prompt_template

class ChatbotState(TypedDict):
    prompt : str
    response : Any

def text_gen_Agent(state : ChatbotState) -> ChatbotState:
    state["prompt"] = input("Enter the prompt (exit or quit to stop) : ")
    state["response"] = llm.invoke(state["prompt"])
    return state


graph = StateGraph(ChatbotState)
graph.add_node("Text_generation", text_gen_Agent)

graph.add_edge(START, "Text_generation")
graph.add_edge("Text_generation", END)

app = graph.compile()
input_parameters = ChatbotState(prompt = "", response="")
result = app.invoke(input_parameters)
print(result["response"].content)
