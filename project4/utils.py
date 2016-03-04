#!/usr/local/bin/python3
import math
import sys


class City(object):
    """
    Represents a City in a TSP problem.
    """

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self):
        return '<City {0}>'.format(self.id)


def distance(c1, c2):
    """
    Calculates the Pythagorean distance between city coordinates on a 2D plane.

    :param c1: City
    :param c2: City
    :return: integer representing distance between two City objects
    """
    if not isinstance(c1, City):
        raise TypeError('Expected City, got {0}'.format(type(c1)))
    if not isinstance(c2, City):
        raise TypeError('Expected City, got {0}'.format(type(c2)))
    term1 = pow((c1.x - c2.x), 2)
    term2 = pow((c1.y - c2.y), 2)
    int(round(math.sqrt(term1 + term2)))


def load(*args):
    """
    Loads raw TSP problem data and initializes new City objects for each
    line of raw data.

    :param args: (tuple) tuple containing sys.argv command line arguments
    :return: (list of City) List of initialized City objects
    """
    raw_cities = [line.rstrip('\n') for line in open(args[0][1])]
    cities = []
    for city in raw_cities:
        id, x, y = city.split(' ')
        cities.append(City(id, x, y))


def results(filename, length, cities):
    """
    Writes TSP solution results in the proper format.

    :param filename: (str) results filename to use
    :param length: (int) length of TSP tour solution
    :param cities: (list of City) list containing all City objects in TSP solution
    :return: writes results to disk
    """
    with open(filename, 'w') as f:
        f.write('{0}\n'.format(length))
        for city in cities:
            if not isinstance(city, City):
                raise TypeError('Expected City, got {0}'.format(type(city)))
            f.write('{0}\n'.format(city.id))


if __name__ == '__main__':
    load(sys.argv)
