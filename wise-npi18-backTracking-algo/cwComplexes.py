class ZeroCell:
    def __init__(self, l):
        self.name=l
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()        
        
class OneCell:
    def __init__(self, i,f,m):
        self.initZeroCell=i
        self.finZeroCell=f
        self.letter=m # We store one cell as a ordered tuple of zero cells. 

    def __str__(self):
        return self.letter

    def __repr__(self):
        return self.__str__()        
 
class TwoCell:
    def __init__(self, l, count):
        self.list=l # We store a two cells as an ordered list of 2-tuple ( once-cell, orientation) 
        self.count = count #unique identifier integer
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
 
class Complexes:
    def __init__(self,z,o,t):
        self.zeroCells=z
        self.oneCells=o
        self.twoCells=t
        self.vertexList=None
        self.edgeList=None

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
