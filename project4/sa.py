import matplotlib.pyplot as plt 
import sys
import time
import math
import random
import pyximport; pyximport.install()
from two_opt import get_distance, get_tour_cost, two_opt_swap


def get_2_opt(T):
    improved = True
    T_cost = 9999999999 #get_tour_cost(T, cities) 
    initial_cost = T_cost
    while improved:
        t = time.strftime('%X %x %Z')
        print("Initial cost: {:,d}\nBest so far: {:,d} @ {}".format(
                initial_cost, T_cost, t)) 
        T, T_cost, improved = somefunc(T, T_cost, cities)
    return T 


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


def dfs(G):
    white = list(G.keys())
    gray = []
    T = []
    for u in G.keys():
        if u in white:
            T, white, gray = dfs_visit(G, u, white, gray, T)
    return T
            
def dfs_visit(G, u, white, gray, T):
    gray.append(u)
    white.remove(u)
    for v in G[u]:
        if v in white:
            dfs_visit(G, v, white, gray, T)
    gray.remove(u)
    T.append(u)
    return T, white, gray


def anneal(seed_tour, cities):
    temperature_start = 1e10
    temperature_end = 0.001
    fCool = 0.9
    num_iter = 10000
    Preverse = 0.5  # how often to choose reverse/transpose trial move

    tour_best = seed_tour 
    cost_best = get_tour_cost(tour_best, cities)  

    print('Best tour so far is {}' .format(cost_best))
    t = time.time()

    #while cost_best / cost_optimal > 1.25:
    temperature = temperature_start
    tour_current = tour_best[:] 
    cost_current = cost_best 
    tour_new = tour_best
    cost_new = cost_best


    while temperature > temperature_end: 
        for i in range(num_iter):
            # swap 2 edges at random
            index_i = random.sample(range(1, len(tour_current) - 2), 1)
            i = index_i[0]
            index_j = random.sample(range(i+1, len(tour_current) - 1), 1)
            j = index_j[0]
            tour_new = two_opt_swap(tour_current, i, j)

            cost_new = get_tour_cost(tour_new, cities) 
            difference = cost_new - cost_current

            if difference < 0 or math.exp(-difference/temperature) > random.random():
                tour_current = tour_new 
                cost_current = cost_new
            else:
                tour_new = tour_current[:]
                cost_new = cost_current

            if cost_current < cost_best :
                tour_best = tour_current[:]
                cost_best = cost_current
                if time.time() > (t + 10):
                    t = time.time()
                    tstr = time.strftime('%X %x %Z')
                    print("Best so far: {:,d} @ {}".format(cost_best, tstr)) 
                    print("Current temp: {}".format(temperature)) 
        temperature = temperature * fCool
                #print('Best tour so far is {}' .format(cost_best))
    return tour_best, cost_best


infile = sys.argv[1] 
cities = {}
with open(infile, 'r') as f:
    for line in f.readlines():
        city, x, y = line.split()
        cities[city] = (int(x), int(y))

# optimal solutions given in assignment
optimal_dict = {'1' : 108159, '2' : 2579, '3' : 1573084}
cost_optimal = optimal_dict[sys.argv[1].split('/')[-1][-5]]

def two_approx(cities):
    # use this block to use 2-approx as seed tour
    root = list(cities.keys())[0] 
    mst = prim(cities, root)
    mst_adj = {c:[] for c in cities.keys()}
    for e in mst:
        mst_adj[e[0]].append(e[1])
    T = dfs(mst_adj)
    T.reverse()
    T.append(T[0])
    return T 

# use this line for a random seed tour
#seed_tour = list(cities.keys())
#seed_tour.append(seed_tour[0])
seed_tour = two_approx(cities)
#tour_best, cost_best = anneal(seed_tour, cities)
tour_best = seed_tour
cost_best = get_tour_cost(seed_tour, cities)

print('Best tour cost is {} with ratio to optimal of {}'.format(cost_best, cost_best /
    cost_optimal))

# plot
x_arr, y_arr = [], []
for city in tour_best:
    x, y = cities[city]
    x_arr.append(x)
    y_arr.append(y)
plt.plot(x_arr, y_arr, '.-')
plt.savefig('{}.png'.format(sys.argv[1].split('/')[-1]))
#plt.show()
