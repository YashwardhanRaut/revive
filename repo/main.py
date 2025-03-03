import graph_display
import graph_reader

# G = graph_reader.graph_reader("un")
G = graph_reader.graph_reader("simple_graph_bidirectionsl.json")

graph_display.draw_graph(G, "Initial Graph")