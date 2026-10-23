#Create multiple nodes that sequentially process and update different parts of the state 

from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name:str
    age:str
    final:str 

def first_node(state:AgentState) -> AgentState:
    """ This is first node of our sequence """
    state["final"] = f"Hi {state['name']}"
    return state

def second_node(state:AgentState) -> AgentState:
    """This is the second node of our sequence"""
    state["final"] += f" You are {state["age"]} years old!"
    return state

graph = StateGraph(AgentState)
graph.add_node("first_node",first_node)
graph.add_node("second_node",second_node)
graph.set_entry_point("first_node")
# To connect first node and second node we use edge 
# We have to provide two point between which we need edge 
# In this case we need between first_node and second_node
graph.add_edge("first_node","second_node")
graph.set_finish_point("second_node")
app = graph.compile()
#print(app.get_graph().draw_mermaid())
# Output
"""
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        first_node(first_node)
        second_node(second_node)
        __end__([<p>__end__</p>]):::last
        __start__ --> first_node;
        first_node --> second_node;
        second_node --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""
result = app.invoke({"name":"bob","age":"20"})
print(result)