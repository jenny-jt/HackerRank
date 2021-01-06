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


########## Stacks: implement q with 2 stacks ############
class MyQueue(object):
    def __init__(self):
        """initialize q using 2 stacks"""
        # new items append to end
        self.inbound = []
        # old items removed from end
        self.outbound = [] 

    def peek(self):
        """return value at front without modifying q"""
        if not self.outbound:
            while self.inbound:
                # add inbound in reversed order to outbound
                self.outbound.append(self.inbound.pop())
        return self.outbound[-1]

    def pop(self):
        """remove value from the front"""
        self.peek()
        return self.outbound.pop()

    def put(self, value):
        """insert value at end"""
        self.inbound.append(value)


############# Stacks: Largest Rectangle ###############
def largestRectangle(h):
    """given array of heights h, return max area"""
    stack = []
    area = 0
    i = 0

    while i < len(h):
        # if stack empty or top height is less than current height
        if not stack or h[stack[-1]] <= h[i]:
            # append position
            stack.append(i)
            i += 1
        # if current height is smaller than top height
        else:
            top = stack.pop()
            # h[top] (height value) * (position now - position of top - 1)
            # area is the larger of these two values. existing area or new area
            area = max(area, h[top]*(i-stack[-1]-1 if stack else i))

    while stack:
        top = stack.pop()
        area = max(area, h[top]*(i-stack[-1]-1 if stack else i))

    return area

###### Stacks: Min Max Riddle ######

# using array, need to optimize to pass last 3 test cases
def riddle(arr):
    """given arr, return an array containing the max value of the minimums 
        for each window size
    """

    size = 0
    arr_max = []
    
    while size < len(arr):
        max_w = 0
        for i in range(len(arr)):
            if (i + 1 + size) <= len(arr):
                window = arr[i: i + 1 + size]
                w_min = min(window)
                max_w = max(max_w, w_min)
        arr_max.append(max_w)
        size += 1

    return(arr_max)


