from cwComplexes import *
#from arcConsistency import *
import copy
import queue

def backTrackSearch(complex):
    assignment=[]
    dicDomain={}   #WARNING maybe this will get messy because changing one will change all of them 
    spineLength=0
    completedTwoCells=set() #keeps track of what two cells are completed, for the goodStacking key: TwoCell, value bool. HELP:Pruning: when 2-cell is done prune MAAAASSE
    dicGoodStackingTop={}   #keys are the onecells and values are (two cell, max value of two cell), this is updated throughout the code
    dicGoodStackingBot={}   #same for bot with min
    #edgeDic={} #keeps track of what is needed to speed up the embedding check, keys are onecells values are lists of ((k,i), interval);. their values can be gotten using assignment[k][i]
    temp=set()
    assForEdgeDic={} #keys are edges, values are lists or sets of (k, i) pairs

    for k in range(len(complex.twoCells)):
        spineLength+=len(complex.twoCells[k].list)
    
    #gets cartesian product:
    for x in range(spineLength):
        for y in range(spineLength):
            if x!=y:
                temp.add((x, y))


    #initialize dicGoodTop&Bot, note that they work together with completedTwoCells
    for e in complex.oneCells:
        assForEdgeDic[e]=[]
        #edgeDic[e]=[]
        dicGoodStackingBot[e]=(None, None)
        dicGoodStackingTop[e]=(None, None)

    for k in range(len(complex.twoCells)):
        assignment.append([])
        for i in range(len(complex.twoCells[k].list)):
            assignment[k].append((None,None))
            dicDomain[(k, i)]=copy.deepcopy(temp)    #Set or list not sure, WARNING:starts at 0
            assForEdgeDic[complex.twoCells[k].list[i][0]].append((k, i))

    #return recursiveBacktracking(assignment, complex, dicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells, spineLength, assForEdgeDic)
    return convertResult(recursiveBacktracking(assignment, complex, dicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells, spineLength, assForEdgeDic))


def recursiveBacktracking(assignment, complex, dicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells, spineLength, assForEdgeDic):
    #print('assignment is')
    #print(assignment)
    var = selectUnnassignedVar(assignment, complex, dicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells, spineLength, assForEdgeDic)   # of form (k,i) stands for ith edge in kth 2-cell of complex 
    #print('var is')
    #print(var)
    if not(var): return assignment #ie. no mor var to ne assigned; to be change to respect list form
    #print('dicdomain[var] is')
    #print(dicDomain)
    for value in dicDomain[var]: #potential value (i.e. what vertex the (k,i) will start from) for var, SPEED UP:Order Dopmain Vale
        
         #copies dicDomain (instead of deep copy since keys are tuples which are weird..)
        newDicDomain={}
        for key in dicDomain.keys():
            newDicDomain[key]=copy.deepcopy(dicDomain[key])

        #print('value is')
        #print(value)
        (isPossibleAssignment, newAssignment)=addToAssignment(var, value, assignment, complex, dicDomain, newDicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells, spineLength)
        #print('isPossibleAssignment')
        #print(isPossibleAssignment)
        #print('newDicDomain')
        #print(newDicDomain)
        if isPossibleAssignment:
            (isStackingGood, newDicGoodStackingBot, newDicGoodStackingTop, newCompletedTwoCells)=checkBadStackingConstructing(var, value, newAssignment, complex, dicDomain, newDicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells)
            #print('isStackingGood')
            #print(isStackingGood)
            if isStackingGood:
                isEmbeddingGood=checkEmbeddingConstructing(var, value, newAssignment, complex, dicDomain, newDicDomain, assForEdgeDic)
                #print('isEmbeddingGood')
                #print(isEmbeddingGood)
                if isEmbeddingGood: 
                    #potSolution=arcConsistency(newDicDomain)                   
                    if arcConsistencyForEmbedding(var, value, assignment, complex, dicDomain, newDicDomain, newDicGoodStackingBot, newDicGoodStackingTop, newCompletedTwoCells, assForEdgeDic):
                    	result=recursiveBacktracking(newAssignment, complex, newDicDomain, newDicGoodStackingBot, newDicGoodStackingTop, newCompletedTwoCells, spineLength, assForEdgeDic)
                    if result != None :
                        return result
            #assignment is still old assignment
    return None

