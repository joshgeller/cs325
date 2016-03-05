import numpy as np
import matplotlib.pyplot as plt 
import sys
import utils
import math

infile = sys.argv[1] 
cities = {}
with open(infile, 'r') as f:
    for line in f.readlines():
        city, x, y = line.split()
        cities[city] = (int(x), int(y))


def get_distance(x1, y1, x2, y2):
    """Returns distance between points 1 and 2."""
    return int(round(math.sqrt((x1 - x2)**2 + (y1 - y2)**2)))


def find_closest(s, V):
    """Find closest vertex to s from vertices in V."""
    min_dist = float('inf')
    for v in V.keys():
        dist_to_v =  get_distance(s[0], s[1], V[v][0], V[v][1])
        if dist_to_v < min_dist:
            min_dist = dist_to_v
            closest = v
    return closest, min_dist


def get_tour_cost(t):
    return sum([i[1] for i in t])

#  Try each city as a starting city
min_cost = float('inf')
for starting_city in cities.keys():
    cities_remaining = dict(cities)
    previous = cities_remaining.pop(starting_city)
    tour = [(starting_city, 0.0)]

    # Calculate greedy tour beginning at starting_city
    while cities_remaining:
        next, distance = find_closest(previous, cities_remaining)
        tour.append((next, distance))
        cities_remaining.pop(next)

    cost = get_tour_cost(tour)
    if cost < min_cost:
        min_cost = cost
        best_tour = tour
        best_start = starting_city

print('Best tour cost is {} starting at {}'
      .format(min_cost, cities[best_start]))

x_arr, y_arr = [], []
for city in best_tour:
    x_arr.append(cities[city[0]][0])
    y_arr.append(cities[city[0]][1])
plt.plot(x_arr, y_arr, 'o-')
#plt.ylim(500, 12200)
plt.show()
