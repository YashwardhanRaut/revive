import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G, title):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    plt.title(title)
        
    # Draw edge labels with capacities
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        if (v, u) in G.edges():
            reverse_edges = list(G[v][u].values())  # Get all reverse edges
            reverse_capacity = reverse_edges[0]['capacity'] if reverse_edges else "N/A"  # Handle missing reverse edges
            edge_labels[(u, v)] = f"{d['capacity']}|{reverse_capacity}"



    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    
        # node_labels = {node: data["alias"] for node, data in G.nodes(data=True)}
    node_labels = {node: G.nodes[node]["alias"] for node in G.nodes()}

    # Draw nodes
    nx.draw(G, pos, labels=node_labels, with_labels=True , node_color='lightblue', node_size=2000, edge_color='gray')

    plt.show()