def addToAssignment(var, value, assignment, complex, dicDomain, newDicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells, spineLength): #find a way to do this fasteeeeeeer
    #Prunning rules: -all var have different values, both for start and for bot
    #                -assigning  (k, i) will assign start for (k, i+1 mod length) and end for (k, i-1 mod length)

    newAssignment=copy.deepcopy(assignment)
    newAssignment[var[0]][var[1]]=value        #possible error check by checking if replaces only -1 values



    return pruneByAssignment(var, value, newAssignment, complex,dicDomain, newDicDomain, spineLength)


def pruneByAssignment(var, value, newAssignment, complex, dicDomain, newDicDomain, spineLength):
    #rule 1: all starts must be different
    #rule 2: all end must be different
    #rule 3: edge after var must have start=end(var)
    #rule 4: edge before var must have end=start(var)

    newDicDomain[var]={value}

    l=len(complex.twoCells[var[0]].list)
    
    boo=partialAssignmentStart((var[0], (var[1]+1)%l), var, value[1], dicDomain, newDicDomain, spineLength)
    if not boo:
        return (False, None)
    boo= partialAssignmentEnd((var[0], (var[1]-1)%l), var, value[0], dicDomain, newDicDomain, spineLength)
    if not boo:
        return (False, None)
    return (True, newAssignment)


#prune when we know the start of var
def partialAssignmentStart(postVar, var, start, dicDomain, newDicDomain, spineLength):
    temp=set()

    #for the next edge, only keep where start is equal to end:
    for x in dicDomain[postVar]:
        if x[0]==start:
            temp.add(x)

    newDicDomain[postVar]=temp #WARNING might need a pseudo deepcopy
    if not(temp):
        #print(var)
        #print("1")
        return False

    for key in dicDomain.keys():  #EXPENSIVE
        if key!=var and key !=postVar :
            #for other vars, remove when start=start
            for x in dicDomain[key]:
                if x[0]==start:
                    try:
                        newDicDomain[key].remove(x)
                    except KeyError:
                        "ach"
                    if not(newDicDomain[key]):
                        #print("2")
                        return False

    return True 

def partialAssignmentEnd(preVar, var,  end, dicDomain, newDicDomain, spineLength):
    temp=set()
    for x in dicDomain[preVar]:
        if x[1]==end:
            temp.add(x)
    newDicDomain[preVar]=temp
    if not(temp):
        return False

    for key in dicDomain.keys():  #EXPENSIVE
        if key != preVar and key != var:
            for x in dicDomain[key]:
                if x[1]==end:
                    try:
                        newDicDomain[key].remove(x)
                    except KeyError:
                        "ach"
                    if not(newDicDomain[key]):
                        return False
    return True 


def selectUnnassignedVar(assignment, complex, dicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells, spineLength, assForEdgeDic): #room for improvement, in changing the order smartly :)
    """for e in assForEdgeDic.keys():
    	for var in assForEdgeDic[e]:
    		if assignment[var[0]][var[1]]==(None, None):
    			return var
    return False"""


    for k in range(len(complex.twoCells)):
        for i in range(len(complex.twoCells[k].list)):
            if assignment[k][i]==(None, None):
                return (k, i)
    return False


