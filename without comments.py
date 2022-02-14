"""
Author: Robert Viragh
License: All of the code and documentation in this file has been dedicated to the public domain by the author. You can do whatever
        you want with it without attribution, similar to this statement: https://www.sqlite.org/copyright.html
        This software comes with no warranty expressed or implied.
Date: 14 February 2022

--------------------------------------------------------------------------------------------------------------------------------------------------
Task:

        Given a dictionary, print the longest sequence (or one of the equal longest sequences) of words that can be made by adding one letter
        at a time to a word in the dictionary such that each word in the sequence is in the dictionary.

--------------------------------------------------------------------------------------------------------------------------------------------------
"""

def longestSequence(words, workingdictionary = {}, checkword = ""):
    weareattoplevel = False

    if (workingdictionary == {}):
        weareattoplevel = True
        newworkingdictionary = {}

        for word in words:
            newworkingdictionary.update({word:-1})

        workingdictionary = newworkingdictionary
        
    if (len(words) == 0):
        return 0

    
    if (checkword == ""):
        longesttoplevelwordlen = 1
        longesttoplevelword = ""
        for word in workingdictionary:

            if word == "":
                continue
            
            cachedtuple = workingdictionary[word]
            
            if cachedtuple != -1:
                thislength = cachedtuple[0]
            else:
                lengthtocache = longestSequence(words, workingdictionary, word)
                workingdictionary[word] = lengthtocache
                thislength = lengthtocache[0]
            if (thislength > longesttoplevelwordlen):
                longesttoplevelwordlen  = thislength
                longesttoplevelword = word
        
        
        listtoprint = []
        pointer = longesttoplevelword;
        while ( pointer != ""):
            listtoprint.append(pointer)
            pointer = workingdictionary[pointer][1]
        listtoprint.reverse()
        return (listtoprint);



    if (checkword != ""):
    
        nextlongest = ""
        
        if (checkword not in workingdictionary):
            return (0, "")
              
        if (len(checkword) == 1):
            return (1, "")

        
        longestlen = 0
    
        i = 0
        for letter in checkword:
            candidatesubstring = checkword[:i]+checkword[i+1:]

            chainlengthwithcandidate = longestSequence(words, workingdictionary, candidatesubstring)
            if (chainlengthwithcandidate[0] > longestlen):
                longestlen = chainlengthwithcandidate[0]
                nextlongest = candidatesubstring

            if (chainlengthwithcandidate == (len(checkword)-1)):
                break
            i += 1


        if (weareattoplevel):
            return longestlen + 1

        else:
            return longestlen + 1, nextlongest


def main():
    result= longestSequence(["a", "at", "hear", "ear", "bat"])

    print ("Result was", result)

if __name__ == "__main__":
    main()