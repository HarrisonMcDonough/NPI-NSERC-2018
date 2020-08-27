class Stacking:
    def __init__(self, complex, vertex_list, augVertexList = None):
        self.complex = complex #original complex
        self.vertexList = vertex_list #ordered list of SpineVertices
        self.augVertexList = augVertexList #list of vertices augmented with
        #directional info on neighbors (type StackingVertex)

    def __repr__(self):
        return str(self.vertexList)

    def copy(self):

        newVertexList = list(self.vertexList)
        if self.augVertexList is not None:
            newAugVertexList = {gen : [v.copy() for v in self.augVertexList[gen]] \
                for gen in self.augVertexList.keys()}
        else:
            newAugVertexList = None

        return Stacking(self.complex, newVertexList, newAugVertexList)






    def augVertexListHelper(self, edgesConsidered):
        """ Constructs augVertexList if requested.
            Needs a list of the edges under consideration,
            i.e. list of edges added so far.
        """
        vertexLists = {key : [] for key in self.complex.oneCells} # return a list of the vertices with more information about them

        stackingVertexDict = {generator : \
            {vertex: StackingVertex(vertex, [], [], [], []) for vertex in self.vertexList} \
            for generator in self.complex.oneCells}
      

        ordering = {}
        for i in range(0, len(self.vertexList)):
            v = self.vertexList[i]
            ordering[v] = i
        for e in edgesConsidered:
            if not e.inverse:
                if ordering[e.initVertex] < ordering[e.destVertex]:
                    stackingVertexDict[e.generator][e.initVertex].higherOutgoing.append(e.destVertex)
                    stackingVertexDict[e.generator][e.destVertex].lowerIncoming.append(e.initVertex)
                else:
                    stackingVertexDict[e.generator][e.initVertex].lowerOutgoing.append(e.destVertex)
                    stackingVertexDict[e.generator][e.destVertex].higherIncoming.append(e.initVertex)
            
            else:
                if ordering[e.initVertex] < ordering[e.destVertex]:
                    stackingVertexDict[e.generator][e.initVertex].higherIncoming.append(e.destVertex)
                    stackingVertexDict[e.generator][e.destVertex].lowerOutgoing.append(e.initVertex)
                else:
                    stackingVertexDict[e.generator][e.initVertex].lowerIncoming.append(e.destVertex)
                    stackingVertexDict[e.generator][e.destVertex].higherOutgoing.append(e.initVertex)

        for i in range(0, len(self.vertexList)):
            for key in vertexLists.keys():
                vertexLists[key].append(stackingVertexDict[key][self.vertexList[i]])
        
        self.augVertexList = vertexLists

    def insertVertex(self, index, v):
        """ Inserts a new vertex into the Stacking.
        index : integer index of the insertion into self.vertexList
        v : vertex to be inserted (of type SpineVertex as defined in getVertices)
        """
        self.vertexList.insert(index, v)
       
        if self.augVertexList is None:
            self.augVertexList = {generator: \
                [StackingVertex(vertex, [], [], [], []) for vertex in self.vertexList]\
                for generator in self.complex.oneCells}
          
        else:
            for generator in self.augVertexList.keys():
                self.augVertexList[generator].insert( \
                    index, StackingVertex(v, [], [], [], []))

    def addEdge(self, e):
        gen = e.generator
        
        if self.augVertexList is None:
            self.augVertexList = {generator:  \
                [StackingVertex(vertex, [], [], [], []) for vertex in self.vertexList] \
                for generator in self.complex.oneCells}
                   
                            

        initIndex = [v.v for v in self.augVertexList[gen]].index(e.initVertex)
        destIndex = [v.v for v in self.augVertexList[gen]].index(e.destVertex)

        
        initStackingVertex = self.augVertexList[gen][initIndex]
        destStackingVertex = self.augVertexList[gen][destIndex]

        if not e.inverse:
            if self.vertexList.index(e.initVertex) < self.vertexList.index(e.destVertex):
                initStackingVertex.higherOutgoing.append(e.destVertex)
                destStackingVertex.lowerIncoming.append(e.initVertex)
            else:
                initStackingVertex.lowerOutgoing.append(e.destVertex)
                destStackingVertex.higherIncoming.append(e.initVertex)
        
        else:    
            if self.vertexList.index(e.initVertex) < self.vertexList.index(e.destVertex):
                initStackingVertex.higherIncoming.append(e.destVertex)
                destStackingVertex.lowerOutgoing.append(e.initVertex)
            else:
                initStackingVertex.lowerIncoming.append(e.destVertex)
                destStackingVertex.higherOutgoing.append(e.initVertex)
    


    def plot(self):
        import matplotlib as mpl
        from mpl_toolkits.mplot3d import Axes3D
        import numpy
        import matplotlib.pyplot as pyplot

        figure = pyplot.figure()
        axes = figure.gca(projection='3d', proj_type='ortho')

        generatorStretch = len(self.complex.oneCells)
        
        samples = 20

        colors = ['b', 'g', 'r', 'c', 'm', 'y']
        cells = list(self.complex.twoCells)
        cellColor = {cells[i] : colors[i % len(colors)] \
			for i in range(len(cells)) }

        lobePoints = {self.complex.oneCells[i] : \
            numpy.linspace(i * 2 * numpy.pi / generatorStretch,\
            (i + 1) * 2 * numpy.pi / generatorStretch, samples) \
            for i in range(generatorStretch)}

        lobe = {}

        for gen in self.complex.oneCells:
            x = numpy.absolute(numpy.sin(generatorStretch*lobePoints[gen]/2)) *\
                numpy.cos(lobePoints[gen])
            
            y = numpy.absolute(numpy.sin(generatorStretch*lobePoints[gen]/2)) *\
                numpy.sin(lobePoints[gen])            
            
            lobe[gen] = (x,y)

        for e in self.complex.edgeList:
            if e.inverse:
                v_1 = e.destVertex
                v_2 = e.initVertex

            else:
                v_1 = e.initVertex
                v_2 = e.destVertex

            # e goes from v_1 to v_2, taking inverses into account
            initHeight = self.vertexList.index(v_1)
            destHeight = self.vertexList.index(v_2)            

            edgeLobe = lobePoints[e.generator]

            line, = axes.plot(lobe[e.generator][0], lobe[e.generator][1], \
                numpy.linspace(initHeight, destHeight, samples))                

            line.set_color(cellColor[e.cell])
            
        for l in lobe:
            line, = axes.plot(lobe[l][0], lobe[l][1], numpy.linspace(-1,-1,samples), \
                label = l.__repr__())
            line.set_color('k') #black
            
        for l in lobe:
            line, = axes.plot(lobe[l][0], lobe[l][1], \
                numpy.linspace(len(self.complex.vertexList),len(self.complex.vertexList), samples), \
                label = l.__repr__())
            line.set_color('k') #black
            
        
            
        #axes.legend()
        pyplot.show()
                  
