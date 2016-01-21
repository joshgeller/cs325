''' 
    CS 325 Winter 2016 -- Project 1: Maximum Sum Subarray

    Program to compare four different algorithms for determining the subarray 
    with the maximum sum given an array of integers.
'''

from math import floor

def mss_enum(ls):
    return 

def mss_better_enum(ls):
    return

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
        # calculate midpoint of sub-array
        mid = int(floor((low + high) / 2))

        # recursive sub-problem: left-array
        left_low, left_high, left_sum = \
            mss_div_and_conq(array, low, mid)

        # recursive sub-problem: right-array
        right_low, right_high, right_sum = \
            mss_div_and_conq(array, mid + 1, high)

        # crossing sub-problem: find the index bounds and sum of the maximum
        # sub-array crossing the midpoint of array[low..high]

        left_sum = float("-inf")
        max_left = None
        max_subarray_sum = 0

        # work from mid->low to find the maximum sub-array on the left side
        for i in range(mid, low - 1, -1):
            max_subarray_sum += array[i]
            if max_subarray_sum > left_sum:
                left_sum = max_subarray_sum
                max_left = i

        right_sum = float("-inf")
        max_right = None
        max_subarray_sum = 0

        # work from mid->high to find the maximum sub-array on the right side
        for i in range(mid + 1, high + 1):
            max_subarray_sum += array[i]
            if max_subarray_sum > right_sum:
                right_sum = max_subarray_sum
                max_right = i

        # combine the left/right arrays crossing the midpoint
        cross_low, cross_high, cross_sum = max_left, max_right, left_sum + right_sum

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
    max_sum = A[0]
    sum_ij = A[0]
    i_max = 0  # lower index of max subarray
    j_max = 0  # upper index of max subarray
    i = 0
    j = 0
    prev = A[0]
    for j, val in enumerate(A[1:], 1):
        sum_ij += val
        if prev < 0 and val > max_sum:
            max_sum = val
            sum_ij = val
            i_max = j 
            j_max = j 
            i = j
        elif -prev > max_sum:
            sum_ij = val 
            i = j 
        elif sum_ij > max_sum:
            max_sum = sum_ij
            j_max = j 
            if i > i_max:
                i_max = i
        prev = val
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
    with open('tests/MSS_TestProblems.txt') as f:
        for line in f:
            line = line.replace('[', '').replace(']', '').replace(' ', '')
            problems.append(
                [int(num) for num in line.split(',') if num not in '\n'])
    return problems


def write_results(filename, original_array, max_subarray, max_sum):
    """
    Writes results to file in proper format.

    :param filename: output filename
    :param original_array: original array
    :param max_subarray: max subarray in original_array
    :param max_sum: sum of elements in max_subarray
    :return: outputs file to disk
    """
    with open(filename, 'a') as f:
        f.write('{}\n'.format(original_array))
        f.write('{}\n'.format(max_subarray))
        f.write('{}\n\n'.format(max_sum))


def main():
    problems = load_problems() 
    for problem in problems:
        #results = mss_linear(problem)
        results = mss_div_and_conq(array=problem, low=0, high=len(problem) - 1)
        write_results(
            filename='MSS_Results.txt',
            original_array=problem,
            max_subarray=problem[results[0]:results[1] + 1],
            max_sum=results[2]
        )


if __name__ == "__main__":
    times = main()
