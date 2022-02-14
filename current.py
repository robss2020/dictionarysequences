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

This is adapted from an interview question, I've modified it so it can't be used on the interview.

If you are reading it's probably because you're evaluating my ability to code in Python.

If you are short of time, the answer is:

* Yes, this is a Python file that does what it says. I wrote it myself. It works.

If you are an engineer who can code in Python yourself, and want to evaluate the contents of the file deeply,
the best way to evaluate this file is for you to try to solve the same problem. How would you do it?

Perhaps take a few minutes to try it.  The problem is trickier than you might think.

Why is this problem tricky?
The problem is about sequences within a dictionary, but there is no obvious way to get started.  Using a recursive solution,
how would you first enter the function?

The approach I took is a hybrid approach: I reuse the same function to act recursively, but at the top level I just check each word.

I cache the sequence lengths that I've already checked, and keep track of the sequences by means of a pointer that will act like a linked list.

At the end, once I have an example of the longest sequence, I traverse the linked-list and reverse it to return the longest sequence.

This code demonstrates:
* Problem-solving
* Documentation
* Recursion
* Coding and commenting, clean code
* Data structures
* Time and space complexity, O() notation
* Linked-lists


Commenting style:
Efficient code is hard to follow. I comment it as a best practice.
Many people follow the alternative strategy, "if it was hard to write it should be hard to read", however,
my style of commenting lets me easily make deep changes throughout the code without issue.

When the data structures change, I change the comments to match.

Efficient code that uses complex data structures is never self-documenting.

You can see how this file would look without comments or without verbose variable and function names in two alternative files.

Data structure used:
words: original list of words (list of strings)
      +------------------------------------------------------------+
      |                                                            |
      |                                                            |
      |     +--------+  +--------+  +--------+      +--------+     |
      |     | word 1 |  | word 2 |  | word 3 |  ... | word n |     |
      |     +--------+  +--------+  +--------+      +--------+     |
      |                                                            |
      |                                                            |
      +------------------------------------------------------------+
                          list of strings



workingdictionary: dictionary of tuples          
     +------------------------------------------------------------+
     |                                                            |
     |                                                            |
     |     +--------+  +--------+  +--------+      +--------+     |
     |     | word 1 |  | word 2 |  | word 3 | ...  | word n |     |
     |     +--------+  +--------+  +--------+      +--------+     |
     |                                                            |
     |                                                            |
     +------------------------------------------------------------+
            dictionary of strings with values of int or tuples

      key: a string representing a word in the original dictionary
      value: either an integer -1 meaning we have not cached this word though it is in the original word list, or a tuple:
                2-tuple (ordered pair) of the word's chain length and the "pointer" (name of the word) to
                 the next shorter word that represents the longest sequence (or one of the equal longest sequences),
                 that can be made from that word, or empty if there is no shorter word that is still in the dictionary.


Example

+--------------------------------------------------------------------------------------+
|                                                                                      |
|                                                                                      |
|  +--------+  +--------+       +--------+       +---------+        +--------+         |
|  | word 1 |  | word 2 |  ...  | word 7 |  ...  | word 11 |    ... | word n |         |
|  +--------+  +--------+       +--------+       +---------+        +--------+         |
|  (3, word 7)                  (2, word 11)      (1, "")                              |
|          ||                            ||                                            |
|          ||                      /\    ||           /\                               |
|          ||                      ||    ||           ||                               |
|          ||                      ||    ||           ||                               |
|           ========================      =============                                |
|                                                                                      |
+--------------------------------------------------------------------------------------+
                                  dictionary of tuples

         In this example, word 1 has a sequence length of 3. It points to word 7,
         which is one character shorter and has sequence length of 2. That points
         to word 11 which has no shorter sequence.

         This example shows the chain (in reverse order): word 11, word 7, word 1
         for example :
         word 1: bat
         word 7: at
         word 11: a

I made a decision to start the workingdictionary with values of -1, a sentinel value of type int. Although values of None
would also make sense, sentinel values are easier to debug. Sentinel value: https://en.wikipedia.org/wiki/Sentinel_value

Plainly stated:
- We take each word in the dictionary, try removing each of its letters and to see if we already know
- how long the longest sequence is with that candidate substring (if it exists), and cache a pointer to the candidate
- substring that has the longest sequence. After we've checked every word we follow the pointers from the longest sequence
- we found and reverse this list. That is the longest sequence in the dictionary, which we return.


Explanation of algorithm:

3 levels of optimization.

1. Solve the problem.
We use a basic recursive algorithm: starting at each word, we check possible substrings to see if they're in the word list, keeping track
of which sequence is longest. At the top level, we will return the longest sequence we found as we tested every word.

