####/usr/bin/python3.2
'''
    CS 325 Winter 2016 -- Project 2: Coin Change 

    This script uses the algorithms developed for project 2 and tests them for
    various input sizes and produces plots and curve fit equations.
'''
import time
import sys
import proj2_main

try:
    import numpy as np
    import matplotlib.pyplot as plt
except Exception:
    pass


def plot_indiv_result(data):  #, algo_name):
    x = [i for i in data['A_list']]
    num_coins = [data['num_coins'][i] for i in x]
    times = [data['times'][i] for i in x]

    f, (ax1, ax2) = plt.subplots(2, 1)
    ax1.scatter(x, num_coins, marker='o')
    ax1.set_xlabel('A')
    ax1.set_ylabel('Minimum Nuber of Coins')
    #ax1.set_xlim(.9*min(x), 1.1*max(x))
    #ax1.set_ylim(.1*min(y), 10*max(y))
    #ax1.set_title('Mean Run Times of *{}* algorithm'.format(algo_name))

    ax2.scatter(x, times, marker='o', label='data')
    ax2.set_xlabel('A')
    ax2.set_ylabel('Run time (seconds)')
    ax2.set_xlim(min(x)*.95, max(x)*1.1)
    ax2.set_ylim(min(times)*.95, max(times))
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
    """Prints mean run times for a single algorithm."""
    print('\n{}'.format('='*79))
    print('RESULTS FOR *{}* ALGORITHM '.format(algo_name.upper()))
    print('Mean Run Times for 10 random problems of size n:\n') 
    print('      n         time (seconds)  ')
    print('  ---------    ----------------- ')
    for n in sorted(data.keys()):
        print('    {:<13,d}{:7.5e}'.format(n, data[n]))


def do_regression(data, algo_name): 
    """Calculates curve fit, prints equation, and calculates max array size
    that can be solved in 1, 2 and 5 minutes."""
    x = sorted(data.keys())
    y = [data[i] for i in x]
    print('\nREGRESSION MODEL FOR {} ALGORITHM'.format(algo_name.upper()))

    if algo_name in ['linear']:
        coeffs = np.polyfit(x, y, 1)
        equation = 'T(n) = {:.5g}*n + {:.5g}\n'.format(*coeffs)
        fit = np.poly1d(coeffs)(x)

    if algo_name in ['divide and conquer']:
        coeffs = np.polyfit(x*np.log2(x), y, 1)
        equation = 'T(n) = {:.5g}*n*log(n) + {:.5g}\n'.format(*coeffs)
        fit = np.poly1d(coeffs)(x*np.log2(x))

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
    #brute_func = proj2_main.changeslow
    greedy_func = proj2_main.changegreedy
    #dp_func = proj2_main.changedp
    #algos = [brute_func, greedy_func, dp_func]
    algos = [greedy_func]

    
    experiments = {4 : {'V_list' : [1, 5, 10, 25, 50], 
                        'A_list' : range(2010, 2205, 5),
                        'num_coins' : {},
                        'times' : {}},
                  }

    for part in [4]: #, 5, 6]:
        for algo in algos:
            for A in experiments[part]['A_list']: 
                exp = (experiments[part]['V_list'], A)

                start_time = time.time()
                answer = algo(exp)
                end_time = time.time()

                experiments[part]['times'][A] = end_time - start_time
                experiments[part]['num_coins'][A] = answer[-1] 

#            results[algo][n] = mean_run_time
#        print_result(results[algo], algo)

            if len(sys.argv) > 1 and sys.argv[1] == '--plot':
                plot_indiv_result(experiments[part])
        #do_regression(results[algo], algo)
#
#    if len(sys.argv) > 1 and sys.argv[1] == '--analyze':
#        plot_all_results(results)
    plt.show()
#
    return experiments


if __name__ == "__main__":
    results = main()
