import graph_display
import graph_reader
import rebalancer
import simulator
from sim_runner import run_experiments_on_graphs
import networkx as nx

G = graph_reader.graph_reader(r"C:\Users\Yashwardhan\Desktop\Revive\revive\repo\simple_graph_bidirectional.json", bidirectional=True)

pos = nx.spring_layout(G, seed=42, k=1.5)
# graph_display.draw_graph(G, pos, "Initial Graph")

graph_files = [
    r"C:\Users\Yashwardhan\Desktop\Revive\revive\repo\simple_graph_bidirectional.json"
    # r"C:\path\to\simple_graph_bidirectional.json"
    # r"C:\path\to\medium_graph.json",
    # r"C:\path\to\large_graph.json"
]

depletion_percents = [10, 20, 30, 40, 50, 60]
run_experiments_on_graphs(graph_files, depletion_percents, repeats_per_percent=5)

# print(G)

# for g in G.nodes():
    # print(G.nodes[g], G.nodes[g].get('alias', g), G.nodes[g].get('degree', g))

# graph_display.draw_graph(G, pos, "After Graph")