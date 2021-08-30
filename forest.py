import networkx as nx
import matplotlib.pyplot as plt
import math
import random
import tree_output_vertices as tree





def find_colorful_forest(G: nx.graph.Graph, F: nx.graph.Graph, n: int, k: int, c, trees):
    # for v a node of G and C a colorset witnesses[v][C] contains a set of nodes of G isomorphic to T,
    # having colors like in C and where v plays the role of the chosen root r in the loop
    witnesses = dict()

    nodes = [tuple(T.nodes) for T in trees]

    for i in range(len(trees)):
        witnesses[nodes[i]] = dict()
        k_i = len(nodes[i])
        r = nodes[i][0]
        treetable = tree.find_colorful_tree_from_root(G, trees[i], n, k_i, c, r)

        for v in G.nodes:
            for C in treetable[v].keys():
                if C in witnesses[nodes[i]].keys():
                    continue
                witnesses[nodes[i]][C] = treetable[v][C]
    
    forest = nodes[0]
    dp = dict()
    dp[forest] = dict()

    for C in witnesses[forest].keys():
        dp[forest][C] = (witnesses[forest][C],)

    for i in range(1, len(trees)):
        new_forest = forest + nodes[i]
        dp[new_forest] = dict()
        for C_1 in dp[forest].keys():
            for C_2 in witnesses[nodes[i]].keys():
                if (C_1.isdisjoint(C_2)):
                    C = set(C_1)
                    C.update(C_2)
                    C = frozenset(C)
                    dp[new_forest][C] = dp[forest][C_1] + (witnesses[nodes[i]][C_2],)

        forest = new_forest

    if (len(dp[forest]) == 0):
        return (None, None)
    
    C = list(dp[forest].keys())[0]
    return C, dp[forest][C]



"""
find a copy of a forest F on k vertices in a graph G on n vertices
"""
def find_forest(G: nx.graph.Graph, F: nx.graph.Graph, n: int, k: int):
    if (k > n):
        return (None, None)
    c = dict()

    trees = [F.subgraph(component).copy() for component in nx.connected_components(F)]

    # get a random coloring e^k times and execute the coloring algorithm with it
    for _ in range(math.ceil(pow(math.e, k))):
        for v in G.nodes:
            # assign uniformly random value to coloring
            c[v] = random.randint(1, k)
        
        colors, forest = find_colorful_forest(G, F, n, k, c, trees)
        if ((colors, forest) != (None, None)):
            return colors, forest

    return (None, None)