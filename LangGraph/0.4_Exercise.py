from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str 

def greeter(state:AgentState) -> AgentState :
    state["name"] = state["name"] + " , you are doing an amazing job learning langraph"

    return state

graph = StateGraph(AgentState)

graph.add_node("greeter",greeter)

graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()

result = app.invoke({"name":"Bob"})
print(result["name"])