#returns true if assigning value to var will result in a partial good stacking (i.e False if the stacking is BAD)
#var is (k,i); values is (start, bot) on spine vertices
def checkBadStackingConstructing(var, value, assignment, complex, dicDomain, newDicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells):
   #prunning rules: 
    #print('dicGoodStackingBot')
    #print(dicGoodStackingBot)
    #print('dicGoodTop')
    #print(dicGoodStackingTop)
    #print('completedTwoCell is')
    #print(completedTwoCells)
    #creates new dictionaies:
    newDicGoodStackingBot={}
    newDicGoodStackingTop={}
    for e in complex.oneCells:
        newDicGoodStackingBot[e]=(dicGoodStackingBot[e][0], dicGoodStackingBot[e][1])
        newDicGoodStackingTop[e]=(dicGoodStackingTop[e][0], dicGoodStackingTop[e][1])

    newCompletedTwoCells=completedTwoCells #won't be changed if not needed
    #the stacking can only become bad through edge considered
    e=complex.twoCells[var[0]].list[var[1]][0]

    if newDicGoodStackingBot[e][1]==None or newDicGoodStackingBot[e][1]>min(value[0], value[1]): #should I keep track in how many edges the cell is viewed? for prunning and potentially good stackings?
        newDicGoodStackingBot[e]=(complex.twoCells[var[0]], min(value[0], value[1])) #gets what cell is viewed at that edge on Bot, should I keep track of the entire edge?
    if newDicGoodStackingTop[e][1]==None or newDicGoodStackingTop[e][1]<max(value[0], value[1]):
        newDicGoodStackingTop[e]=(complex.twoCells[var[0]], max(value[0], value[1]))
    
    #checks if new assignment completes a new 2-cell:
    boo=True
    for i in range(len(complex.twoCells[var[0]].list)):
        if assignment[var[0]][i]==(None, None):
            boo=False
    if boo:
    	newCompletedTwoCells=copy.deepcopy(completedTwoCells)
    	newCompletedTwoCells.add(complex.twoCells[var[0]])

    #print('newdicGoodStackingBot')
    #print(newDicGoodStackingBot)
    #print('newdicGoodTop')
    #print(newDicGoodStackingTop)
    #print('newCompletedTwoCell is')
    #print(newCompletedTwoCells)

    #checks if completed cells is not a bad stacking ie, are all completed two Cells viewable from top and bot
    for c in newCompletedTwoCells:
        cBoolBot=False
        cBoolTop=False
        for e in dicGoodStackingBot.keys():
            if newDicGoodStackingBot[e][1] !=None and c==newDicGoodStackingBot[e][0]:
                cBoolBot=True
            if newDicGoodStackingTop[e][1] != None and c==newDicGoodStackingTop[e][0]:
                cBoolTop=True
        #print('c:')
        #print(c)
        #print(' is viewable from top')
        #print(cBoolTop)
        #print(' from bot')
        #print(cBoolBot)

        if not (cBoolBot and cBoolTop): #if one of them is false, aka is not in a value in BOTH dictionaries, then the assignment is pointless
            return (False, None, None, None)
    return (True, newDicGoodStackingBot, newDicGoodStackingTop, newCompletedTwoCells) #good assignment!
    #return pruneGoodStacking()


#def pruneGoodStacking(...):
    #can only prune for completed loops, in which case you prune everything that will kill the goodness:
    #can also prune when for a lope, all the top things are used
    #rule1: 

def checkEmbeddingConstructing(var, value, assignment, complex, dicDomain, newDicDomain, assForEdgeDic):
    
    #This part checks if having assigned var to value will cause a problem in terms of embedding. ie it gave a nesting or something else


    #does not prune the domain   
    #edgeDic has keys: onecells and has values list of: ((k, i), interval)

    #creates new dictionaries:
    #newEdgeDic={}
    #for e in complex.oneCells:
        #newEdgeDic[e]=copy.deepcopy(edgeDic[e])   #I do not think this is necessary, use assForEdgeDic!!!!!

    e=complex.twoCells[var[0]].list[var[1]]
    temp=((var[0], var[1]), value)
    top=max(value[0], value[1])
    bot=min(value[0], value[1])

    #newEdgeDic[e[0]].append(((var[0], var[1]), set(range(bot, top))))

    if top==value[0]:
        direct=1 #1 for going down
    else:
        direct=0 #0 for going down

    inter=set(range(bot, top))

    for x in assForEdgeDic[e[0]]:
    	assOfX=assignment[x[0]][x[1]]
    	if x!=var and assOfX[0] !=None:
    		xInter=set(range(min(assOfX[0], assOfX[1]), max(assOfX[0], assOfX[1])))
    		tempTop=max(assOfX[0], assOfX[1])
    		if tempTop == assOfX[0]:
    			tempDirect=1
    		else:
    			tempDirect=0
    		sameSign=(e[1]==complex.twoCells[x[0]].list[x[1]][1])
    		nestedness=(xInter.issubset(inter) or inter.issubset(xInter))

    		if inter.intersection(xInter):
    			intersectionness=True
    		else:
    			intersectionness=False

    		if direct==tempDirect:
    			if sameSign:
    				if nestedness:
    					return False
    			else:
    				if intersectionness:
    					return False
    		else:
    			if sameSign:
    				if intersectionness:
    					return False
    			else:
    				if nestedness:
    					return False
    #return (True, newEdgeDic, dicDomain)
    return pruneEmbedding(var, value, complex, dicDomain, newDicDomain, assForEdgeDic)
    #return arcConsistencyForEmbedding(var, value, assignment, complex, dicDomain, newDicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells, assForEdgeDic)