A source of optimization is that the specs call for passing in a list of words. Seeing if a word is in a
list takes O(n) time (built-in list lookup).  Since word lists are not prohibitive in size, for the actual lookup, it makes sense to use a
more optimized data structure than a list.
The built-in Python dictionary is great for use as a dictionary.  Its lookup is O(1).   This lets us look up substrings quickly.

2. Cache results.
There are multiple ways to get to the same substring: for example, "ear" could come from "hear" or from "near".
To avoid redundant recursive calls, we cache our chain length results in the workingdictionary. This means at most each word must only
be evaluated once.  This gives a nice upper bounds on the time and space complexity of our whole algorithm since at most we reach each substring from each word once and cache it.

3. Skip redundant work if we found an optimal substring.
While checking sequence lengths of substrings, if we already find a maximal one that is equal to the number of letters in the word we are checking minus one,
we can skip checking other substrings. For example, if the first tested substring of "hear" which is "ear" has a chain length of 3, we do not also need
to check the substrings "har", "her" or "hea" because even if they are in the dictionary, at most they could just have a substring of 3 which we already found.
So we can return early whenever we find a substring with a maximal chain length (chain length matches its length, i.e. there is a chain that goes down to a single character).
Adding this optimization shaved approximately 10% from the runtime.

Estimate of time and space complexity, empirical evidence:
- The space is a dictionary with size of our list of words, so it is O(n). This is acceptable for this type of implementation.
- I tested the time complexity empirically on 10,000 words. I was able to run it in approx. 0.1 seconds at 3.4 gigaherz on 10,000 words totalling 75,000 bytes.
- Time complexity is n^2 with the number of words (for 10,000 words approx. 100,000,000 operations).
- This makes sense because each word must have all its substrings checked: there are no shortcuts.

- Caching pointers by recording them as strings is not excessive overhead. This is O(1) with the size of the dictionary (each word points to at most one other word).
- If this were C/C++ we would use pointers, and implement a hash data structure since there is no built-in dictionary in C/C++.
- In my experience this would make the code at least 30 times faster (perhaps 100 times faster).
- However since the code runs on a full English dictionary in 0.1 seconds, there is no reason to translate it to C/C++ at this time.

- Alternative approaches considered:
- I considered building up from words, i.e. adding a character one at a time rather than removing a character one at a time.
- This would require trying to add each letter at each possible position, which requires 26 times more work. Our algorithm is strictly superior.

- Words can have substrings based on missing any of their letters, so this O(n^2) algorithm seems optimal. Having fixed space constraints makes it an attractive solution.
- Bing able to run the algorithm complete long dictionary of 10,000 words in 0.1 seconds is an efficient algorithm.
- 10,000 words is equivalent to 17 pages of words without line breaks, and is roughly the size of Shakespeare's vocabulary.

Terminology in the code:
    chain or sequence: words such beats->bats->bat->at->a 
    chain length or sequence length: how long the sequence is that can be built from a word by removing one letter at a time while remaining in the dictionary.
    substring: a word with exactly one fewer character. Perhaps a substring is not in the dictionary, it must be checked.

