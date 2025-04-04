import graph_display
import graph_reader
import rebalancer

G = graph_reader.graph_reader(r"C:\Users\Yashwardhan\Desktop\Revive\revive\repo\simple_graph_bidirectional.json", bidirectional=True)

print(G.edges,"\n\n" ,G.nodes)

graph_display.draw_graph2(G, "Initial Graph")

# Add Algo here
rebalancer.find_and_rebalance_cycles(G)

graph_display.draw_graph2(G, "After Rebalancing")