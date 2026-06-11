from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage, BaseMessage, HumanMessage
from langgraph.graph import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from model import load_model

llm = load_model()

# Global variable 
document = ""

class DrafterState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]

@tool
def update(content : str) -> str:
    """Replace the entire document with updated content.

    Use this whenever the user asks to:
    - create a document
    - modify a document
    - rewrite a document
    - add content
    - remove content
    - edit content

    Args:
        content: The complete new document text."""
    global document
    document = content
    return f"Document updated successfully. The current document is {document}"

@tool
def save(filename : str) -> str:
    """
    This is tool to save the document in the specified filename as a text file. 

    Args : 
    The name of the text file is given as {filename}
    """
    if not filename.endswith("txt"): filename = f'{filename}.txt'

    global document
    try :
        with open(filename, "w") as file:
            file.write(document)
            print(f'The document is saved at {filename}')
            return f"Document saved at {filename}"
    except Exception as e : 
        return f"Saving failed due to {e}"
    
tools = [update, save]
llm = llm.bind_tools(tools=tools)

def process_Agent(state : DrafterState) -> DrafterState:
    """"""
    global document
    system_prompt = f"""
    You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
    
    - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
    - If the user wants to save and finish, you need to use the 'save' tool.
    - Make sure to always show the current document state after modifications.
    The current document is {document}.
    """
    system_message = SystemMessage(content=system_prompt)

    if not state["messages"] : 
        user_input = "There's currently nothing in, what would you like to create ? "
        user_message = HumanMessage(content = user_input)

    else : 
        user_input = input("What would like to do with the document ? ")
        print(f'User : {user_input}')
        user_message = HumanMessage(content = user_input)

    combined_message = [system_message] + list(state["messages"]) + [user_message]
    response = llm.invoke(combined_message)

    print(f'AI Response : {response.content}')

    # Code to know the tool call
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages" : [user_message, response]}

def should_continue(state : DrafterState) -> str:
    """Determines whether to continue or end the conversation. """
    messages = state["messages"]
    if not messages : return "continue"

    for message in reversed(messages):
        # ... and checks if this is a ToolMessage resulting from save
        if (isinstance(message, ToolMessage) and 
            "saved" in message.content.lower() and
            "document" in message.content.lower()):
            return "end" # goes to the end edge which leads to the endpoint
        
    return "continue"


def print_messages(messages):
    """Function to print messages. """
    if not messages : return 

    for element in messages[-3:]:
        if isinstance(element, ToolMessage):
            print(f'Tool result : {element.content}')

graph = StateGraph(DrafterState)
graph.add_node("Process_Agent",process_Agent)

Tool_node = ToolNode(tools=tools)
graph.add_node("tool_node", Tool_node)

graph.add_edge(START, "Process_Agent")
graph.add_edge("Process_Agent","tool_node")
graph.add_conditional_edges(
    "tool_node",
    should_continue,
    {
        "continue" : "Process_Agent",
        "end" : END
    },
)

app = graph.compile()


def run_agent():
    print("--Start of Drafting--")
    state = {"messages" : []}
    for step in app.stream(state, stream_mode="values"):
        if "message" in step : 
            print_messages(step["message"])
    print("--End of the Drafter--")

if __name__ == "__main__":
    run_agent()