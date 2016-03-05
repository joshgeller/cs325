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
    while Q:
        u = min(Q, key=Q.get) 
        mst.append((Q[u][1], u))
        Q.pop(u)
        for v in Q:
            dist_uv = get_distance(G[u][0], G[u][1], G[v][0], G[v][1])
            if dist_uv < Q[v][0]:
                Q[v][0] = dist_uv
                Q[v][1] = u 
    return mst[1:]

def mst_to_tour(mst):
    """Converts a list of tuples representing edges of an MST to a preorder
    walk, or tour"""
    tour = []
    visited = []
    for edge in mst:
        if edge[0] not in visited:
            tour.append(edge[0])
            visited.append(edge[0])
        if edge[1] not in visited:
            tour.append(edge[1])
            visited.append(edge[1])
    tour.append(tour[0])
    return tour


def get_tour_cost(t, cities):
    cost = 0
    prev = t[0]
    for v in t[1:]:
        x1, y1 = cities[prev]
        x2, y2 = cities[v]
        cost += get_distance(x1, y1, x2, y2)
        prev = v
    return cost 


infile = sys.argv[1] 
cities = {}
with open(infile, 'r') as f:
    for line in f.readlines():
        city, x, y = line.split()
        cities[city] = (int(x), int(y))


#  Try each city as a starting city
min_cost = float('inf')
for root in ['1']cities.keys():
    mst = prim(cities, root)
    tour = mst_to_tour(mst)
    cost = get_tour_cost(tour, cities)
    if cost < min_cost:
        min_cost = cost
        best_tour = tour
        best_start = root

print('Best tour cost is {} starting at {}'
      .format(min_cost, cities[best_start]))

x_arr, y_arr = [], []
for city in tour:
    x, y = cities[city]
    x_arr.append(x)
    y_arr.append(y)
plt.plot(x_arr, y_arr, 'o-')
plt.show()
