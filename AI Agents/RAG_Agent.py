from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage, BaseMessage
from langgraph.graph import StateGraph, add_messages, START, END
from model import load_model
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
import os

llm = load_model()


class RagState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]


@tool
def Retriever(state : RagState) -> RagState : 

    return state


@tool
def PDF_extracter(state : RagState):

    return 

tools = []
llm = llm.bind_tools()

def model_Agent(state : RagState) : 

    return state


def should_continue(state : RagState) -> str:

    return "end"





