from stacking import *

def getTopBottom(stacking):
    dictionaryTop={} # This dictionary will be used to store the top edges for each lobe
    dictionaryBottom={} # this dictionary will be used to store the bottom edges for each lobe
    n = len(stacking.vertexList) # get the length of the vertices
    for x in range(n):

        if stacking.vertexList[x].edgeIn[0] not in dictionaryTop:
            dictionaryTop[stacking.vertexList[x].edgeIn[0]]=stacking.vertexList[x].cell
        if stacking.vertexList[x].edgeOut[0] not in dictionaryTop:
            dictionaryTop[stacking.vertexList[x].edgeOut[0]]=stacking.vertexList[x].cell
    for x in range(n-1, -1, -1):
        if stacking.vertexList[x].edgeIn[0] not in dictionaryBottom:
            dictionaryBottom[stacking.vertexList[x].edgeIn[0]]=stacking.vertexList[x].cell
        if stacking.vertexList[x].edgeOut[0] not in dictionaryBottom:
            dictionaryBottom[stacking.vertexList[x].edgeOut[0]]=stacking.vertexList[x].cell
  
    list=[dictionaryTop,dictionaryBottom]
    return list
  
def checkGoodStacking(stacking):
    list=getTopBottom(stacking) # get the top and bottom edges of the stacking for each lobe
    
    for x in stacking.complex.twoCells: # Iterate throguth the two cells
        if x.id not in [y.id for y in list[0].values()] \
            or x.id not in [y.id for y in list[1].values()]: # if the top and bottom dictionary does not contain the twocell , then it is not a good stacking
            return False
    return True
