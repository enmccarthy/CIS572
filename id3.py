#!/usr/bin/python
#
# CIS 472/572 -- Programming Homework #1
#
# Starter code provided by Daniel Lowd, 1/25/2018
#
#
import sys
import re
# Node class for the decision tree
import node
import math

train=None
varnames=None
test=None
testvarnames=None
root=None

# Helper function computes entropy of Bernoulli distribution with
# parameter p
def entropy(p):
	
	# For now, always return "0":
	#need to check is 0 or 1
	if p == 0 or p ==1:
		return 0
	ent = -p*(math.log(p, 2)) - (1-p)*(math.log((1-p), 2))
	return ent;
	
	
# Compute information gain for a particular split, given the counts
# py_pxi : number of occurences of y=1 with x_i=1 for all i=1 to n
# pxi : number of occurrences of x_i=1
# py : number of ocurrences of y=1
# total : total length of the data
def infogain(py_pxi, pxi, py, total):
	#Gain(S,a) = Entropy(S) - Sum in A of S1/S Entropy S1
	if pxi == 0:
		XYPOS = 0
	else:
		XYPOS = float(py_pxi)/pxi
	gainz = entropy(float(py)/total)
	if (total- pxi) == 0:
		XNEGYPOS = 0
	else:
		XNEGYPOS = float(py-py_pxi)/(total- pxi)
	posXGainz = (float(pxi)/total)*entropy(XYPOS)
	negXGainz = (float(total - pxi)/total)*entropy(XNEGYPOS)
	return gainz - posXGainz - negXGainz

# OTHER SUGGESTED HELPER FUNCTIONS:
# - collect counts for each variable value with each class label
# - find the best variable to split on, according to mutual information
# - partition data based on a given variable	
	
	
	
# Load data from a file
def read_data(filename):
	f = open(filename, 'r')
	p = re.compile(',')
	data = []
	header = f.readline().strip()
	varnames = p.split(header)
	namehash = {}
	for l in f:
		data.append([int(x) for x in p.split(l.strip())])
	return (data, varnames)

# Saves the model to a file.  Most of the work here is done in the
# node class.  This should work as-is with no changes needed.
def print_model(root, modelfile):
	f = open(modelfile, 'w+')
	root.write(f, 0)

# Build tree in a top-down manner, selecting splits until we hit a
# pure leaf or all splits look bad.

def count_var(data):
	count = 0
	#How many of the X's are pos
	listofVarNum = [0]*(len(data[1]))
	#XandY POS
	numPos = [0]*(len(data[1]))
	#the gain for that variable  
	for dataRow in data:
		for entry in dataRow:
			listofVarNum[count] += entry
			if entry: 
				numPos[count] += dataRow[-1]
			count += 1
		count = 0
	return zip(listofVarNum, numPos)

def count_Y(data):
	countY = 0
	for dataRow in data:
		countY += dataRow[-1]
	return countY

def build_tree(data, varnames):
	localdata = data[:]
	localVarNames = varnames[:]
	XPosYPos = count_var(localdata)
	totalPosY = count_Y(localdata)
	total = len(localdata)
	
	listofVarGain = [0]*(len(localVarNames)-1)

	ind = 0
	for (XVal, YVal) in XPosYPos:
		#super inefficient maybe change this
		
		if ind != len(XPosYPos)-1:
			listofVarGain[ind] = infogain(YVal,XVal, totalPosY, total)
			ind += 1 
	indextoremove = listofVarGain.index(max(listofVarGain))

	if max(listofVarGain) == 0:
		if YVal >= (totalPosY-YVal):
			return node.Split(localVarNames, indextoremove, node.Leaf(localVarNames, 1), node.Leaf(localVarNames, 0))
		else:
			return node.Split(localVarNames, indextoremove, node.Leaf(localVarNames, 0), node.Leaf(localVarNames, 1))
	#split data
	leftData = []
	rightData = []
	countRight = 0
	countLeft = 0
	newVarNames = localVarNames[:]
	 
	for datarow in localdata:
		if datarow[indextoremove] == 0:
			countLeft += datarow[-1]
			leftData.append(datarow)
		else:
			countRight += datarow[-1]
			rightData.append(datarow)

	if countRight == 0 and countLeft == len(leftData):
		return node.Split(localVarNames, indextoremove, node.Leaf(localVarNames, 1), node.Leaf(localVarNames, 0))
	elif countRight == len(rightData) and countLeft == 0:
		return node.Split(localVarNames, indextoremove, node.Leaf(localVarNames, 0), node.Leaf(localVarNames, 1))
	elif countRight == 0:
		return node.Split(localVarNames, indextoremove, (build_tree(leftData, newVarNames)), node.Leaf(localVarNames, 0))
	elif countRight == len(rightData):
		return node.Split(localVarNames, indextoremove, (build_tree(leftData, newVarNames)), node.Leaf(localVarNames, 1))
	elif countLeft == 0:
		return node.Split(localVarNames, indextoremove, node.Leaf(localVarNames, 0), (build_tree(rightData, newVarNames)))
	elif countLeft == len(leftData):
		return node.Split(localVarNames, indextoremove, node.Leaf(localVarNames, 1), (build_tree(rightData, newVarNames)))
	else:	
		return node.Split(localVarNames, indextoremove, (build_tree(leftData, newVarNames)), (build_tree(rightData, newVarNames)))



# "varnames" is a list of names, one for each variable
# "train" and "test" are lists of examples.
# Each example is a list of attribute values, where the last element in
# the list is the class value.
def loadAndTrain(trainS,testS,modelS):
	global train
	global varnames
	global test
	global testvarnames
	global root
	(train, varnames) = read_data(trainS)
	(test, testvarnames) = read_data(testS)
	modelfile = modelS
	
	# build_tree is the main function you'll have to implement, along with
	# any helper functions needed.  It should return the root node of the
	# decision tree.
	root = build_tree(train, varnames)
	print_model(root, modelfile)
	
def runTest():
	correct = 0
	# The position of the class label is the last element in the list.
	yi = len(test[0]) - 1
	for x in test:
		# Classification is done recursively by the node class.
		# This should work as-is.
		pred = root.classify(x)
		if pred == x[yi]:
			correct += 1
	acc = float(correct)/len(test)
	return acc	
	
	
# Load train and test data.  Learn model.  Report accuracy.
def main(argv):
	if (len(argv) != 3):
		print 'Usage: id3.py <train> <test> <model>'
		sys.exit(2)
	loadAndTrain(argv[0],argv[1],argv[2]) 
					
	acc = runTest()			 
	print "Accuracy: ",acc					  

if __name__ == "__main__":
	main(sys.argv[1:])