'''
    CS 325 Winter 2016 -- Project 1:  Maximum Sum Subarray

    This script uses the algorithms developed for project 1 and tests them for
    various input sizes and produces plots and curve fit equations.
'''
import timeit
import numpy as np
import matplotlib.pyplot as plt
from proj1_main import mss_enum, mss_better_enum, mss_div_and_conq, mss_linear

def get_random_problems(n, x):
    """Returns a list of x lists where each contains n random integers."""
    random_problems = []
    for i in range(x):
        rand_array = np.random.randint(low=-99, high=100, size=n)
        random_problems.append(list(rand_array))
    return random_problems


def plot_result(data, algo_name):
    x = sorted(data.keys())
    y = [data[i] for i in x]
    plt.figure()
    plt.plot(x, y, marker='o', linestyle='solid')
    plt.title('Run Time of {}'.format(algo_name))
    plt.xlabel('Size of Array (n)')
    plt.ylabel('Run time (seconds)')

    return


def main():
    algo_dict = {
        'enumeration' : 
            [100, 200, 300, 400, 500],# 600, 700, 800, 900],
        'better enumeration' : 
            [100, 200, 400, 800, 1000],#, 2000, 4000, 6000, 10000, 12000],
        'divide and conquer' : 
            [100, 200, 500, 1000, 2000, 4000, 6000],# 10000, 12000, 15000],
        'linear' : 
            [100, 200, 500, 1000, 2000, 5000, 10000], #, 20000, 50000, 100000],
    }
    results = {name : {} for name in algo_dict.keys()}

    for algo in algo_dict.keys():
        for n in algo_dict[algo]:
            random_arrays = get_random_problems(n, 3)
            # use the following in final run
            #random_arrays = get_random_problems(n, 10)
            for arr in random_arrays: 
                run_times = []

                if algo == 'enumeration':
                    setup = 'from proj1_main import mss_enum'
                    s = 'mss_enum({})'.format(arr)
                    run_times.append(timeit.timeit(s, setup=setup, number=1))
                    
                if algo == 'better enumeration':
                    setup = 'from proj1_main import mss_better_enum'
                    s = 'mss_better_enum({})'.format(arr)
                    run_times.append(timeit.timeit(s, setup=setup, number=1))

                if algo == 'divide and conquer':
                    setup = 'from proj1_main import mss_div_and_conq'
                    s = 'mss_div_and_conq({}, 0, {})'.format(arr, len(arr)-1)
                    run_times.append(timeit.timeit(s, setup=setup, number=1))

                if algo == 'linear':
                    setup = 'from proj1_main import mss_linear'
                    s = 'mss_linear({})'.format(arr)
                    run_times.append(timeit.timeit(s, setup=setup, number=1))

            mean_run_time = np.mean(run_times)
            results[algo][n] = mean_run_time
        plot_result(results[algo], algo)


    colors = list('rgbcmyk')
    plt.figure()
    for data in list(results.values()):
        x = sorted(data.keys())
        y = [data[i] for i in x]
        plt.plot(x, y, marker='o', linestyle='solid', color=colors.pop())

    
    plt.title('Run Time Comparison of all 4 Algorithms -- Log-Log')
    plt.xlabel('Size of Array (n)')
    plt.ylabel('Run time (seconds)')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(list(results.keys()), loc=2)
    plt.show()

    return results


if __name__ == "__main__":
    results = main()