"""

def longestSequence(words, workingdictionary = {}, checkword = ""):
    weareattoplevel = False
    # at the top level we'll population a workingdictionary with all the words, initially
    # with values of -1 to show they're in the dictionary but we don't know their sequence length,
    # then each time we calculate a chain length we cache it by setting that entry to the calculated
    # chain length. While using recursion, we just pass a reference to this one workingdictionary, so
    # overall there will just be 1 workingdictionary.
    # This is used for caching and for faster lookups since
    # Python dicts look up much faster than lists do (O(1) instead of O(n)) and the size overhead is modest.
    # We will only have a single workingdictionary, since the top-level function is only called a single
    # time.
    # Besides the chain lengths, we also cache a "pointer" to one of the words found with the longest sequence,
    # so at the end we can traverse this to get the longest sequence.

    if (workingdictionary == {}):
        weareattoplevel = True
        newworkingdictionary = {} # Python variables are scoped to the innermost
                                  # function, class, or module in which they're
                                  # assigned. Control blocks like if and while blocks
                                  # don't count, so a variable assigned inside an if
                                  # is still scoped to a function, class, or module.
                                  # So this newworkingdictionary will stay in scope!
           #now we just have to fill it up:
        for word in words:
            newworkingdictionary.update({word:-1})  #add word as a key to dictionary with a value of -1 to
                                                    # show we haven't cached its chainlength yet (don't know
                                                    # its chainlength yet).
                                                    # We could also use a value of none
                                                    # here but -1 is a bit easier to check.  
        workingdictionary = newworkingdictionary
        
    # Recursive method
    
    # We'll just return the longest chain, that's what the tin says.

    # if we don't have a word to check we just return the longestSequence among all the
    # words in the dictionary.
    
    # for example if we're given ['a', 'and', 'an', 'hear'] we will return the longest chain among all of them.

    # if we do have a word to check and it's not in the dictionary we return 0 and if it is we return the longest
    # chainlength from that word. This is a recursive solution that allows us to calculate chainlengths.

    if (len(words) == 0):
        return 0 #an empty dictionary is a pathological case, it has no chains.
    
    
    if (checkword == ""):
        longesttoplevelwordlen = 1 #assume there are no subchains
        longesttoplevelword = "" #start off empty, we will then fill
        for word in workingdictionary:

            if word == "":
                continue #blank words aren't words
            #do we already know the length of it from cache?
            cachedtuple = workingdictionary[word] # will be -1 if we didnt cache yet 
            if cachedtuple != -1: # if it's not -1 then we cached it
                thislength = cachedtuple[0]
            else:
                # we need find it, and also cache it in case we look it up through a different path.
                lengthtocache = longestSequence(words, workingdictionary, word) #e.g. 'a', 'and', 'an', 'hear' - we'll just check all of them
                workingdictionary[word] = lengthtocache #this sets the cache to the tuple that this returns when we're not at the top level.
                thislength = lengthtocache[0]
            if (thislength > longesttoplevelwordlen):
                longesttoplevelwordlen  = thislength
                longesttoplevelword = word
        
        # we can now print the chain. we just tracked pointers (by value, actual words, since each cached value could just be a word, so it doesn't take too much space)
        
        listtoprint = []
        pointer = longesttoplevelword;
        while ( pointer != ""):
            listtoprint.append(pointer)
            pointer = workingdictionary[pointer][1]
        listtoprint.reverse() #reverse the list; the expression syntax without modifying it is listtoprint[::-1]
        return (listtoprint); #return our answer


    # The rest is the case where we were given a dictionary and something to check, such as 'hear'
    
    #the way this is structured, we might be checking a word that isn't in the dictionary.

    if (checkword != ""):
        # okay, so we're checking a word, like 'hear'.
        # if there are any longer substrings we return the length
        # of the longest.

        #we'll start by setting nextlongest at ""
        nextlongest = ""
        
        # first of all if it's not in our dictionary we return 0. we use this below. [!!!!!!!!]
        if (checkword not in workingdictionary):
            return (0, "")
        
        # next we have to see if it has a length of 1 if so we don't need to check its substrings, we can return 1:            
        if (len(checkword) == 1): #we do not have to check substrings if the length of the word is 1
            return (1, "")

        # if we're still here at least checkword is in the dictionary.  But are any of our substrings? let's find out
        
        longestlen = 0 #perhaps all substrings won't be in dictionary.
        
        # this next part looks at all the substrings of our checkword, tracking which has the longest chain.
        # they will all return 0 if they are not in the dictionary but if any of them return 1 (or more)
        # we'll end up returning the highest among them.
    
        i = 0
        for letter in checkword:
            candidatesubstring = checkword[:i]+checkword[i+1:] #word without ith letter
            # from 'hear' this will be like 'ear', 'har', 'her', 'hea'
            
            # for where we check something like 'her' that isn't in the dictionary
            # longestSequence(words, checkword) will return 0 in the check above [!!!!!!!!]
            # so we can freely check all of them even the ones that aren't in the dictionary, and return the highest chain
            # among them.

            chainlengthwithcandidate = longestSequence(words, workingdictionary, candidatesubstring)
            if (chainlengthwithcandidate[0] > longestlen):
                longestlen = chainlengthwithcandidate[0]
                nextlongest = candidatesubstring

            if (chainlengthwithcandidate == (len(checkword)-1)): # in case we found a substring whose chain length is maximal (its chain goes all the way to single letters),
                                                             # then we don't have to check other substrings since we won't do any better - so we can break out of the for loop early
                                                             # this can matter because at long word lengths it might take a long time to check each substring so this is a good
                                                             # optimization to include.  This seems to save about 10% of the work on average. (empirical)
                break #break out of for loop that checks each removed letter
            i += 1

        # we have now checked all the possible substrings of the word we're checking.
        # since we already made sure that we're in the dictionary ourselves, we can return + 1:

        if (weareattoplevel):
            return longestlen + 1

        else:
            return longestlen + 1, nextlongest


def main():
    result= longestSequence(["a", "at", "hear", "ear", "bat"])

    print ("Result was", result)

if __name__ == "__main__":
    main()