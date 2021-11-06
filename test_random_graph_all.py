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
    G = [nx.gnp_random_graph(n, p) for _ in range(10)]
    
    k_begin = int(sys.argv[1])
    k_end = int(sys.argv[2])

    types = ["random_orientations_cycle", "cycle1", "cycle2", "cycle1_derandomized", "cycle2_derandomized", "path", "random_orientations_path", "path_derandomized"]
    get_func = {"path" : path.find_path, "cycle1" : cycle_first_algo.find_cycle, "cycle2" : cycle_second_algo.find_cycle, "random_orientations_path" : random_orientations_path.find_path_random_orientation, "random_orientations_cycle" : random_orientations_cycle.find_cycle_random_orientation, "path_derandomized" : path_derandomized.find_path, "cycle1_derandomized" : cycle_first_algo_derandomized.find_cycle, "cycle2_derandomized" : cycle_second_algo_derandomized.find_cycle}
    # here times[i][j][k] is the time it took to find a graph of type types[j] of size k_begin + k inside the i-th random graph
    times = [[[[0] for _ in range(k_end - k_begin + 1)] for _ in range(len(types))] for _ in range(10)]
    average_times = [[0 for _ in range(k_end - k_begin + 1)] for _ in range(len(types))]
    max_times = [[0 for _ in range(k_end - k_begin + 1)] for _ in range(len(types))]

    for j in range(len(types[:-3])):
        for i in range(10):
            print("The graph H we want to find is a", types[j])
            for k in range(k_begin, k_end + 1):
                start = timer()
                cur_path = get_func[types[j]](G[i], k)
                end = timer()
                print("Does G contain H with H on {} nodes? {}".format(k, cur_path))
                print("Finding it took {:.3f} seconds\n".format(end - start))
                times[i][j][k - k_begin] = end - start

                average_times[j][k - k_begin] += times[i][j][k - k_begin]
                max_times[j][k - k_begin] = max(max_times[j][k - k_begin], times[i][j][k - k_begin])
                # we save plots inbetween because derandomized algorithms are miuch slower and sometimes the process is killed in the middle of the run
                if (types[j].find("derandomized") != -1):
                    plt.xlabel("k")
                    plt.locator_params(axis="x", nbins = k_end - k_begin + 1)
                    plt.ylabel("time in seconds")
                    plt.title("average & max runtime for {} on 10 random graphs".format(types[j]))
                    plt.plot(list(range(k_begin, k_end + 1)), [x / (i + 1) for x in average_times[j]])
                    plt.plot(list(range(k_begin, k_end + 1)), max_times[j])
                    plt.savefig("plots/random/random_{}_{}_graphs_{}_{}_to_{}.png".format(n, p, types[j], k_begin, k_end))
                    plt.clf()

        
        for k in range(k_end - k_begin + 1):
            average_times[j][k] /= 10


        plt.xlabel("k")
        plt.locator_params(axis="x", nbins = k_end - k_begin + 1)
        plt.ylabel("time in seconds")
        plt.title("average & max runtime for {} on 10 random graphs".format(types[j]))
        plt.plot(list(range(k_begin, k_end + 1)), average_times[j])
        plt.plot(list(range(k_begin, k_end + 1)), max_times[j])
        plt.savefig("plots/random/random_{}_{}_graphs_{}_{}_to_{}.png".format(n, p, types[j], k_begin, k_end))
        plt.clf()
    
        f = open("random_{}_{}_graphs_{}_{}_to_{}.csv".format(n, p, type, k_begin, k_end), "w")
        t = str(average_times[j])
        f.write("{}, average, {}\n".format(types[j], t[1:-1]))
        t = str(max_times[j])
        f.write("{}, max, {}\n".format(types[j], t[1:-1]))
        f.close()


if (__name__ == "__main__"):
    main()
