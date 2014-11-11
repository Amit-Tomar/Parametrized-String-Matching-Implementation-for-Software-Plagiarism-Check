'''
Created on Nov 10, 2013

@author: ravali soma
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
    EXP2 = arity_exp
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
    if child_index != 0:
        return (child_index-1)>>EXP2
    else:
        return None
    
def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    if((parent_index<<EXP2)|1)<len(DATA):
        return (parent_index<<EXP2)|1
    else:
        return None

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    if(get_leftmostchild_index(parent_index)>len(DATA)-1):
        return None
    elif((parent_index+1<<EXP2)>len(DATA)-1):
        return len(DATA)-1
    else:
        return (parent_index+1<<EXP2)

def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    ''' 
    l_index = get_leftmostchild_index(parent_index)
    r_index = get_rightmostchild_index(parent_index)
    minimum = get_leftmostchild_index(parent_index)
    maximum = get_rightmostchild_index(parent_index)
    if(MIN_TOP == True):
        for j in range(l_index, r_index+1):
            if CMP_FUNCTION(DATA[j], DATA[minimum])==-1:
                minimum = j
        return minimum
    else:
        for i in range(l_index , r_index+1):
            if CMP_FUNCTION(DATA[i], DATA[maximum])==1:
                maximum = i
        return maximum

def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    if(MIN_TOP == True):
        while(get_leftmostchild_index(i) is not None):
            top_child = get_top_child(i)
            if(top_child is not None and CMP_FUNCTION(DATA[i] , DATA[top_child]) == 1):
                DATA[top_child] , DATA[i] = DATA[i] , DATA[top_child]
                i = top_child
            else:
                break    
            
    else:
        while(get_leftmostchild_index(i) is not None):
            top_child = get_top_child(i)
            if(top_child is not None and CMP_FUNCTION(DATA[i] , DATA[top_child])==-1):
                DATA[top_child] , DATA[i] = DATA[i] , DATA[top_child]
                i = top_child
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
    res_heap = i
    if (MIN_TOP == True):
        while(res_heap>0 and res_heap is not None):
            res_heap = get_parent_index(i)
            if (CMP_FUNCTION(DATA[res_heap] , DATA[i]) == 1):
                DATA[res_heap] , DATA[i] = DATA[i] , DATA[res_heap]
                res_heap = i
            else:
                break
        restore_subtree(i)
    else:            
        while(res_heap>0 and res_heap is not None):
            res_heap = get_parent_index(i)
            if (CMP_FUNCTION(DATA[res_heap] , DATA[i]) == -1):
                DATA[res_heap] , DATA[i] = DATA[i] , DATA[res_heap]
                res_heap = i
            else:
                break
        restore_subtree(i)  
           
def heapify():
    
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    len_size = len(DATA)-1
    while(len_size > 0):
        restore_heap(len_size)
        len_size = len_size - 1
    
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    DATA[i] , DATA[len(DATA)-1] = DATA[len(DATA)-1] , DATA[i]
    ele = DATA.pop()
    heapify()
    return ele
        
def pop():
    '''
    Pull the top element out of the heap
    '''
    ele = remove(0)
    return ele    
    
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
    for ele in lst:
        DATA.append(ele)
    
def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    DATA = []
        
if __name__ == '__main__':
    pass
    