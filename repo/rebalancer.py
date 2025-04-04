import networkx as nx

def find_and_rebalance_cycles(G):
    """
    Finds cycles and simulates rebalancing along them.
    For now, it adjusts weights in the simplest way to simulate capacity balancing.
    """
    cycles = list(nx.simple_cycles(G))
    print(f"Found {len(cycles)} cycles")

    for cycle in cycles:
        # Only consider cycles with 3 or more nodes
        if len(cycle) < 3:
            continue

        # Close the cycle
        cycle.append(cycle[0])

        # Get weights of all edges in the cycle
        weights = []
        for i in range(len(cycle) - 1):
            u, v = cycle[i], cycle[i+1]
            weights.append(G[u][v]['weight'])

        # Find the bottleneck (min flow we can rebalance)
        min_weight = min(weights)

        print(f"Cycle: {cycle}, min transferable: {min_weight}")

        # Subtract from forward edges, add to reverse (simulating a rebalancing step)
        for i in range(len(cycle) - 1):
            u, v = cycle[i], cycle[i+1]
            G[u][v]['weight'] -= min_weight

            if G.has_edge(v, u):
                G[v][u]['weight'] += min_weight
            else:
                G.add_edge(v, u, weight=min_weight)

    return G
