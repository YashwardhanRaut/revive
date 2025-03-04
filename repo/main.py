import graph_display
import graph_reader

G = graph_reader.graph_reader(r"C:\Users\Yashwardhan\Desktop\Revive\revive\repo\simple_graph_bidirectionsl.json")

graph_display.draw_graph(G, "Initial Graph")

# Add Algo here

graph_display.draw_graph(G, "After Rebalancing")