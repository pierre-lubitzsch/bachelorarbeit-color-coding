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
    if (len(sys.argv) < 4):
        print("too few arguments. you need to give 1: type of graph you want to find, 2: starting value for k, 3: end value for k")
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
    
    type = sys.argv[1]
    k_begin = int(sys.argv[2])
    k_end = int(sys.argv[3])

    times = []

    if (type == "path"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = path.find_path(G, i)
            end = timer()
            print("Does G contain P_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            times.append(end - start)
    elif (type == "cycle1"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_first_algo.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            times.append(end - start)
    elif (type == "cycle2"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_second_algo.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            times.append(end - start)

            plt.xlabel("k")
            plt.locator_params(axis="x", nbins = i - k_begin + 1)
            plt.ylabel("time in seconds")
            plt.title("Plotting the running time of the algorithm for {}".format(type))
            plt.plot(list(range(k_begin, i + 1)), times)
            plt.savefig("plots/yeastv3/plot_yeastv3_{}_{}_to_{}.png".format(type, k_begin, k_end))
            plt.clf()
    elif (type == "path_derandomized"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = path_derandomized.find_path(G, i)
            end = timer()
            print("Does G contain P_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            times.append(end - start)

            plt.xlabel("k")
            plt.locator_params(axis="x", nbins = i - k_begin + 1)
            plt.ylabel("time in seconds")
            plt.title("Plotting the running time of the algorithm for {}".format(type))
            plt.plot(list(range(k_begin, i + 1)), times)
            plt.savefig("plots/yeastv3/plot_yeastv3_{}_{}_to_{}.png".format(type, k_begin, k_end))
            plt.clf()
    elif (type == "cycle1_derandomized"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_first_algo_derandomized.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            times.append(end - start)
    elif (type == "cycle2_derandomized"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_second_algo_derandomized.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            times.append(end - start)
    elif (type == "random_orientations_path"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = random_orientations_path.find_path_random_orientation(G, i)
            end = timer()
            print("Does G contain P_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            times.append(end - start)

            plt.xlabel("k")
            plt.locator_params(axis="x", nbins = i - k_begin + 1)
            plt.ylabel("time in seconds")
            plt.title("Plotting the running time of the algorithm for {}".format(type))
            plt.plot(list(range(k_begin, i + 1)), times)
            plt.savefig("plots/yeastv3/plot_yeastv3_{}_{}_to_{}.png".format(type, k_begin, k_end))
            plt.clf()
    elif (type == "random_orientations_cycle"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = random_orientations_cycle.find_cycle_random_orientation(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            times.append(end - start)
    
    



if (__name__ == "__main__"):
    main()
