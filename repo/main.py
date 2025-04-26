import graph_display
import graph_reader
import rebalancer
import simulator
# import sim_runner
import networkx as nx

G = graph_reader.graph_reader(r"C:\Users\Yashwardhan\Desktop\Revive\revive\repo\simple_graph_bidirectional.json", bidirectional=True)

pos = nx.spring_layout(G, seed=42, k=1.5)

# graph_display.draw_graph(G, pos, "Initial Graph")

# def total_deviation(G):
#     deviation = 0
#     for u, v, data in G.edges(data=True):
#         balance = data['weight']  # remember: you're using weight as balance
#         capacity = data['capacity']
#         midpoint = capacity / 2
#         deviation += abs(balance - midpoint)
#     return deviation

# # === BEFORE REBALANCING ===
# initial_deviation = total_deviation(G)
# print(f"Initial total deviation: {initial_deviation:.2f}")

# # === RUN REBALANCER ===
# rebalance = rebalancer.GlobalReviveRebalancer(G)
# rebalance.run()

# # === AFTER REBALANCING ===
# final_deviation = total_deviation(G)
# print(f"Final total deviation: {final_deviation:.2f}")

# # === IMPROVEMENT ===
# improvement = (initial_deviation - final_deviation) / initial_deviation * 100
# print(f"Deviation improvement: {improvement:.2f}%")

# graph_display.draw_graph(G, pos, "Rebalanced Graph")


# sim = simulator.DepletionSimulator(G)

# # Run simulation for different depletion levels
# sim.run_full_simulation(depletion_percents=[10,20,30,40,50,60], repeats_per_percent=5)

# # Plot results
# sim.plot_results()


from sim_runner import run_experiments_on_graphs

graph_files = [
    r"C:\Users\Yashwardhan\Desktop\Revive\revive\repo\simple_graph_bidirectional.json"
    # r"C:\path\to\simple_graph_bidirectional.json"
    # r"C:\path\to\medium_graph.json",
    # r"C:\path\to\large_graph.json"
]

depletion_percents = [10, 20, 30, 40, 50, 60]

run_experiments_on_graphs(graph_files, depletion_percents, repeats_per_percent=5)