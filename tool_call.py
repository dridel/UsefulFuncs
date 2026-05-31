from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
# pip install ollama
# pip install langchain-ollama

class AgentState (TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a: float, b:float):
    """ adds 2 numbers together"""
    print(f"tool: adding {a} and {b}")
    return a+b

def model_call(state: AgentState) -> AgentState:
    """
    Function that calls an LLM with the curr state
    :param state:
    :return:
    """
    system_prompt = SystemMessage(content="You are a skilled computing agent, respond to the best of your abilities")
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    """
    decides if the agent uses a tool or continues or terminates
    :param state:
    :return:
    """
    last_message = state["messages"][-1]
    for tool in last_message.tools_calls:
        print(tool)
    if not last_message.tools_calls:
        return "END_PROCESS"
    else:
        return "CONTINUE"

if __name__ == "__main__":
    tools = [add]
    model = ChatOllama(model="llama3.2", temperature=0).bind_tools(tools)

    graph = StateGraph(AgentState)
    graph.add_node(node="agent", action=model_call)

    tool_node = ToolNode(tools=tools)
    graph.add_node(node="tools", action = tool_node)

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        should_continue,
        path_map={
            "CONTINUE": "tools",
            "END_PROCESS": END
        }
    )
    graph.add_edge("tools", "agent")
    agent = graph.compile()

    inputs = {"messages": [("user", "Calculate x = 300*100; e ate obter um valor negativo,divida cada novo resultado por 5")]}
    res = agent.stream(inputs, stream_mode="values")

    for s in res:
        print(s["messages"][-1].content)