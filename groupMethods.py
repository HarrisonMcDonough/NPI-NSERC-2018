import itertools
import networkx as nx
#from networkx.drawing.nx_pydot import write_dot
import matplotlib.pyplot as plt
#from networkx.drawing.nx_agraph import write_dot
import pygraphviz as pgv
class vertex:
	def __init__(self, l):
		self.name=l

class edges:
	def __init__(self, inv, outv, labels):
		self.invertex=inv
		self.outvertex=outv
		self.label=labels



'''
get a set of alphabet along with their inverses
'''
def getInversealphabet(alphabet):
    result=alphabet[:]
    for a in range(len(result)):
        result.append(result[a]+"'")
    return result


'''
check if two strings are cyclically permutation of each other
'''
def areRotations(string1, string2):
    size1 = len(string1)
    size2 = len(string2)
    temp = ''
 
    # Check if sizes of two strings are same
    if size1 != size2:
        return 0
 
    # Create a temp string with value str1.str1
    temp = string1 + string1
 
    # Now check if str2 is a substring of temp
    # string.count returns the number of occurences of
    # the second string in temp
    if (temp.count(string2)> 0):
        return 1
    else:
        return 0

'''
concatenate two list and removes the dupicates
'''
def concatRmDuplicate(first_list, second_list):
	in_first = set(first_list)
	in_second = set(second_list)
	in_second_but_not_in_first = in_second - in_first
	result = first_list + list(in_second_but_not_in_first)
	return result

'''
Get a list of relators that are the commutators of a set of generators for a free group
'''
def createCommutators(generators):
	result=[]
	for x in list(itertools.combinations(generators, 2)):
		result.append(""+x[0]+" "+x[1]+" "+x[0]+"' "+x[1]+"'")
	return result

'''
a method that return a list of cyclic permutation of a string
'''
def cyclicPermute(aString):
	resutl=''
	strList=list(aString)
	n=len(aString)
	cyclicPermList=[[aString[i - j] for i in range(n)] for j in range(n)]
	cyclicPerm=[]
	for x in range(n):
		cyclicPerm.append(''.join(cyclicPermList[x]))
	return cyclicPerm

#Function to left rotate arr[] of size n by d*/
def leftRotate(arr, d, n):
	for i in range(d):
		leftRotatebyOne(arr, n)
#Function to left Rotate arr[] of size n by 1*/ 
def leftRotatebyOne(arr, n):
    temp = arr[0]
    for i in range(n-1):
        arr[i] = arr[i+1]
    arr[n-1] = temp

def leftRotateStringbyOne(str1):
	result=''
	a=str1[0]
	result=str1[1:]+a
	return result
'''
A method to get the evaluation(length) of a word in a free group
'''
def wordNorm(str1, word):
	aword=word[:]
	(generator, relator) = str1.split("|", 2)
	generator_list = [s.strip(" ") for s in generator.split(",")] #stripping spaces and splitting
	relator_list = [s.strip(" ") for s in relator.split(",")] #stripping spaces and splitting
	relator_list=reversed(sorted(relator_list,key=len))

	for x in relator_list:
		n=len(aword)
		for y in range(n):
			aword= aword.replace(x.replace(" ",""),"")
			if len(aword) < len(x.replace(" ","")):
				break
			else:
				aword=leftRotateStringbyOne(aword)
	return len(aword)


'''
A method that returns a presentation strings of the freee product of two free group given by their presentation string

'''

def freeProduct(h,g):
	(generator_h, relator_h) = h.split("|", 2)
	generator_listh = [s.strip(" ") for s in generator_h.split(",")] #stripping spaces and splitting
	(generator_g, relator_g) = g.split("|", 2)
	generator_listg = [s.strip(" ") for s in generator_g.split(",")] #stripping spaces and splitting
	return " ".join(concatRmDuplicate(generator_listh,generator_listg))+"|"+relator_h+','+relator_g


