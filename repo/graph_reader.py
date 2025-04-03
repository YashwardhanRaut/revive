import json
import networkx as nx
import matplotlib.pyplot as plt


def graph_reader(path):
    # Load JSON data
    # file_path = r"C:\Users\Yashwardhan\Desktop\Revive\revive\repo\simple_graph_bidirectionsl.json"
    with open(path, "r") as f:
        data = json.load(f)

    # Create an undirected graph
    G = nx.Graph()

    # Add nodes with attributes
    for node in data["nodes"]:
        G.add_node(node["pub_key"],
                alias=node["alias"],
                color=node["color"])

    # Add edges with attributes
    for edge in data["edges"]:
        G.add_edge(edge["node1_pub"],
                    edge["node2_pub"],
                    channel_id=edge["channel_id"],
                    capacity=edge["capacity"])
    
    return G
