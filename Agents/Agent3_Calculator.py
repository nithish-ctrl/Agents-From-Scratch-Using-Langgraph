from typing import TypedDict
from langgraph.graph import StateGraph

class CalculatorState(TypedDict):
    num1 : float
    num2 : float
    operation : str 
    result : float

def calculatorNode(state: CalculatorState) -> CalculatorState:
    """Simple function to perform basic arithmetic operations."""
    num1 = state["num1"]
    num2 = state["num2"]
    operation = state["operation"]
    
    if operation == "add" or operation == "sum" or operation == "+" : 
        state["result"] = num1 + num2
    elif operation == "subtract" or operation == "minus" or operation == "-" :
        state["result"] = num1 - num2
    elif operation == "multiply" or operation == "times" or operation == "*" :
        state["result"] = num1 * num2
    elif operation == "divide" or operation == "over" or operation == "/" :
        state["result"] = num1 / num2
    return state

graph = StateGraph(CalculatorState)
graph.add_node("Calculator", calculatorNode)
graph.set_entry_point("Calculator")
graph.set_finish_point("Calculator")

app = graph.compile()

state : CalculatorState = {"num1": 10, "num2": 5, "operation": "add", "result": 0}
answer = app.invoke(state)
print(f'Answer : {answer["result"]}')
