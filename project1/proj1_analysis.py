'''
    CS 325 Winter 2016 -- Project 1:  Maximum Sum Subarray

    This script uses the algorithms developed for project 1 and tests them for
    various input sizes and produces plots and curve fit equations.
'''
import timeit
import numpy as np
import matplotlib.pyplot as plt
from proj1_main import mss_enum, mss_better_enum, mss_div_and_conq, mss_linear

def get_ten_random_problems(n):
    """Returns a list of 10 lists where each contains n random integers."""
    ten_random_problems = []
    for i in range(10):
        rand_array = np.random.randint(low=-99, high=100, size=n)
        ten_random_problems.append(list(rand_array))
    return ten_random_problems


def main():
    algo_dict = {
        'enum' : [100, 200, 400, 600, 800, 
                  1000, 2000, 4000, 6000, 10000],
        'better_enum' : [100, 200, 400, 800, 1000, 
                         2000, 4000, 6000, 10000, 12000],
        'div_and_conq' : [100, 200, 500, 1000, 2000, 
                          4000, 6000, 10000, 12000, 15000],
        'linear' : [100, 200, 500, 1000, 2000, 
                    5000, 10000, 20000, 50000, 100000],
    }
    results = {'enum' : {}, 
               'better_enum' : {},
               'div_and_conq' : {}, 
               'linear' : {}}

    for algo in algo_dict.keys():
        for n in algo_dict[algo]:
            random_arrays = get_ten_random_problems(n)
            for arr in random_arrays: 
                run_times = []

                if algo == 'enum':
                    setup = 'from proj1_main import mss_enum'
                    s = 'mss_enum({})'.format(arr)
                    run_times.append(timeit.timeit(s, setup=setup, number=1))
                    
                if algo == 'better_enum':
                    setup = 'from proj1_main import mss_better_enum'
                    s = 'mss_better_enum({})'.format(arr)
                    run_times.append(timeit.timeit(s, setup=setup, number=1))

                if algo == 'div_and_conq':
                    setup = 'from proj1_main import mss_div_and_conq'
                    s = 'mss_div_and_conq({}, 0, {})'.format(arr, len(arr)-1)
                    run_times.append(timeit.timeit(s, setup=setup, number=1))

                if algo == 'linear':
                    setup = 'from proj1_main import mss_linear'
                    s = 'mss_linear({})'.format(arr)
                    run_times.append(timeit.timeit(s, setup=setup, number=1))

            mean_run_time = np.mean(run_times)
            results[algo][n] = mean_run_time

    colors = list('rgbcmyk')
    for data_dict in list(results.values()):
        x = list(data_dict.keys())
        y = list(data_dict.values())
        plt.scatter(x, y, color=colors.pop())
    plt.legend(list(results.keys()), loc=2)
    plt.show()

    return results


if __name__ == "__main__":
    results = main()

