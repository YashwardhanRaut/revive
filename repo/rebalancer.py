import networkx as nx
from pulp import LpProblem, LpVariable, LpMaximize, LpStatus

def find_cycles(G):
    cycles = list(nx.simple_cycles(G))
    valid_cycles = [cycle for cycle in cycles if len(cycle) >= 3]
    return valid_cycles

def find_cycles_with_depleted_edge(G):
    all_cycles = list(nx.simple_cycles(G))
    filtered_cycles = []

    for cycle in all_cycles:
        if len(cycle) < 3:
            continue
        edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]
        has_depleted_edge = any(G[u][v]['weight'] == 0 for u, v in edges)
        if has_depleted_edge:
            filtered_cycles.append(cycle)

    return filtered_cycles

def reweight_cycle(cycle, G):
    edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]
    prob = LpProblem("MidpointRebalancing", LpMaximize)
    x = LpVariable("x", lowBound=0)
    max_x_possible = []

    for u, v in edges:
        b_fwd = G[u][v]['weight']
        c_fwd = G[u][v]['capacity']
        b_rev = G[v][u]['weight']
        c_rev = G[v][u]['capacity']
        midpoint = c_fwd / 2

        if b_fwd < midpoint:
            max_push = min(midpoint - b_fwd, b_rev)
            prob += b_fwd + x <= midpoint
            prob += b_rev - x >= 0
            max_x_possible.append(max_push)

        elif b_fwd > midpoint:
            max_push = min(b_fwd - midpoint, c_rev - b_rev)
            prob += b_fwd - x >= midpoint
            prob += b_rev + x <= c_rev
            max_x_possible.append(max_push)

        else:
            continue

    prob += x
    if max_x_possible:
        prob += x <= min(max_x_possible)

    status = prob.solve()
    if LpStatus[status] == "Optimal" and x.varValue > 0:
        flow = x.varValue
        for u, v in edges:
            b_fwd = G[u][v]['weight']
            c_fwd = G[u][v]['capacity']
            midpoint = c_fwd / 2

            if b_fwd < midpoint:
                G[u][v]['weight'] += flow
                G[v][u]['weight'] -= flow
            else:
                G[u][v]['weight'] -= flow
                G[v][u]['weight'] += flow
        return True, flow

    return False, 0

def total_flow(cycles, G):
    total = 0
    for cycle in cycles:
        success, flow = reweight_cycle(cycle, G)
        if success:
            aliases = [G.nodes[c].get("alias", c) for c in cycle]
            print(f"Reweightd cycle {aliases} with flow {flow}")
            total += flow
    print(f"Total reweightd flow: {total}")
    return total













# import networkx as nx

# def find_cycles(G):
#     # Assuming G is your directed graph
#     cycles = list(nx.simple_cycles(G))

#     # Filter cycles with length >= 3 (optional)
#     valid_cycles = [cycle for cycle in cycles if len(cycle) >= 3]

#     return valid_cycles
# # print("Found cycles:")
# # for c in valid_cycles:
# #     print(c)


# def find_cycles_with_depleted_edge(G):
#     all_cycles = list(nx.simple_cycles(G))
#     filtered_cycles = []

#     for cycle in all_cycles:
#         if len(cycle) < 3:
#             continue  # skip short cycles

#         # Build edge list for this cycle
#         edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]

#         # Check if at least one edge has weight 0
#         has_depleted_edge = any(G[u][v]['weight'] == 0 for u, v in edges)
#         if has_depleted_edge:
#             filtered_cycles.append(cycle)

#     return filtered_cycles


# from pulp import LpProblem, LpVariable, LpMaximize, LpStatus, lpSum

# def reweight_cycle(cycle, G):
#     # Build directed edges from cycle
#     edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]

#     # Create LP problem
#     # prob = LpProblem("CycleRebalancing", LpMaximize)
#     prob = LpProblem("MidpointRebalancing", LpMaximize)

#     # Single flow variable
#     x = LpVariable("x", lowBound=0)

#     max_x_possible = []

#     # Constraints: For each edge, weight + delta*x in [0, capacity]
#     for u, v in edges:
#         # delta = +1 in direction u->v, -1 in direction v->u
#         delta = 1
#         # b = weight[u][v]
#         # c = capacity[u][v]
#         b = G[u][v]['weight']
#         c = G[u][v]['capacity']
#         midpoint = c / 2

#         if b < midpoint:
#             # Flow should increase weight
#             max_push = midpoint - b
#             prob += b + delta * x <= midpoint
#             prob += b + delta * x >= 0
#             max_x_possible.append(max_push)
#         elif b > midpoint:
#             # Flow should decrease weight
#             max_push = b - midpoint
#             prob += b - delta * x >= midpoint
#             prob += b - delta * x <= c
#             max_x_possible.append(max_push)
#         else:
#             continue

#     # Objective: maximize x
#     prob += x

#     # Upper bound for x is minimum across all edges (to avoid overshooting midpoint)
#     if max_x_possible:
#         prob += x <= min(max_x_possible)


