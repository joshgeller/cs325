#!/usr/local/bin/python3

def changeslow(V, K, total):

    # create an array to keep track of the coins used
    min_coins = [0] * len(V)

    # if there exists a coin that is the same as the change we need,
    # increment the corresponding coin value in the array
    # return array and total (total is passed to function as 1, so remains 1 in this case)
    if K in V:
        min_coins[V.index(K)] += 1
        return min_coins, total

    min_coins[0] = K

    # loop through value list to find minimum number of coins needed
    for i in [coin for coin in V if coin <= K]:
        subproblem_qty, dummy = changeslow(V, K - i, total)
        subproblem_qty[V.index(i)] += 1
        # update min_coins and total if needed
        if sum(min_coins) > sum(subproblem_qty):
            min_coins = subproblem_qty
            total = sum(min_coins)
    return min_coins, total

if __name__ == '__main__':
    print(changeslow([1, 5, 10, 12], 48, 1))
