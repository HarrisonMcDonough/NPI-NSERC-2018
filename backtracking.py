from newGoodStackingCheck import *
from newEmbeddingCheck import *
import cellPQ as CellPQ
from getVertices import *
from stacking import *

import heapq
import pdb
def backtrackFinder(c, exhaustive=False):
    """ Main method (meant for external use) that uses a backtracking
        algorithm to find suitable good stackings or return None if
        so such stacking exists.

        This method sets up default values for use in the main
        backtracking method then exits.

       Inputs:

        c: a Complexes instance.
        exhaustive: A flag to mark if the search should be exhaustive
            (all good stacings) or not

        Outputs:

        If exhaustive search is off, an ordered list of spine vertices
            in an order respecting stacking.vertexList
        If exhaustive search is on, an ordered list of all orderings that work

        None, otherwise.
    """
    #initializing all values in use            
    pq = CellPQ.cellPQ(c)
    currentCell = heapq.heappop(pq)
    pastCells = []

    if c.edgeList is None or c.vertexList is None:
        getVertices(c)

    edgeSet = set()
    for edge in c.edgeList:
        if edge.cell == currentCell[1]:
            edgeSet.add(edge)
    
    stacking = Stacking(c, [])
    jeopardizedTopLobes = []
    jeopardizedBottomLobes = []

    return backtracking(stacking, pq, currentCell, pastCells, edgeSet, \
        jeopardizedTopLobes, jeopardizedBottomLobes, exhaustive)
    

