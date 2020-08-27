from cwComplexes import *
from getVertices import *
from presComplexBuilder import *
from newEmbeddingCheck import *
from stacking import *
from newGoodStackingCheck import *

str = "a,b,c | a b c, a c b"
complex = prescomplex_builder(str)
listOfVertices, listOfEdges = getVertices(complex)
#stack = Stacking(complex, listOfVertices)
#print(getTopBottom(stack))
#print(embeddingCheck(stack))

'''
This function takes a complex(complexs) and a list of vertices(l)
and perform check stakings  and checkgood stacking
on all permutation of the vertices.
'''
def checkStackingsForAllPermutation(complexs,l,prev=[],goodStackings=[], Stackingss=[]): 
    if len(l)==1:
        aStacking=Stacking(complexs,prev+l) # create a stacking to perform check Good stacking and check stacking on it
        if embeddingCheck(aStacking, listOfEdges): # check if it is a stacking
            Stackingss.append(prev+l) # If the permutatation gives a stacking then we append it the the list of good stacking

            if checkGoodStacking(aStacking.complex, aStacking.vertexList): # check if it is a good stacking
                goodStackings.append(prev+l)
    else:   
        for i in range(0,len(l)):    
            checkStackingsForAllPermutation(complexs,l[:i]+l[i+1:],prev+[l[i]], goodStackings, Stackingss)
    return (goodStackings, Stackingss)

(a,b)=checkStackingsForAllPermutation(complex,listOfVertices)

idArray = [[v.count for v in x ]for x in a]

print(idArray)
print([[v.count for v in x] for x in b])
