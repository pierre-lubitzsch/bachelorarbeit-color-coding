import networkx as nx
import matplotlib.pyplot as plt
import math
import random
import numpy as np
import itertools
import derandomization_full_prime_test as derandomize


"""
problems:
 - a problem while the implementation was the base case for the recursion in find_colorful_paths.
 - debugging was not quite easy when all i had as a result were the adjacency matrices, because i did not implement the algorithm for witness finding in boolean matrix multiplication yet
"""



"""
original_G is the graph we had at the first call of this function
colors are the colors we are currently using
"""
def find_colorful_paths(G: nx.graph.Graph, k: int, c: dict, original_G: nx.graph.Graph, colors: []):
    n = len(list(G.nodes))
    if (k == 1):
        B = np.identity(n)
        for v in original_G.nodes:
            if v not in G.nodes:
                B[v][v] = False
        return B
    if (k == 2):
        # return adjacency matrix of G
        B = nx.to_numpy_array(G)
        return B
    """
    if (k == 2):
        B = np.zeros((n, n))
        for u in G.nodes:
            for w in G.nodes:
                if (c[u] == c[w]):
                    continue
                for v in G.adj[u]:
                    if (c[u] != c[v] and c[v] != c[w] and v in G.adj[w]):
                        B[u][w] = B[w][u] = 1
        return B
    """

    paths = np.zeros((n, n))
    # get all subsets of {1, ..., k} having size k // 2
    subsets = set(itertools.combinations(colors, k // 2))

    for c_1 in subsets:
        left_colors = list((i for i in colors if i not in c_1))
        for c_2 in itertools.combinations(left_colors, (k + 1) // 2):
            V_1 = [v for v in G.nodes if c[v] in c_1]
            V_2 = [v for v in G.nodes if c[v] in c_2]

            G_1 = G.copy()
            G_2 = G.copy()

            for e in G_1.edges:
                if (e[0] not in V_1 or e[1] not in V_1):
                    G_1.remove_edge(e[0], e[1])
            for e in G_2.edges:
                if (e[0] not in V_2 or e[1] not in V_2):
                    G_2.remove_edge(e[0], e[1])

            A_1 = find_colorful_paths(G_1, k // 2, c, original_G, c_1)
            A_2 = find_colorful_paths(G_2, (k + 1) // 2, c, original_G, c_2) # (k + 1) // 2 is k/2 rounded up

            # adjacency matrix between nodes of V_1 and V_2
            B = np.zeros((n, n))
            for i in V_1:
                for j in V_2:
                    if (original_G.has_edge(i, j)):
                        B[i][j] = B[j][i] = 1

            #print("At k = {}".format(k))
            #print("Got from {}:\n{}".format(V_1, A_1))
            #print("Got from {}:\n{}".format(V_2, A_2))
            #print("Adjacency between {} and {}:\n{}".format(V_1, V_2, B))

            cur_paths = np.dot(np.dot(A_1, B), A_2)

            #print("Result for this time:\n{}".format(cur_paths))
            #print("\n\n\n")

            paths = np.logical_or(paths, cur_paths)

    return paths


def find_cycle(G: nx.graph.Graph, k: int):
    if (k <= 2 or k > len(list(G.nodes))):
        return False

    c = dict()
    n = len(list(G.nodes))

    for (k_prime, p, kappa, rho, K, c_prime, C) in derandomize.get_kperfect_hash_family(n, k):
        # initialize coloring c using the hash function given by the tuple of for loop
        for v in G.nodes:
            # calculate color using given hash function f : {0, 1, ..., n - 1} -> {0, 1, ..., 3k - 1}
            t = derandomize.h_alpha(v, k_prime, p, k)
            i = derandomize.h_beta(t, kappa, rho, k)
            c[v] = C[i] + derandomize.h_i(t, K[i], rho, c_prime[i])
        
        cycles = find_colorful_paths(G, k, c, G, list(range(0, 3 * k)))
        for i in range(n):
            for j in range(n):
                if ((cycles[i][j] or cycles[j][i]) and G.has_edge(i, j)):
                    return (i, j)
                    #return True    
        
    return False


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
            G.add_edge(int(u), int(v))

    G.add_edge(4, 5)
    G.add_edge(5, 9)
    #T = prim(G, len(list(G.nodes)))

    for i in range(1,11):
        print("Does G contain C_{}? {}".format(i, find_cycle(G, i)))
    """
    for i in (3, 4):
        print("Does G contain C_{}? {}".format(i, find_cycle(G, i)))
    """

if(__name__ == "__main__"):
    test()



"""
print(A_1)
print(A_2)
print(B)
print(type(A_1))
print(type(A_2))
print(type(B))
return cycles
"""