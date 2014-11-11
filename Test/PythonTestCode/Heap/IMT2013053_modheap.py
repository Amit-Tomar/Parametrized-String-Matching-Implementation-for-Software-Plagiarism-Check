'''
Created on 28-Oct-2013

@author: raghavan
'''
MIN_TOP = False 
# Says whether the heap is a Min-Heap (True) or a Max-Heap (False)
# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and 
#returns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None
# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1
# The list of elements organised as a heap
DATA = []

def initialize_heap(is_min = True, arity_exp = 1, compare_fn = None):
    '''
    Initialising heap variable
    '''
    global MIN_TOP, CMP_FUNCTION, EXP2, DATA
    MIN_TOP = is_min
    CMP_FUNCTION = compare_fn
    EXP2  = arity_exp
    DATA = []

def size():
    '''
    Return the size of the heap
    '''
    return len(DATA)

def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
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
    if child_index == 0:
        #To ensure the child index is not the root of heap                     
        return None
    return (child_index-1)>>EXP2

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    if (parent_index<<EXP2)+1>len(DATA):
        #To check whether the parent has any children or not
        return None
    return (parent_index<<EXP2)+1
    
def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    if ((parent_index<<EXP2)+1) > (len(DATA)-1):
        #To check if the parent has a child
        return None
    elif (((parent_index+1)<<EXP2))>(len(DATA)-1):
        #If the parent has less children, return the last child
        return len(DATA)-1
    else:
        return (parent_index+1)<<EXP2

def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    favoured_child = (parent_index<<EXP2)+1
    #Initialising the variable to the index of the leftmost child of the parent
    for i in range((parent_index<<EXP2)+1,((parent_index+1)<<EXP2)+1 ):
        if MIN_TOP:
            if CMP_FUNCTION(DATA[i], DATA[favoured_child])==-1:
                favoured_child = i
        else:
            if CMP_FUNCTION(DATA[i], DATA[favoured_child])==1:
                favoured_child = i
    return favoured_child

def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    while(get_rightmostchild_index(i) is not None):
        minimum = get_leftmostchild_index(i)
        maximum = get_leftmostchild_index(i)
        #The variables store index of min and max child of each level of heap
        for j in range(get_leftmostchild_index(i), get_rightmostchild_index(i)+1):
            if CMP_FUNCTION(DATA[j], DATA[minimum])==-1:
                minimum = j
            if CMP_FUNCTION(DATA[j], DATA[maximum])==1:
                maximum = j
        if MIN_TOP:
            if CMP_FUNCTION(DATA[i], DATA[minimum])==1:
                DATA[i], DATA[minimum] = DATA[minimum], DATA[i]
                i = minimum
            else:
                break 
        else:
            if CMP_FUNCTION(DATA[i], DATA[maximum])==-1:
                DATA[i], DATA[maximum] = DATA[maximum], DATA[i]
                i = maximum
            else:
                break
    
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    if MIN_TOP:
        if (get_parent_index(i) is not None and CMP_FUNCTION(DATA[get_parent_index(i)], DATA[i])==1):
            while (CMP_FUNCTION(DATA[get_parent_index(i)], DATA[i])==1 and get_parent_index(i)>0):
                DATA[get_parent_index(i)], DATA[i] = DATA[i], DATA[get_parent_index(i)]
                i = get_parent_index(i)
        else:
            restore_subtree(i)
    else:
        if (get_parent_index(i) is not None and DATA[get_parent_index(i)]<DATA[i]):
            while (CMP_FUNCTION(DATA[get_parent_index(i)], DATA[i])==-1 and get_parent_index(i)>0):
                DATA[get_parent_index(i)], DATA[i] = DATA[i], DATA[get_parent_index(i)]
                i = get_parent_index(i)
        else:
            restore_subtree(i)            
        
def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    parent = get_parent_index(len(DATA)-1)
    while(parent >-1):
        restore_subtree(parent)
        parent = parent-1
        #Changing the parent each time
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    DATA[i], DATA[-1] = DATA[-1], DATA[i]
    DATA.pop()
    restore_subtree(i)
    
def pop():
    '''
    Pull the top element out of the heap
    '''
    to_be_poped = DATA[0]
    remove(0)
    return to_be_poped
    
def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    DATA.append(obj)
    heapify()

def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    # Your code
    for element in lst:
        add(element)
    
def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    DATA = []

if __name__ == '__main__':
    pass