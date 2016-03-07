import time
from libc.math cimport sqrt

def two_opt_swap(list T, int  i, int k):
    return T[:i] + T[k:i-1:-1] + T[k+1:]


def get_distance(int x1, int y1, int x2, int y2):
    """Returns distance between points 1 and 2."""
    cdef int dx, dy
    dx = x1 - x2
    dy = y1 - y2
    return int(round(sqrt(dx*dx + dy*dy)))


def get_tour_cost(list tour, dict cities):
    cdef int cost, x1, x2, y1, y2
    cost = 0
    prev = tour[0]
    for v in tour[1:]:
        x1, y1 = cities[prev]
        x2, y2 = cities[v]
        cost += get_distance(x1, y1, x2, y2)
        prev = v
    return cost 


def somefunc(list T, long T_cost, dict cities):
    cdef int i, k
    cdef long Tp_cost
    cdef list Tp
    improved = False
    t = time.time()
    for i in range(1, len(T[1:-1])): 
        if time.time() > (t + 60):
            t = time.time()
            tstr = time.strftime('%X %x %Z')
            print("Best so far: {:,d} @ {}".format(T_cost, tstr)) 
        for k in range(i+1, len(T[1:-1]) + 1):
            Tp = two_opt_swap(T, i, k) 
            Tp_cost = get_tour_cost(Tp, cities)
            if Tp_cost < T_cost:
                T = Tp
                T_cost = Tp_cost
                improved = True
                break
    return T, T_cost, improved
