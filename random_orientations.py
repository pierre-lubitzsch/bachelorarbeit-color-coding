import numpy as np
import networkx as nx


# algorithm from [CLR90]
def longest_directed_path(G: nx.DiGraph, pi: [], n: int) -> []:
    # construct topological sort from permutation which influenced the edges
    toposorted_vertices = [0] * n
    for u in range(n):
        toposorted_vertices[pi[u]] = u
    
    # at path_end_length[u] we save the length of the longest path which ends on u
    path_end_length = [1] * n
    # in pred[u] we save the predecessor of u in the longest path ending on u
    pred = [None] * n
    
    # in G.adj[u] there can only be nodes which come later in the toposort because of the construction of G
    # therefore we can iterate in toposort order and look at all neighbors and maybe increase their longest path length
    for u in toposorted_vertices:
        for v in G.adj[u]:
            if (path_end_length[u] + 1 > path_end_length[v]):
                path_end_length[v] = path_end_length[u] + 1
                pred[v] = u
    
    # search for node which is the end of the longest path
    max_path_end_node = 0
    for u in range(1, n):
        if (path_end_length[u] > path_end_length[max_path_end_node]):
            max_path_end_node = u
    
    # construct the longest path from the predecessors
    path = []
    u = max_path_end_node
    while (u != None):
        path.append(u)
        u = pred[u]

    return path




"""
returns True iff path is a path of length k in G
"""
def test_path_length_k(G: nx.graph.Graph, path : [], k: int):
    if (len(path) < k):
        return False
    for i in range(k - 1):
        if (not G.has_edge(path[i], path[i + 1])):
            return False
    return True
    


# setup directed acyclic graph from random permutation of vertices and run longest directed path in DAG algo on it (k + 1)! / 2 times to get the right result in the expected case
def find_path_random_orientation(G: nx.graph.Graph, k: int) -> []:
    n = len(list(G.nodes))
    if (k > n):
        return []
    # execute algorithm (k + 1)! / 2 rounded up times to get the correct result in the expected case
    for _ in range((np.math.factorial(k + 1) + 1) // 2):
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

        path = longest_directed_path(G_directed, pi, n)
        if (len(path) >= k):
            if (test_path_length_k(G, path, k)):
                return path[:k]
            else:
                print("ERROR: found wrong path: {}".format(path))

    return []

    


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
        print("Does G contain P_{}? {}".format(i, find_path_random_orientation(G, i)))



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

