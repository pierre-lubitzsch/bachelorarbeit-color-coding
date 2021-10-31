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
from matplotlib import pyplot as plt

# source: https://www.inetbio.org/yeastnet/downloadnetwork.php
# we have n = 5808

def main():
    if (len(sys.argv) < 3):
        print("too few arguments. you need to give 1: starting value for k, 2: end value for k")
        sys.exit(-1)

    G = nx.Graph()
    # the nodes in the file are labeled with strings. therefore we map each unique string to an unique integer such that the constructed graph G has the nodes {0, 1, ... n - 1}.
    with open("example_graphs/YeastNet.v3.txt") as f:
        n = 0
        nodes = dict()
        for line in f:
            (u, v, w) = line.split()
            # we want simple graphs and therefore no loops
            if (u == v):
                continue
            if (u not in nodes):
                nodes[u] = n
                n += 1
            if (v not in nodes):
                nodes[v] = n
                n += 1
            G.add_edge(nodes[u], nodes[v])
    
    k_begin = int(sys.argv[1])
    k_end = int(sys.argv[2])

    times = []
    types = ["path", "cycle1", "cycle2", "random_orientations_path", "random_orientations_cycle"]

    for type in types:
        print("The graph H we want to find is a", type)
        times.append([])
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = path.find_path(G, i)
            end = timer()
            print("Does G contain H with H on {} nodes? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            times[-1].append(end - start)
    
        plt.xlabel("k")
        plt.locator_params(axis="x", nbins = k_end - k_begin + 1)
        plt.ylabel("time in seconds")
        plt.plot(list(range(k_begin, k_end + 1)), times[-1])
        plt.show()
        plt.savefig("plots/plot_yeastv3_{}_{}_to{}.png".format(type, k_begin, k_end))
        plt.clf()
    



if (__name__ == "__main__"):
    main()
