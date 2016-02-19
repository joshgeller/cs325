#  Project 3
#  #2, Part A
#
from scipy.optimize import linprog


CALORIES = [21, 16, 40, 41, 585, 120, 164, 884]
COST = [1.00, 0.75, 0.50, 0.50, 0.45, 2.15, 0.95, 2.00] 
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

c = CALORIES
resA = linprog(c, A, b)

c = COST
resB = linprog(c, A, b)

print('Part A, Minimizing Calories...')
print('Total Calories = {:.0f}'.format(resA['fun']))
print('Total Cost: ${:.2f}'.format(sum(resA['x'] * COST)))
print_results(resA)
print('\nPart B, Minimizing Cost...')
print('Total Calories = {:.0f}'.format(sum(resB['x'] * CALORIES)))
print('Total Cost: ${:.2f}'.format(resB['fun']))
print_results(resB)
