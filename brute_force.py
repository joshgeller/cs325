#!/usr/local/bin/python3

def changeslow(V, K):

    if K in V:
        qty = [0] * len(V)
        qty[V.index(K)] += 1
        return qty

    min_coins = [0] * len(V)
    min_coins[0] = K

    for i in [coin for coin in V if coin <= K]:
        subproblem_qty = changeslow(V, K - i)
        subproblem_qty[V.index(i)] += 1
        if sum(min_coins) > sum(subproblem_qty):
            min_coins = subproblem_qty

    return min_coins

if __name__ == '__main__':
    print(changeslow([1, 5, 10, 25], 13), sum(changeslow([1, 5, 10, 25], 13)))
