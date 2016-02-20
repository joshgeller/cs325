#  Project 3, Problem 2
#
from scipy.optimize import linprog
import matplotlib.pyplot as plt

CALORIES = [21, 16, 40, 41, 585, 120, 164, 884]
COST = [1.00, 0.75, 0.50, 0.50, 0.45, 2.15, 0.95, 2.00] 
COMBINED = [i/150+j for i,j in zip(CALORIES, COST)]
A = [[-0.85, -1.62, -2.86, -0.93, -23.4, -16.0, -9.0, 0.0],
     [-0.33, -0.20, -0.39, -0.24, -48.7, -5.0, -2.6, -100.0],
     [0.33, 0.20, 0.39, 0.24, 48.7, 5.0, 2.6, 100.0],
     [-4.64, -2.37, -3.63, -9.58, -15.0, -3.0, -27.0, 0.0],
     [.009, .028, .065, .069, .0038, .120, .078, 0.0],
     [0.4, -0.6, -0.6, 0.4, 0.4, 0.4, 0.4, 0.4]]
b = [-15, -2, 8, -4, 0.2, 0.0]     


def print_results(res):
    print('Quantities Used (grams):') 
    print("Tomato: {:.0f}\n"
    "Lettuce: {:.0f}\n"
    "Spinach: {:.0f}\n"
    "Carrot: {:.0f}\n"
    "Sunflower Seeds: {:.0f}\n"
    "Smoked Tofu: {:.0f}\n"
    "Chickpeas: {:.0f}\n"
    "Oil: {:.0f}".format(*(res['x'])*100.0))
    return

# Part A
c = CALORIES
resA = linprog(c, A, b)
cals_A = resA['fun']
cost_A = sum(resA['x'] * COST)
print('Part A, Minimizing Calories...')
print('Total Calories = {:.0f}'.format(cals_A))
print('Total Cost: ${:.2f}'.format(cost_A))
print_results(resA)

# Part B
c = COST
resB = linprog(c, A, b)
cost_B = resB['fun']
cals_B = sum(resB['x'] * CALORIES)
print('\nPart B, Minimizing Cost...')
print('Total Calories = {:.0f}'.format(cals_B))
print('Total Cost: ${:.2f}'.format(cost_B))
print_results(resB)

# Part C
c = COST
resC = linprog(c, A, b)
cost_C = [] 
cals_C = [] 

A_partC = A[:]
b_partC = b[:]
A_partC.append(CALORIES)
b_partC.append(cals_B)
for cal_ub in range(int(cals_B), int(cals_A), -1):
    b_partC[-1] = cal_ub
    resC = linprog(c, A_partC, b_partC)
    cost_C.append(resC['fun'])
    cals_C.append(sum(resC['x'] * CALORIES))

plt.plot(cals_C, cost_C, 'bo')
plt.xlabel('Total Calories, kcals')
plt.ylabel('Total Cost, $')
plt.grid()
plt.title('Minimum Cost as Calorie Limit Varies')

c = COMBINED
resC2 = linprog(c, A, b)
cost_C2 = sum(resC2['x'] * COST)
cals_C2 = sum(resC2['x'] * CALORIES)

print('\nPart C, Minimizing Both...')
print('Total Calories = {:.0f}'.format(cals_C2))
print('Total Cost: ${:.2f}'.format(cost_C2))
print_results(resC2)
plt.show()
