import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G, pos, title="Bidirectional Network Graph"):
    import matplotlib.pyplot as plt
    import networkx as nx

    # More spread out layout
    # pos = nx.spring_layout(G, seed=42, k=1.5)

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


# def draw_graph(G, title):
#     # Draw the graph
#     plt.figure(figsize=(10, 6))
#     pos = nx.spring_layout(G, seed=69)  # Layout for visualization
#     plt.title(title)
#     nx.draw(
#         G, 
#         pos, 
#         connectionstyle='arc3,rad=0.2',
#         with_labels=False, 
#         node_size=500, 
#         node_color="lightblue", 
#         edge_color="gray")
#     labels = {node: G.nodes[node]["alias"] for node in G.nodes}
#     edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges}
#     nx.draw_networkx_labels(G, pos, labels)
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
#     print(title)
    
#     plt.show()

# def draw_graph2(G, title="Network Graph"):
#     pos = nx.spring_layout(G, seed=69)  # layout for consistent visualization

#     plt.figure(figsize=(8, 6))
#     nx.draw_networkx_nodes(G, pos, node_size=700)
#     nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle='->', arrowsize=20)
#     # nx.draw_networkx_labels(G, pos, font_size=14, font_family="sans-serif")

#     # Draw edge labels with weights (balances)
#     edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

#     plt.title(title)
#     plt.axis("off")
#     plt.tight_layout()
#     plt.show()

# def draw_graph3(G, title="Network Graph"):
#     pos = nx.kamada_kawai_layout(G)

#     plt.figure(figsize=(10, 7))
#     nx.draw_networkx_nodes(G, pos, node_size=700)
#     nx.draw_networkx_labels(G, pos, font_size=14)

#     # Split edges into forward and reverse for curving
#     forward_edges = [(u, v) for u, v in G.edges() if G.has_edge(u, v) and not G.has_edge(v, u)]
#     bidirectional_edges = [(u, v) for u, v in G.edges() if G.has_edge(v, u)]

#     nx.draw_networkx_edges(G, pos, edgelist=forward_edges, connectionstyle='arc3,rad=0.0', arrowstyle='->', arrowsize=20)
#     nx.draw_networkx_edges(G, pos, edgelist=bidirectional_edges, connectionstyle='arc3,rad=0.2', arrowstyle='->', arrowsize=20)
#     nx.draw_networkx_edges(G, pos, edgelist=[(v, u) for u, v in bidirectional_edges], connectionstyle='arc3,rad=-0.2', arrowstyle='->', arrowsize=20)

#     # Edge labels
#     edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

#     plt.title(title)
#     plt.axis("off")
#     plt.tight_layout()
#     plt.show()



# def draw_graph4(G, title="Bidirectional Network Graph"):
#     pos = nx.spring_layout(G, seed=42)  # Stable layout

#     plt.figure(figsize=(10, 7))
#     nx.draw_networkx_nodes(G, pos, node_size=700)
#     # nx.draw_networkx_labels(G, pos, font_size=14)

#     drawn_edges = set()

#     for u, v in G.edges():
#         if (v, u) in G.edges() and (v, u) not in drawn_edges:
#             # Bidirectional edge
#             w1 = G[u][v].get('weight', 0)
#             w2 = G[v][u].get('weight', 0)

#             label = f"{w1} / {w2}"
#             mid_x = (pos[u][0] + pos[v][0]) / 2
#             mid_y = (pos[u][1] + pos[v][1]) / 2

#             plt.text(mid_x, mid_y + 0.05, label, fontsize=10, ha='center', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

#             nx.draw_networkx_edges(
#                 G, pos,
#                 edgelist=[(u, v)],
#                 connectionstyle='arc3,rad=0.2',
#                 arrowstyle='->',
#                 arrowsize=20
#             )
#             nx.draw_networkx_edges(
#                 G, pos,
#                 edgelist=[(v, u)],
#                 connectionstyle='arc3,rad=-0.2',
#                 arrowstyle='->',
#                 arrowsize=20
#             )
#             drawn_edges.add((u, v))
#             drawn_edges.add((v, u))
#         elif (v, u) not in G.edges():
#             # One-way edge
#             w = G[u][v].get('weight', 0)
#             mid_x = (pos[u][0] + pos[v][0]) / 2
#             mid_y = (pos[u][1] + pos[v][1]) / 2

#             plt.text(mid_x, mid_y + 0.05, f"{w}", fontsize=10, ha='center', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

#             nx.draw_networkx_edges(
#                 G, pos,
#                 edgelist=[(u, v)],
#                 connectionstyle='arc3,rad=0.0',
#                 arrowstyle='->',
#                 arrowsize=20
#             )

#     plt.title(title)
#     plt.axis("off")
#     plt.tight_layout()
#     plt.show()



# def draw_graph_5(G, title="Bidirectional Network Graph"):
#     import matplotlib.pyplot as plt
#     import networkx as nx

#     pos = nx.spring_layout(G, seed=42)
#     plt.figure(figsize=(10, 7))
    
#     nx.draw_networkx_nodes(G, pos, node_size=700)
#     nx.draw_networkx_labels(G, pos, font_size=14)

#     # Draw only one edge between bidirectional nodes
#     drawn_edges = set()
#     edge_labels = {}
#     for u, v in G.edges():
#         if (v, u) not in drawn_edges:
#             weight_uv = G[u][v]["weight"]
#             weight_vu = G[v][u]["weight"] if G.has_edge(v, u) else 0
#             label = f"{weight_uv} / {weight_vu}"
#             edge_labels[(u, v)] = label
#             drawn_edges.add((u, v))
#             drawn_edges.add((v, u))

#     # Draw edges (undirected style)
#     nx.draw_networkx_edges(G, pos, edgelist=list(edge_labels.keys()), arrows=False)
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

#     plt.title(title)
#     plt.axis("off")
#     plt.tight_layout()
#     plt.show()