class StackingVertex: #helper class
    """
        Helper class containing a Vertex object along with augmented info
        about the neighbors. This information is needed for embeddingCheck.
    """
    def __init__(self, v, higherOutgoing = [], higherIncoming = [], lowerOutgoing = [], lowerIncoming = []):
        self.v = v

        self.higherOutgoing = higherOutgoing
        self.higherIncoming = higherIncoming
        self.lowerOutgoing = lowerOutgoing
        self.lowerIncoming = lowerIncoming

    def __repr__(self):
        return "v: " + self.v.__repr__() \
            + ", ho: " + str(self.higherOutgoing) \
            + ", hi: " + str(self.higherIncoming) \
            + ", lo: " + str(self.lowerOutgoing) \
            + ", li: " + str(self.lowerIncoming)     

                initStackingVertex.lowerOutgoing.append(e.destVertex)
                destStackingVertex.higherIncoming.append(e.initVertex)
        
<<<<<<< HEAD
        else:    
            if self.vertexList.index(e.initVertex) < self.vertexList.index(e.destVertex):
                initStackingVertex.higherIncoming.append(e.destVertex)
                destStackingVertex.lowerOutgoing.append(e.initVertex)
            else:
                initStackingVertex.lowerIncoming.append(e.destVertex)
                destStackingVertex.higherOutgoing.append(e.initVertex)
=======

        
>>>>>>> 7473d7db20fcdd6c35b94526e2693ff407007c48
