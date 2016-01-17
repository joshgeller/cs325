def load_problems():
    """
    Loads problem data from MSS_Problems.txt.
    Converts each line to an array containing integers.
    All arrays are then appended to a single containing array.

    :return: array of arrays containing integers, e.g.

    [[1,2,3],[4,5,6],[7,8,9]]

    """
    problems = []
    with open('tests/MSS_Problems.txt') as f:
        for line in f:
            line = line.replace('[', '').replace(']', '').replace(',', '')
            problems.append(
                [int(num) for num in line.split(' ') if num not in ' \n'])
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
