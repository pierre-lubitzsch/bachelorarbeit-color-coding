import networkx as nx
import matplotlib.pyplot as plt
import math
import random

"""
implementation problems:
 - in the predecessor array do we save the whole path up until now or just the last vertex?
   i decided to save the whole path because if we would only save the last node we would have to reconstruct the set and because we save the colorset in dp also
   the space is 2k instead of k + 1, which is both O(k) and it is easier to implement using the method where yo save the whole path
 - another problem was that i needed a set of sets/lists and in python lists and sets are not hashable (because they are mutable).
   then i discovered that socalled "frozensets" exists, which is basically a constant set which is hashable. i used this then for my dp table and pred table
"""


"""
Spanning tree algo
"""
def prim(G: nx.graph.Graph, n: int) -> nx.graph.Graph:
    if (len(list(G.nodes)) < 1):
        return nx.Graph()
    T = nx.Graph()

    x = list(G.nodes)[0]
    T.add_node(x)

    visited_nodes = set()
    visited_nodes.add(x)
    T_weight = 0

    for i in range(n - 1):
        e = None
        for u in T.nodes:
            for v in G.adj[u]:
                if v in visited_nodes:
                    continue

                if e == None or G[u][v]["weight"] < G[e[0]][e[1]]["weight"]:
                    e = (u, v)

        
        (u, v) = e
        if (u not in visited_nodes):
            u, v = v, u
        T.add_node(v)
        visited_nodes.add(v)
        T.add_edge(u, v, weight=G[u][v]["weight"])
        T_weight += G[u][v]["weight"]

    print("weight of T:", T_weight)
    return T


"""
dp[v][l] contains all colorsets appearing on a path of length l from start_vertex to v.
pred[v][colorset] contains the predecessor node of a path from start_vertex to v using the set of colors "colorset"

we need frozenset for sets of colors, because the collection of colorset has to contain them, and normal sets are not hashable
"""
def find_colorful_paths_from_node(G: nx.graph.Graph, k: int, c: dict, start_vertex: int) -> [()]:
    paths = set()
    dp = dict()
    pred = dict()

    for v in G.nodes:
        dp[v] = [set() for _ in range(k)]
        pred[v] = dict()
    
    dp[start_vertex][0].add(frozenset([c[start_vertex]]))
    pred[start_vertex][frozenset([c[start_vertex]])] = ()

    for length in range(k - 1):
        for v in G.nodes:
            for colorset in dp[v][length]:
                for u in G.adj[v]:
                    if c[u] not in colorset:
                        new_colorset = set(colorset)
                        new_colorset.add(c[u])
                        const_set = frozenset(new_colorset)
                        dp[u][length + 1].add(const_set)
                        pred[u][const_set] = pred[v][colorset] + (v,)

    for v in G.nodes:
        for colorset in dp[v][k - 1]:
            paths.add(pred[v][colorset] + (v,))
    
    return paths


"""
execute the colorful copy path-finding algorithm to find P_k at most e^k times
with uniformly random colorings c : V -> [k]
"""
def find_path(G_in: nx.graph.Graph, k: int) -> bool:
    if (k > len(list(G_in.nodes))):
        return []
    c = dict()
    G = nx.graph.Graph(G_in)

    # add a vertex "start_vertex" to G and connect it to all other vertices and color it with the new color 0.
    # now we need to find a colorful path of length k + 1 starting from start_vertex.
    start_vertex = 1 + max(G.nodes)
    G.add_node(start_vertex)
    c[start_vertex] = 0
    for v in G.nodes:
        if v != start_vertex:
            G.add_edge(start_vertex, v)


    # get a random coloring e^k times and execute the coloring algorithm with it
    for _ in range(math.ceil(pow(math.e, k))):
        for v in G.nodes:
            if v == start_vertex:
                continue
            # assign uniformly random value to coloring
            c[v] = random.randint(1, k)
        
        paths = find_colorful_paths_from_node(G, k + 1, c, start_vertex)
        if (len(paths) > 0):
            path = list(paths)[0][1:]
            if (not test_path_length_k(G, path, k)):
                print("Algorithm for path gave wrong output: {}".format(path))
                return []
            return path

    return []

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

    for i in range(1, 12):
        print("Does G contain P_{}? {}".format(i, find_path(G, i)))



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

