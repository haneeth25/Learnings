from typing import TypedDict,Union
from langgraph.graph import StateGraph,START,END

class AgentState(TypedDict):
    number1:Union[int,str]
    operation:str
    number2:Union[int,str]
    finalNumber:int
    message:str

def prepare_input(state:AgentState)-> AgentState:
    """This node is to convert number to int"""
    state['number1'] = int(state['number1'])
    state['number2'] = int(state['number2'])

    return state;

def adder(state:AgentState) -> AgentState:
    """This node adds the 2 numbers"""

    state["finalNumber"] = state["number1"] + state["number2"]
    return state 

def subtractor(state:AgentState) -> AgentState:
    """This node subtracts the 2 numbers"""
    state["finalNumber"] = state["number1"] - state["number2"]
    return state

def decide_next_node(state:AgentState) -> AgentState:
    """This node will select the next node of the graph"""

    if state["operation"] == "+":
        return "addition_operation"
    elif state["operation"] == "-":
        return "subtraction_operation"

def format_response(state:AgentState) -> AgentState:
    """This node is to prepare response"""
    state["message"] = f"Final value = {state['finalNumber']}"
    return state

graph = StateGraph(AgentState)
#Created all node 
graph.add_node("prepare_input", prepare_input)
graph.add_node("router", lambda state: state)
graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)
graph.add_node("format_response", format_response)

graph.add_edge(START,"prepare_input")
graph.add_edge("prepare_input","router")
graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        "addition_operation": "add_node",
        "subtraction_operation": "subtract_node"
    }
    )
graph.add_edge("add_node","format_response")
graph.add_edge("subtract_node","format_response")
graph.add_edge("format_response",END)

app = graph.compile()
print(app.get_graph().draw_mermaid())

