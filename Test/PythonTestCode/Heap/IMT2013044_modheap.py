'''
Created on 28-Oct-2013

@author: raghavan
'''
MIN_TOP = False # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

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
    '''
    Return the size of the heap
    '''
    # Your code
    return len( DATA )

def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    # Your code
    return 2**EXP2
    
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
    parent_index = ( child_index - 1 ) >> EXP2
    if( parent_index >= 0):
        return parent_index
    else:
        return None

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    leftmost_child = ( parent_index << EXP2 ) + 1
    if ( leftmost_child < size() ):
        return leftmost_child
    else:
        return None

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    count = 1
    leftmost_child = get_leftmostchild_index(parent_index)
    if ( leftmost_child !=None ):
        while ( count < arity() ):
            rightmost_child = leftmost_child + 1
            if ( rightmost_child >= size() ):
                return leftmost_child
            else:
                leftmost_child = rightmost_child
            count = count + 1
    else:
        return None
    if(count==arity()):
        return rightmost_child

def get_top_child(parent_index):
    '''
    Return the index of the child which is most favored to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
    child_index = ( parent_index << EXP2 ) + 1
    if(child_index < size()):
        count = child_index
        min_child = DATA[child_index]
        max_child = DATA[child_index]
        if ( MIN_TOP==True ):
            while ( child_index <= count + arity() - 1 \
                    and child_index < size()):
                if ( CMP_FUNCTION(DATA[child_index], min_child)==0 \
                     or CMP_FUNCTION(DATA[child_index], min_child)==-1 ):
                    min_index = child_index
                    min_child = DATA[min_index]
                child_index = child_index + 1
            return min_index
    
        else:
            while ( child_index <= count + arity() - 1 \
                    and child_index < size()):
                if ( CMP_FUNCTION(DATA[child_index], max_child)==0 \
                     or CMP_FUNCTION(DATA[child_index], max_child)==1 ):
                    max_index = child_index
                    max_child = DATA[max_index]
                child_index = child_index + 1
            return max_index
    else:
        return None

def restore_subtree(i):
    '''global MIN_TOP, CMP_FUNCTION, EXP2, DATA
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    child_index = get_top_child(i)
    if ( child_index!=None ):
        if ( MIN_TOP==True ):
            if ( CMP_FUNCTION(DATA[i], DATA[child_index])==1 ):
                DATA[i] , DATA[child_index] = DATA[child_index] , DATA[i]
            restore_subtree(child_index)
        else:
            if ( CMP_FUNCTION(DATA[i], DATA[child_index])==-1 ):
                DATA[i] , DATA[child_index] = DATA[child_index] , DATA[i]
            restore_subtree(child_index)
            
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code
    count = 0
    parent_index = get_parent_index(i)
    original_i = i
    if ( MIN_TOP==True ):
        while ( i!=0 ):
            parent_index = get_parent_index(i)
            if ( CMP_FUNCTION(DATA[i], DATA[parent_index])==-1 ):
                DATA[i] , DATA[parent_index] = DATA[parent_index] , DATA[i]
                count = count + 1
                i = parent_index
            else:
                break
        restore_subtree(i)
    else:
        while ( i!=0 ):
            parent_index = get_parent_index(i)
            if ( CMP_FUNCTION(DATA[i], DATA[parent_index])==1 ):
                DATA[i] , DATA[parent_index] = DATA[parent_index] , DATA[i]
                count = count + 1
                i = parent_index
            else:
                break
        restore_subtree(i)           
    if ( count == 0 ):
        restore_subtree(original_i)
         
def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    parent_index = ( size() - 1 - 1 ) >> EXP2
    while (parent_index >= 0):
        restore_subtree(parent_index)
        parent_index = parent_index - 1
    
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    global DATA
    DATA[i], DATA[size()-1]=DATA[size()-1], DATA[i]
    element = DATA[size()-1]
    DATA = DATA[:size()-1]
    return element
    
def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    element = remove(0)
    heapify()
    return element

def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    # Your code
    DATA.append(obj)
    heapify()
    
def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    # Your code
    for i in lst:
        DATA.append(i)

def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    DATA = []

if __name__ == '__main__':
    pass