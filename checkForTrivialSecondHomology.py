from cwComplexes import *
from scipy.linalg import det
"""
A Fucntion that returns true if the second Homology of a compelx is trivial
"""
#independent implies trivial 2nd homology

def isTrivialSecondHomology(complex):
    twoCellVectors=[] # use to store the vectors representing each two cell
    for x in range(len(complex.twoCells)): # iterate throught the two cells and create vectors for each of them
        tempDictionary={} # temporary dictionary to store the number of generators in a 2cell
        #populate the dictionary with trivial values
        for y in range(len(complex.oneCells)):
            tempDictionary[complex.oneCells[y]]=0
        for m in range(len(complex.twoCells[x].list)): # iterate throught the one cells of the two cell
            if complex.twoCells[x].list[m][1] is False:
                tempDictionary[complex.twoCells[x].list[m][0]]=tempDictionary[complex.twoCells[x].list[m][0]]+1
            else:
                tempDictionary[complex.twoCells[x].list[m][0]]=tempDictionary[complex.twoCells[x].list[m][0]]-1
        twoCellVectors.append(tempDictionary)
        twoCellVectorsL=[]
        for z in range(len(twoCellVectors)):
            twoCellVectorsL.append(list(twoCellVectors[z].values()))
    if len(twoCellVectorsL) is 0:
        return True
    if len(twoCellVectorsL) is len(twoCellVectorsL[0]):
        val=det(twoCellVectorsL)
        if val is 0:
            return False
        else:    
            return True
    else:
        return False    

     
    
