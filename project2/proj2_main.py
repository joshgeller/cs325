####! /usr/local/bin/python3

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
                coins = [int(num) for num in coins.replace('[', '')
                            .replace(']', '')
                            .replace(' ', '')
                            .split(',') if num not in '\n']
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

def changegreedy(V, A):
    """ Naive greedy algorithm."""
    min = 0
    qtys = [0] * len(V)
    change_made = 0
    i = len(V) - 1 
    while change_made < A:
        if (V[i] + change_made <= A):
            change_made += V[i]
            qtys[i] += 1
            min += 1
        else:
            i -= 1

    return qtys, min


def changedp(coins, change):

    # first, we create an array with n indices, where n = change
    # min_coins[i] = the minimum number of coins needed to make i change
    # e.g. let change=5, min_coins = [0, 0, 0, 0, 0]
    min_coins = [0] * (change + 1)

    # create an array with m indices, where m = change
    # table used to calculate the quantity of each coin used to make m change
    # coins_used[i] = the value of the last coin used to make i change
    # e.g. let change=1, coins_used[i] = 1
    coins_used = [0] * (change + 1)

    # final results array - quantity used for each coin value
    # e.g. let coins=[1,5], change=5, qty_used=[0,1]
    qty_used = [0] * len(coins)

    # bottom-up approach - solve small sub-problems first, from [0..change]
    for change_subproblem in range(change + 1):

        # base case: zero or one coin needed for every cent in the sub-problem
        coins_needed = change_subproblem
        if change_subproblem == 0:
            last_coin_used = 0
        else:
            last_coin_used = 1

        # use optimal sub-structure of sub-problems to determine the
        # minimum number of coins required for the current sub-problem
        for coin in coins:
            if coin <= change_subproblem:
                if 1 + min_coins[change_subproblem - coin] < coins_needed:
                    coins_needed = 1 + min_coins[change_subproblem - coin]
                    last_coin_used = coin

        # store the sub-problem solution in the table
        min_coins[change_subproblem] = coins_needed

        # store the last coin used
        coins_used[change_subproblem] = last_coin_used

    # add up how many coins of each value were used
    coin = change
    while coin > 0:
        # get the coin used to make the change at the current position
        coin_used = coins_used[coin]
        # increment the quantity used for this denomination
        qty_used[coins.index(coin_used)] += 1
        # subtract the value of the coin used to find the next coin
        coin -= coin_used

    return qty_used, min_coins[change]


def changeslow(V, K, total):
    min_coins = [0] * len(V)

    if K in V:
        min_coins[V.index(K)] += 1
        return min_coins, total

    min_coins[0] = K

    for i in [coin for coin in V if coin <= K]:
        subproblem_qty, dummy = changeslow(V, K - i, total)
        subproblem_qty[V.index(i)] += 1
        if sum(min_coins) > sum(subproblem_qty):
            min_coins = subproblem_qty
            total = sum(min_coins)
    return min_coins, total


def main():
    #problems = load_problems() 
    problems = [([1, 2, 4, 8], 15),
                ([1, 3, 7, 12], 29),
                ([1, 3, 7, 12], 31)]
    for problem  in problems:
        print("Problem: {}, {}".format(*problem))
        #qty_array, min_coins = changeslow(problem[0], problem[1], 1)
        qty_array, min_coins = changegreedy(problem[0], problem[1])
        #qty_array, min_coins = changedp(problem[0], problem[1])
        print("Min: {}  Qtys: {}".format(min_coins, qty_array))

    #write_results('greedy_out.txt', 'greedy', qty_array, min_coins)

    return qty_array


if __name__ == "__main__":
    results = main()
