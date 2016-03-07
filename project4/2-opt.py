import numpy as np
import matplotlib.pyplot as plt 
import sys
import utils
import math
import time

def get_distance(x1, y1, x2, y2):
    """Returns distance between points 1 and 2."""
    return int(round(math.sqrt((x1 - x2)**2 + (y1 - y2)**2)))


def get_tour_cost(t, cities):
    cost = 0
    prev = t[0]
    for v in t[1:]:
        x1, y1 = cities[prev]
        x2, y2 = cities[v]
        cost += get_distance(x1, y1, x2, y2)
        prev = v
    return cost 


def two_opt_swap(T, i, k):
    return T[:i] + T[k:i-1:-1] + T[k+1:]


def get_2_opt(T):
    improved = True
    T_cost = get_tour_cost(T, cities) 
    initial_cost = T_cost
    t = time.strftime('%X %x %Z')
    while improved:
        improved = False
        for i in range(1, len(T[1:-1])): 
            print("Initial cost: {:,d}\nBest so far: {:,d} @ {}".format(
                  initial_cost, T_cost, t)) 
            for k in range(i+1, len(T[1:-1]) + 1):
                Tp = two_opt_swap(T, i, k) 
                Tp_cost = get_tour_cost(Tp, cities)
                if Tp_cost < T_cost:
                    t = time.strftime('%X %x %Z')
                    T = Tp
                    T_cost = Tp_cost
                    improved = True
                    break
    return T 
# 134,373,971
infile = sys.argv[1] 
cities = {}
with open(infile, 'r') as f:
    for line in f.readlines():
        city, x, y = line.split()
        cities[city] = (int(x), int(y))

# use random tour as starting point for 2-opt
best_tour = list(cities.keys())
best_tour.append(best_tour[-1])
two_opt_tour = get_2_opt(best_tour)
two_opt_cost = get_tour_cost(two_opt_tour, cities)

print('Best tour cost is {} starting at {}'
      .format(two_opt_cost, cities[best_tour[0]]))

x_arr, y_arr = [], []
for city in two_opt_tour:
    x, y = cities[city]
    x_arr.append(x)
    y_arr.append(y)
plt.plot(x_arr, y_arr, 'o-')
plt.savefig('{}.png'.format(sys.argv[1].split('/')[-1]))
#plt.show()
