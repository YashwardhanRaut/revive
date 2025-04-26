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