from cwComplexes import *

def getVertices(c): #c is a complex
    ''' get the vertices on the Spine'''
    pointsOnSpine=[]
    edgeList = []    

    count=-1 # count to label the vertices(create a number for the vertices)
    for x in c.twoCells: # Go throught the two cells
        pointsInX = []
        edgesInX = []
        l = len(x.list)        

        for y in range(0,l):
            count += 1
            point = SpineVertex(count, x)
            edge = Edge(count, point, x.list[y%l][0], x.list[y%l][1], x) #missing destVertex 
            
            pointsInX.append(point) # add the vertices on the points on the spine
            edgesInX.append(edge)
    
        for i in range(0,l):
            pointsInX[i].vertexIn = pointsInX[(i-1)%l]
            pointsInX[i].vertexOut = pointsInX[(i+1)%l]
            
            pointsInX[i].edgeIn = edgesInX[(i-1)%l]
            pointsInX[i].edgeOut = edgesInX[i%l]
            
            edgesInX[i].destVertex = pointsInX[(i+1)%l]
            
        pointsOnSpine += pointsInX
        edgeList += edgesInX

    
    c.vertexList = pointsOnSpine
    c.edgeList = edgeList

    return (pointsOnSpine, edgeList)

def getEdges(vertexList): #c is a complex
    """ Get the edge list using a vertex list"""

    edgeList = []

    for v in vertexList:
        edge = Edge(v, v.vertexOut, v.edgeOut[0], v.edgeOut[1], \
            v.cell, v.count)

        edgeList.append(edge)

    return edgeList

class SpineVertex:
    def __init__(self, count, cell, \
        edgeIn = None, edgeOut = None, vertexIn = None, vertexOut = None):
        
        self.count = count
        self.edgeIn = edgeIn
        self.edgeOut = edgeOut
        self.cell = cell
        self.vertexIn = vertexIn
        self.vertexOut = vertexOut

    def __eq__(self, other):
        return (self.count == other.count)

    def __hash__(self):
        return self.count

    def __repr__(self):
        return "V-" + str(self.count) 

class Edge:
    def __init__(self, count, initVertex, generator, inverse,
        cell, destVertex = None):

        self.initVertex = initVertex
        self.destVertex = destVertex
        self.generator = generator
        self.inverse = inverse
        self.cell = cell
        self.count = count

    def __eq__(self, other):
        return (self.count == other.count)

    def __hash__(self):
        return self.count

    def __repr__(self):
        return "E-" + str(self.count) + ": " + self.generator.__repr__() + \
            ("'" if self.inverse else "")
