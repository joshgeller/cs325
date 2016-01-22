from utils import load_problems, write_results


"""
Based on pseudocode from Glencora Borradaile's
"Designing Poly-Time Algorithms" lecture
"""


def better_enum_max_subarray(ls):
	maxSum = newSum = 0
	low = high = 0
	i = 0
	for i in range (len(ls)):
		newSum = 0
		for j in range(i, len(ls)):
			newSum = newSum + ls[j]
			if newSum > maxSum:
				maxSum = newSum
				low = i
				high = j
	return low, high, maxSum


if __name__ == '__main__':
	problems = load_problems()
    	for problem in problems
		results = better_enum_max_subarray(ls = problem)
        	write_results(
            		filename='MSS_Results.txt',
            		original_array=problem,
           	  	max_subarray=problem[results[0]:results[1] + 1],
            		max_sum=results1[2]

        )
