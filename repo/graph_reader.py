import networkx as nx
import json

def graph_reader(path):
    # "simple_graph_bidirectionsl.json"
    with open(path, "r") as f:
        data = json.load(f)

    # Create a MultiDiGraph to allow multiple directed edges between nodes
    G = nx.MultiDiGraph()
        
    # Add nodes
    alias_map = {}
    for node in data["nodes"]:
        pub_key = node["pub_key"]
        alias = node["alias"]
        G.add_node(node["pub_key"], alias=node["alias"])
        alias_map[pub_key] = alias 

    # Add edges with capacities (support multiple edges)
    for edge in data["edges"]:
        node1 = edge["node1_pub"]
        node2 = edge["node2_pub"]
        channel_id = edge["channel_id"]
        capacity = int(edge["capacity"])  # Convert from string to int
            
        G.add_edge(node1, node2, key=channel_id, capacity=capacity)

    return G