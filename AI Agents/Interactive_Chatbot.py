from typing import TypedDict, List
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langchain_community.chat_models import ChatLlamaCpp
from Prompt_template import prompt_template
from model import load_model

llm = load_model()

class chatbotState(TypedDict):
    message : List[HumanMessage]

def chatbot_agent(state : chatbotState) -> chatbotState : 
    response = llm.invoke(state["message"])
    print(f'Response : {response.content}')
    return state

graph = StateGraph(chatbotState)
graph.add_node("chatbot",chatbot_agent)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)
agent = graph.compile()

user_input = input("Enter the prompt : ")
while user_input!= "exit" and user_input!="quit" : 
    state = agent.invoke({"message" : [HumanMessage(content=user_input)]})
    user_input = input("Enter the prompt : ")

