import networkx as nx
import matplotlib.pyplot as plt
import math
import path_v4 as path
import cycle_first_algo
import cycle_second_algo
import sys
from timeit import default_timer as timer
import path_derandomized
import cycle_first_algo_derandomized
import cycle_second_algo_derandomized
import random_orientations_cycle
import random_orientations_path

# source: http://vlado.fmf.uni-lj.si/pub/networks/data/bio/yeast/yeast.htm

def main():
    if (len(sys.argv) < 4):
        print("too few arguments. you need to give 1: type of graph you want to find, 2: starting value for k, 3: end value for k")
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
                # we want simple graphs and therefore no loops
                if (u == v):
                    continue
                assert(u > 0 and v > 0)
                # in the file the vertices are labeled from 1 to 2361 but we want vertices from 0 to 2360
                G.add_edge(u - 1, v - 1)
    
    type = sys.argv[1]
    k_begin = int(sys.argv[2])
    k_end = int(sys.argv[3])

    if (type == "path"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = path.find_path(G, i)
            end = timer()
            print("Does G contain P_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
    elif (type == "cycle1"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_first_algo.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
    elif (type == "cycle2"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_second_algo.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
    elif (type == "path_derandomized"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = path_derandomized.find_path(G, i)
            end = timer()
            print("Does G contain P_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
    elif (type == "cycle1_derandomized"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_first_algo_derandomized.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
    elif (type == "cycle2_derandomized"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_second_algo_derandomized.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
    elif (type == "random_orientations_path"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = random_orientations_path.find_path_random_orientation(G, i)
            end = timer()
            print("Does G contain P_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
    elif (type == "random_orientations_cycle"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = random_orientations_cycle.find_cycle_random_orientation(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
    



if (__name__ == "__main__"):
    main()
