from current import longestSequence
with open("wordlist.10000.txt") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

#print ("Testing longestSequence")
import time

start = time.time()

print("The longest chain in wordlist.10000.txt is", longestSequence(lines))


end = time.time()
print(end - start, "seconds")