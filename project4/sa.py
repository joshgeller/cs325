#============================================================================== 
#    CS 325, Winter 2016.  Group 2. Project 4.  Traveling Salesman Problem
#    This program based in large part on methods discussed at:
#    www.physics.rutgers.edu/~haule/681/MC.pdf
#    and associated code found at:
#    www.physics.rutgers.edu/~haule/681/src_MC/python_codes/salesman.py
#============================================================================== 
import numpy as np
import sys
import math
import random
import time


def prim(G, r):
    """
    G is a dictionary with city names as keys and x,y coords tuple as values.
    r is the root city name.

    Returns:  list of tuples (u,v) corresponding to edges in the MST 
              using Prim's algorithm starting from r.
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
            dist_uv = Distance(np.array((G[u][0], G[u][1])), 
                               np.array((G[v][0], G[v][1])))
            if dist_uv < Q[v][0]:
                Q[v][0] = dist_uv
                Q[v][1] = u 
    return mst[1:]


def dfs(G, start):
    """
    G is a dictionary with city names as keys and x,y coords tuple as values.
    start is the root city name.

    Returns:  an ordered list of vertices in G corresponding to the order
              in which they are processed in the search (i.e. a preorder
              walk).
    """
    visited, stack = set(), [start]
    T = []
    while stack:
        vertex = stack.pop()
        T.append(vertex)
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(G[vertex] - visited)
    return T


def two_approx(G):
    """
    G is a dictionary with city names as keys and x,y coords tuple as values.

    Returns:  an ordered list of vertices in G corresponding to an approximate
              solution to the minimum cost hamiltonian cycle. 

    Notes:   First calculates a minimum spanning tree (MST) using Prim's
             algorithm and then finds the solutions by doing a pre-order 
             walk (depth first search) of the MST. Guaranteed to give
             a tour that is at most 2 times the optimal solution.  
    """
    root = list(G.keys())[0] 
    mst = prim(G, root)
    mst_adj = {}

    # convert G to an adjacency list
    for c in G.keys():
        mst_adj[c] = set()
    for e in mst:
        mst_adj[e[0]].add(e[1])
    T = dfs(mst_adj, root)
    T.reverse()
    return T 


def Distance(R1, R2):
    """ 
    R1, R2:  numpy arrays containing x,y coorrdinates for a node. 

    Returns:  Distance between R1 and R2 in XY plane.
    """
    return int(round(math.sqrt(
            math.pow((R1[0] - R2[0]),2) + math.pow((R1[1] - R2[1]),2))))


def TotalDistance(tour, R):
    """
    Returns the total distance of a tour.
    """
    dist = 0
    for i in xrange(len(tour) - 1):
        dist += Distance(R[tour[i]], R[tour[i+1]])
    dist += Distance(R[tour[-1]], R[tour[0]])
    return dist


def two_opt(tour, n):
    """ 
    Swaps two edges in a tour.
    Based on code found at:
    www.physics.rutgers.edu/~haule/681/src_MC/python_codes/salesman.py
    """
    tour[n[0]:n[1]+1] = reversed(tour[n[0]:n[1]+1])
    return tour


def three_opt(tour, n):
    """ 
    Swaps three edges in a tour.
    Based on code found at:
    www.physics.rutgers.edu/~haule/681/src_MC/python_codes/salesman.py
    """
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


def anneal(tour, cities, start_time):
    """
    Performs simulated annealing on a given ordering of vertices (tour)
    in a graph (cities) with nodes on the XY plane.

    Returns: tour, dist
        tour = list of cities corresponding to solution
        dist = total distance of tour
    Based on code found at:
    www.physics.rutgers.edu/~haule/681/src_MC/python_codes/salesman.py
    """
    ncities = len(cities)
    Tstart = 0.3                 # Starting temperature - has to be high enough
    Tend = 0.1
    # fCool is Factor to multiply temperature at each cooling step
    # It is tuned to provide a good balance between performance and finding a
    # good approximation for problems sizes up to 20,000 nodes.
    fCool = 0.9 + 0.1*ncities/20000.0  
    if fCool > 1: fCool = 0.99   # make sure temp decreases
    maxSteps = 200 * ncities     # Number of steps at constant temperature
    maxAccepted = 20 * ncities   # Number of accepted steps at constant temperature
    P_2opt_3_opt = 0.5           # How often to choose 2-opt/3-opt 

    # Build numpy array of coordinates (indices correspond to city labels) 
    R = np.zeros((ncities, 2))   # ncities rows, 1st col is x, 2nd col is y
    for k in cities.keys():
        R[k] = [cities[k][0], cities[k][1]]

    # Distance of the travel at the beginning
    dist = TotalDistance(tour, R)

    # Store points to be swapped for a move
    n = np.zeros(6, dtype=int)

    # Set max run time in seconds (assignment allows for 180s total) 
    max_time = 170

    T = Tstart       

    #anneal until max_time reached, or solution doesn't improve
    while (time.time() < start_time + max_time):   
    #while T > Tend:   # uncomment this line to remove time restriction
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
            
            if P_2opt_3_opt > random.random(): 
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
        T *= fCool               # The system is cooled down

        # If solution can't be further improved, stop
        if accepted == 0: break  

    print ("Params:  Tstart=%6.4f, fCool=%6.4f, maxSteps=%d, maxAccepted=%d" % 
          (Tstart, fCool, maxSteps, maxAccepted))

    return tour, dist


def write_results(filename, length, cities):
    """
    Writes TSP solution results in the proper format.

    :param filename: (str) results filename to use
    :param length: (int) length of TSP tour solution
    :param cities: list of city labels in TSP solution
    :return: writes results to disk
    """
    with open(filename, 'w') as f:
        f.write('%d\n' % (length))
        for city in cities:
            f.write('%d\n' % (city))


def plot_tour(T, cities, case):
    """ Saves a plot of a given tour of cities with name 'case' to a .png file."""
    import matplotlib.pyplot as plt
    T.append(T[0])
    x_arr, y_arr = [], []
    for city in T:
        x, y = cities[city]
        x_arr.append(x)
        y_arr.append(y)
    plt.plot(x_arr, y_arr, '.-')
    plt.savefig('plots/%s.png' % (case))
    plt.close('all')
    #plt.show()
    

if __name__=='__main__':

    # Get start time of run
    start_time = time.time()

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
    final_tour, cost = anneal(start_tour, cities, start_time)

    # write solution to output
    write_results("%s.tour" % case_name, cost, final_tour)

    # plot
    if len(sys.argv) > 2 and sys.argv[2] == '-p':
        plot_tour(start_tour, cities, "start_%s" % (case_name))
        plot_tour(final_tour, cities, "final_%s" % (case_name))
