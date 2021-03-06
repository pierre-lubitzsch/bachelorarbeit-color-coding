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
    # descriptors for possible algorithms we can use to find a specific graph H in G
    types = ["path", "random_orientations_path", "random_orientations_cycle", "cycle1", "cycle2"]

    # map for the name of the algorithm name of the graph we want to find to the function which does it
    get_func = {"path" : path.find_path, "cycle1" : cycle_first_algo.find_cycle, "cycle2" : cycle_second_algo.find_cycle, "random_orientations_path" : random_orientations_path.find_path_random_orientation, "random_orientations_cycle" : random_orientations_cycle.find_cycle_random_orientation}

    for type in types:
        print("The graph H we want to find is a", type)
        times.append([])
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = get_func[type](G, i)
            end = timer()
            print("Does G contain H with H on {} nodes? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            times[-1].append(end - start)

            plt.xlabel("k")
            plt.locator_params(axis="x", nbins = i - k_begin + 1)
            plt.ylabel("time in seconds")
            plt.title("Plotting the running time of the algorithm for {}".format(type))
            plt.plot(list(range(k_begin, i + 1)), times[-1])
            plt.savefig("plots/yeastv3/plot_yeastv3_{}_{}_to_{}.png".format(type, k_begin, k_end))
            plt.clf()

        t = str(times[-1])
        f = open("plots/yeastv3/yeastv3_{}_{}_to_{}.csv".format(type, k_begin, k_end), "w")
        f.write(t[1:-1] + "\n")       
        f.close()


if (__name__ == "__main__"):
    main()
