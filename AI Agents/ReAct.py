from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from model import load_model

llm = load_model()

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]

@tool 
def Add(a:int, b:int): 
    """This is an additon function that adds up 2 numbers"""
    return a+b

tools = [Add]
llm_with_tools = llm.bind_tools(tools)

def model_def(state : AgentState) -> AgentState: 
    System_message = SystemMessage(content = "You are an helpful AI assistant and have tools in case they are necessary.")
    response = llm_with_tools.invoke([System_message] + list(state["messages"]))
    return {"messages" : [response]}

def should_continue(state : AgentState):
    messages_in = state["messages"]
    last_message = messages_in[-1]
    if not last_message.tool_calls:  # type: ignore
        return "end"
    else : 
        return "continue"


graph = StateGraph(AgentState)
graph.add_node("model_agent", model_def)

toolNode = ToolNode(tools=tools)
graph.add_node("tools_access", toolNode)

graph.add_node("should_continue", should_continue)
graph.add_edge(START, "model_agent")
graph.add_conditional_edges(
"model_agent",
should_continue,
{
    "continue" : "tools_access",
    "end" : END
},
)

graph.add_edge("tools_access", "model_agent")
app = graph.compile()

# This is to see the usage of tools : 
def print_stream(stream):
    for s in stream : 
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else : 
            message.pretty_print()


inputs = {"messages": [("user", "Add 40 + 16 and then add 50 to their result. Also tell me a joke.")]}
print_stream(app.stream(inputs, stream_mode="values")) # type: ignore