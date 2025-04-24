import graph_display
import graph_reader
import rebalancer
import networkx as nx

G = graph_reader.graph_reader(r"C:\Users\Yashwardhan\Desktop\Revive\revive\repo\simple_graph_bidirectional.json", bidirectional=True)

# print(G.edges, "\n\n", G.nodes)

pos = nx.spring_layout(G, seed=42, k=1.5)

graph_display.draw_graph(G, pos, "Initial Graph")

# cycles = rebalancer.find_cycles(G)
# print(cycles)

cycles2 = rebalancer.find_cycles_with_depleted_edge(G)
print(cycles2)

rebalance = rebalancer.total_flow(cycles2,G)
print(rebalance)

graph_display.draw_graph(G, pos, "Initial Graph")

# LP-based rebalancing
# rb = rebalancer.Rebalancer(G)
# rb.cyclic_rebalance()

# graph_display.draw_graph(G, pos, "After Rebalancing")