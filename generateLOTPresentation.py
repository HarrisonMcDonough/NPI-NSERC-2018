

def generateOrderedTree(numOfGen):
	#returns a list of trees with numOfGen vertices, and numOfGen-1 edges. The vertices are represented as numbers from 1 to numOfGen and the edges as ordered pairs of vertices
	#returns: [[(1 i), (2 j).....],[(1 k)...],..other tree..,...]
	#we just want to avoid cycles (definition of a tree)\
	if numOfGen==2:
		return [[(1, 2)], [(2, 1)]]
	newList=list()
	for i in range(numOfGen-1):
		tempTree=generateOrderedTree(numOfGen-1)
		for e in tempTree:
			newList.append(e+[(i+1,numOfGen)])
			newList.append(e+[(numOfGen,i+1)])
	return newList





def permutation(lst):
 
    # If lst is empty then there are no permutations
    if len(lst) == 0:
        return []
 
    # If there is only one element in lst then, only
    # one permuatation is possible
    if len(lst) == 1:
        return [lst]
 
    # Find the permutations for lst if there are
    # more than 1 characters
 
    l = [] # empty list that will store current permutation
 
    # Iterate the input(lst) and calculate the permutation
    for i in range(len(lst)):
       m = lst[i]
 
       # Extract lst[i] or m from the list.  remLst is
       # remaining list
       remLst = lst[:i] + lst[i+1:]
 
       # Generating all permutations where m is first
       # element
       for p in permutation(remLst):
           l.append([m] + p)
    return l

a=[1,2,3,4,5]
b= [(1, 2), (2, 3), (3, 4), (4, 5)]

#print(permutation(a))

def generateLOT(orderedTree):
	#returns a list of all possible injective, non-degenerate LOT given an ordered tree
	listOfLOT=list()
	ls=list()
	for i in range(len(orderedTree)+1):
		ls.append(i+1)
	perm=permutation(ls)
	for x in perm:
		#temp=x[:len(orderedTree)-1]
		#print(zip(orderedTree, temp))
		temp=list(zip(orderedTree, x))
		boo=True
		for i in temp:
			if i[0][0]==i[1] or i[0][1]==i[1]:
				boo=False
		if boo:
			listOfLOT.append(temp)
	return listOfLOT



#print(generateLOT(b))

def fromLOTToComplex(labelledOrientedTree):
	#list of length the number of edges and each element is ((a b), vertex))
	n=1
	compl=""
	for x in labelledOrientedTree:
		if n==1:
			compl=compl+"1"
		else:
			compl=compl+", " + str(n)
		n=n+1
	compl=compl+ ", " + str(n)
	compl=compl+" | "
	for x in labelledOrientedTree:
		compl=compl + "" + str(x[0][0]) + " "+ str(x[1]) + " " + str(x[0][1]) + "' " + str(x[1]) + "' ,"
	compl=compl[:-1]
	return compl

#b=generateLOT(b)

#print(b[0])
#print(fromLOTToComplex(b[0]))

def genAllLabelledOrientedTrees(numGen):
	ls=list()
	iteratum=generateOrderedTree(numGen)
	#print(iteratum)
	for x in iteratum:
		for y in generateLOT(x):
			ls.append(fromLOTToComplex(y))
	return ls


# get allinjetive lot that are chains
def getChains(number):
	result=[]
	ex=genAllLabelledOrientedTrees(number)
	for x in ex:
		(generator, relator) = x.split("|", 2) # get generator string and relator string  # get the list of generators and relators for the first presentation string
		relator_list = [s.strip(" ") for s in relator.split(",")] #stripping spaces and splitting to get a list of relator strings
		chainCheck={}
		for y in relator_list:
			relator_list_list= y.replace("'", "").split(" ")
			if not relator_list_list[0] in chainCheck:
				chainCheck[relator_list_list[0]]=1
			else:	
				chainCheck[relator_list_list[0]]=chainCheck[relator_list_list[0]]+1
			if not relator_list_list[2] in chainCheck:
				chainCheck[relator_list_list[2]]=1
			else:	
				chainCheck[relator_list_list[2]]=chainCheck[relator_list_list[2]]+1
		if all(i <= 2 for i in chainCheck.values()) is True:
			result.append(x)
	return result


#print(genAllLabelledOrientedTrees(4))
