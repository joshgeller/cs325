#! /usr/local/bin/python3

def load_problems():
    """
    Loads problem data from Coin1.txt.
    Converts each line to an array containing integers.
    All arrays are then appended to a single containing array.

    :return: array of arrays containing integers, e.g.

    [[1,2,3],[4,5,6],[7,8,9]]
    """
    problems = []
    with open('tests/Coin1.txt') as f:
        for line in f:
            line = line.replace('[', '').replace(']', '').replace(' ', '')
            problems.append(
                [int(num) for num in line.split(',') if num not in '\n'])
    return problems
