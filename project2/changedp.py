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


if __name__ == '__main__':
    print(changedp([1, 3, 7, 12], 31))
