import numpy as np
import sys
import math
import random


def prim(G, r):
    """
    G is a dictionary with city names as keys and x,y coords tuple as values.
    r is the root city name.

    Returns:  list of tuples (u,v) corresponding to edges in the mst from r.
    """
    # Q is {label : (key, parent)}
    G_copy = dict(G)
    Q = {}
    for u in G_copy.keys():
        Q[u] = [float('inf'), -1]
    Q[r] = [0, -1]
    mst = [] 
    while Q:
        u = min(Q, key=Q.get) 
        mst.append((Q[u][1], u))
        Q.pop(u)
        for v in Q:
            dist_uv = Distance(np.array((G[u][0], G[u][1])), np.array((G[v][0], G[v][1])))
            if dist_uv < Q[v][0]:
                Q[v][0] = dist_uv
                Q[v][1] = u 
    return mst[1:]


def dfs(G, start):
    visited, stack = set(), [start]
    T = []
    while stack:
        vertex = stack.pop()
        T.append(vertex)
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(G[vertex] - visited)
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


def two_approx(cities):
    root = list(cities.keys())[0] 
    mst = prim(cities, root)
    #mst_adj = {c:set() for c in cities.keys()}
    mst_adj = {}
    for c in cities.keys():
        mst_adj[c] = set()
    for e in mst:
        mst_adj[e[0]].add(e[1])
    T = dfs(mst_adj, root)
    T.reverse()
    return T 


def Distance(R1, R2):
    return int(round(math.sqrt(
            math.pow((R1[0] - R2[0]),2) + math.pow((R1[1] - R2[1]),2))))


def TotalDistance(tour, R):
    dist = 0
    for i in xrange(len(tour) - 1):
        dist += Distance(R[tour[i]], R[tour[i+1]])
    dist += Distance(R[tour[-1]], R[tour[0]])
    return dist


def two_opt(tour, n):
    tour[n[0]:n[1]+1] = reversed(tour[n[0]:n[1]+1])
    return tour

def three_opt(tour, n):
    nct = len(tour)
    newtour=[]

    # Segment in the range n[0]...n[1]
    for j in xrange((n[1] - n[0]) % nct + 1):
        newtour.append(tour[(j + n[0]) % nct])

    # is followed by segment n[5]...n[2]
    for j in xrange((n[2] - n[5]) % nct + 1):
        newtour.append(tour[(j + n[5]) % nct])

    # is followed by segment n[3]...n[4]
    for j in xrange((n[4] - n[3]) % nct + 1):
        newtour.append(tour[(j + n[3]) % nct])
    return newtour

def anneal(tour, cities):
    ncities = len(cities)
    Tstart = 0.3                 # Starting temperature - has to be high enough
    Tend = 0.1                   # Ending temperature - quit when reached
    fCool = 0.9 + 0.1*ncities/20000.0  # Factor to multiply temperature at each cooling step
    if fCool > 1: fCool = 0.99   # make sure temp decreases
    maxSteps = 200 * ncities     # Number of steps at constant temperature
    maxAccepted = 20 * ncities   # Number of accepted steps at constant temperature
    Preverse = 0.5      # How often to choose 2-opt/3-opt 

    # Build numpy array of coordinates (indices correspond to city labels) 
    R = np.zeros((ncities, 2))   # ncities rows, 1st col is x, 2nd col is y
    for k in cities.keys():
        R[k] = [cities[k][0], cities[k][1]]

    # Distance of the travel at the beginning
    dist = TotalDistance(tour, R)

    # Store points to be swapped for a move
    n = np.zeros(6, dtype=int)
    
    T = Tstart       
    while T > Tend:
        accepted = 0

        for i in xrange(maxSteps): # At each temperature, try several neighbor solutions

            while True: # Find two random cities sufficiently close by
                n[0] = int((ncities) * random.random())   
                n[1] = int((ncities-1) * random.random()) 
                if n[1] >= n[0]:  n[1] += 1  # can't have them be the same 
                if n[1] < n[0]:  n[0], n[1] = n[1], n[0] # swap, need: n[0]<n[1]
                # nn = number of cities not on segment n[0]..n[1]
                nn = (ncities - (n[1] - n[0] + 1)) % ncities
                if nn >= 3: break
        
            # We want to have one index before and one after the two cities
            # The order hence is [n2,n0,n1,n3]
            n[2] = (n[0]-1) % ncities  # index before n0 
            n[3] = (n[1]+1) % ncities  # index after n2 
            
            if Preverse > random.random(): 
                # Swap 2 edges (reverse path between tour[n[0]]-tour[n[1]])
                # compute difference relative to cost of current tour
                diff = (Distance(R[tour[n[2]]], R[tour[n[1]]]) + 
                        Distance(R[tour[n[3]]], R[tour[n[0]]]) - 
                        Distance(R[tour[n[2]]], R[tour[n[0]]]) - 
                        Distance(R[tour[n[3]]], R[tour[n[1]]]))
                
                if diff < 0 or np.exp(-diff/T) > random.random():
                    accepted += 1
                    dist += diff
                    tour = two_opt(tour, n)
            else:
                # Swap 3 edges
                # Get another random point outside n[0],n[1] segment.
                n[4] = (n[1] + 1 + int(random.random() * (nn - 1))) % ncities  
                n[5] = (n[4] + 1) % ncities
        
                # compute difference relative to cost of current tour
                diff = (-Distance(R[tour[n[1]]], R[tour[n[3]]]) - 
                         Distance(R[tour[n[0]]], R[tour[n[2]]]) - 
                         Distance(R[tour[n[4]]], R[tour[n[5]]]))
                diff += (Distance(R[tour[n[0]]], R[tour[n[4]]]) + 
                         Distance(R[tour[n[1]]], R[tour[n[5]]]) + 
                         Distance(R[tour[n[2]]], R[tour[n[3]]]))
                
                if diff < 0 or np.exp(-diff/T) > random.random(): 
                    accepted += 1
                    dist += diff 
                    tour = three_opt(tour, n)
                    
            if accepted > maxAccepted: break
            
        print "T=%10.5f , distance= %d, accepted steps= %d" % (T, dist, accepted)
        T *= fCool             # The system is cooled down
        if accepted == 0: break  # If the path does not want to change any more, stop

    print ("Params:  Tstart=%6.4f, fCool=%6.4f, maxSteps=%d, maxAccepted=%d" % 
          (Tstart, fCool, maxSteps, maxAccepted))

    return tour

def plot_tour(T, cities, case):
    import matplotlib.pyplot as plt
    T.append(T[0])
    x_arr, y_arr = [], []
    for city in T:
        x, y = cities[city]
        x_arr.append(x)
        y_arr.append(y)
    plt.plot(x_arr, y_arr, '.-')
    plt.savefig('%s.png' % (case))
    plt.close('all')
    #plt.show()
    

if __name__=='__main__':

    # build dict of cities from file {city : (x,y)}
    infile = sys.argv[1] 
    case_name = sys.argv[1].split('/')[-1]
    cities = {}
    with open(infile, 'r') as f:
        for line in f.readlines():
            city, x, y = line.split()
            city = int(city)
            cities[city] = (int(x), int(y))

    # get a starting tour using the MST method from textbook 
    start_tour = two_approx(cities)  

    # now optimize the tour using simulated annealing
    final_tour = anneal(start_tour, cities)

    # plot
    if sys.argv[2] and sys.argv[2] == '-p':
        plot_tour(start_tour, cities, "start_%s" % (case_name))
        plot_tour(final_tour, cities, "final_%s" % (case_name))
