import graph_reader
from simulator import DepletionSimulator
import matplotlib.pyplot as plt

def run_experiments_on_graphs(graph_paths, depletion_percents, repeats_per_percent=5):
    for graph_path in graph_paths:
        G = graph_reader.graph_reader(graph_path, bidirectional=True)
        print(f"Running simulation on graph: {graph_path}")

        sim = DepletionSimulator(G)
        sim.run_full_simulation(depletion_percents, repeats_per_percent)

        sim.plot_results()