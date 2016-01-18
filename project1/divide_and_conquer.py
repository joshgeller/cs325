from utils import load_problems, write_results
from math import floor


def find_max_crossing_subarray(array, low, mid, high):
    """
    Based on pseudocode in Introduction to Algorithms, 3rd edition

    O(n) utility function to find the maximum sub-array crossing the midpoint in
    a sub-array size A[low..high].

    :return: tuple containing indices of a max subarray that crosses the
    midpoint, as well as the sum of the values in the max sub-array.
    """

    # calculate index boundary and sum of left max sub-array

    left_sum = float("-inf")
    max_left = None
    max_subarray_sum = 0

    for i in range(mid, low - 1, -1):
        max_subarray_sum += array[i]
        if max_subarray_sum > left_sum:
            left_sum = max_subarray_sum
            max_left = i

    # calculate index boundary and sum of right max sub-array

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

    Recursively searches the left, right, and crossing sub-arrays in
    array[low..high] to find the maximum sub-array.

    :return: tuple containing indices of a max sub-array, as well as the sum of
    the values in the max sub-array.
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

        # crossing sub-problem
        cross_low, cross_high, cross_sum = \
            find_max_crossing_subarray(array, low, mid, high)

        # case 1: max sub-array is in left array
        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum

        # case 2: max sub-array is in right array
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum

        # case 3: max sub-array is in array crossing midpoint
        else:
            return cross_low, cross_high, cross_sum


if __name__ == '__main__':
    problems = load_problems()
    for problem in problems:
        results = divide_and_conquer_find_max_subarray(array=problem,
                                                       low=0,
                                                       high=len(problem) - 1)
        write_results(
            filename='divide_and_conquer_results.txt',
            original_array=problem,
            max_subarray=problem[results[0]:results[1] + 1],
            max_sum=results[2]
        )
