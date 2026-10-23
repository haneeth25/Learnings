#Implement looping logic to route the flow of data back to nodes
from typing import TypedDict,Dict,List
from langgraph.graph import StateGraph,START,END
import random

class AgentState(TypedDict):
    name:str 
    number:List[int]
    counter: int 

def greeting_node(state:AgentState) -> AgentState:
    state['name'] = f"Hi there , {state['name']}"
    state["counter"] = 0 
    return state

def random_node(state:AgentState) -> AgentState:
    state["number"].append(random.randint(0,10))
    state["counter"] += 1

    return state 

def should_continue(state:AgentState)-> AgentState:
    if(state["counter"] < 5):
        print("Entering loop", state["counter"])
        return "loop"
    else:
        return "exit"

graph = StateGraph(AgentState)
graph.add_node("greeting_node",greeting_node)
graph.add_node("random_node",random_node)
graph.add_edge(START,"greeting_node")
graph.add_edge("greeting_node","random_node")
graph.add_conditional_edges(
    "random_node",
    should_continue,
    {
        "loop":"random_node",
        "exit":END
    }
)
app = graph.compile()
print(app.invoke({"name":"bob","number":[]}))
