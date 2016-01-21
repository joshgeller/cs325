from utils import load_problems, write_results

"""
Based on pseudocode from Glencora Borradaile's
"Designing Poly-Time Algorithms" lecture
"""

def enum_max_subarray(ls):
	maxSum = newSum = 0
	low = high = 0
	i = 0
	for j in range (1, len(ls)):
		if ls[j] > (newSum + ls[j]
			newSum = ls[j]
			i = j
		else:
			newSum += ls[j]

		if newSum > maxSum:
			maxSum = newSum
			low = i
			high = j
	
	return maxSum, low, high



if __name__ == '__main__':
	problems = load_problems()
    	for problem in problems:
        	results = enum_max_subarray(ls = problem)
        	write_results(
            		filename='MSS_Results.txt',
            		original_array=problem,
           		  max_subarray=problem[results[1]:results[2] + 1],
            		max_sum=results1[0]

        )
