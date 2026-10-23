from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY"),
)


def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])

    print(f"\nAI: {response.text}")

    # Get token usage
    usage = response.usage_metadata

    if usage:
        print("\n--- Token Usage ---")
        print(f"Input tokens:  {usage.get('input_tokens', 0)}")
        print(f"Output tokens: {usage.get('output_tokens', 0)}")
        print(f"Total tokens:  {usage.get('total_tokens', 0)}")
    else:
        print("Token usage metadata unavailable.")

    return state


graph = StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)
agent = graph.compile()

user_input = input("Enter : ")
while user_input != "exit":
    agent.invoke({"messages":[HumanMessage(content=user_input)]})
    user_input = input("Enter : ")