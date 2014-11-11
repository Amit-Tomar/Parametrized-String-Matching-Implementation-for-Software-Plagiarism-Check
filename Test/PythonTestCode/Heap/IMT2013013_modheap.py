'''
Created on Oct 31, 2013

@author: imt2013013
'''

MIN_TOP = True # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and returns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
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
    '''#
    Return the size of the heap
    '''
    return len(DATA)


def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    arity = 2**EXP2
    return arity
   
   
def get_item_at(i):
    '''
    Return the i-th element of the data list (DATA)
    '''
    if(i >= size()):
        return None
    else:
        return DATA[i]


def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    if(child_index <= 0 or child_index > size()):
        return None
    else:
        return ((child_index-1) >> EXP2)


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    #if(MIN_TOP):
    if (parent_index is None):
        return None
    else:
        if((parent_index << EXP2)+1 >= size()):
            return None
        else:
            return (parent_index << EXP2)+1
    

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    if(parent_index is None or get_leftmostchild_index is None):
        return None
    elif (((parent_index) << EXP2) + arity()) <= (size()-1):
        return ((parent_index << EXP2) + arity())
    else:
        return size()-1
    

def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    a = get_leftmostchild_index(parent_index)
    b = get_rightmostchild_index(parent_index)
    minx = a
    maxx = a
    if a is None:
        return None
    else:
        if(MIN_TOP):
            for x in range(a , b+1):
                if(CMP_FUNCTION(DATA[minx] , DATA[x]) is 1):
                    minx = x
            return minx
        else:
            for y in range(a , b+1):
                if(CMP_FUNCTION(DATA[maxx] , DATA[y]) is -1):
                    maxx = y
            return maxx
          

def restore_subtree(i):
    
    ''' Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property'''
    
    a = get_leftmostchild_index(i)
    b = get_top_child(i)
    if(MIN_TOP):
            while(a is not None and i is not None and b is not None):
                if(CMP_FUNCTION(DATA[i] , DATA[b]) is 1):
                    DATA[b],DATA[i]=DATA[i] , DATA[b]
                    i = b
                    a = get_leftmostchild_index(i)
                    b = get_top_child(i)
                else:
                    break
    else:
            while(a is not None and i is not None and b is not None):
                if(CMP_FUNCTION(DATA[i] , DATA[b]) is -1):
                    DATA[b] , DATA[i] = DATA[i] , DATA[b]
                    i = b
                    a = get_leftmostchild_index(i)
                    b = get_top_child(i)
                else:
                    break
       
def restore_heap(i):
    
    '''Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element
    '''
    p = get_parent_index(i)
    if MIN_TOP:
        if p is not None and i is not None and CMP_FUNCTION(DATA[p] , DATA[i]) is 1:
            while(p>0 and CMP_FUNCTION(DATA[p] , DATA[i]) is 1):
                DATA[i] , DATA[p] = DATA[p] , DATA[i]
                i = p
                p = get_parent_index(i)
        else:
            restore_subtree(i)
    else:
        if p is not None and i is not None and CMP_FUNCTION(DATA[p] , DATA[i]) is -1:
            while(p>0 and CMP_FUNCTION(DATA[p] , DATA[i]) is -1):
                DATA[i] , DATA[p] = DATA[p] , DATA[i]
                i = p
                p = get_parent_index(i)
        else:
            restore_subtree(i)
   
           
def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''

    a = get_parent_index(len(DATA)-1)
    while(a >= 0):
        restore_subtree(a)
        a = a-1
    


def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    a = len(DATA)-1
    c = DATA[i]
    (DATA[a] , DATA[i]) = (DATA[i] , DATA[a])
    del DATA[a]
    heapify()
    return c

def pop():
    '''
    Pull the top element out of the heap
    '''
    return remove(0)
   

def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    DATA.append(obj)
    i = DATA.index(obj)
    restore_heap(i)
    heapify()
    

def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    
    for i in range(0 , len(lst)):
        DATA.append(lst[i])

def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    DATA = []

if __name__ == '__main__':
    #initialize_heap()
    #print get_rightmostchild_index(2)
    #print restore_heap(2)
    #print DATA
    #print get_top_child(1)
    #print get_leftmostchild_index(2)
    #print DATA
    pass