#     # Solve LP
#     status = prob.solve()
#     if LpStatus[status] == "Optimal" and x.varValue > 0:
#         flow = x.varValue
#         for u, v in edges:
#             b = G[u][v]['weight']
#             c = G[u][v]['capacity']
#             midpoint = int(c / 2)

#             if b < midpoint:
#                 G[u][v]['weight'] += flow
#                 G[v][u]['weight'] -= flow
#             else:
#                 G[u][v]['weight'] -= flow
#                 G[v][u]['weight'] += flow
#         return True, flow
#     return False, 0

# def total_flow(cycles, G):
#     total_flow = 0
#     for cycle in cycles:
#         success, flow = reweight_cycle(cycle, G)
#         if success:
#             a = []
#             for c in cycle:
#                 # print(c)
#                 # print(G.nodes[c].get("alias", c))
#                 a.append(G.nodes[c].get("alias", c))
#             print(f"Reweightd cycle {a} with flow {flow}")
#             total_flow += flow
#     print(f"Total reweightd flow: {total_flow}")
#     return total_flow




# import networkx as nx
# from scipy.optimize import linprog

# class Reweightr:
#     def __init__(self, G):
#         self.G = G  # G is a NetworkX DiGraph with capacity attributes

#     def cyclic_reweight(self):
#         depleted_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d.get('capacity', 1) == 0]
#         all_cycles = self.find_all_cycles(limit=6)  # small cycles only for tractability

#         # Filter cycles that include reverse of depleted channels
#         candidate_cycles = [cycle for cycle in all_cycles if any((v, u) in self.edges_in_cycle(cycle) for (u, v) in depleted_edges)]

#         if not candidate_cycles:
#             print("No candidate cycles found for rebalancing.")
#             return

#         edge_index = {e: i for i, e in enumerate(self.G.edges())}
#         num_edges = len(edge_index)
#         num_cycles = len(candidate_cycles)

#         A = [[0] * num_cycles for _ in range(num_edges)]
#         b = [self.G.edges[e].get('capacity', 0) for e in edge_index]

#         # Fill A matrix
#         for j, cycle in enumerate(candidate_cycles):
#             edges = self.edges_in_cycle(cycle)
#             for e in edges:
#                 if e in edge_index:
#                     A[edge_index[e]][j] = 1

#         # LP: max sum of cycle flows -> min -sum
#         c = [-1.0] * num_cycles

#         bounds = [(0, None)] * num_cycles

#         res = linprog(c=c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

#         if res.success:
#             flows = res.x
#             for j, flow in enumerate(flows):
#                 if flow > 0:
#                     print(f"Cycle {candidate_cycles[j]} -> Flow: {flow:.4f}")
#                     self.apply_flow(candidate_cycles[j], flow)
#         else:
#             print("Rebalancing LP failed:", res.message)

#     def find_all_cycles(self, limit=6):
#         cycles = []
#         for cycle in nx.simple_cycles(self.G):
#             if 2 <= len(cycle) <= limit:
#                 # Ensure it's a proper cycle
#                 cycle.append(cycle[0])
#                 cycles.append(cycle)
#         return cycles

#     def edges_in_cycle(self, cycle):
#         return [(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)]

#     def apply_flow(self, cycle, flow):
#         for u, v in self.edges_in_cycle(cycle):
#             if self.G[u][v]['capacity'] >= flow:
#                 self.G[u][v]['capacity'] -= flow
#                 if self.G.has_edge(v, u):
#                     self.G[v][u]['capacity'] += flow
#             else:
#                 print(f"Warning: Insufficient capacity on edge ({u}->{v}) for flow {flow}")









# # import networkx as nx
# # from scipy.optimize import linprog

# # def optimize_flow_in_cycle(G, cycle):
# #     """
# #     Given a directed cycle, this sets up and solves an LP to reweight the cycle.
# #     """
# #     edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]

# #     capacities = []
# #     for u, v in edges:
# #         if 'weight' not in G[u][v]:
# #             print(f"Missing weight on edge {u}->{v}")
# #             return
# #         capacities.append(G[u][v]['weight'])

# #     # Linear Program: maximize x (flow pushed through the cycle)
# #     # Convert to minimize -x for linprog
# #     c = [-1]

# #     # Constraints: x <= capacity on each edge
# #     A_ub = [[1] for _ in edges]
# #     b_ub = capacities

# #     bounds = [(0, None)]  # x >= 0

# #     res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

# #     if res.success:
# #         flow = res.x[0]
# #         print(f"Pushing flow {flow:.2f} through cycle {cycle}")
# #         for u, v in edges:
# #             G[u][v]['weight'] -= flow
# #             if G.has_edge(v, u):
# #                 G[v][u]['weight'] += flow
# #             else:
# #                 G.add_edge(v, u, weight=flow)
# #     else:
# #         print(f"LP failed on cycle {cycle}: {res.message}")


# # def reweight_with_lp(G):
# #     """
# #     Finds simple cycles and applies LP-based rebalancing.
# #     """
# #     print("Finding cycles for LP-based rebalancing...")
# #     cycles = list(nx.simple_cycles(G))
# #     print(f"Found {len(cycles)} cycles")

# #     for cycle in cycles:
# #         if len(cycle) >= 3:
# #             optimize_flow_in_cycle(G, cycle)
