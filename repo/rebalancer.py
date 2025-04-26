# import networkx as nx
# from pulp import LpProblem, LpVariable, LpMaximize, LpStatus

# def find_cycles(G):
#     cycles = list(nx.simple_cycles(G))
#     valid_cycles = [cycle for cycle in cycles if len(cycle) >= 3]
#     return valid_cycles

# def find_cycles_with_depleted_edge(G):
#     all_cycles = list(nx.simple_cycles(G))
#     filtered_cycles = []
#     for cycle in all_cycles:
#         if len(cycle) < 3:
#             continue
#         edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]
#         has_depleted_edge = any(G[u][v]['weight'] == 0 for u, v in edges)
#         if has_depleted_edge:
#             filtered_cycles.append(cycle)
#     return filtered_cycles


# def reweight_cycle(cycle, G):
#     edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]
#     prob = LpProblem("HealthyMidpointRebalancing", LpMaximize)
#     x = LpVariable("x", lowBound=0)
#     max_x_possible = []

#     for u, v in edges:
#         b_fwd = G[u][v]['weight']
#         c_fwd = G[u][v]['capacity']
#         b_rev = G[v][u]['weight']
#         c_rev = G[v][u]['capacity']
#         midpoint = c_fwd / 2

#         # 🧠 Healthy Threshold {Must be tested experimentally}
#         healthy_threshold_fwd = max(10000, 0.1 * c_fwd)  # min(10k sats or 10% of capacity)
#         healthy_threshold_rev = max(10000, 0.1 * c_rev)

#         if b_fwd == 0:
#             # If originally depleted, don't need to maintain threshold
#             continue

#         if b_fwd < midpoint:
#             max_push = min(midpoint - b_fwd, b_rev)
#             prob += b_fwd + x <= midpoint
#             prob += b_rev - x >= healthy_threshold_rev
#             prob += b_fwd + x >= healthy_threshold_fwd
#             max_x_possible.append(max_push)

#         elif b_fwd > midpoint:
#             max_push = min(b_fwd - midpoint, c_rev - b_rev)
#             prob += b_fwd - x >= midpoint
#             prob += b_rev + x <= c_rev
#             prob += b_fwd - x >= healthy_threshold_fwd
#             prob += b_rev + x >= healthy_threshold_rev
#             max_x_possible.append(max_push)

#         else:
#             continue

#     prob += x
#     if max_x_possible:
#         prob += x <= min(max_x_possible)

#     status = prob.solve()
#     if LpStatus[status] == "Optimal" and x.varValue > 0:
#         flow = x.varValue
#         for u, v in edges:
#             b_fwd = G[u][v]['weight']
#             c_fwd = G[u][v]['capacity']
#             midpoint = c_fwd / 2

#             if b_fwd < midpoint:
#                 G[u][v]['weight'] += flow
#                 G[v][u]['weight'] -= flow
#             else:
#                 G[u][v]['weight'] -= flow
#                 G[v][u]['weight'] += flow

#         return True, flow

#     return False, 0

# def total_flow(cycles, G):
#     total = 0
#     for cycle in cycles:
#         success, flow = reweight_cycle(cycle, G)
#         if success:
#             aliases = [G.nodes[c].get("alias", c) for c in cycle]
#             print(f"Reweightd cycle {aliases} with flow {flow}")
#             total += flow
#     print(f"Total reweightd flow: {total}")
#     return total


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


    def apply_flows1(self):
        """
        Apply the solved flows back to the graph.
        """
        # First, build a mapping of net adjustments
        adjustment = {(u, v): 0 for u, v in self.G.edges}
        for idx, cycle in enumerate(self.cycles):
            flow_value = pulp.value(self.cycle_vars[idx])
            for i in range(len(cycle) - 1):
                u, v = cycle[i], cycle[i+1]
                if (u, v) in adjustment:
                    adjustment[(u, v)] += flow_value
                elif (v, u) in adjustment:
                    adjustment[(v, u)] -= flow_value

        # Now apply adjustments
        for (u, v), delta in adjustment.items():
            self.G[u][v]['weight'] += delta

    def run(self):
        """
        Full pipeline: setup, solve, apply.
        """
        self.setup_lp()
        self.solve_lp()
        self.apply_flows()
