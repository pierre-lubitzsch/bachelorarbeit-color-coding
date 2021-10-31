import networkx as nx
import matplotlib.pyplot as plt
import math
import random


"""
problems:
 - here the only task was to output all possible k-paths using the previous algorithm and then checking whether there is an edge between the first and last node of the path
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
        # break the loop instantly because we only need one path from start_vertex to v if one exists
        for colorset in dp[v][k - 1]:
            paths.add(pred[v][colorset] + (v,))
            break
    
    return paths



def find_paths(G: nx.graph.Graph, k: int, start_vertex: int) -> [()]:
    if (k > len(list(G.nodes))):
        return ()

    paths = set()
    c = dict()

    # get a random coloring e^k times and execute the coloring algorithm with it
    for _ in range(math.ceil(pow(math.e, k))):
        for v in G.nodes:
            # assign uniformly random value to coloring
            c[v] = random.randint(1, k)
        
        cur_paths = find_colorful_paths_from_node(G, k, c, start_vertex)
        for path in cur_paths:
            paths.add(path)
    
    return list(paths)


def find_cycle(G: nx.graph.Graph, k: int) -> ():
    # we return () on k <= 2 because we only take simple graphs as input
    if (k <= 2 or k > len(list(G.nodes))):
        return ()

    for v in G.nodes:
        paths = find_paths(G, k, v)

        """
        path_ends = dict()
        for (i, path) in enumerate(paths):
            last = path[-1] if v != path[-1] else path[0]
            path_ends[last] = i
        """

        for path in paths:
            if (G.has_edge(path[0], path[-1]) and test_path_length_k(G, path, k)):
                cycle = path + (path[0],)
                return cycle

    return ()


def test_path_length_k(G: nx.graph.Graph, path : [], k: int):
    if (len(path) < k):
        return False
    for i in range(len(path) - 1):
        if (not G.has_edge(path[i], path[i + 1])):
            return False
    return True


def test_cycle_length_k(G: nx.graph.Graph, cycle : [], k: int):
    if (len(cycle) < k + 1):
        return False
    for i in range(len(path) - 1):
        if (not G.has_edge(cycle[i], cycle[i + 1])):
            return False
    return True


def test():
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

    for i in range(1,12):
        print("Does G contain C_{}? {}".format(i, find_cycle(G, i)))




if(__name__ == "__main__"):
    test()