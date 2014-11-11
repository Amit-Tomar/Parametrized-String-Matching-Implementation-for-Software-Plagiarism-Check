'''
Created on 28-Oct-2013

@author: raghavan
'''
MIN_TOP = False # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)
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
    EXP2  = arity_exp
    DATA = []

def size():
    '''
        Return the size of the heap
    '''
    # Your code
    return len(DATA)

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
    if child_index == 0:
        return None
    return (child_index-1)>>EXP2

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    if (parent_index<<EXP2)+1<len(DATA):
        return (parent_index<<EXP2)+1
    return None
    
def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    if ((parent_index<<EXP2)+1) > (len(DATA)-1):
        return None
    elif (((parent_index+1)<<EXP2))>(len(DATA)-1):
        return len(DATA)-1
    else:
        return (parent_index+1)<<EXP2

            
def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
    mins = (parent_index<<EXP2)+1
    for i in range((parent_index<<EXP2)+1,((parent_index+1)<<EXP2)+1):
        if MIN_TOP:
            if CMP_FUNCTION(DATA[i], DATA[mins])==-1:
                mins = i
        else:
            if CMP_FUNCTION(DATA[i], DATA[mins])==1:
                mins = i
    return mins

def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    newroot = i
    while(get_rightmostchild_index(newroot) is not None):
        minx = get_leftmostchild_index(newroot)
        maxx = get_leftmostchild_index(newroot)
    
        for j in range(get_leftmostchild_index(newroot), get_rightmostchild_index(newroot)+1):
            if CMP_FUNCTION(DATA[j], DATA[minx])==-1:
                minx = j
            if CMP_FUNCTION(DATA[j], DATA[maxx])==1:
                maxx = j
        if MIN_TOP:
            if CMP_FUNCTION(DATA[newroot], DATA[minx])==1:
                DATA[newroot], DATA[minx] = DATA[minx], DATA[newroot]
                newroot = minx
            else:
                break 
        else:
            if CMP_FUNCTION(DATA[newroot], DATA[maxx])==-1:
                DATA[newroot], DATA[maxx] = DATA[maxx], DATA[newroot]
                newroot = maxx
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
    # Your code
    
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
    # Your code
    parent = get_parent_index(len(DATA)-1)
    while(parent >-1):
        restore_subtree(parent)
        parent = parent-1
    
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    DATA[i], DATA[-1] = DATA[-1], DATA[i]
    DATA.pop()
    restore_subtree(i)
    
def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    
    to_be_poped = DATA[0]
    remove(0)
    return to_be_poped
    

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
    heapify()
    

def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    DATA=[]

if __name__ == '__main__':
    pass