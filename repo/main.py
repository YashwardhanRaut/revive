import graph_display
import graph_reader
import rebalancer
import networkx as nx

G = graph_reader.graph_reader(r"C:\Users\Yashwardhan\Desktop\Revive\revive\repo\simple_graph_bidirectional.json", bidirectional=True)

print(G.edges, "\n\n", G.nodes)

pos = nx.spring_layout(G, seed=42, k=1.5)

graph_display.draw_graph(G, pos, "Initial Graph")

# LP-based rebalancing
rebalancer.rebalance_with_lp(G)

graph_display.draw_graph(G, pos, "After Rebalancing")


rebalancer.rebalance_with_lp(G)

graph_display.draw_graph(G, pos, "After Rebalancing")

# import graph_display
# import graph_reader
# import rebalancer

# G = graph_reader.graph_reader(r"C:\Users\Yashwardhan\Desktop\Revive\revive\repo\simple_graph_bidirectional.json", bidirectional=True)

# print(G.edges,"\n\n" ,G.nodes)

# graph_display.draw_graph2(G, "Initial Graph")

# # Add Algo here
# rebalancer.find_and_rebalance_cycles(G)

# graph_display.draw_graph2(G, "After Rebalancing")