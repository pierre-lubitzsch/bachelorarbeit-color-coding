import numpy as np
import networkx as nx


"""
returns True iff path is a path of length >= k in G
"""
def test_path_length_k(G: nx.graph.Graph, path : [], k: int):
    if (len(path) < k):
        return False
    for i in range(k - 1):
        if (not G.has_edge(path[i], path[i + 1])):
            return False
    return True
    


# setup directed acyclic graph to raise its adjacency matrix to the (k - 1)st power.
def find_cycle_random_orientation(G: nx.graph.Graph, k: int) -> []:
    n = len(list(G.nodes))
    if (k > n):
        return ()

    # execute algorithm k! / 2 rounded up times to get the correct result in the expected case
    for _ in range((np.math.factorial(k) + 1) // 2):
        # choose random permutation
        pi = np.random.permutation(n)
        G_directed = nx.DiGraph()
        #print(pi)

        # build directed version of G where (u, v) \in E(G_directed) \iff {u, v} \in E(G) and pi[u] < pi[v]
        for v in G.nodes:
            G_directed.add_node(v)

        for (u, v) in G.edges:
            if (pi[u] < pi[v]):
                G_directed.add_edge(u, v)
            else:
                G_directed.add_edge(v, u)

        # take the adjacency matrix of G_directed to the (k - 1)st power to find all pairs of vertices connected by a path of length k - 1
        A = nx.to_numpy_array(G_directed)
        B = np.linalg.matrix_power(A, k - 1)
        for u in range(n):
            for v in range(n):
                if (B[u][v] != 0 and G.has_edge(u, v)):
                    return (u, v)

    return ()

    


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


    for i in range(1, 12):
        print("Does G contain C_{}? {}".format(i, find_cycle_random_orientation(G, i)))



if (__name__ == "__main__"):
    main()