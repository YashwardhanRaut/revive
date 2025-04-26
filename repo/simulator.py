import random
import copy
import matplotlib.pyplot as plt
import rebalancer  # Your GlobalReviveRebalancer

class DepletionSimulator:
    def __init__(self, G):
        """
        G: NetworkX DiGraph with 'weight' and 'capacity' on edges
        """
        self.G_original = G
        self.results = {}

    def total_deviation(self, G):
        deviation = 0
        for u, v, data in G.edges(data=True):
            balance = data['weight']
            capacity = data['capacity']
            midpoint = capacity / 2
            deviation += abs(balance - midpoint)
        return deviation

    def deplete_random_edges(self, G, percentage):
        """
        Set weight=0 on percentage% random edges
        """
        num_edges_to_deplete = int(len(G.edges) * percentage / 100)
        edges = list(G.edges)
        edges_to_deplete = random.sample(edges, num_edges_to_deplete)

        for u, v in edges_to_deplete:
            G[u][v]['weight'] = 0

    def run_single_experiment(self, depletion_percent):
        """
        Run one experiment: deplete, rebalance, measure improvement
        """
        G_copy = copy.deepcopy(self.G_original)

        self.deplete_random_edges(G_copy, depletion_percent)

        initial_dev = self.total_deviation(G_copy)

        rebalance = rebalancer.GlobalReviveRebalancer(G_copy)
        rebalance.run()

        final_dev = self.total_deviation(G_copy)

        if initial_dev == 0:
            return 0  # Avoid divide by zero

        improvement = (initial_dev - final_dev) / initial_dev * 100

        return improvement

    def run_full_simulation(self, depletion_percents, repeats_per_percent=5):
        """
        Run simulation across multiple depletion percentages
        """
        for percent in depletion_percents:
            improvements = []
            for _ in range(repeats_per_percent):
                improvement = self.run_single_experiment(percent)
                improvements.append(improvement)
            avg_improvement = sum(improvements) / len(improvements)
            self.results[percent] = avg_improvement

    def plot_results(self):
        """
        Plot depletion percentage vs average improvement
        """
        percents = sorted(self.results.keys())
        improvements = [self.results[p] for p in percents]

        plt.figure(figsize=(10,6))
        plt.plot(percents, improvements, marker='o', linestyle='-', color='blue')
        plt.title('Rebalancing Improvement vs Channel Depletion')
        plt.xlabel('Channel Depletion Percentage (%)')
        plt.ylabel('Deviation Improvement (%)')
        plt.grid(True)
        plt.show()