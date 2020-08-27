
'''
get a set of alphabet along with their inverses
'''
def getInversealphabet(alphabet):
    result=alphabet[:]
    for a in range(len(result)):
        result.append(result[a]+"'")
    return result

"""
Find the list of all strings of 'alphabet' of length 'length'
"""
def allStringsN(alphabet, length):
    aplusinverses=getInversealphabet(alphabet)
    c = [""]
    for i in range(length):
        c = [x+" "+y for x in aplusinverses for y in c]
    return c

''' 
This method generate all string made up 
of the alphabet in the alphabet of lenght zero all the way to length n
'''
def allStringsUpToN(alphabet1, length):
    result=[]
    for i in range(1,length+1):
        result=result+allStringsN(alphabet1, i)
    return result

'''
all string of n relators strings of  relators with lenght up to n
'''
def allStringsNRelators(alphabet, length, nOfRelators):
    c=allStringsUpToN(alphabet, length)
    result=c[:]
    for i in range(nOfRelators-1):
        result=[(y+", "+x) for x in c for y in result]
    return result
'''
number of relator up to n and lenght of relators up to length
'''

def allStringsUpToNRelators( alphabet, length, n):
    result=[]
    for i in range(1,n+1):
        result=result+allStringsNRelators(alphabet, length, i)
    return result
'''
return a set of presentation string with generators in alphabet,
relators lenght up to length
and up to n relators
'''
    
def makePresString(alphabet, length, n):
    result=allStringsUpToNRelators(alphabet, length, n)
    for i in range(len(result)):
        result[i]=" ".join(alphabet)+" | "+result[i]
    return result
