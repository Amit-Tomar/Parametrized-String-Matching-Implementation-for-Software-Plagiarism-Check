import math
'''
Created on 28-Oct-2013

@author: raghavan
'''

MIN_TOP = False 
# Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1 

# The list of elements organized as a heap
DATA = []

def initialize_heap(is_min = True, arity_exp = 1, compare_fn = None):
    global MIN_TOP, CMP_FUNCTION, EXP2, DATA
    MIN_TOP = is_min
    CMP_FUNCTION = compare_fn
    EXP2 = arity_exp
    DATA = []


def size():
    '''
    Return the size of the heap
    '''
    # Your code
    length = len(DATA)
    return length
    


def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    # Your code
    return 2 ** EXP2
    
    
def get_item_at(i):
    '''
    Return the i-th element of the data list (DATA)
    '''
    return DATA[i]


def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    # Your code
    arit = arity()
    parent_index = (child_index-1)//arit
    if(parent_index >= 0):
        return parent_index
    else:
        return None

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    rc = get_rightmostchild_index(parent_index)
    if(rc == None):
        return None
    global DATA
    ar = arity()
    size = len(DATA)
    a = ( ar * parent_index ) + 1
    if(a < size):
        return a
    else:
        return None

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    global DATA
    ar = arity()
    size = len(DATA)
    b = 0
    a = ( ar * parent_index ) + 1
    if(a < size):
        b = a
    else:
        b = None
    size = len(DATA)
    a = ( ar * parent_index ) + ar
    while( a > b ):
        if( a < size ):
            return a
        else:
            ar -= 1
            a = ( ar * parent_index ) + ar
    return None


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
    global DATA , MIN_TOP
    lc = get_leftmostchild_index(parent_index)
    rc = get_rightmostchild_index(parent_index)
    
    if(MIN_TOP == False):
        i = lc
        max_val = DATA[lc]
        max_index = lc
        while(i <= rc):
            if DATA[i] > max_val:
                max_val = DATA[i]
                max_index = i
            i += 1
        return max_index
    else:
        i = lc
        min_val = DATA[lc]
        min_index = lc
        while(i <= rc):
            if DATA[i] < min_val and DATA[i] != -1:
                min_val = DATA[i]
                min_index = i
            i += 1
        return min_index
    
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    heapify()
    
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code
    global DATA,MIN_TOP
    a = 1
    l = len(DATA)
    ar = arity()
    while(l>0):
        if(l == 2):
            a = 0
            DATA.append(-1)
            break
        l -= ar
    lc , rc = get_leftmostchild_index(i) , get_rightmostchild_index(i)
    if( lc != None and rc != None ):
        if(MIN_TOP == False):
            j = get_top_child(i)
            while(DATA[i] < DATA[j]):
                DATA[i] , DATA[j] = DATA[j] , DATA[i]
                i = j
                lc , rc = get_leftmostchild_index(i) , get_rightmostchild_index(i)
                if(lc == None or rc == None):
                    break
                else:
                    j = get_top_child(i)
        else:
            j = get_top_child(i)
            while(DATA[i] > DATA[j]):
                DATA[i] , DATA[j] = DATA[j] , DATA[i]
                i = j
                lc , rc = get_leftmostchild_index(i) , get_rightmostchild_index(i)
                if(lc==None or rc==None):
                    break
                else:
                    j = get_top_child(i)
                
            
    if(a == 0):
        DATA = DATA[:len(DATA)-1]
        
def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    l = len(DATA)-1
    ar = arity()
    i = int(math.floor(l/ar))
    while(i >= 0):
        restore_heap(i)
        i -= 1
          
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    DATA[i] , DATA[len(DATA)-1] = DATA[len(DATA)-1] , DATA[i]
    return DATA.pop()


def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    global DATA
    DATA[0] , DATA[len(DATA)-1] = DATA[len(DATA)-1] , DATA[0]
    a = DATA.pop()
    heapify()
    return a


def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    # Your code
    DATA.append(obj)
    heapify()
def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    DATA = []

def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    # Your code
    for i in lst:
        DATA.append(i)


if __name__ == '__main__':
    pass