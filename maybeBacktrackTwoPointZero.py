
import copy
from cwComplexes import *


def backTrackSearch(complex):
	assignment=[]
	dicDomain={}   #WARNING maybe this will get messy because changing one will change all of them 
	spineLength=0
	for k in range(len(complex.twoCells)):
		spineLength+=len(complex.twoCells[k].list)
	for k in range(len(complex.twoCells)):
		assignment.append([])
		for i in range(len(complex.twoCells[k].list)):
			assignment[k].append(-1)
			dicDomain[(k, i)]=set(range(spineLength))    #Set or list not sure, WARNING:starts at 0

	return recursiveBacktracking(assignment, complex, dicDomain)

def recursiveBacktracking(assignment, complex, dicDomain):
	var = selectUnnassignedVar(assignment, complex, dicDomain)   # of form (k,i) stands for ith edge in kth 2-cell of complex 
	if var=="all good": return assignment #ie. no mor var to ne assigned; to be change to respect list form
	for value in dicDomain[var]: #potential value (i.e. what vertex the (k,i) will start from) for var, Order Dopmain Vale
		if checkConstraints(var, value, assignment, complex, dicDomain):     #checks if no nested and not bad stacking
			(newAssignment, newDicDomain) = addToAssignment(var, value, assignment, complex, dicDomain)  #check if need to copy assignment!!!careful with losing track!!!
			result=recursiveBacktracking(newAssignment, complex, newDicDomain)
			if result != "failure :)":
				return result
			#assignment is still old assignment
	return "failure :)"


def selectUnnassignedVar(assignment, complex, dicDomain): #room for improvement, in changing the order smartly :)
	for k in range(len(complex.twoCells)):
		for i in range(len(complex.twoCells[k].list)):
			if assignment[k][i]==-1:
				return (k, i)
	return "all good"

def orderDomainValues(var, assignment, complex, dicDomain): #replace line 23 for value in dicDomain by this, room for improvement, in chaning the order smartly :)
	return dicDomain[var]   #should depend on assignment!! :/ WARNING

def checkConstraints(var, value, assignment, complex, dicDomain):
	
	(stack, emb)=(checkBadStacking(var, value, assignment, complex, dicDomain) , checkEmbedding(var, value, assignment, complex, dicDomain)) #checkBadStacking is way faster, so is first :)
	#print(assignment)
	#print(dicDomain)
	return stack and emb

def addToAssignment(var, value, assignment, complex, dicDomain):
	newAssignment=copy.deepcopy(assignment)
	newAssignment[var[0]][var[1]]=value        #possible error check by checking if replaces only -1 values
	newDicDomain=copy.deepcopy(dicDomain)          #for dicDomain warning
	for k in range(len(complex.twoCells)):
		for i in range(len(complex.twoCells[k].list)):
			try: 
				if k == var[0] and i==var[1]:
					newDicDomain[(k, i)]=[value]
				else:
					temp=newDicDomain[(k,i)]   #WARNING hella expensive
					temp.remove(value)
					newDicDomain[(k, i)]=temp
			except ValueError:
				"ein error"
	return (newAssignment, newDicDomain)

