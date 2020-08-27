from cwComplexes import *
from enum import Enum
from collections import deque
from stacking import *

import pdb
def embeddingCheck(stacking):
    #pdb.set_trace() 

    for g in stacking.complex.oneCells:
        if not embeddingLobeCheck(stacking, stacking.augVertexList[g]):
            return False

    return True

def embeddingLobeCheck(stacking, vertexList):
    """A helper method for embeddingCheck, checks if the embedding works
        for a specific lobe give by <generator>.

        This is a queue-based algorithm to detect crossings. Please
        see doc/embeddingCheck.pdf (or tex) for more details.
    """
    
    #pdb.set_trace()
    
    q = deque()
    q_direction = Dir.IN #dummy value

    for v in vertexList:

        if not q: #if the queue is empty
            if v.higherIncoming and v.higherOutgoing:
                
                if v.higherIncoming[0] == v.v \
                    and v.higherOutgoing[0] == v.v:
                        continue #Empty stack and one-cell consisting of single relator is consistent
                else:
                    return False #conflicting directions
            
            elif v.higherIncoming:
                for w in v.higherIncoming:
                    q.append(v)
                q_direction = Dir.IN
                continue                

            elif v.higherOutgoing:
                for w in v.higherOutgoing:
                    q.append(v)
                q_direction = Dir.OUT
                continue

            else: #no neighbors
                continue                


        elif q_direction == Dir.IN and v.lowerOutgoing:
            for w in v.lowerOutgoing:
                p = q.popleft() #dequeues the head of the queue

                if p.v not in v.lowerOutgoing:
                    return False
             
 
        elif q_direction == Dir.OUT and v.lowerIncoming:
            for w in v.lowerIncoming: 
                p = q.popleft() #dequeues the head of the queue

                if p.v not in v.lowerIncoming:
                    return False
            
        if (q_direction == Dir.IN and v.higherOutgoing) or \
            (q_direction == Dir.OUT and v.higherIncoming):
            return False

        if v.higherOutgoing and v.higherIncoming:
            return False

        elif q_direction == Dir.IN and v.higherIncoming:
            for w in v.higherIncoming:
                q.append(v)

        elif q_direction == Dir.OUT and v.higherOutgoing:
            for w in v.higherOutgoing:
                q.append(v)

    
    return True


class Dir(Enum):
    IN = True
    OUT = False       
                
