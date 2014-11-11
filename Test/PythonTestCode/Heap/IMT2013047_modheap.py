'''
Created on 28-Oct-2013

@author: Veda
'''

MIN_TOP = False # Says whether the heap is 
#a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments
# and retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA = []

def initialize_heap(is_min = True, arity_exp = 1, compare_fn = None):
    '''
    initializes the heap
    '''
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
    return pow(2, EXP2)
    
    
    
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
    
    parent_index = (child_index-1) >> EXP2
    if(parent_index >= 0):
        return parent_index
        
    else:
        return None
    

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    lastelement_index = len(DATA)-1
    finalparent_index = get_parent_index(lastelement_index)
    
    if(parent_index>finalparent_index):
        return None
    
    else:
        leftmostchild_index = (parent_index << EXP2) + 1
        return leftmostchild_index

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    
    temp_arity = arity()

    if(get_leftmostchild_index(parent_index) == None):
        return None
    
    leftchild_index = get_leftmostchild_index(parent_index)
    rightmostchild_index = leftchild_index+temp_arity-1
    
    if(rightmostchild_index > size()-1):
        return size()-1
    
    else:
        return rightmostchild_index


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    
    lastelement_index = len(DATA)-1
    finalparent_index = get_parent_index(lastelement_index)
    
    if(parent_index > finalparent_index):
        return None
    
    else:
        leftchild_index = get_leftmostchild_index(parent_index)
        top_child = leftchild_index
        rightchild_index = get_rightmostchild_index(parent_index)
        for i in range(leftchild_index, rightchild_index+1):
            if (MIN_TOP):
                if(CMP_FUNCTION(DATA[i], DATA[top_child]) == -1):
                    top_child = i
            
            else:
                if(CMP_FUNCTION(DATA[i], DATA[top_child]) == 1):
                    top_child = i
    return top_child

def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    fchild_index = get_top_child(i)
    while (fchild_index > 0):
        if MIN_TOP:
            if(CMP_FUNCTION(DATA[i], DATA[fchild_index]) == 1):
                DATA[i], DATA[fchild_index] = DATA[fchild_index], DATA[i]
                
        else:
            if(CMP_FUNCTION(DATA[i], DATA[fchild_index]) == -1):
                DATA[i], DATA[fchild_index] = DATA[fchild_index] , DATA[i]
        
        i = fchild_index
        fchild_index = get_top_child(i)
    
    return DATA
            

    
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    
    pindex = get_parent_index(i)
    
    if (MIN_TOP):
        if(pindex != None and CMP_FUNCTION(DATA[i], DATA[pindex]) == -1):
            while(pindex != None and CMP_FUNCTION(DATA[i], DATA[pindex]) == -1
                   and i!=None):
                DATA[i], DATA[pindex] = DATA[pindex], DATA[i]
                i = pindex
                pindex = get_parent_index(i)

        else:
            restore_subtree(i)
    
    else:
        if(pindex!=None and CMP_FUNCTION(DATA[i], DATA[pindex]) == 1):
            while(pindex!=None and CMP_FUNCTION(DATA[i], DATA[pindex]) == 1
                   and i!=None):
                DATA[i], DATA[pindex] = DATA[pindex], DATA[i]
                i = pindex
                pindex = get_parent_index(i)
       
                
        else:
            restore_subtree(i)

    return DATA


def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    
    finalelement_index = len(DATA)-1
    finalparent_index = get_parent_index(finalelement_index)
    
    while(finalparent_index >= 0):
        restore_subtree(finalparent_index)
        finalparent_index = finalparent_index-1


def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    
    DATA[i], DATA[-1] = DATA[-1], DATA[i]
    del DATA[-1]
    restore_heap(i)

def pop():
    '''
    Pull the top element out of the heap
    '''
    if(size()):
        top_element = DATA[0]
        DATA[0], DATA[-1] = DATA[-1], DATA[0]
        del DATA[-1]
        restore_heap(0)
        
    return top_element

def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    DATA.append(obj)
    restore_heap(len(DATA)-1)


def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    
    DATA.extend(lst)


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    global DATA
    DATA = []


if __name__ == '__main__':
    pass