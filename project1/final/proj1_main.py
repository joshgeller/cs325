#/usr/bin/python3.2
'''
    CS 325 Winter 2016 -- Project 1: Maximum Sum Subarray

    Program to compare four different algorithms for determining the subarray 
    with the maximum sum given an array of integers.
'''

from math import floor


def mss_enum(ls):
    maxSum = newSum = 0
    low = high = 0
    i = 0
    for i in range(len(ls)):
        for j in range(i, len(ls)):
            newSum = 0
            for a in ls[i:j+1]:
                newSum += a
            if newSum > maxSum:
                maxSum = newSum
                low = i
                high = j
    return low, high, maxSum


def mss_better_enum(ls):
    maxSum = newSum = 0
    low = high = 0
    i = 0
    for i in range(len(ls)):
        newSum = 0
        for j in range(i, len(ls)):
            newSum = newSum + ls[j]
            if newSum > maxSum:
                maxSum = newSum
                low = i
                high = j
    return low, high, maxSum


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


def mss_div_and_conq(array, low, high):
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
        mid = int(floor((low + high) / 2))

        # recursive sub-problems

        left_low, left_high, left_sum = \
            mss_div_and_conq(array, low, mid)

        right_low, right_high, right_sum = \
            mss_div_and_conq(array, mid + 1, high)

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


def mss_linear(A):
    sum_ij = max_sum = A[0]
    i = j = 0          # indices of current subarray
    i_max = j_max = 0  # indices of max subarray
    for j, val in enumerate(A[1:], 1):
        sum_ij += val
        if val > (sum_ij):
            sum_ij = val
            i = j

        if sum_ij > max_sum:
            max_sum = sum_ij
            j_max = j 
            i_max = i
    return i_max, j_max, max_sum


def load_problems():
    """
    Loads problem data from MSS_Problems.txt.
    Converts each line to an array containing integers.
    All arrays are then appended to a single containing array.

    :return: array of arrays containing integers, e.g.

    [[1,2,3],[4,5,6],[7,8,9]]
    """
    problems = []
    #with open('tests/MSS_Problems.txt') as f:
    with open('MSS_Problems.txt') as f:
        for line in f:
            line = line.replace('[', '').replace(']', '').replace(' ', '')
            problems.append(
                [int(num) for num in line.split(',') if num not in '\n'])
    return problems


def write_results(filename, algorithm_name, original_array, max_subarray, max_sum):
    """
    Writes results to file in proper format.

    :param filename: output filename
    :param algorithm_name: name of algorithm to categorize results file
    :param original_array: original array
    :param max_subarray: max subarray in original_array
    :param max_sum: sum of elements in max_subarray
    :return: outputs file to disk
    """
    with open(filename, 'a') as f:
        f.write('{0}\n'.format(algorithm_name))
        f.write('{0}\n'.format(original_array))
        f.write('{0}\n'.format(max_subarray))
        f.write('{0}\n\n'.format(max_sum))


def main():

    algorithms = {
        'Linear': mss_linear,
        'Enum': mss_enum,
        'Better Enum': mss_better_enum,
        'Divide and Conquer': mss_div_and_conq
    }

    problems = load_problems()
    for algorithm_name, algorithm_func in algorithms.items():
        print('Running {0}...'.format(algorithm_name))
        for problem in problems:
            if algorithm_name == 'Divide and Conquer':
                results = algorithm_func(array=problem, low=0, high=len(problem) - 1)
                write_results(
                    filename='MSS_Results.txt',
                    algorithm_name=algorithm_name,
                    original_array=problem,
                    max_subarray=problem[results[0]:results[1] + 1],
                    max_sum=results[2]
                )
            else:
                results = algorithm_func(problem)
                write_results(
                    filename='MSS_Results.txt',
                    algorithm_name=algorithm_name,
                    original_array=problem,
                    max_subarray=problem[results[0]:results[1] + 1],
                    max_sum=results[2]
                )


if __name__ == "__main__":
    main()
