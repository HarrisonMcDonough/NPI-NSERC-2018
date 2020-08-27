from __future__ import print_function
from cwComplexes import *
from getVertices import *
from presComplexBuilder import *
from newEmbeddingCheck import *
from stacking import *
from newGoodStackingCheck import *
from presentationHomeomorphism import *
from backtracking import *
from generatePresentations import*
from checkForTrivialSecondHomology import *
import csv

alphabet=['a','b']
listOfPresStrings=makePresStringUpToM(1,2,2)
checked=[]

with open("output.tsv", "w") as f:
    print("%s\t\t%s\t\t%s\t\t%s" % ("Presentation String"," Homeomorphic Class", "Trivial Second Homology", "Good Stacking"), file=f)
    for a in listOfPresStrings:
        alreadyExist=None
        
        for b in checked:
            if areHomeomorphic(a,b):
                alreadyExist= True
                print("%s\t\t%s\t\t%s\t\t%s" % (a, b, "Refer to homeomorphic class","Refer to homeomorphic class"), file=f)
                break
        if not alreadyExist:
            checked.append(a)
            c=prescomplex_builder(a)
            listOfVertices, listOfEdges = getVertices(c)
            trivial=isTrivialSecondHomology(c)
            b = backtrackFinder(c)
            print("%s\t\t%s\t\t%s\t\t%s" % (a, "Homeomorphic to None before", str(trivial),b), file=f)
        
