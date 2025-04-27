import random
import copy
import matplotlib.pyplot as plt
import rebalancer  # Your GlobalReviveRebalancer
import networkx as nx
import graph_display

class DepletionSimulator:
    def __init__(self, G):
        """
        G: NetworkX DiGraph with 'weight' and 'capacity' on edges
        """
        self.G_original = G
        self.results = {}
        self.results_stuck = {}

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
            temp = G[u][v]['weight']
            G[u][v]['weight'] = 0
            G[v][u]['weight'] += temp

    def count_stuck_nodes(self, G):
        """
        Count number of nodes that have depleted channels and are not part of any cycle.
        """
        stuck_nodes = 0

        # Find all simple cycles (up to max length, say 6)
        all_cycles = list(nx.simple_cycles(G))

        nodes_in_cycles = set()
        for cycle in all_cycles:
            for node in cycle:
                nodes_in_cycles.add(node)

        for node in G.nodes:
            outgoing_edges = G.out_edges(node, data=True)

            # Check if all outgoing edges are weight = 0
            all_depleted = all(data['weight'] == 0 for _, _, data in outgoing_edges)

            # If node is depleted and not part of any cycle -> stuck
            if all_depleted and node not in nodes_in_cycles:
                stuck_nodes += 1

        return stuck_nodes


    def run_single_experiment(self, depletion_percent):
        """
        Run one experiment: deplete, rebalance, measure improvement, count stuck nodes.
        """
        G_copy = copy.deepcopy(self.G_original)

        self.deplete_random_edges(G_copy, depletion_percent)

        stuck_nodes = self.count_stuck_nodes(G_copy)

        initial_dev = self.total_deviation(G_copy)

        rebalance = rebalancer.GlobalReviveRebalancer(G_copy)
        rebalance.run()

        final_dev = self.total_deviation(G_copy)

        if initial_dev == 0:
            improvement = 0
        else:
            improvement = (initial_dev - final_dev) / initial_dev * 100

        return improvement, stuck_nodes


    def run_single_experiment_prime(self, depletion_percent):
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

        # pos = nx.spring_layout(G_copy, seed=42, k=1.5)
        # graph_display.draw_graph(G_copy, pos, "Initial Graph")

        return improvement

    def run_full_simulation(self, depletion_percents, repeats_per_percent=5):
        """
        Run simulation across multiple depletion percentages
        """
        for percent in depletion_percents:
            improvements = []
            stuck_nodes = []
            for _ in range(repeats_per_percent):
                improvement, stuck_node = self.run_single_experiment(percent)
                improvements.append(improvement)
                stuck_nodes.append(stuck_node)
            avg_improvement = sum(improvements) / len(improvements)
            avg_stuck_nodes = sum(stuck_nodes) / len(stuck_nodes)
            self.results[percent] = avg_improvement
            self.results_stuck[percent] = avg_stuck_nodes

    def plot_results(self):
        """
        Plot depletion percentage vs average improvement
        """
        percents = sorted(self.results.keys())
        improvements = [self.results[p] for p in percents]
        stuck_nodes = [self.results_stuck[p] for p in percents]

        plt.figure(figsize=(10,6))
        plt.plot(percents, improvements, marker='o', linestyle='-', color='blue')
        plt.title('Rebalancing Improvement vs Channel Depletion')
        plt.xlabel('Channel Depletion Percentage (%)')
        plt.ylabel('Deviation Improvement (%)')
        plt.grid(True)
        plt.show()


        print(self.results_stuck)


        # """
        # Plot stuck nodes count vs depletion percentage as a bar graph.
        # """
        # percents = sorted(self.results_stuck.keys())
        # stuck_counts = [self.results_stuck[p] for p in percents]

        # plt.figure(figsize=(10,6))
        # plt.bar(percents, stuck_counts, color='red', width=5)
        # plt.title('On-Chain Operations Needed vs Channel Depletion')
        # plt.xlabel('Channel Depletion Percentage (%)')
        # plt.ylabel('Average Stuck Nodes (Need On-Chain)')
        # plt.grid(axis='y')
        # plt.show()