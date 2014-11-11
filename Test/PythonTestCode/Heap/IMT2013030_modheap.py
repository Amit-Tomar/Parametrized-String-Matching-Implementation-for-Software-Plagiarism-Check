'''
Created on 28-Oct-2013

@author: raghavan
'''

MIN_TOP = False # Says whether the heap is Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and 
#retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1
# The list of elements organized as a heap
DATA = []

def initialize_heap(is_min = True, arity_exp = 1, compare_fn = None):
    '''initializes global variables'''
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
    return 2 << (EXP2-1)

    
def get_item_at(i):
    '''
    Return the i-th element of the data list (DATA)
    '''
    if (i > size()-1):
        return DATA[size()-1]
    return DATA[i]

def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    if (child_index==0 or child_index==None):
        return None
    else:
        return ((child_index-1)>>EXP2)

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    i = (parent_index<<EXP2)+1
    if i > (size()-1):
        return None
    return i

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no childfrom random import randrange
    '''
    return ((parent_index<<EXP2)+arity())

def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    initial_child = get_leftmostchild_index(parent_index)
    cmp_elem = DATA[initial_child]
    index = initial_child
    for children in range(0, arity()):
        position = initial_child+children
        if position < size():
            if (CMP_FUNCTION(DATA[position], cmp_elem)==-1 and MIN_TOP==True):
                cmp_elem = DATA[position]
                index = position
            elif(CMP_FUNCTION(DATA[position], cmp_elem)==1 and MIN_TOP==False):
                cmp_elem = DATA[position]
                index = position
    return index


def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    left_child = get_leftmostchild_index(i)
    while((size() > left_child) and left_child!=None):
        child_index = get_top_child(i)
        if(CMP_FUNCTION(DATA[child_index], DATA[i])==-1 and MIN_TOP==True):
            DATA[i], DATA[child_index] = DATA[child_index], DATA[i]
            i = child_index
        elif(CMP_FUNCTION(DATA[child_index], DATA[i])==1 and MIN_TOP==False):
            DATA[i], DATA[child_index] = DATA[child_index], DATA[i]
            i = child_index
        else:
            break
        left_child = get_leftmostchild_index(i)
        
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    parent = get_parent_index(i)
    flag = 0
    if parent != None:
        while(CMP_FUNCTION(DATA[i], DATA[parent])==-1 and MIN_TOP==True):
            flag = 1
            DATA[i], DATA[parent] = DATA[parent], DATA[i]
            i = get_parent_index(parent)
            if(i==None):
                break
        while(CMP_FUNCTION(DATA[i], DATA[parent])==1 and MIN_TOP==False):
            
            flag = 1
            DATA[i], DATA[parent] = DATA[parent], DATA[i]
            i = get_parent_index(parent)
            if(i==None):
                break
    if(flag==0):
        restore_subtree(i)

def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    if size()!=0:
        index = get_parent_index(size()-1)
        higher_parent = get_parent_index(index)
        while(index!=None):
            if (higher_parent==None):
                restore_subtree(0)
            else:
                initial_child = get_leftmostchild_index(higher_parent)
                final_child = get_rightmostchild_index(higher_parent)
                for parent in range(initial_child, final_child+1):
                    if parent < size():
                        restore_subtree(parent)
            index = higher_parent
            if(index!=None):
                higher_parent = get_parent_index(index)
    
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    DATA[i], DATA[-1] = DATA[-1], DATA[i]
    k = DATA.pop(-1)
    restore_heap(0)
    return k

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
    heapify()

def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    global DATA
    DATA = lst[:]

#def clear():
    
# Clear the data in the heap - initialize to empty list
    
#  DATA = []

#if __name__ == '__main__':
#    pass