from theSuperTester import *
from cwComplexes import *
import math
import itertools
import time


# for i in itertools.permutations([1,2,3]):
# 	print(i)


str = "a, b, c, d | a c b' c', b a c' a', a b d' b'"

pres = presComplexBuilder(str)

#print(pres.twoCells[0].getList())
#print(pres.cornerCount())
pres.buildCorners()

edgeList, eggList = pres.getEdges()
#print(edgeList)

#ordering = [4, 3, 0, 7, 5, 1, 6, 2]
#ordering = [4, 3, 0, 7, 1, 6, 5, 2]

# heightDict = {}
# for i in range(len(ordering)):
# 	heightDict[ordering[i]] = i    

#------------------------------------------------------------------------------------------------------

def crossCheckerXtreme(edge1, edge2, heightDict):
	#Nested
	if (((heightDict[edge1[1]] < heightDict[edge2[2]]) and heightDict[edge1[2]] < heightDict[edge2[2]]) and (heightDict[edge1[1]] > heightDict[edge2[1]] and heightDict[edge1[2]] > heightDict[edge2[1]])):
		return True
	if (((heightDict[edge2[1]] < heightDict[edge1[2]]) and heightDict[edge2[2]] < heightDict[edge1[2]]) and (heightDict[edge2[1]] > heightDict[edge1[1]] and heightDict[edge2[2]] > heightDict[edge1[1]])):
		return True
	if (((heightDict[edge2[1]] < heightDict[edge1[1]]) and heightDict[edge2[2]] < heightDict[edge1[1]]) and (heightDict[edge2[1]] > heightDict[edge1[2]] and heightDict[edge2[2]] > heightDict[edge1[2]])):
		return True
	if (((heightDict[edge1[1]] < heightDict[edge2[1]]) and heightDict[edge1[2]] < heightDict[edge2[1]]) and (heightDict[edge1[1]] > heightDict[edge2[2]] and heightDict[edge1[2]] > heightDict[edge2[2]])):
		return True		

	#Crossing
	if (((heightDict[edge1[2]] > heightDict[edge2[1]]) and (heightDict[edge1[2]] > heightDict[edge2[2]])) and (heightDict[edge2[1]] > heightDict[edge1[1]] > heightDict[edge2[2]])):
		return True
	if (((heightDict[edge1[1]] > heightDict[edge2[1]]) and (heightDict[edge1[1]] > heightDict[edge2[2]])) and (heightDict[edge2[2]] > heightDict[edge1[2]] > heightDict[edge2[1]])):
		return True
	if (((heightDict[edge2[1]] > heightDict[edge1[1]]) and (heightDict[edge2[1]] > heightDict[edge1[2]])) and (heightDict[edge1[2]] > heightDict[edge2[2]] > heightDict[edge1[1]])):
		return True
	if (((heightDict[edge2[2]] > heightDict[edge1[1]]) and (heightDict[edge2[2]] > heightDict[edge1[2]])) and (heightDict[edge1[1]] > heightDict[edge2[1]] > heightDict[edge1[2]])):
		return True

	return False

#------------------------------------------------------------------------------------------------------

def stacker3000(lobeList, ordering, heightDict):
	for lobe in lobeList:
		for i in range(len(lobe)):
			edge1 = lobe[i]
			for j in range(len(lobe)):
				if (j>i):
					edge2 = lobe[j]
					boole = crossCheckerXtreme(edge1, edge2, heightDict)
					if boole == True:
						#print(edge1, edge2)
						return False
	return True

#------------------------------------------------------------------------------------------------------

#print(stacker3000(eggList, ordering, heightDict))

#------------------------------------------------------------------------------------------------------

def goodnessChecker(relatorList, lobeList, heightDict, ordering):
	goodList = []
	for lobe in lobeList:
		temp = []
		for i in range(len(lobe)):
			edge = lobe[i]
			if (i == 0):
				top = edge
				bottom = edge
			else:
				if (((heightDict[edge[1]] > heightDict[top[1]]) and (heightDict[edge[1]] > heightDict[top[2]])) or ((heightDict[edge[2]] > heightDict[top[1]]) and (heightDict[edge[2]] > heightDict[top[2]]))):
					top = edge
				if (((heightDict[edge[1]] < heightDict[bottom[1]]) and (heightDict[edge[1]] < heightDict[bottom[2]])) or ((heightDict[edge[2]] < heightDict[bottom[1]]) and (heightDict[edge[2]] < heightDict[bottom[2]]))):
					bottom = edge
		temp.append(top)
		temp.append(bottom)
		goodList.append(temp)

	booler = False				#Just to initialize
	counter = 0
	for relator in relatorList:
		bottom = False
		top = False
		for lobe in goodList:
			if lobe[0] in relator:
				bottom = True
			if lobe[1] in relator:
				top = True
		if (bottom and top):
					counter += 1
	if counter == len(relatorList):
		return True
	else:
		return False

#------------------------------------------------------------------------------------------------------

#print(goodnessChecker(edgeList, eggList, heightDict, ordering))

#------------------------------------------------------------------------------------------------------
#Itertools Test

k = 0

# start = time.time()

# for i in itertools.permutations([0,1,2,3,4,5,6,7,8,9]):
# 	k += 1

# end = time.time()
# print(k, (end - start))

#------------------------------------------------------------------------------------------------------

def goodStackingCheck(presComplex):			#The ultimate method to see if a presentation complex has a GS
	relatorList, lobeList = presComplex.getEdges()
	# length = presComplex.cornerCount
	# print(length)
	# lister = []
	# for i in range(length):
	# 	lister.append[i]
	lister = pres.getCornList()
	boole = False
	for ordering in itertools.permutations(lister):
		heightDict = {}
		for k in range(len(lister)):
			heightDict[ordering[k]] = k
		stack = stacker3000(lobeList, ordering, heightDict)
		good  = goodnessChecker(relatorList, lobeList, heightDict, ordering)
		if (stack and good):
			return "Success!", ordering
	if boole == False:
		return "FAILURE"

#------------------------------------------------------------------------------------------------------

# begin = time.time()
# print(goodStackingCheck(pres))
# end = time.time()
# print((end - begin))

#------------------------------------------------------------------------------------------------------



def allGoodChecker(presComplex):			#The ultimate method to see if a presentation complex has a GS
	relatorList, lobeList = presComplex.getEdges()
	stackingList = []
	# length = presComplex.cornerCount
	# print(length)
	# lister = []
	# for i in range(length):
	# 	lister.append[i]
	lister = pres.getCornList()
	boole = False
	for ordering in itertools.permutations(lister):
		heightDict = {}
		for k in range(len(lister)):
			heightDict[ordering[k]] = k
		stack = stacker3000(lobeList, ordering, heightDict)
		good  = goodnessChecker(relatorList, lobeList, heightDict, ordering)
		if (stack and good):
			stackingList.append(ordering)
	return stackingList


#------------------------------------------------------------------------------------------------------

start = time.time()
print(len(allGoodChecker(pres)))
end = time.time()

print((end - start))

#------------------------------------------------------------------------------------------------------

# Tester 

# edgeList, lobeList = pres.getEdges()
# def checkGoodStacking(edgeList, lobeList, ordering):
# 	heightDict = {}
# 	for i in range(len(ordering)):
# 		heightDict[i] = ordering[i]



#------------------------------------------------------------------------------------------------------

#print(pres.buildCorners())
#print(pres.twoCells[0].getList())