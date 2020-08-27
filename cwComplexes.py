class ZeroCell:
    def __init__(self, l):
        self.name=l    
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()   

#------------------------------------------------------------------------------------------------
        
class OneCell:
    def __init__(self, i,f,m):
        self.letter=m # We store one cell as a ordered tuple of zero cells. 
        self.initZeroCell= i
        self.finZeroCell= f
    def __str__(self):
        return self.letter
    def __repr__(self):
        return self.__str__()  

#------------------------------------------------------------------------------------------------
 
class TwoCell:
    def __init__(self, l, count):
        self.list=l # We store a two cells as an ordered list of 2-tuple ( once-cell, orientation) 
        self.count = count #unique identifier integer
    def getList(self):
        return self.list
    def __str__(self):
        s = ""
        for o in self.list:
            s += (o[0].__str__() + "' ") if o[1] else  (o[0].__str__() + " ") # adds apostrophe if inverse
        return s.strip()
    def __hash__(self):
        return self.count
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return (self.count == other.count)
    def __lt__(self, other):
        return (self.count < other.count)

#------------------------------------------------------------------------------------------------
 
class Complexes:
    def __init__(self,z,o,t):
        self.zeroCells=z
        self.oneCells=o
        self.twoCells=t
        self.vertexList=None
        self.edgeList=None

    def cornerCount(self):
        count = 0
        for k in range(len(self.twoCells)):
            for i in range(len(self.twoCells[k].list)):
                count += 1
        return count

#------------------------------------------------------------------------------------------------

    def buildCorners(self):
        corners = []
        for k in range(len(self.twoCells)):
            superList = self.twoCells[k].getList()
            length = len(superList)
            lister = []
            lister.append(k)
            for i in range(length):
                part1 = superList[i%length]
                part2 = superList[(i-1)%length]
                if part1[1] == False:
                    tuple1 = (part1[0], "out")
                else:
                    tuple1 = (part1[0], "in")
                if part2[1] == False:
                    tuple2 = (part2[0], "in")
                else:
                    tuple2 = (part2[0], "out")
                fucktuple = (tuple1, tuple2)
                lister.append(fucktuple)
            corners.append(list(lister))
        return corners

#------------------------------------------------------------------------------------------------

    def getCornList(self):
        cornList = []
        k = self.cornerCount()
        for i in range(k):
            cornList.append(i)
        return cornList

#------------------------------------------------------------------------------------------------

    def getEdges(self):
        edgeList = []
        counter = 0
        for twoC in self.twoCells:
            ultraList = twoC.getList()
            length = len(ultraList)
            temp = []
            for j in range(length):
                if ultraList[j][1] == False:
                    edge = ((ultraList[j][0]), ((j%length)+counter), ((j+1)%length+counter))
                else:
                    edge = ((ultraList[j][0]), ((j+1)%length+counter), ((j%length)+counter))
                temp.append(edge)
            counter += length
            edgeList.append(temp)

        lobeList = []
        for oneCell in self.oneCells:
            oneCellList = []
            for relator in edgeList:
                for edge in relator:
                    if edge[0] == oneCell:
                        oneCellList.append(edge)
            if oneCellList != []:
                lobeList.append(oneCellList)



        return edgeList, lobeList

#------------------------------------------------------------------------------------------------

    def edgeMatrix(self):
        corners = self.getCornList()
        lobeDic = {}
        #for i in self.twoCells:
            




#------------------------------------------------------------------------------------------------
    def __str__(self):
        s = ""
        for z in self.zeroCells:
            s += z.__str__()
        s += (",") if (s != "") else ""
        for o in self.oneCells:
            s += o.__str__()
        s += "|"
        for t in self.twoCells:
            s += t.__str__() + ","
        return s.strip(" ,")
    def __repr__(self):
        return self.__str__()        
