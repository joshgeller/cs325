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
    plt.title('{}'.format(part_num))
    plt.legend()
    plt.grid()
    plt.savefig('MinCoins_{}.png'.format(part_num))

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

    plt.xlabel('Amount of Change to Make (A) - Log Scale')
    plt.ylabel('Run Time (sec) - Log Scale')
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
    plt.title('{}'.format(part_num))
    plt.legend(loc='best')
    plt.grid(True, which="both")
    plt.savefig('Times_{}.png'.format(part_num))

    return


def plot_time_vs_num_denom(data):
    """Plot mean run times vs. number of denominations."""
    for algo in ['changegreedy', 'changedp', 'changeslow']:
        plt.figure()
        for part in list(data.keys()):
            print(algo, part)
            min_y, max_y = 10.0, 0.0  # used to set plot limits 
            if algo == 'changeslow' and min(data[part]['A_list']) > CHANGESLOW_MAX_A:
                continue
            else:
                x = len(data[part]['V'])  # number of denominations
                y = np.mean(data[part][algo]['times'])
                if y < min_y:
                    min_y = y 
                if y > max_y:
                    max_y = y 
                plt.plot(x, y, 'bo')

        plt.xlabel('Number of Available Denominations')
        plt.ylabel('Run Time (sec)')
        plt.xlim(4, 17)
        #plt.ylim(min_y*.95, max_y*1.05)
        #plt.ylim(0.0, max_y*1.05)
        plt.yscale('log')
        plt.title('Part 8: {}'.format(algo))
        plt.grid()
        plt.savefig('8_{}.png'.format(algo))

    return
   

def main():

    algos = {'changegreedy' : proj2_main.changegreedy,
             'changeslow' : proj2_main.changeslow,
             'changedp' : proj2_main.changedp}

    experiments = {'Part 4 -- A = 2010, 2015, 2020,...,2200' : 
                          {'V' : [1, 5, 10, 25, 50], 
                           'A_list' : range(2010, 2205, 5),
                           'changeslow' : {'times' : [], 'num' : []},
                           'changegreedy' : {'times' : [], 'num' : []},
                           'changedp' : {'times' : [], 'num' : []}}, 
                    'Part 4 -- A = 5, 10, 15,...,50' :
                          {'V' : [1, 5, 10, 25, 50], 
                           'A_list' : range(5, 55, 5),
                           'changeslow' : {'times' : [], 'num' : []},
                           'changegreedy' : {'times' : [], 'num' : []},
                           'changedp' : {'times' : [], 'num' : []}}, 
                    'Part 5 -- with V1 and A = 2000, 2001, 2002,...,2200' :
                          {'V' : [1, 2, 6, 12, 24, 48, 60], 
                           'A_list' : range(2000, 2201, 1),
                           'changeslow' : {'times' : [], 'num' : []},
                           'changegreedy' : {'times' : [], 'num' : []},
                           'changedp' : {'times' : [], 'num' : []}}, 
                    'Part 5 -- with V1 and A = 5, 6, 7,...,30' :
                          {'V' : [1, 2, 6, 12, 24, 48, 60], 
                           'A_list' : range(5, 31, 1),
                           'changeslow' : {'times' : [], 'num' : []},
                           'changegreedy' : {'times' : [], 'num' : []},
                           'changedp' : {'times' : [], 'num' : []}}, 
                    'Part 5 -- with V2 and A = 2000, 2001, 2002,...,2200' :
                          {'V' : [1, 6, 13, 37, 150],       
                           'A_list' : range(2000, 2201, 1),
                           'changeslow' : {'times' : [], 'num' : []},
                           'changegreedy' : {'times' : [], 'num' : []},
                           'changedp' : {'times' : [], 'num' : []}}, 
                    'Part 5 -- with V2 and A = 5, 6, 7,...,30' :
                          {'V' : [1, 6, 13, 37, 150],       
                           'A_list' : range(5, 31, 1),
                           'changeslow' : {'times' : [], 'num' : []},
                           'changegreedy' : {'times' : [], 'num' : []},
                           'changedp' : {'times' : [], 'num' : []}}, 
                    'Part 6 -- A = 2000, 2001, 2002,...,2200' :
                          {'V' : [1] + list(range(2, 32, 2)), 
                           'A_list' : range(2000, 2201, 1),
                           'changeslow' : {'times' : [], 'num' : []},
                           'changegreedy' : {'times' : [], 'num' : []},
                           'changedp' : {'times' : [], 'num' : []}},
                    'Part 6 -- A = 5, 6, 7,...,30' :
                          {'V' : [1] + list(range(2, 32, 2)), 
                           'A_list' : range(5, 31, 1),
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
                qty, min_coins = algos[algo](*args)
                end_time = time.time()
                experiments[part][algo]['times'].append(end_time - start_time)
                experiments[part][algo]['num'].append(min_coins)

        if len(sys.argv) > 1 and sys.argv[1] == '--plot':
            plt.figure()
            plot_coins(experiments[part], part)
            plt.figure()
            plot_times(experiments[part], part)

    plot_time_vs_num_denom(experiments)
    plt.show()
    return experiments


if __name__ == "__main__":
    results = main()
