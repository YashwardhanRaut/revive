import networkx as nx
from scipy.optimize import linprog

class Rebalancer:
    def __init__(self, G):
        self.G = G  # G is a NetworkX DiGraph with capacity attributes

    def cyclic_rebalance(self):
        depleted_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d.get('capacity', 1) == 0]
        all_cycles = self.find_all_cycles(limit=6)  # small cycles only for tractability

        # Filter cycles that include reverse of depleted channels
        candidate_cycles = [cycle for cycle in all_cycles if any((v, u) in self.edges_in_cycle(cycle) for (u, v) in depleted_edges)]

        if not candidate_cycles:
            print("No candidate cycles found for rebalancing.")
            return

        edge_index = {e: i for i, e in enumerate(self.G.edges())}
        num_edges = len(edge_index)
        num_cycles = len(candidate_cycles)

        A = [[0] * num_cycles for _ in range(num_edges)]
        b = [self.G.edges[e].get('capacity', 0) for e in edge_index]

        # Fill A matrix
        for j, cycle in enumerate(candidate_cycles):
            edges = self.edges_in_cycle(cycle)
            for e in edges:
                if e in edge_index:
                    A[edge_index[e]][j] = 1

        # LP: max sum of cycle flows -> min -sum
        c = [-1.0] * num_cycles

        bounds = [(0, None)] * num_cycles

        res = linprog(c=c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

        if res.success:
            flows = res.x
            for j, flow in enumerate(flows):
                if flow > 0:
                    print(f"Cycle {candidate_cycles[j]} -> Flow: {flow:.4f}")
                    self.apply_flow(candidate_cycles[j], flow)
        else:
            print("Rebalancing LP failed:", res.message)

    def find_all_cycles(self, limit=6):
        cycles = []
        for cycle in nx.simple_cycles(self.G):
            if 2 <= len(cycle) <= limit:
                # Ensure it's a proper cycle
                cycle.append(cycle[0])
                cycles.append(cycle)
        return cycles

    def edges_in_cycle(self, cycle):
        return [(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)]

    def apply_flow(self, cycle, flow):
        for u, v in self.edges_in_cycle(cycle):
            if self.G[u][v]['capacity'] >= flow:
                self.G[u][v]['capacity'] -= flow
                if self.G.has_edge(v, u):
                    self.G[v][u]['capacity'] += flow
            else:
                print(f"Warning: Insufficient capacity on edge ({u}->{v}) for flow {flow}")









# import networkx as nx
# from scipy.optimize import linprog

# def optimize_flow_in_cycle(G, cycle):
#     """
#     Given a directed cycle, this sets up and solves an LP to rebalance the cycle.
#     """
#     edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]

#     capacities = []
#     for u, v in edges:
#         if 'weight' not in G[u][v]:
#             print(f"Missing weight on edge {u}->{v}")
#             return
#         capacities.append(G[u][v]['weight'])

#     # Linear Program: maximize x (flow pushed through the cycle)
#     # Convert to minimize -x for linprog
#     c = [-1]

#     # Constraints: x <= capacity on each edge
#     A_ub = [[1] for _ in edges]
#     b_ub = capacities

#     bounds = [(0, None)]  # x >= 0

#     res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

#     if res.success:
#         flow = res.x[0]
#         print(f"Pushing flow {flow:.2f} through cycle {cycle}")
#         for u, v in edges:
#             G[u][v]['weight'] -= flow
#             if G.has_edge(v, u):
#                 G[v][u]['weight'] += flow
#             else:
#                 G.add_edge(v, u, weight=flow)
#     else:
#         print(f"LP failed on cycle {cycle}: {res.message}")


# def rebalance_with_lp(G):
#     """
#     Finds simple cycles and applies LP-based rebalancing.
#     """
#     print("Finding cycles for LP-based rebalancing...")
#     cycles = list(nx.simple_cycles(G))
#     print(f"Found {len(cycles)} cycles")

#     for cycle in cycles:
#         if len(cycle) >= 3:
#             optimize_flow_in_cycle(G, cycle)
