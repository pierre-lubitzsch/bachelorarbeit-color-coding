import networkx as nx
import matplotlib.pyplot as plt
import math
import random
import itertools



"""
for v \in V(G) colortable[v] contains all color sets that appear on colorful copies of T in G in which v has the role of r.
we assume that V(G) = {0, 1, ..., n - 1}
"""
def find_colorful_tree_from_root(G: nx.graph.Graph, T: nx.graph.Graph, n: int, k: int, c, r):
    colortable = [set() for _ in range(n)]
    if (k == 1):
        for v in G.nodes:
            colortable[v].add(frozenset([c[v]]))
        return colortable
    
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

    color_1 = find_colorful_tree_from_root(G, T_1, n, len(T_1.nodes), c, r)
    color_2 = find_colorful_tree_from_root(G, T_2, n, len(T_2.nodes), c, r_prime)

    for (u, v) in G.edges:
        for C_1 in color_1[u]:
            for C_2 in color_2[v]:
                if (C_1.isdisjoint(C_2)):
                    C = set(C_1)
                    C.update(C_2)
                    colortable[u].add(frozenset(C))
        
        for C_1 in color_1[v]:
            for C_2 in color_2[u]:
                if (C_1.isdisjoint(C_2)):
                    C = set(C_1)
                    C.update(C_2)
                    colortable[v].add(frozenset(C))

    return colortable

"""
execute the colorful copy path-finding algorithm to find P_k at most e^k times
with uniformly random colorings c : V -> [k]
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
        
        colortable = find_colorful_tree_from_root(G, T, n, k, c, tuple(G.nodes)[0])
        for v in G.nodes:
            if (len(colortable[v]) > 0):
                return list(colortable[v])[0]

    return "NO"

"""
returns True iff path is a path of length k in G
"""
def test_path_length_k(G: nx.graph.Graph, path : [], k: int):
    if (len(path) < k):
        return False
    for i in range(len(path) - 1):
        if (not G.has_edge(path[i], path[i + 1])):
            return False
    return True
    


def main():
    G = nx.Graph()
    with open("nodes.txt", 'r') as f:
        for v in f:
            if (v == ''):
                continue
            G.add_node(int(v))

    with open("edges.txt", 'r') as f:
        for line in f:
            (u, v, w) = line.split(';')
            G.add_edge(int(u), int(v), weight=float(w))

    #T = prim(G, len(list(G.nodes)))

    T = nx.star_graph(3)

    print("Does G contain the 3-star graph? {}".format(find_tree(G, T, len(G.nodes), len(T.nodes))))



if (__name__ == "__main__"):
    main()

    """
    print(list(G.nodes))
    for (u, v) in G.edges:
        print(u, v, G[u][v]["weight"])

    nx.draw(T, with_labels=True, font_weight="bold")
    plt.savefig("abcdefg.png")
    plt.show()


    debug
    print('\n\n\n\n\n')
    for i in range(k):
        print("length =", i)
        for v in G.nodes:
            print("Node: {}, colorsets: {}".format(v, dp[v][i]))
    """

"""
    print("T:", list(T.nodes), list(T.edges))
    print("connected componets of T", list(nx.connected_components(T)))
    print("T_1:", list(T_1.nodes), list(T_1.edges))
    print("T_2:", list(T_2.nodes), list(T_2.edges))
    print("r =", r, "r_prime =", r_prime)
    input()
"""