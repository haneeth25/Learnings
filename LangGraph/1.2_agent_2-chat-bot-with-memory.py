#Chat bot with memory 
import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage,AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

class AgentState(TypedDict):
    messages: List[Union[HumanMessage,AIMessage]]

def process(state:AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.text}")
    state["messages"].append(AIMessage(content=response.text))

    return state

graph = StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)
agent = graph.compile()

# WE are maintaning whole conversation and sending whole conversation again and again to agent 
# Since agent can't remember our previous conversation
# We can keep only lastest 5 messages if we want to reduce no of tokens 
conversation_history = []

user_input = input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages":conversation_history})
    # print(result["messages"])
    conversation_history = result["messages"]
    user_input = input("Enter: ")