def pruneEmbedding(var, value, complex, dicDomain, newDicDomain, assForEdgeDic):
    
    #This part prunes the domain of each variable that will be assigned to the same edge as var (in assForEdgeDic), in order for them never to be assigned to a value that will conflict with the edge just added
    

    #can only prune for the things of same edge, so assForEdgeDic
    #rule 1: for assignments which are the same lobe: if same&same, do that, if diff&same etc
    #rule 2: partial assignments embedding Not Done Yet

    #print("dicDomain is:")
    #print(newDicDomain)



    (edge, orient)=complex.twoCells[var[0]].list[var[1]]

    if value[0]>value[1]:
        direct=1 #goes down
        interv=set(range(value[1], value[0]))
    else:
        direct=0
        interv=set(range(value[0], value[1]))

    for x in assForEdgeDic[edge]: #on same lobe
        if x != var:
            xOrient=complex.twoCells[x[0]].list[x[1]][1]
            for xValue in dicDomain[x]:
                #willThisResultInBadEmbedding()
                if xValue[0]>xValue[1]:
                    xDirect=1
                    xInterv=set(range(xValue[1],xValue[0]))
                else:
                    xDirect=0
                    xInterv=set(range(xValue[0], xValue[1]))
                sameSign=(orient==xOrient)
                if interv.intersection(xInterv):
                    intersectionness=True
                else:
                    intersectionness=False
                nestedness=interv.issubset(xInterv) or xInterv.issubset(interv)
                try:
                    if  direct==xDirect:
                        if sameSign:
                            if nestedness:
                                newDicDomain[x].remove(xValue)
                        else:
                            if intersectionness:
                                newDicDomain[x].remove(xValue)
                    else:
                        if sameSign:
                            if intersectionness:
                                newDicDomain[x].remove(xValue)
                        else:
                            if nestedness:
                                newDicDomain[x].remove(xValue)
                except KeyError:
                    "doch"
            if not(newDicDomain[x]):
                return False

    return True

def arcConsistencyForEmbedding(var, value, assignment, complex, dicDomain, newDicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells, assForEdgeDic): #only embedding nodes!!
    Q=queue.Queue()
    e=complex.twoCells[var[0]].list[var[1]]
    for x in assForEdgeDic[e[0]]: #all var that can impact or be impacted by the assignment
    	if x!=var and assignment[x[0]][x[1]]!=(None,None):
    		Q.put((x, var)) 
    		Q.put((var, x))

    while not(Q.empty()):
        (var1, var2)=Q.get()
        boo=removeInconsistentValues(assignment, var1, var2, complex, dicDomain, newDicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells) #var1----->var2 (modifies newDicDomain[])
        if boo:
        	if not(newDicDomain[var]):
        		return False
        	for x in assForEdgeDic[complex.twoCells[var1[0]].list[var1[1]][0]]:
        		Q.put(x, var1)
    return True


