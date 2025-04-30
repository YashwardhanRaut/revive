import networkx as nx
import pulp

class GlobalReviveRebalancer:
    def __init__(self, G, cycles=None, max_cycle_length=6):
        """
        G: NetworkX DiGraph
        cycles: optional list of cycles [(u,v,w,u), ...]
        max_cycle_length: maximum length of cycles to consider
        """
        self.G = G
        self.max_cycle_length = max_cycle_length
        self.cycles = cycles or self.find_cycles()
        self.lp = None
        self.cycle_vars = {}
        self.deviation_vars = {}

    def plot_stuck_nodes(self):
        """
        Plot stuck degree-1 nodes vs depletion percentage as a bar graph.
        """
        if not self.results_stuck:
            print("No stuck node results to plot!")
            return

        percents = sorted(self.results_stuck.keys())
        stuck_counts = [self.results_stuck[p] for p in percents]

        plt.figure(figsize=(10,6))
        plt.bar(percents, stuck_counts, color='orange', width=5)
        plt.title('Stuck Degree-1 Nodes vs Channel Depletion')
        plt.xlabel('Channel Depletion Percentage (%)')
        plt.ylabel('Avg. Stuck Nodes (Deg=1, Depleted Outgoing)')
        plt.grid(axis='y')
        plt.show()


    def find_cycles(self):
        """
        Find all simple cycles up to a given length.
        (You can replace this later with smarter cycle finding.)
        """
        all_cycles = []
        for cycle in nx.simple_cycles(self.G):
            if 2 <= len(cycle) <= self.max_cycle_length:
                # Simple fix to ensure cycles are closed
                cycle.append(cycle[0])
                all_cycles.append(cycle)
        return all_cycles

    def setup_lp(self):
        """
        Set up the global Revive LP problem.
        """
        self.lp = pulp.LpProblem("ReviveGlobalRebalance", pulp.LpMinimize)

        # 1. Create variables
        for idx, cycle in enumerate(self.cycles):
            var = pulp.LpVariable(f"flow_c{idx}", lowBound=-1e9, upBound=1e9)
            self.cycle_vars[idx] = var

        for u, v in self.G.edges:
            var = pulp.LpVariable(f"deviation_{u}_{v}", lowBound=0)
            self.deviation_vars[(u, v)] = var

        # 2. Edge constraints (balance after applying cycles must be within [0, capacity])
        for u, v, data in self.G.edges(data=True):
            capacity = data['capacity']
            balance = data['weight']

            flow_contribs = []
            for idx, cycle in enumerate(self.cycles):
                for i in range(len(cycle) - 1):
                    if (cycle[i], cycle[i+1]) == (u, v):
                        flow_contribs.append(+1 * self.cycle_vars[idx])
                    elif (cycle[i+1], cycle[i]) == (u, v):
                        flow_contribs.append(-1 * self.cycle_vars[idx])

            total_flow = pulp.lpSum(flow_contribs)
            final_balance = balance + total_flow

            self.lp += (final_balance >= 0), f"edge_capacity_low_{u}_{v}"
            self.lp += (final_balance <= capacity), f"edge_capacity_high_{u}_{v}"

            # 3. Link final balances and deviation variables
            midpoint = capacity / 2
            deviation = self.deviation_vars[(u, v)]
            self.lp += (final_balance - midpoint <= deviation), f"deviation_pos_{u}_{v}"
            self.lp += (midpoint - final_balance <= deviation), f"deviation_neg_{u}_{v}"

        # 4. Objective: Minimize sum of deviations
        self.lp += pulp.lpSum(self.deviation_vars.values()), "TotalDeviation"

    def solve_lp(self):
        """
        Solve the LP.
        """
        self.lp.solve()
        if self.lp.status != pulp.LpStatusOptimal:
            raise Exception("LP did not find optimal solution!")

    def apply_flows(self):
    # """Apply the solved flows back to the graph."""
        for idx, cycle in enumerate(self.cycles):
            flow_value = pulp.value(self.cycle_vars[idx])
            for i in range(len(cycle) - 1):
                u, v = cycle[i], cycle[i+1]
                if self.G.has_edge(u, v):
                    self.G[u][v]['weight'] += flow_value
                if self.G.has_edge(v, u):
                    self.G[v][u]['weight'] -= flow_value


    def count_stuck_nodes_degree_one(self):
        """
        Count nodes that had degree == 1 and their single outgoing edge has weight == 0.
        """
        stuck = 0

        for node in self.G.nodes:
            degree = self.G.nodes[node].get('degree', 0)
            if degree != 1:
                continue  # Only count nodes with degree exactly 1

            outgoing_edges = list(self.G.out_edges(node, data=True))
            if len(outgoing_edges) != 1:
                continue  # Must have exactly one outgoing edge

            _, _, data = outgoing_edges[0]
            if data['weight'] == 0:
                stuck += 1

        return stuck



    def run(self):
        """
        Full pipeline: setup, solve, apply.
        """
        self.setup_lp()
        self.solve_lp()
        self.apply_flows()