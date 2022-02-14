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

def longestSequence(wds, wkdic = {}, ckwd = ""):
    tplvl = False
    if (wkdic == {}):
        tplvl = True
        for wd in wds:
            wkdic.update({wd:-1})
    if (len(wds) == 0):
        return 0
    if (ckwd == ""):
        lngsttplen = 1
        lngsttpwd = ""
        for wd in wkdic:
            if wd == "":
                continue
            cchtuple = wkdic[wd]
            if cchtuple != -1:
                thislen = cchtuple[0]
            else:
                lentocache = longestSequence(wds, wkdic, wd)
                wkdic[wd] = lentocache
                thislen = lentocache[0]
            if (thislen > lngsttplen):
                lngsttplen  = thislen
                lngsttpwd = wd
        listtoprint = []
        pointer = lngsttpwd;
        while ( pointer != ""):
            listtoprint.append(pointer)
            pointer = wkdic[pointer][1]
        listtoprint.reverse()
        return (listtoprint);
    if (ckwd != ""):
        nextlngst = ""
        if (ckwd not in wkdic):
            return (0, "")
        if (len(ckwd) == 1):
            return (1, "")
        lngstlen = 0
        for i in range(0,len(ckwd)):
            candsbstr = ckwd[:i]+ckwd[i+1:]
            chnlenwcand = longestSequence(wds, wkdic, candsbstr)
            if (chnlenwcand[0] > lngstlen):
                lngstlen = chnlenwcand[0]
                nextlngst = candsbstr
            if (chnlenwcand == (len(ckwd)-1)):
                break
        if (tplvl):
            return lngstlen + 1
        else:
            return lngstlen + 1, nextlngst
def main():
    result= longestSequence(["a", "at", "hear", "ear", "bat"])
    print ("Result was", result)
if __name__ == "__main__":
    main()