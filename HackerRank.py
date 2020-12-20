########### Frequency queries############
# You are given  queries. Each query is of the form two integers described below:
# -  : Insert x in your data structure.
# -  : Delete one occurence of y from your data structure, if present.
# -  : Check if any integer is present whose frequency is exactly . If yes, print 1 else 0.

# The queries are given in the form of a 2-D array  of size  where  contains the operation, 
# and  contains the data element. 

# using arrays, need to optimize

from collections import defaultdict

def fQuery(queries):
    """takes in queries, outputs array of 0,1 based on answers to queries that start with 3"""

    l, result = [], []
    for (a, b) in queries:
        if a == 1:
            l.append(b)
        elif a == 2:
            if b in l:
                l.remove(b)
        else:
            # look through l and append 1 if count is exactly b
            # if not, append 0
            x = len(result)
            for item in l:
                if l.count(item) == b:
                    result.append(1)
                    break # will continue with next line
            y = len(result)
            if x == y:
                result.append(0)

    return result


# using dict, still need to optimize
def frQuery(queries):
    """takes in queries, outputs array of 0,1 based on answers to queries that start with 3"""
    d = {}
    result = []

    for (a, b) in queries:
        if a == 1:
            if b not in d:
                d[b] = 1
            else:
                d[b] += 1
     
        elif a == 2:
            if b in d and d[b] >= 1:
                d[b] -= 1

        else:
            # look through key-value pairs; if b in d.values(), append 1, else append 0
            if b in d.values():
                result.append(1)
            else:
                result.append(0)

    return result


# using 2 dict, one for freq-num; one for num-freq, otherwise lookup for freq takes too long as a value
def freqQuery(queries):
    """takes in queries, outputs array of 0,1 based on answers to queries that start with 3"""
    results = []
    d = {}
    freqs = defaultdict(set) # initalized with freq as key and empty set as default value

    for command, num in queries:
        # freq is value of key num in d
        freq = d.get(num, 0)
        if command == 1:
            # d is dict with num as key and freq as value, adding 1 to value
            d[num] = freq + 1
            # freqs is dict with freq as key and num as value
            freqs[freq].discard(num)
            # store num as value for a freq that is greater by 1
            freqs[freq + 1].add(num)
        elif command == 2:
            # subtract one from value of key num in d. if none, then value is set to 0
            d[num] = max(0, freq - 1)
            freqs[freq].discard(num)
            # reassign num to one less freq value
            freqs[freq - 1].add(num)
        elif command == 3:
            results.append(1 if freqs[num] else 0)

    return results
