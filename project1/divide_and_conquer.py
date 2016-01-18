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


def divide_and_conquer_max_subarray():
    # problems = load_problems()
    pass


if __name__ == '__main__':
    A = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    print(find_max_crossing_subarray(A, 0, floor(len(A) / 2), len(A) - 1))
