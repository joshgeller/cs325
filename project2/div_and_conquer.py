#!/usr/bin/env python
import sys

def changeslow(valueList, change, outFile):
	minCoins = change
	myList = []
	if change in valueList:
		  return 1

	else:
		for i in [c for c in valueList if c <= change]:
			  numCoins = 1 + changeslow(valueList, change - i, outFile)
			  if numCoins < minCoins:
			  	  minCoins = numCoins
				    myList[i] = c

	outFile.write('Hello!\n')
	outFile.write(myList)
	print("Hello\n")
	for i in myList:   #trying to see if myList has anything in it, nothing printed
		  print(i)
	print(minCoins)
	outFile.write(minCoins)
	return 1


inName = sys.argv[1]
splitName = inName.split('.', 2)
newName = splitName[0]
inputFile = open(sys.argv[1])
inputFile.readlines()
outputFile = open(newName + "change.txt", 'w+')
i = 0
while i in inputFile:
	  print("i 1", i)
	  changeslow(i, i + 1, outputFile)
	  i + 2
	  print("i 2", i)
#print(changeslow(List, Change)) 
print("Hello!\n")

inputFile.close()
outputFile.close()
