from langgraph.graph import StateGraph, START, END 
from typing_extensions import TypedDict




class OverallState(TypedDict):
    a:str   # contains only 'a' field which is a string
    
    # Node1Output: A PRIVATE data structure that is only returned by node_1
    # this data is Not part of the OverallState and is only visible to node2
class Node1Output(TypedDict):
    private_data: str   # contains private data that node1 generate
    

# node 1: Takes OverallState as input, returnes Node1Output (private data)
def node_1(state:OverallState) -> Node1Output:
    output = { "private_data": "set by node_1"}
    print(f"Entered node 'node_1': \n\tInput: {state}.\n\ntReturned: {output}")
    return output

# Node 2 input only requests the private data available after node_2
class Node2Input(TypedDict):
    private_data:str

def node_2(state:Node2Input) -> OverallState:
    output = {"a": "set by node_2"}
    print(f"Entered node 'node_2' :\n\tInput: {state}.\n\tReturnded: {output}")
    return output

# Node 3 only has access to the overall state (no access to private data from node_1)
def node_3(state:OverallState) -> OverallState:
    output = {"a": "set by node_3"}
    print(f"Entered node 'node_3' :\n\ntInput: {state}. \n\tReturned: {output}")
    return output
builder = StateGraph(OverallState).add_sequence([node_1, node_2, node_3])
builder.add_edge(START, "node_1")
graph = builder.compile()

response = graph.invoke(
    {
        "a": "set at start",
        
    }
)
print()
print(f"Output of graph invocation: {response}")
    