# try 10 different random graphs and save avarage and worst time results
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

def main():
    if (len(sys.argv) < 5):
        print("too few arguments. you need to give 1: starting value for k, 2: end value for k, 3: value n for the size of the random graphs, 4: value p probability for each edge to be present")
        sys.exit(-1)

    n = int(sys.argv[3])
    p = eval(sys.argv[4]) if len(sys.argv) >= 5 else 1 / 2
    G = nx.gnp_random_graph(n, p)
    
    k_begin = int(sys.argv[1])
    k_end = int(sys.argv[2])

    # here times[i][j][k] is the time it took to find a graph of type types[j] of size k_begin + k inside the i-th random graph
    times = []
    types = ["path", "cycle1", "cycle2", "random_orientations_path", "random_orientations_cycle"]
    get_func = {"path" : path.find_path, "cycle1" : cycle_first_algo.find_cycle, "cycle2" : cycle_second_algo.find_cycle, "random_orientations_path" : random_orientations_path.find_path_random_orientation, "random_orientations_cycle" : random_orientations_cycle.find_cycle_random_orientation}

    for i in range(10):
        times.append([])
        for type in types:
            print("The graph H we want to find is a", type)
            times[i].append([])
            for i in range(k_begin, k_end + 1):
                start = timer()
                cur_path = get_func[type](G, i)
                end = timer()
                print("Does G contain H with H on {} nodes? {}".format(i, cur_path))
                print("Finding it took {:.3f} seconds\n".format(end - start))
                times[i][-1].append(end - start)
    

    average_times = [[0 for _ in range(k_end - k_begin + 1)] for _ in range(len(types))]
    for i in range(len(types)):
        for j in range(k_end - k_begin + 1):
            for x in range(10):
                average_times[i][j] += times[x][i][j]
            average_times[i][j] /= 10
    

    max_times = [[0 for _ in range(k_end - k_begin + 1)] for _ in range(len(types))]
    for i in range(len(types)):
        for j in range(k_end - k_begin + 1):
            for x in range(10):
                max_times[i][j] = max(max_times[i][j], times[x][i][j])


    for i in range(len(types)):
        plt.xlabel("k")
        plt.locator_params(axis="x", nbins = k_end - k_begin + 1)
        plt.ylabel("time in seconds")
        plt.yscale("log")
        plt.title("Plotting the average and max running time of the algorithm for {} on 10 random graphs".format(type))
        plt.plot(list(range(k_begin, k_end + 1)), average_times[i])
        plt.plot(list(range(k_begin, k_end + 1)), max_times[i])
        plt.savefig("random_{}_{}_graphs_{}_{}_to_{}.csv".format(n, p, types[i], k_begin, k_end), "w")
        plt.clf()
    
    f = open("random_{}_{}_graphs_{}_{}_to_{}.csv".format(n, p, type, k_begin, k_end), "w")
    for i in range(len(types)):
        t = str(average_times[i])
        f.write("{}, average, {}\n".format(i, t[1:-1]))
        t = str(max_times[i])
        f.write("{}, max, {}\n".format(i, t[1:-1]))
    f.close()


if (__name__ == "__main__"):
    main()
