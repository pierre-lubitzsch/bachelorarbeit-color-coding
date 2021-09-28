import networkx as nx
import matplotlib.pyplot as plt
import math
import path_v4 as path
import cycle_first_algo
import sys
from timeit import default_timer as timer

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
    

    if (len(sys.argv) > 1):
        if (sys.argv[1] == "path"):
            for i in range(1, 15):
                start = timer()
                cur_path = path.find_path(G, i)
                end = timer()
                print("Does G contain P_{}? {}".format(i, cur_path))
                print("Finding it took {:.3f} seconds\n".format(end - start))

        if (sys.argv[1] == "cycle1"):
            for i in range(1, 15):
                start = timer()
                cur_path = cycle_first_algo.find_cycle(G, i)
                end = timer()
                print("Does G contain C_{}? {}".format(i, cur_path))
                print("Finding it took {:.3f} seconds\n".format(end - start))
    else:
        # find path
        for i in range(1, 15):
            start = timer()
            cur_path = path.find_path(G, i)
            end = timer()
            print("Does G contain P_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
    



if (__name__ == "__main__"):
    main()
