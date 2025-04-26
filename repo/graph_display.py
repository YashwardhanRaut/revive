import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G, pos, title="Bidirectional Network Graph"):
    import matplotlib.pyplot as plt
    import networkx as nx
    
    plt.figure(figsize=(12, 8))
    # Draw nodes and alias labels
    nx.draw_networkx_nodes(G, pos, node_size=700)
    aliases = {node: G.nodes[node].get("alias", node) for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=aliases, font_size=14)

    # Combine bidirectional edges into one edge with combined weight label
    drawn_edges = set()
    edge_labels = {}
    for u, v in G.edges():
        if (v, u) not in drawn_edges:
            weight_uv = G[u][v]["weight"]
            weight_vu = G[v][u]["weight"] if G.has_edge(v, u) else 0
            label = f"{weight_uv} / {weight_vu}"
            edge_labels[(u, v)] = label
            drawn_edges.add((u, v))
            drawn_edges.add((v, u))

    # Draw straight edges (no arrows)
    nx.draw_networkx_edges(G, pos, edgelist=list(edge_labels.keys()), arrows=False)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()