import json
import networkx as nx
import matplotlib.pyplot as plt

def graph_reader(path, bidirectional=False):
    with open(path, "r") as f:
        data = json.load(f)
    G = nx.DiGraph()

    for node in data["nodes"]:
        G.add_node(node["pub_key"],alias=node["alias"],color=node["color"],degree=0)
        
    for edge in data['edges']:
        u = edge['node1_pub']
        v = edge['node2_pub']
        weight = int(edge['weight'])
        capacity = int(edge['capacity'])
        G.add_edge(u, v, weight=weight, capacity=capacity)
        # G.nodes[u]['degree'] += 1
        G.nodes[v]['degree'] += 1


    if bidirectional:
        # Ensure that every edge has a reverse direction
        edges_to_add = []
        for u, v, data in G.edges(data=True):
            if not G.has_edge(v, u):
                # Add reverse edge with weight 0 (or customize default)
                edges_to_add.append((v, u, {'weight': 0}))
        G.add_edges_from(edges_to_add)

    return G