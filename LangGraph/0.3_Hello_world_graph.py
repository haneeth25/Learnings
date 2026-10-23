# Start -> Node -> End

from typing import Dict,TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict): # Our state schema
    message:str

def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting message to state"""

    state['message'] = "Hey "+ state['message'] + " , How is your day going ?"

    return state

graph = StateGraph(AgentState)

# To add a node 
# First paramter is name , It can be anything and second paramter is what action it should do 
graph.add_node("greeter",greeting_node)

#To declare starting point we use this
graph.set_entry_point("greeter")

#To declare ending point we use this 
graph.set_finish_point("greeter")

app = graph.compile()

# To Visualize it we can do this 
# print(app.get_graph().draw_mermaid())

# Output:- 
"""
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        greeter(greeter)
        __end__([<p>__end__</p>]):::last
        __start__ --> greeter;
        greeter --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc

"""

# To run the graph 
result = app.invoke({"message":"bob"})
print(result)