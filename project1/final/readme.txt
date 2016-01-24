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

The Python file proj1_timing.py is also provided.This script generates 10
random problems of size n and then calculates the mean run time for each of
the algorithms. Execute by running the following command:

python3 proj1_timing.py

******************************************

The experimental analysis script is also provided. This script can calculate the
curve fit using regression techniques and produce the required plots. Execute
by running the following command: (NOTE: numpy and matplotlib libraries required!)

python3 proj1_analysis.py --analyze
