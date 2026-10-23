
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    number1: int
    operation: str
    number2: int
    finalNumber: int
    method_note: str
    response: str


def prepare_input(state: AgentState) -> AgentState:
    if state["operation"] not in ["+", "-"]:
        raise ValueError("Unsupported operation")
    return state


def adder(state: AgentState) -> AgentState:
    return {
        **state,
        "finalNumber": state["number1"] + state["number2"]
    }


def subtractor(state: AgentState) -> AgentState:
    return {
        **state,
        "finalNumber": state["number1"] - state["number2"]
    }


# Router 1: Choose addition or subtraction
def decide_operation(state: AgentState) -> str:
    if state["operation"] == "+":
        return "addition"
    return "subtraction"


# Router 2: Choose a method after subtraction
def decide_subtraction_method(state: AgentState) -> str:
    if state["finalNumber"] < 0:
        return "negative_method"
    return "non_negative_method"


def negative_method(state: AgentState) -> AgentState:
    return {
        **state,
        "method_note": "The subtraction result is negative."
    }


def non_negative_method(state: AgentState) -> AgentState:
    return {
        **state,
        "method_note": "The subtraction result is zero or positive."
    }


def format_response(state: AgentState) -> AgentState:
    if state["operation"] == "+":
        response = (
            f"Addition result: {state['finalNumber']}"
        )
    else:
        response = (
            f"Subtraction result: {state['finalNumber']}. "
            f"{state['method_note']}"
        )

    return {
        **state,
        "response": response
    }


graph = StateGraph(AgentState)

# Register all nodes
graph.add_node("prepare_input", prepare_input)
graph.add_node("router_1", lambda state: state)
graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)

graph.add_node("router_2", lambda state: state)
graph.add_node("negative_method", negative_method)
graph.add_node("non_negative_method", non_negative_method)

graph.add_node("format_response", format_response)


# Initial path
graph.add_edge(START, "prepare_input")
graph.add_edge("prepare_input", "router_1")


# First router
graph.add_conditional_edges(
    "router_1",
    decide_operation,
    {
        "addition": "add_node",
        "subtraction": "subtract_node"
    }
)


# Addition goes directly to the final response node
graph.add_edge("add_node", "format_response")


# Subtraction goes to the second router
graph.add_edge("subtract_node", "router_2")


# Second router chooses between two methods
graph.add_conditional_edges(
    "router_2",
    decide_subtraction_method,
    {
        "negative_method": "negative_method",
        "non_negative_method": "non_negative_method"
    }
)


# Both methods converge on the response node
graph.add_edge("negative_method", "format_response")
graph.add_edge("non_negative_method", "format_response")

graph.add_edge("format_response", END)


app = graph.compile()


initial_state: AgentState = {
    "number1": 10,
    "operation": "-",
    "number2": 15,
    "finalNumber": 0,
    "method_note": "",
    "response": ""
}

result = app.invoke(initial_state)
print(result["response"])
