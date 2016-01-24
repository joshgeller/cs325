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


def plot_indiv_result(data, algo_name):
    x = sorted(data.keys())
    y = [data[i] for i in x]

    f, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(x, y, marker='o')
    ax1.set_xlabel('Size of Array (n) -- Log')
    ax1.set_ylabel('Run time (seconds) -- Log')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlim(.9*min(x), 1.1*max(x))
    ax1.set_ylim(.1*min(y), 10*max(y))
    ax1.set_title('Mean Run Times of *{}* algorithm'.format(algo_name))

    ax2.scatter(x, y, marker='o', label='data')
    ax2.set_xlabel('Size of Array (n) -- Linear')
    ax2.set_ylabel('Run time (seconds) -- Linear')
    ax2.set_xlim(0, max(x)*1.1)
    ax2.set_ylim(0, max(y)*1.1)
    f.tight_layout()
    return


def solve_for_n(y, coeffs):
    """Solves a polynomial equation of the following form:

          y = ax^k + bx^(k-1) + cx^(k-2) + dx^(k-3) + ...

       given y and a list of coefficients.
       i.e. coeffs = [a, b, c, d,....]

       Returns the maximum real solution as an integer.
    """
    coeffs = list(coeffs[:-1]) + [coeffs[-1] - y]
    roots = np.roots(list(coeffs[:-1]) + [coeffs[-1] - y])
    n = roots[np.isreal(roots)]
    return int(n.real.max())


def print_result(data, algo_name):
    print('\n{}'.format('='*79))
    print('RESULTS FOR *{}* ALGORITHM '.format(algo_name.upper()))
    print('Mean Run Times for 10 random problems of size n:\n') 
    print('      n         time (seconds)  ')
    print('  ---------    ----------------- ')
    for n in sorted(data.keys()):
        print('    {:<13,d}{:7.5e}'.format(n, data[n]))


def do_regression(data, algo_name):
    x = sorted(data.keys())
    y = [data[i] for i in x]
    print('\nREGRESSION MODEL FOR {} ALGORITHM'.format(algo_name.upper()))

    if algo_name in ['linear']:
        coeffs = np.polyfit(x, y, 1)
        equation = 'T(n) = {:.5g}*n + {:.5g}\n'.format(*coeffs)
        fit = np.poly1d(coeffs)(x)

    if algo_name in ['divide and conquer']:
        coeffs = np.polyfit(x*np.log(x), y, 1)
        equation = 'T(n) = {:.5g}*n*log(n) + {:.5g}\n'.format(*coeffs)
        fit = np.poly1d(coeffs)(x*np.log(x))

    if algo_name in ['better enumeration']:
        coeffs = np.polyfit(x, y, 2)
        equation = 'T(n) = {:.5g}*n^2 + {:.5g}*n + {:.5g}\n'.format(*coeffs)
        fit = np.poly1d(coeffs)(x)

    if algo_name in ['enumeration']:
        coeffs = np.polyfit(x, y, 3)
        equation = ('T(n) = {:.5g}*n^3 + {:.5g}*n^2 + {:.5g}*n + '
                   '{:.5g}\n'.format(*coeffs))
        fit = np.poly1d(coeffs)(x)

    plt.plot(x, fit, "--", label="fit")
    plt.legend(loc=4)
    nmax = [solve_for_n(t, coeffs) for t in [60, 120, 300]] 
    print('Equation: {}'.format(equation), end="")
    print('Largest input that can be solved in 1 min: {:,}'.format(nmax[0]))
    print('Largest input that can be solved in 2 min: {:,}'.format(nmax[1]))
    print('Largest input that can be solved in 5 min: {:,}'.format(nmax[2]))
    return
   

def plot_all_results(results):
    """Plots all 4 algorithms on log-log."""
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
    plt.legend(list(results.keys()), loc=4)


def main():
    algo_dict = {
        'enumeration' : 
            [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        'better enumeration' : 
            [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        'divide and conquer' : 
            [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000],
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
        print_result(results[algo], algo)
        plot_indiv_result(results[algo], algo)
        do_regression(results[algo], algo)

    plot_all_results(results)
    plt.show()

    return results


if __name__ == "__main__":
    results = main()
