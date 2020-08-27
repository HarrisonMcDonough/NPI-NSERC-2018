from cwComplexes import *
import random

def getRandomPermutation(prev, listOfVertices):
	if len(listOfVertices) is 1:
		print(prev+listOfVertices)
	else:
		numberOfVertices= len(listOfVertices)
		randomN=random.randint(0,numberOfVertices-1)
		prev.append(listOfVertices[randomN])
		getRandomPermutation(prev,listOfVertices[:randomN]+listOfVertices[randomN+1:])
    
    
    
    