def backtracking(
    stacking,
    cellPQ,
    currentCell,
    pastCells,
    edgeSet,
    jeopardizedTopLobes,
    jeopardizedBottomLobes,
    exhaustive=False):

    """ Main method for this file.

    Iterates through the edges of a complex in order to set up an ordering
    on the vertices of the complex seen so far, in a way that results in a
    consistent stacking. Also checks for goodness of the stacking once
    the entirety of a 2-cell has been added.

    This method works recursively, using a DFS-like traversal of the
    tree of possible spine vertex orderings.

    Inputs:

    stacking: A Stacking instance, containing te stacking so far.
    cellPQ: An instance of CellPQ, a priority queue containing an order
        on the cells to be inserted. Note that entries of CellPQ are
        tuples of the form (priority, cell).
    currentCell: A TwoCell instance, the cell whose edges are currently being
        inserted in the order.
    pastCells: A list of the cells whose edges have already been added
        to stacking.vertexList.
    edgeSet: A Set of the edges **in currentCell** that have not been yet added
        to stacking.vertexList.
    jeopardizedTopLobes: A list of tuples, the first coordinate of which is
        a jeopardized lobe (lobe where adding edges on top jeopardizes goodness
        of previously inserted cells). The second coordinate of the tuple is
        the index in stacking.vertexList not to be exceeded.
    jeopardizedBottomLobes: Same, but for the bottom of the lobe.
    exhaustive: A boolean flag indicating if the search should be exhaustive
        or not.

    Output:

    A Stacking object that is consistent and good, if it exists

    None, otherwise.
    """

    if not edgeSet: #if the edge queue is currently empty, i.e. finished currecntCell
        #Makes copy of cell list, then check for goodness    
        newPastCells = list(pastCells)
        newPastCells.append(currentCell[1])
        good, newJeopardizedTopLobes, newJeopardizedBottomLobes = \
            checkGoodStacking(stacking, newPastCells)

        if good and cellPQ: #cells remaining
            newCellPQ = list(cellPQ) #copies cellPQ
            heapq.heapify(newCellPQ)            
            newCurrentCell = heapq.heappop(newCellPQ)
 
            for edge in stacking.complex.edgeList:
                if edge.cell == newCurrentCell[1]:
                    edgeSet.add(edge)

            return backtracking(
                stacking,
                newCellPQ,
                newCurrentCell,
                newPastCells,
                edgeSet,
                newJeopardizedTopLobes,
                newJeopardizedBottomLobes,
                exhaustive)

        elif good: #no cells remaining
            return stacking if not exhaustive else [stacking]

        else:
            return None

    
    else: #have to add an edge
        e = edgeSet.pop() #take the first edge off the edgelist

        v_1 = e.initVertex
        v_2 = e.destVertex

        goodStackings = [] #good stacking tracker in case search is exhaustive

        if v_1 in stacking.vertexList and v_2 in stacking.vertexList: #adding edge between known vertices
            newStacking = stacking.copy()
            newStacking.addEdge(e)

            if embeddingCheck(newStacking): #if the embedding is consistent

                return backtracking(
                    newStacking,
                    cellPQ,
                    currentCell,
                    pastCells,
                    edgeSet.copy(),
                    jeopardizedTopLobes,
                    jeopardizedBottomLobes,
                    exhaustive ) 
                    #edgeSet has to be copied due to the fact that it has been modified

            else:
                return None #adding the edge creates an inconsistent stacking

        elif v_1 in stacking.vertexList: #adding edge where v_1 is known

            init = stacking.vertexList.index(v_1)
            insertLength = len(stacking.vertexList) + 1

            for i in range(insertLength): #inserting v_2 at all positions 
                newStacking = stacking.copy()
                newStacking.insertVertex((init + i) % insertLength, v_2)
                newStacking.addEdge(e)
                
                #"""
                #if we're trying to incorrectly insert v_2 at the top or bottom
                if e.generator in [tup[0] for tup in jeopardizedTopLobes \
                    if tup[1] < (init + i) % insertLength] or \
                    e.generator in [tup[0] for tup in jeopardizedBottomLobes \
                    if tup[1] > (init + i) % insertLength]:

                    continue
                #"""    
                if embeddingCheck(newStacking):

                    b = backtracking(
                        newStacking,
                        cellPQ,
                        currentCell,
                        pastCells,
                        edgeSet.copy(),
                        jeopardizedTopLobes,
                        jeopardizedBottomLobes,
                        exhaustive )

                    if b is not None and not exhaustive:
                        return b

                    if b is not None and exhaustive:
                        goodStackings.extend(b)
            
            if not exhaustive:  #if no return statement was already done,
                                #branch is a dud
                return None
            else:
                return goodStackings

        elif v_2 in stacking.vertexList: #adding edge where v_2 is known
            init = stacking.vertexList.index(v_2)
            insertLength = len(stacking.vertexList) + 1

            for i in range(insertLength): #inserting v_1 at all positions
                newStacking = stacking.copy()
                newStacking.insertVertex((i+ init) % insertLength, v_1)
                newStacking.addEdge(e)
                #"""
                #if we're trying to incorrectly insert v_1 at the top or bottom
                if e.generator in [tup[0] for tup in jeopardizedTopLobes \
                    if tup[1] < (init + i) % insertLength] or \
                    e.generator in [tup[0] for tup in jeopardizedBottomLobes \
                    if tup[1] > (init + i) % insertLength]:

                    continue
                #"""
                if embeddingCheck(newStacking):

                    b = backtracking(
                        newStacking,
                        cellPQ,
                        currentCell,
                        pastCells,
                        edgeSet.copy(),
                        jeopardizedTopLobes,
                        jeopardizedBottomLobes,
                        exhaustive )

                    if b is not None and not exhaustive:
                        return b
                    elif b is not None and exhaustive:
                        goodStackings.extend(b)

            if not exhaustive:
                return None
            else:
                return goodStackings


        else: #neither vertex has already been seen

            for i in range( len(stacking.vertexList) + 1 ): #inserting v_1, v_2 at all positions 
                for j in range( len(stacking.vertexList) + 2):
                    
                    newStacking = stacking.copy()
                    newStacking.insertVertex(i, v_1)
                    newStacking.insertVertex(j, v_2)
                    newStacking.addEdge(e)
                    #"""
                    #if we're trying to incorrectly insert v_1 at the top or bottom
                    if e.generator in [tup[0] for tup in jeopardizedTopLobes \
                        if tup[1] < i] or \
                        e.generator in [tup[0] for tup in jeopardizedBottomLobes \
                        if tup[1] > i]:

                        continue
     
                     #if we're trying to incorrectly insert v_2 at the top or bottom
                    if e.generator in [tup[0] for tup in jeopardizedTopLobes \
                        if tup[1] < j - 1] or \
                        e.generator in [tup[0] for tup in jeopardizedBottomLobes \
                        if tup[1] > j + 1]:

                        continue
                    #"""
                    if embeddingCheck(newStacking):

                        b = backtracking(
                            newStacking,
                            cellPQ,
                            currentCell,
                            pastCells,
                            edgeSet.copy(),
                            jeopardizedTopLobes,
                            jeopardizedBottomLobes,
                            exhaustive ) #list() creates copies

                        if b is not None and not exhaustive:
                            return b
                        elif b is not None and exhaustive:
                            goodStackings.extend(b)

            if not exhaustive:
                return None
            else:
                return goodStackings

