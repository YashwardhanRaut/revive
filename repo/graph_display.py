import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G, title):
    # Draw the graph
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=69)  # Layout for visualization
    plt.title(title)
    nx.draw(G, pos, with_labels=False, node_size=500, node_color="lightblue", edge_color="gray")
    labels = {node: G.nodes[node]["alias"] for node in G.nodes}
    edge_labels = {(u, v): G[u][v]['capacity'] for u, v in G.edges}
    nx.draw_networkx_labels(G, pos, labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    print(title)
    
    plt.show()