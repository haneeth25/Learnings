# Agent decide which tool to use 
import os
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage # The foundational class for all nmessage types in langgraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph , START,END 
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage] , add_messages]

# To create a tool we use @tool
@tool
def add(a:int,b:int):
    """This is an addition function that adds 2 numbers together"""
    return a + b

@tool 
def subtract(a:int,b:int):
    """Subtraction function"""
    return a-b 

@tool
def multiply(a:int, b:int):
    """Multiplication function"""
    return a * b

#We add all our tools names in below list
tools = [add, subtract, multiply]

#By using .bind_tools I am saying to LLM these all tools are there 
model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY"),
).bind_tools(tools)

def model_call(state:AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are My AI assistant, please answer my query to the best of your ability. ")

    # We are passing system prompt and user conversation
    response = model.invoke([system_prompt] + state["messages"])
    
    #Since add_messages does appending we no need to explicity do +=
    return {"messages":[response]}

# Our router
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)
graph.add_node("our_agent",model_call)

#We are creating tool_node 
tool_node = ToolNode(tools=tools)
graph.add_node("tools",tool_node)

graph.add_edge(START,"our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue":"tools",
        "end":END
    }
)

# Since conditional edge is uni direction , from tool we have to go back to agent so we have this edge 
graph.add_edge("tools","our_agent")
app = graph.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message,tuple):
            print(message)
        else:
            message.pretty_print()

# inputs = {"messages":[("user","add 40 and 12 and then multiply the result by 6")]}
inputs = {"messages":[("user","add 40 and 12 and then multiply the result by 6 and tell me a joke")]}
print_stream(app.stream(inputs,stream_mode="values"))