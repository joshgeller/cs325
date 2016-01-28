def changedp(coins, change):
    # first, we create an array with n indices, where n = change
    # min_coins[i] = the minimum number of coins needed to make i change
    # e.g. let change=5, min_coins = [0, 0, 0, 0, 0]
    min_coins = [0] * (change + 1)

    # bottom-up approach - solve small sub-problems first, from [0..change]
    for change_subproblem in range(change + 1):

        # worst-case scenario: we need one coin for every cent in the sub-problem
        coins_needed = change_subproblem

        # use optimal sub-structure of sub-problems to determine the
        # minimum number of coins required for the current sub-problem
        for coin_value in coins:
            if coin_value <= change_subproblem:
                coins_needed = min(
                    coins_needed,
                    1 + min_coins[change_subproblem - coin_value]
                )

        # store the sub-problem solution in the table
        min_coins[change_subproblem] = coins_needed

    return min_coins[change]


if __name__ == '__main__':
    print(changedp([1, 3, 4], 11))