###### Recursion: Fibonacci Numbers######
def fibonacci(n):
    cache = {}

    def fib(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        if n not in cache:
            cache[n] = fib(n-1) + fib(n-2)
        return cache[n]

    return fib(n)


###### Sorting: Mark and Toys ######
def maximumToys(prices, k):
    """given list of prices and budget, return max toys"""
    # may be multiple amounts of toys per k
    # have k be key, and amounts as val
    # for prices subtract amount of price from k and look for matching price
    d = {}
    prices.sort()
    count = 0
    
    for price in prices:
        if price > k:
            break
        elif price == k:
            d[k] = price
        else:
            count += 1
            k = k - price
            continue
    return count


###### Sorting: Comoparator ######
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score
        
    def __repr__(self):
        return {"Name:", self.name, "Score:", self.score}
        
    def comparator(a, b):
        if a.score != b.score:
            # need to return -1 because sorting in desc not asc order
            if a.score > b.score:
                return -1
            else:
                return 1
        else:
            if a.name > b.name:
                return 1
            else:
                return -1


###### Sorting: Fraudulent Activity Notification ######

# need to optimize
def activityNotifications(expenditure, d):
    """return number of alerts given d trailing days and array expenditure"""
    # only need to check from index d to end of expenditure list
    # calculate median of expenditures in d
    # compare to expenditure[i]
    # initialize alert count
    alert = 0

    for i in range(d, len(expenditure)):
        # calculate median, how optimize this
        m = sum(expenditure[i-d:i])/(d/2)
        # incremenent alert if median*2 <= that day's expenditure
        if m <= expenditure[i]:
            alert += 1
            
    return alert


###### LL: Insert node at specific position ######
class Node:
    def __init__(self, data, next):
        self.data = data
        self.next = next
        
def insertNodeAtPosition(head, data, position):
    """insert data at position, given head of ll"""
    
    if position == 0:
        new = Node(data, None)
        return new
    
    curr = head
    
    for i in range(position-1):
        curr = curr.next
    
    temp = curr.next
    new = Node(data, temp)
    curr.next = new

    return head


###### LL: Insert node into sorted DLL ######
def sortedInsert(curr, data):
    new = DoublyLinkedListNode(data)

    # list is empty
    if not curr:
        return new
    elif curr.data > data:
        # if curr is bigger than data, insert new node before
        new.prev = curr.prev
        new.next = curr
        curr.prev = new
        return new
    # curr.data < data
    else:
        curr.next = sortedInsert(curr.next, data)

    return curr


###### LL: Reverse DLL ######

# recursive solution
def reverse(curr):
    """given a DLL, reverse it and return the head"""
    # the list was empty
    if not curr:
        return curr
    curr.next, curr.prev = curr.prev, curr.next
    print("curr", curr.data)
    # this means that we have reached the original tail, return where we are now
    if not curr.prev:
        print("curr at end", curr.data)
        return curr
    # if not, keep swapping prev and next
    print("curr prev", curr.prev.data)
    return reverse(curr.prev)

# iterative solution
def reverse(head):
    """given a DLL, reverse it and return the head"""
    curr = temp = head
    while curr:
        curr.prev, curr.next = curr.next, curr.prev
        temp = curr
        curr = curr.prev
    return temp


###### LL: intersection ######
def findMergeNode(head1, head2):
    """given 2 ll, return data value of intersecting node. otherwise return none"""
    # find lengths and tails of each list
    # advance longer list by the diff in lengths
    curr1 = head1
    curr2 = head2
    len1, len2, diff = 0, 0, 0
    
    while curr1:
        len1 += 1
        curr1 = curr1.next
        
    while curr2:
        len2 += 1
        curr2 = curr2.next
    
# if tails not same, then no intersection
    if curr1 != curr2:
        return
    
# if diff lengths, find diff   
    if len1 - len2 != 0:
        diff +=  (len1 - len2)
        print("diff", diff, "l1", len1, "l2", len2)
        
# reset to beginning
    curr1 = head1
    curr2 = head2
    
# if diff lengths:
    # if 1 longer than 2
    if diff > 0:
        for i in range(diff):
            curr1 = curr1.next
    # if 2 longer than 1
    if diff < 0:
        for i in range(abs(diff)):
            curr2 = curr2.next
        
    # traverse lists from this starting point. when curr1 and curr2 are equal, then return that value
    while curr1 and curr2:
        if curr1 == curr2:
            return curr1.data
        curr1 = curr1.next
        curr2 = curr2.next


###### LL: cycle ######
def has_cycle(head):
    """given random ll, return true if contains cycle, otherwise return false"""

    # use 2 pointers, one slow and one fast
    # start fast one on the second node, otherwise will always return true
    curr1 = head.next
    curr2 = head

    # if 2 pointers end up at the same point eventually, then return True
    # will never reach none if there is a cycle
    while curr1 and curr2:
        if curr1 == curr2:
            return True
        curr1 = curr1.next
        curr2 = curr2.next.next

    return False


###### Greedy: Minimum Absolute Difference in Array ######
def minimumAbsoluteDifference(arr):
    """given arr of ints, return min absolute diff"""
    # if sort, then least is probably between first and second elements
    arr.sort()
    min_diff = abs(arr[0] - arr[1])
    for i in range(len(arr)-1):
        a_diff = abs(arr[i]-arr[i+1])
        min_diff = min(min_diff, a_diff)

    return min_diff


###### Tree: Height of Binary Tree ######
# class TreeNode:
#       def __init__(self,info):
#           self.info = info
#           self.left = None
#           self.right = None

def height(root):
    """given tree, return height as int"""
    if not root:
        return -1
    # max of either left or right subtrees, plus the root level
    return(max(height(root.left), height(root.right)) + 1)


###### Tree: BST:  Lowest Common Ancestor ######
def lca(root, v1, v2):
    """given ref to root, find the lca of v1 and v2, return reference to lca"""
    if root is None:
        return None
    # if root is smaller than v1 and v2, check right node
    if root.info < v1 and root.info < v2:
        return lca(root.right, v1, v2)
    # if root is bigger than v1 and v2, check left node
    if root.info > v1 and root.info > v2:
        return lca(root.left, v1, v2)
    # if root is in between v1 and v2, because BST, then is lca
    return root

###### Tree: is BST ######
class node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def checkBST(node, lv=None, rv=None):
    if not node:
        return True
    # if curr (L) node data is bigger or equal to parent node's data:
    if lv and node.data >= lv: 
        return False
    # if curr (R) node data is smaller or equal to parent node's data:
    if rv and node.data <= rv:
        return False
    # otherwise, check left node and right node
    # checking node.left, set left value to current node data
        # if value of node.left is larger than current node data, then return False
    # checking node.right, set right value to current node data
        # if value of node.right is smaller than current node data, then return False
    return checkBST(node.left,node.data,rv) and checkBST(node.right,lv,node.data)