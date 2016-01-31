#/usr/bin/python3.2
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


def plot_coins(data, part_num):
    """Plots Number of Coins vs A for all 3 algorithms on one figure."""
    marks = list('o*^')
    for algo in ['changegreedy', 'changedp']: #, 'changeslow']:
        x = [i for i in data['A_list']]
        y = data[algo]['num']
        plt.plot(x, y, linestyle='None', marker=marks.pop(), label=algo)

    plt.xlabel('Amount of Change to Make (A)')
    plt.ylabel('Minimum Nuber of Coins Needed')
    plt.xlim(min(x)-10, max(x)+10)
    plt.ylim(min(y)-1, max(y)+1)
    plt.title('Part {} -- Number of Coins vs. A'.format(part_num))
    plt.legend()
    plt.grid()

    return


def plot_times(data, part_num):
    """Plots Run Times vs A for all 3 algorithms on one figure."""
    marks = list('o*^')
    #for algo in ['changeslow', 'changedp', 'changegreedy']:
    for algo in ['changedp', 'changegreedy']:
        x = [i for i in data['A_list']]
        y = data[algo]['times']
        plt.plot(x, y, linestyle='None', marker=marks.pop(), label=algo)

    plt.xlabel('Amount of Change to Make (A)')
    plt.ylabel('Run Time (seconds)')
    plt.xlim(min(x)-10, max(x)+10)
    #plt.ylim(0.0, max_y*1.05)
    ticklocs = ticklabels = [A for A in x[::5]]
    plt.xticks(ticklocs, ticklabels)
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Part {} -- Run Time vs. A'.format(part_num))
    plt.legend()
    plt.grid()

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
    algos = {'changegreedy' : proj2_main.changegreedy,
           #  'changeslow' : proj2_main.changeslow,
             'changedp' : proj2_main.changedp}
    experiments = {'4' : {'V' : [1, 5, 10, 25, 50], 
                          'A_list' : range(2010, 2205, 5),
                          'changeslow' : {'times' : [], 'num' : []},
                          'changegreedy' : {'times' : [], 'num' : []},
                          'changedp' : {'times' : [], 'num' : []}}, 
                   '5_V1': {'V' : [1, 2, 6, 12, 24, 48, 60], 
                            'A_list' : range(2000, 2201, 1),
                            'changeslow' : {'times' : [], 'num' : []},
                            'changegreedy' : {'times' : [], 'num' : []},
                            'changedp' : {'times' : [], 'num' : []}}, 
                   '5_V2': {'V' : [1, 6, 13, 37, 150],       
                            'A_list' : range(2000, 2201, 1),
                            'changeslow' : {'times' : [], 'num' : []},
                            'changegreedy' : {'times' : [], 'num' : []},
                            'changedp' : {'times' : [], 'num' : []}}, 
                   '6':  {'V' : [1] + list(range(2, 32, 2)), 
                          'A_list' : range(2000, 2201, 1),
                          'changeslow' : {'times' : [], 'num' : []},
                          'changegreedy' : {'times' : [], 'num' : []},
                          'changedp' : {'times' : [], 'num' : []}}} 

    for part in ['4', '5_V1', '5_V2', '6']:
        for algo in ['changegreedy', 'changedp']:
        #for algo in ['changeslow', 'changegreedy', 'changedp']:
            for A in experiments[part]['A_list']: 
                start_time = time.time()
                qty, min_coins = algos[algo](experiments[part]['V'], A)
                end_time = time.time()
                experiments[part][algo]['times'].append(end_time - start_time)
                experiments[part][algo]['num'].append(min_coins)

        if len(sys.argv) > 1 and sys.argv[1] == '--plot':
            plt.figure()
            plot_coins(experiments[part], part)
            plt.figure()
            plot_times(experiments[part], part)
    #do_regression(results[algo], algo)
    plt.show()
    return experiments


if __name__ == "__main__":
    results = main()
