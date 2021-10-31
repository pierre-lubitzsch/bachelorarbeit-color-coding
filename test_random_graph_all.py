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

# try 10 different random graphs and save avarage and worst time results
def main():
    if (len(sys.argv) < 5):
        print("too few arguments. you need to give 1: type of graph you want to find, 2: starting value for k, 3: end value for k, 4: number of nodes in G, probability for each edge in G to exist")
        sys.exit(-1)
    n = int(sys.argv[4])
    p = eval(sys.argv[5]) if len(sys.argv) >= 6 else 1 / 2
    G = nx.gnp_random_graph(n, 1 / 20)
    
    type = sys.argv[1]
    k_begin = int(sys.argv[2])
    k_end = int(sys.argv[3])

    plot_values = [[], []]

    if (type == "path"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = path.find_path(G, i)
            end = timer()
            print("Does G contain P_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            plot_values[0].append(i)
            plot_values[1].append(end - start)
    elif (type == "cycle1"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_first_algo.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            plot_values[0].append(i)
            plot_values[1].append(end - start)
    elif (type == "cycle2"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_second_algo.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            plot_values[0].append(i)
            plot_values[1].append(end - start)
    elif (type == "path_derandomized"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = path_derandomized.find_path(G, i)
            end = timer()
            print("Does G contain P_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            plot_values[0].append(i)
            plot_values[1].append(end - start)
    elif (type == "cycle1_derandomized"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_first_algo_derandomized.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            plot_values[0].append(i)
            plot_values[1].append(end - start)
    elif (type == "cycle2_derandomized"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = cycle_second_algo_derandomized.find_cycle(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            plot_values[0].append(i)
            plot_values[1].append(end - start)
    elif (type == "random_orientations_path"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = random_orientations_path.find_path_random_orientation(G, i)
            end = timer()
            print("Does G contain P_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            plot_values[0].append(i)
            plot_values[1].append(end - start)
    elif (type == "random_orientations_cycle"):
        for i in range(k_begin, k_end + 1):
            start = timer()
            cur_path = random_orientations_cycle.find_cycle_random_orientation(G, i)
            end = timer()
            print("Does G contain C_{}? {}".format(i, cur_path))
            print("Finding it took {:.3f} seconds\n".format(end - start))
            plot_values[0].append(i)
            plot_values[1].append(end - start)
    
    plt.xlabel("k")
    plt.locator_params(axis="x", nbins = k_end - k_begin + 1)
    plt.ylabel("time in seconds")
    plt.plot(*plot_values)
    plt.show()
    



if (__name__ == "__main__"):
    main()
