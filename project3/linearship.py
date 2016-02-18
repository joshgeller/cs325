from scipy.optimize import linprog

def linear_shipment():
    """
    p       = plant
    w       = warehouse
    r       = retailer
    s       = supply        constraint
    d       = demand        constraint
    n       = # of plans
    q       = # of warehouses
    m       = # of retailers
    (i,j)   = edge from plant to warehouse
    cp(i,j) = cost of edge from plant(i) to warehouse(j)
    (j,k)   = edge from warehouse to retailer
    cw(j,k) = cost of edge from warehouse to retailer

    # of fridges shipped from plants to warehouses

    xp1w1, xp1w2, xp2w1, xp2w2, xp3w1, xp3w2, xp3w3, xp4w2, xp4w3

    # of fridges shipped from warehouses to retailers

    xw1r1, xw1r2, xw1r3, xw1r4, xw2r3, xw2r4, xw2r5, xw2r6, xw3r4, xw3r5, xw3r6, xw3r7

    # cp is cost table with cp(1,3), cp(2,3), cp(4,1) = 0

    # cw is cost table with cw(1,5), cw(1,6), cw(1,7), cw(2,1), cw(2,2), cw(2,7), cw(3,1)
                            cw(3,2), cw(3,3) = 0


    # objective function

    cp(1,1)*xp1w1 + cp(1,2)*xp1w2 + cp(2,1)*xp2w1 + cp(2,2)*xp2w2 + cp(3,1)*xp3w1 + cp(3,2)*xp3w2 +
    cp(3,3)*xp3w3 + cp(4,2)*xp4w2 + cp(4,3)*xp3w3 + cw(1,1)*xw1r1 + cw(1,2)*xw1r2 + cw(1,3)*xw1r3 +
    cw(1,4)*xw1r4 + cw(2,3)*xw2r3 + cw(2,4)*xw2r4 + cw(2,5)*xw2r5 + cw(2,6)*xw2r6 + cw(3,4)*xw3r4 +
    cw(3,5)*xw3r5 + cw(3,6)*xw3r6 + cw(3,7)*xw3r7

    =

    10xp1w1 + 15xp1w2 + 11xp2w1 + 8xp2w2 + 13xp3w1 + 8xp3w2 + 9xp3w3 + 14xp4w2 + 8xp4w3 + 5xw1r1 +
    6xw1r2 + 7xw1r3 + 10xw1r4 + 12xw2r3 + 8xw2r4 + 10xw2r5 + 14xw2r6 + 14xw3r4 + 12xw3r5 +
    12xw3r6 + 6xw3r7

    # supply constraints

    xp1w1 + xp1w2 <= 150
    xp2w1 + xp2w2 <= 450
    xp3w1 + xp3w2 + xp3w3 <= 250
    xp4w2 + xp4w3 <= 150

    # demand constraints

    xw1r1 >= 100
    xw1r2 >= 150
    xw1r3 + xw2r3 >= 100
    xw1r4 + xw2r4 + xw3r4 >= 200
    xw2r5 + xw3r5 >= 200
    xw2r6 + xw3r6 >= 150
    xw3r7 >= 100

    # flow constraints

    xw1r1 + xw1r2 + xw1r3 + xw1r4 - xp1w1 - xp2w1 - xp3w1 <= 0
    xw2r3 + xw2r4 + xw2r5 + xw2r6 - xp1w2 - xp2w2 - xp3w2 - xp4w2 <= 0
    xw3r4 + xw3r5 + xw3r6 + xw3r7 - xp3w3 - xp4w3 <= 0

    :return:
    """

    c = [10, 15, 11, 8, 13, 8, 9, 14, 8, 5, 6, 7, 10, 12, 8, 10, 14, 14, 12, 12, 6]

    A = [
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, -1, 0, -1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, -1, 0, -1, 0, -1, 0, -1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    ]

    b = [150, 450, 250, 150, -100, -150, -100, -200, -200, -150, -100, 0, 0, 0]

    return linprog(c, A_ub=A, b_ub=b, options={'disp': True})

if __name__ == '__main__':
    print(linear_shipment())