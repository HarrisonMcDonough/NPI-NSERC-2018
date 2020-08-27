from cwComplexes import *
import heapq

def cellPQ(c):
    #Input: c is a complex
    """ Builds a priority queue out of all the two-cells
    in the presentation """


    pq = []

    for cell in c.twoCells:
        #heapq.heappush(pq, (len(cell.list), cell)) #highest priority is lowest length
        heapq.heappush(pq, (-len(cell.list), cell)) #higher priority is highest length

    return pq
