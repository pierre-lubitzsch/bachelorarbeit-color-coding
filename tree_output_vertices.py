import networkx as nx
import matplotlib.pyplot as plt
import math
import random


"""
for v \in V(G) colortable[v] contains all color sets that appear on colorful copies of T in G in which v has the role of r.
we assume that V(G) = {0, 1, ..., n - 1}
in treetable[v][C] we save the vertices of a subgraph of G, where this subgraph corresponds to T in G. here also v plays the role of r in T
and C is the set of colors appearing on the copy of T in G we saved
"""
def find_colorful_tree_from_root(G: nx.graph.Graph, T: nx.graph.Graph, n: int, k: int, c, r):
    treetable = [dict() for _ in range(n)]
    if (k == 1):
        for v in G.nodes:
            treetable[v][frozenset([c[v]])] = (v,)
        return treetable
    
    # now we pick any r' \in V(T) with {r, r'} \in E(T)
    assert(len(list(T.adj[r])) > 0)
    r_prime = list(T.adj[r])[0]

    # create the subgraphes induced when removing {r, r'} and call find_colorful_tree_from_root on them
    T.remove_edge(r, r_prime)
    components = list(nx.connected_components(T))
    assert(len(components) == 2)
    T_1 = T.subgraph(components[0]).copy()
    T_2 = T.subgraph(components[1]).copy()

    T.add_edge(r, r_prime)
    # make sure that r \in T_1 and r_prime \in T_2
    if (r not in T_1.nodes):
        T_1, T_2 = T_2, T_1
    assert(r in T_1.nodes)
    assert(r_prime in T_2.nodes)

    treetable_1 = find_colorful_tree_from_root(G, T_1, n, len(T_1.nodes), c, r)
    treetable_2 = find_colorful_tree_from_root(G, T_2, n, len(T_2.nodes), c, r_prime)

    for (u, v) in G.edges:
        for C_1 in treetable_1[u].keys():
            for C_2 in treetable_2[v].keys():
                if (C_1.isdisjoint(C_2)):
                    C = set(C_1)
                    C.update(C_2)
                    C = frozenset(C)
                    treetable[u][C] = treetable_1[u][C_1] + treetable_2[v][C_2]
        
        for C_1 in treetable_1[v].keys():
            for C_2 in treetable_2[u].keys():
                if (C_1.isdisjoint(C_2)):
                    C = set(C_1)
                    C.update(C_2)
                    C = frozenset(C)
                    treetable[v][C] = treetable_1[v][C_1] + treetable_2[u][C_2]

    return treetable

"""
find a copy of a tree T on k vertices in a graph G on n vertices
"""
def find_tree(G: nx.graph.Graph, T: nx.graph.Graph, n: int, k: int):
    if (k > n):
        return "NO"
    c = dict()

    # get a random coloring e^k times and execute the coloring algorithm with it
    for _ in range(math.ceil(pow(math.e, k))):
        for v in G.nodes:
            # assign uniformly random value to coloring
            c[v] = random.randint(1, k)
        
        treetable = find_colorful_tree_from_root(G, T, n, k, c, tuple(G.nodes)[0])
        for v in G.nodes:
            if (len(treetable[v].keys()) > 0):
                tree_colorset = list(treetable[v].keys())[0]
                return tree_colorset, treetable[v][tree_colorset]

    return "NO"