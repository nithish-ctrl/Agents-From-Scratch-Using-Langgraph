from typing import TypedDict, List, Any
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatLlamaCpp

model_path = r"c:\Users\Nithish\Downloads\qwen2.5-3b-instruct-q5_0.gguf"
llm = ChatLlamaCpp(
    model_path = model_path,
    temperature = 0.1,
    streaming = False, 
    max_tokens = 128,
    n_ctx = 2048,
    n_batch = 512,
    top_p = 0.9,
    model_kwargs={
        "device" : "cuda",
        "chat_format" : "chatml",
        "flash_attn" : True
    },
    verbose=False
)

prompt_template = ChatPromptTemplate.from_messages(
    [
    (
        "system",
    """
        You are a highly intelligent and helpful AI assistant.
        Use the relevant memories below to answer questions about the user.
        Relevant memories from past conversations: 

                Guidelines:
                - Answer clearly and naturally.
                - Remember details from previous conversation.
                - Keep responses concise unless asked otherwise.
                - Do not invent fake conversations.
                - Do not generate 'Human:' or 'Assistant:' labels.
                - If the user's name or details were mentioned earlier, remember them.
                - Stay consistent with previous context.
                - Do not say you lack access to previous messages unless history is actually unavailable.
                - If you do not know something, say so honestly.
                - Always be helpful and polite.
    """
    )
    ]
)

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
