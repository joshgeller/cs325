CS352 Group 2 Project 1
Tim Thomas <thomasti@oregonstate.edu>
Kimberly McLeod <mcleodki@oregonstate.edu>
Josh Geller <gellerj@oregonstate.edu>

******************************************

To compile and execute the main program, run the following command:

python3 proj1_main.py

This will run all four algorithms against MSS_Problems.txt and output the
results to MSS_Results.txt.

******************************************

The Python file proj1_analysis.py is also provided.  This script does the
experimental analysis portion of the project.  It generates 10 random problems
for various values of n and outputs the mean run times for each of the
algorithms.  Execute with the following command:

python3 proj1_analysis.py

This script can also calculate the curve fit using regression techniques and
produce the required plots.  To activate this option supply the
optional command line argument --analyze, like this:

python3 proj1_analysis.py --analyze

NOTE: python libraries numpy and matplotlib are required for this option to run
correctly.