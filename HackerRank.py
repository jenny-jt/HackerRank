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

########### Count Triplets ############
# You are given an array and you need to find number of tripets of indices
# such that the elements at those indices are in geometric progression 
# for a given common ratio. i < j < k

def countTriplets(arr, r):
    """ given arr with ratio r, return number of triplets of indices
    """
# arr: 4 2 1 
# k j i 
# j = i*2
# k = j*2
 
# 1 2 4         
# i j K 
# 0 1 2

# j = k/2
# i = j/2

    # loop through array in reverse
    # 1 5 5 25 125
    # 125 25 5 5 1
    # k = 125, j = 25, i = 5
    
    if len(arr) <= 2:
        return 0
    d_arr = {}
    d_doubles = {} # key of (j,k) tuple, value of 
    count = 0
    
    # Traversing the array from rear, helps avoid division
    for i in arr[::-1]:
        j = r*i
        k = r*j
        # case: i is the first element (i, j, k)
        count += d_doubles.get((j, k), 0)

        # case: i is the second element (i/r, i, i*r)
        d_doubles[(i, j)] = d_doubles.get((i, j), 0) + d_arr.get(j, 0)

        # case: i is the third element (i/(r*r), i/r, i)
        d_arr[i] = d_arr.get(i, 0) + 1

    return count

# according to the problem statement, it is only considered a triplet if i < j < k, from left to right, so [4, 2, 1] with r = 2 isn't a triplet.
# consider this array with a triplet: [1, 2, 4]. if you traverse it normally, you won't know if you have a triplet until you get to the third element: 4. in order to confirm this, you would check that the second element is 4/r, and that the first element is 4/r/r. this uses division
# the first bullet point in the example he gave states that he wants to avoid division (because it's expensive and can produce floating point numbers). when the array is traversed in reverse, in order to check if you have a triplet, you check that the next element was 4*r, and that the one after that was 4*r*r

# froom discussion
def countTriplets(arr, r):
    """given arr with ratio r, return number of triplets of indices
    """
    if len(arr) <= 2:
        return 0
    map_arr = {}
    map_doubles = {}
    count = 0
    # Traversing the array from rear, helps avoid division
    for x in arr[::-1]:
        r_x = r*x
        r_r_x = r*r_x

        # case: x is the first element (x, x*r, x*r*r)
        count += map_doubles.get((r_x, r_r_x), 0)

        # case: x is the second element (x/r, x, x*r)
        map_doubles[(x,r_x)] = map_doubles.get((x,r_x), 0) + map_arr.get(r_x, 0)

        # case: x is the third element (x/(r*r), x/r, x)
        map_arr[x] = map_arr.get(x, 0) + 1

######### Strings: Special String again #####
# string special if all letters same OR all letters except middle are the same

def substrCount(n, s):
    """ given s, return number of special substrings"""
    # initial count of len of s, because each letter is a special substring
    count = n
    for i, char in enumerate(s):
        diff_i = None
        for j in range(i+1, n):
            if char == s[j]:
                # if all letters same so far
                if not diff_i:
                    count +=1
                # if length before pivot equals length after pivot
                #  and letter before(char) equals letter after(s[j])
                elif j - diff_i == diff_i - i:
                    count += 1
                    break
            else:
                if not diff_i:
                    diff_i = j # setting the pivot (one char that can be diff)
                else:
                    break # one letter already is diff, can't be special if more diff
    return count


######### Stacks: Balanced Parens #####
def isBalanced(s):
    """given string, return YES if parens are balanced, and NO if parens are not balanced"""
    stack = []
    d = {"(": ")", "[": "]", "{": "}"}

    for char in s:
        if not stack:
            if char in d.values():
                return("NO")
            else:
                stack.append(char)
        # if stack (so already some open parens)
        else:
            # char is closing parens for the top open parens
            if char in d.values():
                if char == d[stack[-1]]:
                    stack.pop()
                else:
                    return("NO")
            else: 
                stack.append(char)

    if stack:
        return("NO")
    else:
        return("YES")  

