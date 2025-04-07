import json
import networkx as nx
import matplotlib.pyplot as plt


def graph_reader(path, bidirectional=False):
    # Load JSON data
    # file_path = r"C:\Users\Yashwardhan\Desktop\Revive\revive\repo\simple_graph_bidirectionsl.json"
    with open(path, "r") as f:
        data = json.load(f)

    # # Create an undirected graph
    # G = nx.Graph()
    
    # # Add nodes with attributes
  

    # # Add edges with attributes
    # for edge in data["edges"]:
    #     G.add_edge(edge["node1_pub"],
    #                 edge["node2_pub"],
    #                 channel_id=edge["channel_id"],
    #                 capacity=edge["capacity"])


    #Create a directed graph 
    G = nx.DiGraph()

    for node in data["nodes"]:
        G.add_node(node["pub_key"],
                alias=node["alias"],
                color=node["color"])
        
    for edge in data['edges']:
        u = edge['node1_pub']
        v = edge['node2_pub']
        w = int(edge['weight'])
        G.add_edge(u, v, weight=w)

    # if bidirectional:
    #     # Ensure that every edge has a reverse direction
    #     edges_to_add = []
    #     for u, v, data in G.edges(data=True):
    #         if not G.has_edge(v, u):
    #             # Add reverse edge with weight 0 (or customize default)
    #             edges_to_add.append((v, u, {'weight': 0}))
    #     G.add_edges_from(edges_to_add)

    return G


