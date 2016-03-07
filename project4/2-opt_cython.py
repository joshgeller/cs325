import matplotlib.pyplot as plt 
import sys
import time
import pyximport; pyximport.install()
from two_opt import get_distance, get_tour_cost, somefunc 


def get_2_opt(T):
    improved = True
    T_cost = 9999999999 #get_tour_cost(T, cities) 
    initial_cost = T_cost
    t = time.strftime('%X %x %Z')
    while improved:
        print("Initial cost: {:,d}\nBest so far: {:,d} @ {}".format(
                initial_cost, T_cost, t)) 
        T, T_cost, improved = somefunc(T, T_cost, cities)
    return T 

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
