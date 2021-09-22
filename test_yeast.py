import networkx as nx
import matplotlib.pyplot as plt
import math
import path_v4 as path


def main():
    G = nx.Graph()
    # the file contains the number of vertices in the first line and each remaining lines represents an edge between 2 vertices
    with open("example_graphs/yeast/yeast_edges.txt") as f:
        first_line = True
        for line in f:
            if first_line:
                G.add_nodes_from(list(range(int(line))))
                first_line = False
            else:
                (u, v) = map(int, line.split())
                assert(u > 0 and v > 0)
                # in the file the vertices are labeled from 1 to 2361 but we want vertices from 0 to 2360
                G.add_edge(u - 1, v - 1)
    

    for i in range(1, 15):
        print("Does G contain P_{}? {}".format(i, path.find_path(G, i)))



if (__name__ == "__main__"):
    main()
