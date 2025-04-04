import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G, title):
    # Draw the graph
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=69)  # Layout for visualization
    plt.title(title)
    nx.draw(
        G, 
        pos, 
        connectionstyle='arc3,rad=0.2',
        with_labels=False, 
        node_size=500, 
        node_color="lightblue", 
        edge_color="gray")
    labels = {node: G.nodes[node]["alias"] for node in G.nodes}
    edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges}
    nx.draw_networkx_labels(G, pos, labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    print(title)
    
    plt.show()

def draw_graph2(G, title="Network Graph"):
    pos = nx.spring_layout(G, seed=69)  # layout for consistent visualization

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle='->', arrowsize=20)
    # nx.draw_networkx_labels(G, pos, font_size=14, font_family="sans-serif")

    # Draw edge labels with weights (balances)
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def draw_graph3(G, title="Network Graph"):
    pos = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_labels(G, pos, font_size=14)

    # Split edges into forward and reverse for curving
    forward_edges = [(u, v) for u, v in G.edges() if G.has_edge(u, v) and not G.has_edge(v, u)]
    bidirectional_edges = [(u, v) for u, v in G.edges() if G.has_edge(v, u)]

    nx.draw_networkx_edges(G, pos, edgelist=forward_edges, connectionstyle='arc3,rad=0.0', arrowstyle='->', arrowsize=20)
    nx.draw_networkx_edges(G, pos, edgelist=bidirectional_edges, connectionstyle='arc3,rad=0.2', arrowstyle='->', arrowsize=20)
    nx.draw_networkx_edges(G, pos, edgelist=[(v, u) for u, v in bidirectional_edges], connectionstyle='arc3,rad=-0.2', arrowstyle='->', arrowsize=20)

    # Edge labels
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
