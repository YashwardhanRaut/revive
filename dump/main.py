import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Load the JSON file
def load_graph(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    G = nx.MultiGraph()
    
    # Add nodes
    for node in data["nodes"]:
        G.add_node(node["pub_key"], alias=node["alias"])
    
    # Add edges with capacities (support multiple edges)
    for edge in data["edges"]:
        node1 = edge["node1_pub"]
        node2 = edge["node2_pub"]
        channel_id = edge["channel_id"]
        capacity = int(edge["capacity"])  # Convert from string to int
        
        G.add_edge(node1, node2, key=channel_id, capacity=capacity)
    
    return G

# Draw the graph
def draw_graph(G, title):
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G)
    labels = {node: G.nodes[node]['alias'] for node in G.nodes}
    edge_labels = {(u, v, k): G[u][v][k]['capacity'] for u, v, k in G.edges(keys=True)}
    
    nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', edge_color='gray', node_size=1000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.show()

# Construct the linear program
def rebalance_network(G):
    nodes = list(G.nodes)
    edges = list(G.edges(keys=True, data=True))
    n = len(edges)
    
    # Define variables for balance shifts (one per edge)
    c = -np.ones(n)  # Maximize sum of balance shifts
    A_eq = np.zeros((len(nodes), n))  # Balance conservation
    b_eq = np.zeros(len(nodes))
    bounds = []
    
    for i, (u, v, k, attr) in enumerate(edges):
        capacity = attr['capacity']
        bounds.append((0, capacity))  # Constraints for balance shifts
        
        A_eq[nodes.index(u)][i] = 1
        A_eq[nodes.index(v)][i] = -1
    
    # Solve the linear program
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    
    if result.success:
        print("Rebalancing successful!")
        for i, (u, v, k, _) in enumerate(edges):
            print(f"Transfer {result.x[i]:.2f} from {u} to {v} on channel {k}")
            G[u][v][k]['capacity'] -= result.x[i]  # Update graph capacities
    else:
        print("Rebalancing failed.")

# Load graph
graph = load_graph("simple_graph_bidirectionsl.json")

# Draw initial graph
draw_graph(graph, "Before Rebalancing")

# Perform rebalancing
rebalance_network(graph)

# Draw final graph
draw_graph(graph, "After Rebalancing")