def removeInconsistentValues(assignment, var1, var2, complex, dicDomain, newDicDomain, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells ):
    removed=False
    temp1=dicDomain[var1] #deepCopy??
    temp2=dicDomain[var2]
    didnewDicDomainChange=False
    for val1 in temp1: #set changes size??
    	boo=False
    	for val2 in temp2:
    		boo=boo or (resultsInGoodEmbedding(var1, val1, var2, val2, complex) and resultsInNotBadStacking(var1, val1, var2, val2, assignment, complex, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells))
    		#if boo is True, exit one for loop!!!!!! break??
    	if not(boo):
    		try:
    			newDicDomain[var1].remove(val1)
    			didnewDicDomainChange=True
    		except KeyError:
    			"nein"
    return didnewDicDomainChange

def resultsInNotBadStacking(var1, val1, var2, val2, assignment, complex, dicGoodStackingBot, dicGoodStackingTop, completedTwoCells):
	#can only kill goodness of a completed twocell, or a cell that gets completed by adding var1 assignment
	cell1Completed=willCellGetCompleted(var1, complex, assignment, completedTwoCells)
	if cell1Completed:
		if isVarOnlyBot(var1, val1, complex, dicGoodStackingBot):
			if min(val2[0], val2[1])<min(val1[0], val1[1]):
				return False
		if isVarOnlyTop(var1, val1, complex, dicGoodStackingTop):
			if max(val2[0], val2[1])>max(val1[0], val1[1]):
				return False
	return True




def willCellGetCompleted(var, complex, assignment, completedTwoCells):
	cell=complex.twoCells[var[0]]
	if cell in completedTwoCells:
		return True
	k=0
	l=len(cell.list)
	for e in cell.list:
		if k!=var[1]:
			if assignment[var[0]][k]==(None, None):
				return False
		k=(k+1)%l
	return True

def isVarOnlyBot(var, val, complex, dicGoodStackingBot):
	c=complex.twoCells[var[0]]
	e=complex.twoCells[var[0]].list[var[1]][0]
	for x in complex.oneCells:
		if x != e:
			if dicGoodStackingBot[x][1]!=None and dicGoodStackingBot[x][0]==c:
				return False #there is another bot
	if dicGoodStackingBot[e][1]<min(val[0], val[1]):
		return False
	return True

def isVarOnlyTop(var, val, complex, dicGoodStackingTop):
	c=complex.twoCells[var[0]]
	e=complex.twoCells[var[0]].list[var[1]][0]
	for x in complex.oneCells:
		if x != e:
			if dicGoodStackingTop[x][1]!=None and dicGoodStackingTop[x][0]==c:
					return False #there is another bot
	if dicGoodStackingTop[e][1]>max(val[0], val[1]):
		return False
	return True


def resultsInGoodEmbedding(var1, val1, var2, val2, complex):
	var1Orient=complex.twoCells[var1[0]].list[var1[1]][1]
	var2Orient=complex.twoCells[var2[0]].list[var2[1]][1]
	if val1[0]>val1[1]:
		val1Direct=1 #going down
		val1Inter=set(range(val1[1], val1[0]))
	else:
		val1Direct=0
		val1Inter=set(range(val1[0], val1[1]))
	if val2[0]>val2[1]:
		val2Direct=1 #going down
		val2Inter=set(range(val2[1], val2[0]))
	else:
		val2Direct=0
		val2Inter=set(range(val2[0], val2[1]))
	sameSign=(var1Orient==var2Orient)
	if val1Inter.intersection(val2Inter):
		intersectionness=True
	else:
		intersectionness=False
	nestedness=(val1Inter.issubset(val2Inter) or val2Inter.issubset(val1Inter))

	if val1Direct==val2Direct:
		if sameSign:
			if nestedness:
				return False
		else:
			if intersectionness:
				return False
	else:
		if sameSign:
			if intersectionness:
				return False
		else:
			if nestedness:
				return False
	return True

def convertResult(assignment):
	if assignment==None:
		return None
	else:
		result=[]
		for x in assignment:
			for y in x:
				result= result+[y[0]]
	return result





