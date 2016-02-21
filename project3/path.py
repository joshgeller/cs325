from scipy.optimize import linprog

#      a  b  c  d  e  f  g  h  i  j  k  l  m
c =  [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]         #partA-C objective
c_no_l_m =  [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 0, 0]  #partD objective
A = [[-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # constraint matrix
     [-1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [-1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [-1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [ 1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [ 0,-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [ 0,-1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
     [ 0,-1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
     [ 0, 0,-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [ 0, 1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [ 0, 0,-1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [ 0, 0,-1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
     [ 0, 0,-1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
     [ 1, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [ 0, 0, 0,-1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [ 0, 0, 0,-1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
     [ 0, 0, 0,-1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
     [ 0, 0, 0, 0,-1, 0, 0, 1, 0, 0, 0, 0, 0],
     [ 0, 0, 1, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0],
     [ 0, 0, 0, 0,-1, 0, 0, 0, 1, 0, 0, 0, 0],
     [ 0, 0, 0, 0, 0,-1, 0, 0, 1, 0, 0, 0, 0],
     [ 0, 0, 0, 0, 0,-1, 1, 0, 0, 0, 0, 0, 0],
     [ 0, 0, 0, 1, 0, 0,-1, 0, 0, 0, 0, 0, 0],
     [ 0, 0, 0, 0, 0, 0,-1, 0, 0, 1, 0, 0, 0],
     [ 0, 0, 0, 0, 0, 0,-1, 0, 0, 0, 1, 0, 0],
     [ 0, 0, 0, 0, 0, 0, 0,-1, 1, 0, 0, 0, 0],
     [ 0, 0, 0, 0, 0, 0, 0,-1, 0, 0, 1, 0, 0],
     [ 1, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0, 0],
     [ 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 1, 0, 0],
     [ 0, 0, 0, 0, 0, 0, 0, 0,-1, 1, 0, 0, 0],
     [ 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0, 1],
     [ 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 0],
     [ 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 1, 0, 0],
     [ 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 1, 0],
     [ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,-1, 0, 0],
     [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 1],
     [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 1]]

A_reversed = [[-1*i for i in j] for j in A]         # parts C and D 

A_eq_a = [[ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]  # start node, part A
A_eq_m = [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]  # start node, part C
A_eq_i = [[ 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]  # start node, part D

b = [2, 3, 8, 9, 4, 5, 7, 4, 10, 5,     # RHS of inequality constraints
     9, 11, 4, 8, 2, 5, 1, 5, 4, 10, 
     2, 2, 2, 8, 12, 5, 10, 20, 6, 2, 
     12, 2, 4, 5, 10, 10, 2]

b_eq = [0]    # RHS of equality constraint

nodes='abcdefghijklm'

def print_header():
    '''Just prints output column headings.'''
    print('     ', end='')
    for n in nodes:
        print('{:5}'.format(n), end='')
    print('')
    return

# calculations
result_partA = linprog(c, A, b, A_eq_a, b_eq)
result_partC = linprog(c, A_reversed, b, A_eq_m, b_eq)
result_partD_to_i = linprog(c_no_l_m, A_reversed, b, A_eq_i, b_eq) 
result_partD_from_i = linprog(c, A, b, A_eq_i, b_eq) 

# output
print("\nPART A: Shortest path from a to all nodes")
print_header()
print(' ', end='')
for i, n in enumerate(nodes):
    print('{:5.0f}'.format(result_partA['x'][i]), end='')
print('')

print("\nPART C: Shortest path from all nodes to m")
print_header()
print(' ', end='')
for i, n in enumerate(nodes):
    print('{:5.0f}'.format(result_partC['x'][i]), end='')
print('')

x_to_i = result_partD_to_i['x']
i_to_y = result_partD_from_i['x']
print("\nPART D: Shortest path from x to y thru i")
print_header()
for x, n in enumerate(nodes):
    print('{}'.format(n), end='')
    for y in range(len(nodes)):
        if n in 'lm':
            print('  inf', end='')
        else:
            x_i_y = x_to_i[x] + i_to_y[y]
            print('{:>5.0f}'.format(x_i_y), end='')
    print('\n')
