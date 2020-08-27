from cwComplexes import *
from enum import Enum
from collections import deque

def embeddingCheck(stacking):
    
    for g in stacking.complex.oneCells:
        if not embeddingLobeCheck(stacking, g):
            return False

    return True

def embeddingLobeCheck(stacking, generator):
    """A helper method for embeddingCheck, checks if the embedding works
        for a specific lobe give by <generator>.

        This is a queue-based algorithm to detect crossings. Please
        see doc/embeddingCheck.pdf (or tex) for more details.
    """


    vertexList = vertexListHelper(stacking, generator)

    q = deque()
    q_direction = Dir.IN #dummy value

    for v in vertexList:
      
        if not q: #if the queue is empty
            if v.neighbors["higherIncoming"] and v.neighbors["higherOutgoing"]:
                
                if v.neighbors["higherIncoming"][0] == v.v \
                    and v.neighbors["higherOutgoing"][0] == v.v:
                        continue #Empty stack and one-cell consisting of single relator is consistent
                else:
                    return False #conflicting directions
            
            elif v.neighbors["higherIncoming"]:
                for w in v.neighbors["higherIncoming"]:
                    q.append(v)
                q_direction = Dir.IN
                continue                

            elif v.neighbors["higherOutgoing"]:
                for w in v.neighbors["higherOutgoing"]:
                    q.append(v)
                q_direction = Dir.OUT
                continue

            else: #no neighbors
                continue                


        elif q_direction == Dir.IN and v.neighbors["lowerOutgoing"]:
            for w in v.neighbors["lowerOutgoing"]:
                p = q.pop() #dequeues the head of the queue

                if p.v not in v.neighbors["lowerOutgoing"]:
                    return False
             
 
        elif q_direction == Dir.OUT and v.neighbors["lowerIncoming"]:
            for w in v.neighbors["lowerIncoming"]: 
                p = q.pop() #dequeues the head of the queue

                if p.v not in v.neighbors["lowerIncoming"]:
                    return False
            
        if (q_direction == Dir.IN and v.neighbors["higherOutgoing"]) or \
            (q_direction == Dir.OUT and v.neighbors["higherIncoming"]):
            return False

        if v.neighbors["higherOutgoing"] and v.neighbors["higherIncoming"]:
            return False

        elif q_direction == Dir.IN and v.neighbors["higherIncoming"]:
            for w in v.neighbors["higherIncoming"]:
                q.append(v)

        elif q_direction == Dir.OUT and v.neighbors["higherOutgoing"]:
            for w in v.neighbors["higherOutgoing"]:
                q.append(v)

    
    return True



def vertexListHelper(stacking, generator): # generator is a specific lobe
    visited = {key : False for key in stacking.vertexList}    

    vertexList = [] # return a list of the vertices with more information about them

    for v in stacking.vertexList: # iterate throught the vertices in the spine.
        higherOutgoing = [] # use to store a list of vertices that are higher than the current vertex and there is an outgoing edge from the vertex to it. 
        higherIncoming = [] # use to store a list of vertices that are higher than the current vertex and there is an incomming edge from the vertex to it.
        lowerOutgoing = []  # use to store a list of vertices that are lower than the current vertex and there is an outgoing edge from the vertex to it.
        lowerIncoming = []  # use to store a list of vertices that are lower than the current vertex and there is an incomming edge from the vertex to it.

        if v.edgeIn.generator is generator: # If vertex that we are currently looking in the set of vertices on the spine is the one in the lobe.

            vi = v.vertexIn  
            inverse_in = v.edgeIn.inverse

            if visited[vi] and not inverse_in:
                lowerIncoming.append(vi)

            elif visited[vi] and inverse_in:
                lowerOutgoing.append(vi)

            elif not visited[vi] and not inverse_in:
                higherIncoming.append(vi)

            elif not visited[vi] and inverse_in:
                higherOutgoing.append(vi)


        if v.edgeOut.generator is generator:
            vo = v.vertexOut
            inverse_out = v.edgeOut.inverse
                
            if visited[vo] and not inverse_out:
                lowerOutgoing.append(vo)

            elif visited[vo] and inverse_out:
                lowerIncoming.append(vo)

            elif not visited[vo] and not inverse_out:
                higherOutgoing.append(vo)

            elif not visited[vo] and inverse_out:
                higherIncoming.append(vo)


        visited[v] = True
        neighbors = {"higherIncoming" : higherIncoming, "lowerIncoming" : lowerIncoming, \
            "higherOutgoing" : higherOutgoing, "lowerOutgoing" : lowerOutgoing}

        vertexList.append(StackingVertex(v, neighbors))


    return vertexList

class Dir(Enum):
    IN = True
    OUT = False       
                 
class StackingVertex: #helper class
    def __init__(self, v, neighbors, visited=False):
        self.v = v

        #contains a dictionary of neighbors of v, with keys
        # 'higherOutgoing'
        # 'higherIncoming'
        # 'lowerIncoming'
        # 'lowerOutgoing'
        # Each entry is a list of at most two vertices.
        self.neighbors = neighbors 

        self.visited = visited
