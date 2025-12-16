
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END


def reasoning_node(state: dict, config: RunnableConfig) -> dict:
    """
    Main reasoning node.
    This node is executed repeatedly until the graph decides to stop
    or route to a fallback path.
    """

    # Current execution step of the graph (tracked automatically by LangGraph)
    current_step = config["metadata"]["langgraph_step"]

    # Maximum allowed recursion depth for the graph
    # This key is always present and defaults to 25 if not overridden
    recursion_limit = config["recursion_limit"]

    # Check if the current step has reached 80% of the recursion limit
    # This acts as a safety threshold to prevent infinite or excessive loops
    if current_step >= recursion_limit * 0.8:
        return {
            **state,  # Preserve the existing state
            "route_to": "fallback",  # Signal that execution should move to fallback
            "reason": "Approaching recursion limit"  # Optional explanation
        }

    # Normal reasoning path
    # Append a new message to the existing list of messages
    return {
        "messages": state["messages"] + ["thinking..."]
    }


def fallback_node(state: dict, config: RunnableConfig) -> dict:
    """
    Fallback node.
    Executed when the graph is close to the recursion limit.
    Provides a best-effort response and stops further reasoning.
    """

    return {
        **state,  # Preserve all existing state values
        "messages": state["messages"] + [
            "Reached complexity limit, providing best effort answer"
        ]
    }


def route_based_on_state(state: dict) -> str:
    """
    Routing function.
    Determines which node should execute next based on the current state.
    """

    # If the reasoning node requested a fallback, route to the fallback node
    if state.get("route_to") == "fallback":
        return "fallback"

    # If the state indicates completion, end the graph execution
    elif state.get("done"):
        return END

    # Otherwise, continue reasoning
    return "reasoning"


# Create a state graph where the state is represented as a dictionary
graph = StateGraph(dict)

# Register nodes in the graph
graph.add_node("reasoning", reasoning_node)
graph.add_node("fallback", fallback_node)

# Add conditional edges from the reasoning node
# The next node is chosen by the route_based_on_state function
graph.add_conditional_edges("reasoning", route_based_on_state)

# Define that after the fallback node, execution always ends
graph.add_edge("fallback", END)

# Set the starting node of the graph
graph.set_entry_point("reasoning")

# Compile the graph into a runnable application
app = graph.compile()