'''
Return the presentation strings of the direct product of two free group given their presentation strings
'''
def directProduct(h,g):
	result=freeProduct(h,g)
	(generator_h, relator_h) = h.split("|", 2)
	generator_listh = [s.strip(" ") for s in generator_h.split(",")] #stripping spaces and splitting
	(generator_g, relator_g) = g.split("|", 2)
	generator_listg = [s.strip(" ") for s in generator_g.split(",")] #stripping spaces and splitting
	commutators=createCommutators(concatRmDuplicate(generator_listh,generator_listg))
	return result+". "+",".join(commutators)



'''
Returns a presentation strings of the amalgamated free product of two free group given by their presentation string
'''
def amalgamatedFreeProduct(h,g):
	(generator_h, relator_h) = h.split("|", 2)
	generator_listh = [s.strip(" ") for s in generator_h.split(",")] #stripping spaces and splitting
	relator_listh = [s.strip(" ") for s in relator_h.split(",")] #stripping spaces and splitting
	
	(generator_g, relator_g) = g.split("|", 2)
	generator_listg = [s.strip(" ") for s in generator_g.split(",")] #stripping spaces and splitting
	relator_listg = [s.strip(" ") for s in relator_g.split(",")] #stripping spaces and splitting

	amalgamatedrelators=[] # use to store the relators of the amalgamated product
	if len(relator_listg)<=len(relator_listh):
		for x in relator_listg:
			rotated=None
			# create inverse of the relator and check for if they are the same relator
			inverseRelatorList=list(reversed(x.split(" ")))
			for a in range(len(inverseRelatorList)):
				if len(inverseRelatorList[a]) is 1:
					inverseRelatorList[a]=inverseRelatorList[a]+"'"
				else:
					inverseRelatorList[a]=inverseRelatorList[a][0]
			for y in relator_listh:
				if areRotations(x,y):
					rotated=True
					break
				if areRotations(y.replace(" ", ""),"".join(inverseRelatorList)):
					rotated=True
					break
			if not rotated:
				amalgamatedrelators.append(x)
		amalgamatedrelators=amalgamatedrelators+relator_listh
	else:
		for x in relator_listh:
			rotated=None
			# create inverse of the relator and check for if they are the same relator
			inverseRelatorList=list(reversed(x.split(" ")))
			for a in range(len(inverseRelatorList)):
				if len(inverseRelatorList[a]) is 1:
					inverseRelatorList[a]=inverseRelatorList[a]+"'"
				else:
					inverseRelatorList[a]=inverseRelatorList[a][0]
			for y in relator_listg:
				if areRotations(x,y):
					rotated=True
					break
				if areRotations(y.replace(" ", ""),"".join(inverseRelatorList)):
					rotated=True
					break
			if not rotated:
				amalgamatedrelators.append(x)
		amalgamatedrelators=amalgamatedrelators+relator_listg
	return(" ".join(concatRmDuplicate(generator_listh,generator_listg))+"|"+",".join(amalgamatedrelators))


""" 
Deterministic labbeled digraph
"""

DLG= nx.MultiDiGraph()
#DLDG=nx.DiGraph(DLG)
DLG.add_edges_from([('v4','v1',{'label':'a'}),('v4','v1',{'label':'b'}),('v1','v2',{'label':'a'}),('v3','v2',{'label':'b'})])
DLG.add_edges_from([('v2','v5',{'label':'a'}),('v2','v5',{'label':'b'}),('v5','v4',{'label':'b'}),('v5','v6',{'label':'a'})])
DLG.add_edges_from([('v6','v3',{'label':'a'}),('v6','v3',{'label':'b'}),('v3','v7',{'label':'a'}),('v7','v4',{'label':'a'})])
DLG.add_edges_from([('v8','v7',{'label':'b'}),('v8','v8',{'label':'a'}),('v7','v6',{'label':'b'})])

print(DLG.nodes(data=True))
#nx.write_dot(G,'multi.dot')

'''
 input a deterministic labeled digraph and draw it.
'''
def draw(G):
	pos=nx.spring_layout(G)
	nx.draw_networkx(G,pos)
	edge_labels=dict([((u,v,),d['label'])
             for u,v,d in G.edges(data=True)])

	nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)
	plt.show()
draw(DLG)
