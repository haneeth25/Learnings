from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    results: str

def process_values(state:AgentState) -> AgentState :
    """ This function handles multiple different inputs """

    state["results"] = f"hi There {state['name']} ! Your sum = {sum(state['values'])}"
    return state

graph = StateGraph(AgentState)
graph.add_node("processor",process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")
app = graph.compile()

d = {
    "values":[1,2,3,4,5],
    "name" : "Bob"
}
result = app.invoke(d)
print(result)