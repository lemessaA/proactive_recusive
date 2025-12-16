from langgraph.graph import END, StateGraph, START
from langgraph.runtime import Runtime
from typing_extensions import TypedDict


# 1. Specify config schema

class ContextSchema(TypedDict):
    my_runtime_value:str
    
class State(TypedDict):
    my_state_value:str
    
def node(state: State, runtime: Runtime[ContextSchema]):
    if runtime.context["my_runtime_value"] == "a":
        return {"my_state_value":1 }
    elif runtime.context["my_state_value"] == "b":
        return {"my_state_value": 2}
    else:
        raise ValueError("unknown values")
builder = StateGraph(State, context_schema=ContextSchema)
builder.add_node("node", node)
builder.add_edge(START, "node")
builder.add_edge("node", END)


graph = builder.compile() 

# pass in configuration at runtime: 
print(graph.invoke({}, context={"my_runtime_value": "a"}))
print(graph.invoke({}, context={"my_runtime_value": "b"}))
       
    