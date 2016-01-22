from utils import load_problems, write_results

"""
Based on pseudocode from Glencora Borradaile's
"Designing Poly-Time Algorithms" lecture
"""

def enum_max_subarray(ls):
	
	maxSum = curSum = ls[0]
	low = high = 0
	i = 0
	
	for i in range (len(ls)):
		for j in range (i, len(ls)):
			curSum = 0
			curLen = 0
			for k in range (i, j):
				curSum += ls[k]
				curLen += 1
			if curSum > maxSum:
				maxSum = curSum
				low = i
				high = (i + (curLen - 1))

	
	return low, high, maxSum



if __name__ == '__main__':
	problems = load_problems()
    	for problem in problems:
        	results = enum_max_subarray(ls = problem)
        	write_results(
            		filename='MSS_Results.txt',
            		original_array=problem,
           		  max_subarray=problem[results[0]:results[1] + 1],
            		max_sum=results1[2]

        )
