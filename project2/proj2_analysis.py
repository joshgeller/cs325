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
    from matplotlib.ticker import FormatStrFormatter
except Exception:
    pass


CHANGESLOW_MAX_A = 50   # changeslow will not execute if A > this value

def plot_coins(data, part_num):
    """Plots Number of Coins vs A for each algorithm on one figure."""

    if min(data['A_list']) > CHANGESLOW_MAX_A: 
        algos = ['changegreedy', 'changedp']
    else:
        algos = ['changegreedy', 'changedp', 'changeslow']

    marks = list('o*^')
    for algo in algos: 
        x = [i for i in data['A_list']]
        y = data[algo]['num']
        plt.plot(x, y, linestyle='None', marker=marks.pop(), label=algo)

    plt.xlabel('Amount of Change to Make (A)')
    plt.ylabel('Minimum Nuber of Coins Needed')
    plt.xlim(min(x)-5, max(x)+10)
    plt.ylim(min(y)-5, max(y)+5)
    plt.title('Part {} -- Number of Coins vs. A'.format(part_num))
    plt.legend()
    plt.grid()

    return


def plot_times(data, part_num):
    """Plots Run Times vs A for all 3 algorithms on one figure."""

    if min(data['A_list']) > CHANGESLOW_MAX_A: 
        algos = ['changegreedy', 'changedp']
    else:
        algos = ['changegreedy', 'changedp', 'changeslow']

    marks = list('o*^')
    min_y, max_y = 1.0, 0.0  # used to set plot limits 
    for algo in algos: 
        x = [i for i in data['A_list']]
        y = data[algo]['times']
        if min(y) < min_y:
            min_y = min(y)
        if max(y) > max_y:
            max_y = max(y)
        plt.plot(x, y, linestyle='None', marker=marks.pop(), label=algo)

    plt.xlabel('Amount of Change to Make (A)')
    plt.ylabel('Run Time (seconds)')
    plt.xlim(min(x)*.98, max(x)*1.02)
    plt.ylim(min_y*.90, max_y*1.10)
    plt.xscale('log')
    plt.yscale('log')
    ax = plt.gca()
    plt.tick_params(axis='x', which='both')
    ax.xaxis.set_minor_formatter(FormatStrFormatter('%d'))
    ax.xaxis.set_major_locator(plt.NullLocator())
    if min(data['A_list']) > CHANGESLOW_MAX_A: 
        ax.xaxis.set_minor_locator(plt.FixedLocator(
                                   range(min(x), max(x)+100, 100)))
    else:
        ax.xaxis.set_minor_locator(plt.FixedLocator(
                                   range(min(x), max(x)+5, 5)))
    plt.title('Part {} -- Run Time vs. A'.format(part_num))
    plt.legend(loc='best')
    plt.grid(True, which="both")

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
   

def main():

    algos = {'changegreedy' : proj2_main.changegreedy,
             'changeslow' : proj2_main.changeslow,
             'changedp' : proj2_main.changedp}

    experiments = {'4 big A' : {'V' : [1, 5, 10, 25, 50], 
                          'A_list' : range(2010, 2205, 5),
                          'changeslow' : {'times' : [], 'num' : []},
                          'changegreedy' : {'times' : [], 'num' : []},
                          'changedp' : {'times' : [], 'num' : []}}, 
                   '4 small A' : {'V' : [1, 5, 10, 25, 50], 
                          'A_list' : range(5, 55, 5),
                          'changeslow' : {'times' : [], 'num' : []},
                          'changegreedy' : {'times' : [], 'num' : []},
                          'changedp' : {'times' : [], 'num' : []}}, 
                   '5_V1 big A': {'V' : [1, 2, 6, 12, 24, 48, 60], 
                            'A_list' : range(2000, 2201, 1),
                            'changeslow' : {'times' : [], 'num' : []},
                            'changegreedy' : {'times' : [], 'num' : []},
                            'changedp' : {'times' : [], 'num' : []}}, 
                   '5_V1 small A': {'V' : [1, 2, 6, 12, 24, 48, 60], 
                            'A_list' : range(5, 30, 1),
                            'changeslow' : {'times' : [], 'num' : []},
                            'changegreedy' : {'times' : [], 'num' : []},
                            'changedp' : {'times' : [], 'num' : []}}, 
                   '5_V2 big A': {'V' : [1, 6, 13, 37, 150],       
                            'A_list' : range(2000, 2201, 1),
                            'changeslow' : {'times' : [], 'num' : []},
                            'changegreedy' : {'times' : [], 'num' : []},
                            'changedp' : {'times' : [], 'num' : []}}, 
                   '5_V2 small A': {'V' : [1, 6, 13, 37, 150],       
                            'A_list' : range(5, 30, 1),
                            'changeslow' : {'times' : [], 'num' : []},
                            'changegreedy' : {'times' : [], 'num' : []},
                            'changedp' : {'times' : [], 'num' : []}}, 
                   '6 big A':  {'V' : [1] + list(range(2, 32, 2)), 
                          'A_list' : range(2000, 2201, 1),
                          'changeslow' : {'times' : [], 'num' : []},
                          'changegreedy' : {'times' : [], 'num' : []},
                          'changedp' : {'times' : [], 'num' : []}},
                   '6 small A':  {'V' : [1] + list(range(2, 32, 2)), 
                          'A_list' : range(5, 30, 1),
                          'changeslow' : {'times' : [], 'num' : []},
                          'changegreedy' : {'times' : [], 'num' : []},
                          'changedp' : {'times' : [], 'num' : []}}} 

    for part in sorted(list(experiments.keys())):
        for algo in ['changeslow', 'changegreedy', 'changedp']:
            for A in experiments[part]['A_list']: 
                print("running {} on {} for A = {}".format(part, algo, A))
                if algo == 'changeslow': 
                    if A > CHANGESLOW_MAX_A: 
                        continue
                    else:
                        args = (experiments[part]['V'], A, 1)
                else:
                    args = (experiments[part]['V'], A)
                start_time = time.time()
                #qty, min_coins = algos[algo](experiments[part]['V'], A)
                qty, min_coins = algos[algo](*args)
                end_time = time.time()
                experiments[part][algo]['times'].append(end_time - start_time)
                experiments[part][algo]['num'].append(min_coins)

        if len(sys.argv) > 1 and sys.argv[1] == '--plot':
            plt.figure()
            plot_coins(experiments[part], part)
            plt.figure()
            plot_times(experiments[part], part)
    plt.show()
    return experiments


if __name__ == "__main__":
    results = main()
