import matplotlib.pyplot as plt 
import sys
import time
import pyximport; pyximport.install()
from two_opt import get_distance, get_tour_cost, somefunc 


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
    for u in G.keys():
        if u in white:
            dfs_visit(G, u)
            
def dfs_visit(G, u):
    gray.append(u)
    white.remove(u)
    for v in G[u]:
        if v in white:
            dfs_visit(G, v)
    gray.remove(u)
    T.append(u)


infile = sys.argv[1] 
cities = {}
with open(infile, 'r') as f:
    for line in f.readlines():
        city, x, y = line.split()
        cities[city] = (int(x), int(y))

# use 2-approx tour as starting point for 2-opt
root = '1'
mst = prim(cities, root)
mst_adj = {c:[] for c in cities.keys()}
for e in mst:
    mst_adj[e[0]].append(e[1])

# do DFS to get preorder traversal of MST
white = list(mst_adj.keys())
gray = []
T = []
dfs(mst_adj)
T.reverse()
T.append(T[0])
seed_tour = T

# run 2-opt on seed tour
two_opt_tour = get_2_opt(seed_tour)
two_opt_cost = get_tour_cost(two_opt_tour, cities)
print('Best tour cost is {} starting at {}'
      .format(two_opt_cost, cities[two_opt_tour[0]]))

# plot
x_arr, y_arr = [], []
for city in two_opt_tour:
    x, y = cities[city]
    x_arr.append(x)
    y_arr.append(y)
plt.plot(x_arr, y_arr, '.-')
plt.savefig('{}.png'.format(sys.argv[1].split('/')[-1]))
plt.show()
