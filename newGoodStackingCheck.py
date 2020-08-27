from stacking import *

def getTopBottom(stacking):
    """ Helper method that takes a stacking and returns dictionaryTop
        and dictionaryBottom, dictionaries of tuples where the first entry
        is the visible cell for that lobe and the second entry is the
        vertex **index** where the visibility event occurs.

        Input:
        stacking : a Stacking instance.
        
        Output:

        dictionaryTop, dictionaryBottom : dictionaries with keys being the
        generator associated to each lobe and values being the tuples
        listed above.
    """
    dictionaryTop = {}
    dictionaryBottom = {}


    for v in stacking.vertexList: #ordered list of SpineVertex, going for top
        generatorIn = v.edgeIn.generator
        generatorOut = v.edgeOut.generator

        
        # Check if the two edges associated to the vertex are hidden
        # from the top. Otherwise, set it as top visible vertex in
        # applicable lobes.
        if generatorIn not in dictionaryTop:
            dictionaryTop[generatorIn] = (v.cell, stacking.vertexList.index(v))
        if generatorOut not in dictionaryTop:
            dictionaryTop[generatorOut] = (v.cell, stacking.vertexList.index(v))

    for v in reversed(stacking.vertexList): #going for bottom
        generatorIn = v.edgeIn.generator
        generatorOut = v.edgeOut.generator
    

        #Same process, but for the bottom
        if generatorIn not in dictionaryBottom:
            dictionaryBottom[generatorIn] = (v.cell, stacking.vertexList.index(v))
        if generatorOut not in dictionaryBottom:
            dictionaryBottom[generatorOut]= (v.cell, stacking.vertexList.index(v))

    list = [dictionaryTop, dictionaryBottom]
    return list

def checkGoodStacking(stacking, cells):
    """ Main method for this file.
        Determines if a stacking is good, and if so returns critical
        vertices for visibility (jeopardized lobes) if any.

        Input:

        stacking : a Stacking instance
        cells: a list of cells under consideration

        Output:

        boolean : True if the stacking is good, False otherwise
        jeopardizedTopLobes : list of tuples of jeopardized lobes from the top,
            along with the corresponding visibility index.
        jeopardizedBottomLobes : same but for the bottom.
    """
    top, bottom = getTopBottom(stacking)

    jeopardizedTopLobes = []
    jeopardizedBottomLobes = []
    
    for x in cells:
        #keeps a list of lobes in which x is visible

        #u[0] is the dictionary key (lobe)
        #u[1] is the dictionary value (tuple)
        #u[1][0] is the cell
        #u[1][1] is the index of the visibility vertex

        topLobes = [(u[0], u[1][1]) for u in top.items() if u[1][0] == x]
        bottomLobes = [(u[0], u[1][1]) for u in bottom.items() if u[1][0] == x]

        
        if not topLobes or not bottomLobes: #if x is not visible on top or on bottom
            return (False, None, None)
        
        if len(topLobes) == 1: #if x is only visible in one lobe from the top
            #append a tuple of the cell and the visibility vertex height
            jeopardizedTopLobes.append(topLobes[0])

        if len(bottomLobes) == 1: #same for bottom
            jeopardizedBottomLobes.append(bottomLobes[0])

    return (True, jeopardizedTopLobes,jeopardizedBottomLobes)
