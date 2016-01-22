'''
    CS 325 Winter 2016 -- Project 1:  Maximum Sum Subarray

    This script uses the algorithms developed for project 1 and tests them for
    various input sizes and produces plots and curve fit equations.
'''
import timeit
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
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


def calc_n_linear(t, slope, intercept):
    n = int((t - intercept) / slope)
    return n

def calc_n_quadratic(t, coeffs):
    coeffs = list(coeffs[:-1]) + [coeffs[-1] - t]
    roots = np.roots(list(coeffs[:-1]) + [coeffs[-1] - t])
    n = roots[np.isreal(roots)]
    return int(max(n))


def do_regression(data, algo_name):
    x = sorted(data.keys())
    y = [data[i] for i in x]
    print('\nREGRESSION MODEL FOR {} SOLUTION: '.format(algo_name.upper()))
    if algo_name in ['linear', 'divide and conquer']:
        slope, intercept, r, p, std_err = stats.linregress(x,y)
        equation = 'T(n) = {:.5g}*n + {:.5g}\n'.format(slope, intercept)
        nmax = [calc_n_linear(t, slope, intercept) for t in [60, 120, 300]] 

    if algo_name in ['enumeration', 'better enumeration']:
        coeffs = np.polyfit(x, y, 2)
        equation = 'T(n) = {:.5g}*n^2 + {:.5g}*n + {:.5g}\n'.format(*coeffs)
        nmax = [calc_n_quadratic(t, coeffs) for t in [60, 120, 300]] 

    print('Curve Fit Equation: {}'.format(equation), end="")
    print('Largest input size that can be solved in 1 min: {:,}'.format(nmax[0]))
    print('Largest input size that can be solved in 2 min: {:,}'.format(nmax[1]))
    print('Largest input size that can be solved in 5 min: {:,}'.format(nmax[2]))

    return
    

def main():
    algo_dict = {
        'enumeration' : 
            [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        'better enumeration' : 
            [100, 200, 300, 400, 500, 900, 1000, 2000, 3000, 4000],
        'divide and conquer' : 
            [100, 200, 500, 1000, 2000, 4000, 6000, 10000, 12000, 15000],
        'linear' : 
            [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000],
    }
    results = {name : {} for name in algo_dict.keys()}

    for algo in algo_dict.keys():
        for n in algo_dict[algo]:
            random_arrays = get_random_problems(n, 10)
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
        do_regression(results[algo], algo)

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
    plt.legend(list(results.keys()))
    plt.show()

    return results


if __name__ == "__main__":
    results = main()

