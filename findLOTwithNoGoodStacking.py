from cwComplexes import *
from getVertices import *
from presComplexBuilder import *
from newEmbeddingCheck import *
from stacking import *
from newGoodStackingCheck import *

from backtracking import *
from generateLOTPresentation import *

counter = 2100
for n in range(1):
	LOT=genAllLabelledOrientedTrees(n+5)
	size=len(LOT)
	noGoodStacking=list()
	i=1
	for x in range(2100, 2200):
		c=prescomplex_builder(LOT[x])
		listOfVertices, listOfEdges = getVertices(c)
		b = backtrackFinder(c)
		print(LOT[x], b, str(counter) + " out of " + str(size))
		counter += 1
		if b is None:
				noGoodStacking.append(x)
	print(noGoodStacking, len(noGoodStacking), " out of ", size)
