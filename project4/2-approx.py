import numpy as np
import matplotlib.pyplot as plt 
import sys
import utils
import math


def get_distance(x1, y1, x2, y2):
    """Returns distance between points 1 and 2."""
    return int(round(math.sqrt((x1 - x2)**2 + (y1 - y2)**2)))

def prim(G, r):
    """
    G is a dictionary with city names as keys and x,y coords tuple as values.
    r is the root city name.

    Returns:  list of tuples (u,v) corresponding to edges in the mst from r.
    """
    # Q is {label : (key, parent)}
    G_copy = dict(G)
    Q = {u : [float('inf'), -1] for u in G_copy.keys()} 
    Q[r] = [0, -1]
    mst = [] 
    prev = Q[r][1]
    while Q:
        u = min(Q, key=Q.get) 
        mst.append((prev, u))
        prev = u
        Q.pop(u)
        for v in Q:
            dist_uv = get_distance(G[u][0], G[u][1], G[v][0], G[v][1])
            if dist_uv < Q[v][0]:
                Q[v][0] = dist_uv
                Q[v][1] = u 
    mst.append((prev, r))
    return mst[1:]


def get_tour_cost(t, cities):
    cost = 0
    for e in t:
        x1, y1 = cities[e[0]]
        x2, y2 = cities[e[1]]
        cost += get_distance(x1, y1, x2, y2)
    return cost 


infile = sys.argv[1] 
cities = {}
with open(infile, 'r') as f:
    for line in f.readlines():
        city, x, y = line.split()
        cities[city] = (int(x), int(y))


#  Try each city as a starting city
min_cost = float('inf')
for root in cities.keys():
    tour = prim(cities, root)
    cost = get_tour_cost(tour, cities)
    if cost < min_cost:
        min_cost = cost
        best_tour = tour
        best_start = root

print('Best tour cost is {} starting at {}'
      .format(min_cost, cities[best_start]))

x_arr, y_arr = [], []
for edge in best_tour:
    x1, y1 = cities[edge[0]]
    x2, y2 = cities[edge[1]]
    x_arr.append(x1)
    x_arr.append(x2)
    y_arr.append(y1)
    y_arr.append(y2)
plt.plot(x_arr, y_arr, 'o-')
plt.show()
