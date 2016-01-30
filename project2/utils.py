#!/usr/local/bin/python3

def load_problems():
    """
    Loads problem data from Coin1.txt.
    Reads two lines at a time to extract full problem data.

    :return: array of tuples, each tuple represents a coin change problem

    [([1, 5, 10, 25, 50], 75), ([1, 10, 21, 50], 63), ([1, 2, 4, 8, 16], 120)]

    """
    problems = []
    f = open('tests/Coin1.txt', 'r')
    while 1:
        try:
            coins = f.readline()
            if coins:
                coins = [int(num) for num in coins.replace('[', '').replace(']', '').replace(' ', '').split(',') if num not in '\n']
            else:
                break
            change = f.readline()
            if change:
                change = change.replace('\n', '')
                change = int(change)
            else:
                break
        except Exception:
            break

        problems.append((coins, change))

    return problems

def write_results(filename, algorithm_name, qty_array, min_coins):
    """
    Writes results to file in proper format.

    :param filename: output filename
    :param algorithm_name: name of algorithm to categorize results file
    :param qty_array: results array representing qty of each coin used
    :param min_coins: integer representing min # of coins used for problem
    :return: outputs file to disk
    """
    with open(filename, 'a') as f:
        f.write('{0}\n'.format(algorithm_name))
        f.write('{0}\n'.format(qty_array))
        f.write('{0}\n\n'.format(min_coins))
