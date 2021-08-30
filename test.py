import networkx as nx
import matplotlib.pyplot as plt
import math
import random
import forest

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

    return T



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

    # we want to form a forest containing 3 star graphs
    F = nx.star_graph(2)

    F.add_nodes_from([3, 4, 5, 6, 7, 8, 9])
    F.add_edges_from([(3, 4), (3, 5), (6, 7), (6, 8)])

    colorset, subtrees = forest.find_forest(G, F, len(G.nodes), len(F.nodes))
    print("does G contain three stargraphs having 3 nodes and an isolated one?", colorset, subtrees)
    #print("does G contain its spanning tree?", tree.find_tree(G, T, len(G.nodes), len(T.nodes)))



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