def checkBadStacking(var, value, assignment, complex, dicDomain): #only check for completed loops //
											#is there a way to keep track of this to not run it every single iteration?? 
	k=0
	assignment[var[0]][var[1]]=value
	completedTwoCells=set()    #maybe we want a specific order in here, to see what 2-cell to check first. I assumed that there is no way we can predict a BAD stacking, thats probably false
	botTwoCellAndValue={}
	topTwoCellAndValue={}
	for e in complex.oneCells:
		botTwoCellAndValue[e]=(None, None)
		topTwoCellAndValue[e]=(None,None)
	for c in complex.twoCells:    #magic magic abradacabra
		toBeChecked=True    #checks if twoCell is fully assigned
		for i in range(len(c.list)):
			e=c.list[i][0]         #Should point to right edge, maybe not WARNING
			if assignment[k][i] == -1:
				toBeChecked=False
			else:
				# Do not need this anymore: dicVertValuesForEdges[e].append(assignment[k][i])    #should append value of starting vertex for edge (k, i) for that two cell to the list of values for that edge (or lobe)   WARNING kinda not clear, inchallah it works
				if botTwoCellAndValue[e][1]==None:  #just to initialize, could use inf representation but felt sketchy
					botTwoCellAndValue[e]=(c, assignment[k][i])
				if topTwoCellAndValue[e][1]==None:
					topTwoCellAndValue[e]=(c, assignment[k][i])

				if botTwoCellAndValue[e][1]>assignment[k][i]:         #keeps track of minimal twoCell AND value (2-cell, value) for a particular edge
					botTwoCellAndValue[e]=(c, assignment[k][i])
				if topTwoCellAndValue[e][1]<assignment[k][i]:
					topTwoCellAndValue[e]=(c, assignment[k][i])
		k=+1
		if toBeChecked:
			completedTwoCells.add(c)

	tempBot=copy.deepcopy(completedTwoCells)    #WARNING EXPENSIVE
	tempTop=copy.deepcopy(completedTwoCells)

	for e in complex.oneCells:
		x=botTwoCellAndValue[e]
		if x[0] in tempBot:
			tempBot.remove(x[0])   #WARNING expensive
		x=topTwoCellAndValue[e]
		if x[0] in tempTop:
			tempTop.remove(x[0])

	return not(tempBot) and not(tempTop) #True iff both empty

def checkEmbedding(var, value, assignment, complex, dicDomain): #What order? Right now just dummy order Use a heuristic and a heap here?
	assignment[var[0]][var[1]]=value
	lk=len(complex.twoCells) #what k iterates through
	for k in range(lk):
		li=len(complex.twoCells[k].list)
		for i in range(li): #(k, i) is our first edge read ith edge in kth starting from 0
			lp=len(complex.twoCells)
			for p in range(lp):
				lq=len(complex.twoCells[p].list)
				for q in range(lq): #(q, p) is our second edge, we check no crossing  between (k, i) & (p, q)
					if k != p or i != q:
						if assignment[k][i] != -1 and assignment[p][q] != -1 : #ie both edges have been given a start point
							if (assignment[k][(i+1)%li] != -1) and (assignment[p][(q+1)%lq] != -1): #ie both edges have been given an end point, i+1 mod length of cell tho
								if complex.twoCells[k].list[i][0]==complex.twoCells[p].list[q][0]: #if same edge, otherwise all good bc no crossing possible
									firstMax=max(assignment[k][i],assignment[k][(i+1)%li])
									if assignment[k][i]==firstMax:
										firstDir="down"
									else:
										firstDir="up"
									secondMax=max(assignment[p][q],assignment[p][(q+1)%lq])
									if assignment[p][q]==secondMax:
										secondDir="down"
									else:
										secondDir="up"
									firstInterv=set(range(min(assignment[k][i],assignment[k][(i+1)%li]), max(assignment[k][i],assignment[k][(i+1)%li])+1))
									secondInterv=set(range(min(assignment[p][q],assignment[p][(q+1)%lq]), max(assignment[p][q],assignment[p][(q+1)%lq])+1))
									if firstDir==secondDir: #both up or both down
										if complex.twoCells[k].list[i][1]==complex.twoCells[p].list[q][1]: #same sign ie a and a inverse
											if firstInterv.issubset(secondInterv) or secondInterv.issubset(firstInterv): #if nested, can be replaced by intersection with set objects
												return False
										else: #different sign (but both up or both down)
											if firstInterv.intersection(secondInterv):
												return False
									else: #one up, one down
										if complex.twoCells[k].list[i][1]==complex.twoCells[p].list[q][1]: #same sign
											if firstInterv.intersection(secondInterv):
												return False
										else:#different sign 
											if firstInterv.intersection(secondInterv):
												return False
	return True											