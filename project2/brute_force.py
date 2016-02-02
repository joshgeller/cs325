#!/usr/local/bin/python3

def changeslow(V, K):

    min_coins = [0] * len(V)

    if K in V:
        min_coins[V.index(K)] += 1
        return min_coins

    min_coins[0] = K

    for i in [coin for coin in V if coin <= K]:
        subproblem_qty = changeslow(V, K - i)
        subproblem_qty[V.index(i)] += 1
        if sum(min_coins) > sum(subproblem_qty):
            min_coins = subproblem_qty
    return min_coins

if __name__ == '__main__':
    print(changeslow([1, 5, 10, 12], 29), sum(changeslow([1, 5, 10, 12], 29)))
