import networkx as nx
from scipy.optimize import linprog

def optimize_flow_in_cycle(G, cycle):
    """
    Given a directed cycle, this sets up and solves an LP to rebalance the cycle.
    """
    edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]

    capacities = []
    for u, v in edges:
        if 'weight' not in G[u][v]:
            print(f"Missing weight on edge {u}->{v}")
            return
        capacities.append(G[u][v]['weight'])

    # Linear Program: maximize x (flow pushed through the cycle)
    # Convert to minimize -x for linprog
    c = [-1]

    # Constraints: x <= capacity on each edge
    A_ub = [[1] for _ in edges]
    b_ub = capacities

    bounds = [(0, None)]  # x >= 0

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if res.success:
        flow = res.x[0]
        print(f"Pushing flow {flow:.2f} through cycle {cycle}")
        for u, v in edges:
            G[u][v]['weight'] -= flow
            if G.has_edge(v, u):
                G[v][u]['weight'] += flow
            else:
                G.add_edge(v, u, weight=flow)
    else:
        print(f"LP failed on cycle {cycle}: {res.message}")


def rebalance_with_lp(G):
    """
    Finds simple cycles and applies LP-based rebalancing.
    """
    print("Finding cycles for LP-based rebalancing...")
    cycles = list(nx.simple_cycles(G))
    print(f"Found {len(cycles)} cycles")

    for cycle in cycles:
        if len(cycle) >= 3:
            optimize_flow_in_cycle(G, cycle)
