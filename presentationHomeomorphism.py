
from collections import Counter
import collections

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


def strTranslate(str1, input_chars, output_chars):
    table = str.maketrans(input_chars, output_chars)
    return str1.translate(table)


'''
str1: first presentation string
str2: second presentation string
l: permuted list of second generators
prev: auxilary used to complete the permutation
the method first relabels the 2nd list of generators with the mapping then chekc if the two string represent the same permutation
'''
def checkAllBijections(str1,generators_list1,l,prev,relator_list2):

    if len(l)==1:
        res=prev+l # this is a bijection
        str2c=str1 # str2c is str1 but replaced by generator2 alphabets according to the bijection 
        str2c=strTranslate(str2c,"".join(generators_list1),"".join(res))
        (generator_str1, relator_str1) = str2c.split("|", 2) # get generator string and relator string  # get the list of generators and relators for the first presentation string
        relator_list1 = [s.strip(" ") for s in relator_str1.split(",")] #stripping spaces and splitting        
        # check the relators matches together up to cyclic permutation
        for x in range(len(relator_list2)):
            for y in range(len(relator_list1)):
                if areRotations(relator_list2[x].replace(" ", ""),relator_list1[y].replace(" ", "")):
                    del relator_list1[y]
                    break
                # create inverse of the relator and check for if they are the same relator
                inverseRelatorList=list(reversed(relator_list1[y].split(" ")))
                for a in range(len(inverseRelatorList)):
                    if len(inverseRelatorList[a]) is 1:
                        inverseRelatorList[a]=inverseRelatorList[a]+"'"
                    else:
                        inverseRelatorList[a]=inverseRelatorList[a][0]
                if areRotations(relator_list2[x].replace(" ", ""),"".join(inverseRelatorList)):
                    del relator_list1[y]
                    break            
        if len(relator_list1) is 0:
            return True # are homeomorphic!!
    else:    
        for i in range(0,len(l)):
            if checkAllBijections(str1,generators_list1,l[:i]+l[i+1:],prev+[l[i]],relator_list2):
                return True
    return False

 
'''
 Naive algorithm then 
 Using a backtracking algorithm if have time
'''

def areHomeomorphic(pres_str1, pres_str2):

    (generator_str1, relator_str1) = pres_str1.split("|", 2) # get generator string and relator string  # get the list of generators and relators for the first presentation string
    generator_list1 = [s.strip(" ") for s in generator_str1.split(",")] #stripping spaces and splitting
    relator_list1 = [s.strip(" ") for s in relator_str1.split(",")] #stripping spaces and splitting
    
    (generator_str2, relator_str2) = pres_str2.split("|", 2) # get generator string and relator string # get the list of generators and relators for the second presentation string
    generator_list2 = [s.strip(" ") for s in generator_str2.split(",")] #stripping spaces and splitting
    relator_list2 = [s.strip(" ") for s in relator_str2.split(",")] #stripping spaces and splitting

    if len(generator_list1) != len(generator_list2): # different number of generators return false
        return False
    if len(relator_list1) != len(relator_list2): # different number of relators means no homeomorphic
        return False

    results=checkAllBijections(pres_str1,generator_list1,generator_list2,[],relator_list2)
    #print(results)
    if results== True:
        return True
    return False
