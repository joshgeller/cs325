def changedp(coins, change):
    # first, we create an array with n indices, where n = change
    # min_coins[i] = the minimum number of coins needed to make i change
    # e.g. let change=5, min_coins = [0, 0, 0, 0, 0]
    min_coins = [0] * (change + 1)

    coins_used = [0] * (change + 1)

    # bottom-up approach - solve small sub-problems first, from [0..change]
    for change_subproblem in range(change + 1):

        # base case: one cent coin needed for every cent in the sub-problem
        coins_needed = change_subproblem
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

    # TODO output
    return coins_used, min_coins[change]


if __name__ == '__main__':
    print(changedp([1, 5, 10, 21, 25], 63))
