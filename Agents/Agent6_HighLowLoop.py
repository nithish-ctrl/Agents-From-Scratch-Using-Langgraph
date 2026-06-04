from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
import random

class HighLowState(TypedDict):
    Low : int
    High : int
    guess : int
    number : int
    feedback : str
    counter : int 
    all_guesses : List[int]
    max_tries : int

def guessNode(state : HighLowState) -> HighLowState:
    """Simple function to guess a number between Low and high."""
    state["guess"] = random.randint(state["Low"], state["High"])
    state["all_guesses"].append(state["guess"])
    return state

def feedbackNode(state: HighLowState) -> HighLowState:
    """Simple function to provide the feedback for the guess."""
    if state["guess"]<state["number"]:
        state["feedback"]= "Low"
        state["Low"] = state["guess"] + 1
        state["counter"] += 1
    elif state["guess"]>state["number"]:
        state["feedback"]="High"
        state["High"] = state["guess"] - 1 
        state["counter"] += 1
    else : 
        state["feedback"] = "correct"
        state["counter"] += 1 
    return state

def continue_node(state:HighLowState) -> str:
    """Simple function to check if the loop should continue or not. """
    if state["feedback"] == "correct":
        print(f'Guessed the number {state["number"]} in {state["counter"]} attempts!!')
        return "exit"
    elif state["counter"] >= state["max_tries"]:
        print(f'Failed to guess the number {state["number"]} in 7 attempts!!')
        return "exit"
    else : 
        return "StartAgain"

graph = StateGraph(HighLowState)
graph.add_node("GuessNode", guessNode) 
graph.add_node("FeedbackNode", feedbackNode)
graph.add_node("ContinueNode", lambda state : state)

graph.add_edge(START, "GuessNode")
graph.add_edge("GuessNode", "FeedbackNode")
graph.add_edge("FeedbackNode", "ContinueNode")
graph.add_conditional_edges(
    "ContinueNode",
    continue_node,
    {
        "StartAgain" : "GuessNode",
        "exit" : END 
    }
)

app = graph.compile()
initial_state = HighLowState(Low=1, High=100, guess=0, number=42, feedback="", counter=0, max_tries = 10, all_guesses=[])
result = app.invoke(initial_state)
print(result["all_guesses"])