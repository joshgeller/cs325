from __future__ import absolute_import
from utils import load_problems
from math import floor


def find_max_crossing_subarray(array, low, mid, high):
    """
    Based on pseudocode in Introduction to Algorithms, 3rd edition

    O(n) utility function to find the maximum subarray crossing the midpoint in
    a subarray size A[low..high].

    :return: tuple containing indices of a max subarray that crosses the
    midpoint, as well as the sum of the values in the max subarray.
    """

    # calculate index boundary and sum of left max subarray

    left_sum = float("-inf")
    max_left = None
    max_subarray_sum = 0

    for i in range(mid, low - 1, -1):
        max_subarray_sum += array[i]
        if max_subarray_sum > left_sum:
            left_sum = max_subarray_sum
            max_left = i

    # calculate index boundary and sum of right max subarray

    right_sum = float("-inf")
    max_right = None
    max_subarray_sum = 0

    for i in range(mid + 1, high + 1):
        max_subarray_sum += array[i]
        if max_subarray_sum > right_sum:
            right_sum = max_subarray_sum
            max_right = i

    return max_left, max_right, left_sum + right_sum


def divide_and_conquer_find_max_subarray(array, low, high):
    """
    Based on pseudocode in Introduction to Algorithms, 3rd edition

    :return:
    """

    # base case: one element in array
    if high == low:
        return low, high, array[low]

    # recursive case: >1 element in array

    else:
        mid = floor((low + high) / 2)

        # recursive sub-problems
        left_low, left_high, left_sum = \
            divide_and_conquer_find_max_subarray(array, low, mid)
        right_low, right_high, right_sum = \
            divide_and_conquer_find_max_subarray(array, mid + 1, high)

        # crossing problem
        cross_low, cross_high, cross_sum = \
            find_max_crossing_subarray(array, low, mid, high)

        # case 1: max subarray is in left array
        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum

        # case 2: max subarray is in right array
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum

        # case 3: max subarray is in array crossing midpoint
        else:
            return cross_low, cross_high, cross_sum


if __name__ == '__main__':
    problems = load_problems()
    for problem in problems:
        print(problem)
        print(
            divide_and_conquer_find_max_subarray(problem, 0, len(problem) - 1))
        print('\n\n')
