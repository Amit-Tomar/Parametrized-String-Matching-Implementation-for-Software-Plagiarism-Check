'''
Created on 28-Oct-2013

@author: raghavan
'''
from multiprocessing.heap import Heap

MIN_TOP = False 
''' 
Says whether the heap is a Min-Heap (True) or a Max-Heap (False)
Comparison Function for the heap
Takes two elements - e1, e1 - of the heap as arguments and returns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
'''

CMP_FUNCTION = None

'''The arity (number of children for a parent) is taken to be 2^EXP2'''
EXP2 = 1

''' The list of elements organized as a heap'''
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
    if child_index == 0:
        return None
    else:
        return (child_index-1)>>EXP2


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    child_index = (parent_index<<EXP2)+1
    if child_index < size():
        return (parent_index<<EXP2)+1
    else:
        return None

    
def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    child_index = ((parent_index<<EXP2)+1)
    if (child_index > (size()-1)):
        return None
    elif (((parent_index+1)<<EXP2))>(size()-1):
        return (size()-1)
    else:
        return (parent_index+1)<<EXP2


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    global DATA , MIN_TOP
    l_index = get_leftmostchild_index(parent_index)
    if l_index:
        r_index = get_rightmostchild_index(parent_index)
    else:
        return None
    if not r_index:
        return l_index
    if MIN_TOP:
        min_max = l_index
        for i in range(l_index, r_index+1):
            if CMP_FUNCTION(DATA[i] , DATA[min_max]) < 0:
                min_max = i
    else:
        min_max = l_index
        for i in range(l_index, r_index+1):
            if CMP_FUNCTION(DATA[i] , DATA[min_max]) > 0:
                min_max = i
    return min_max


def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    p_ind = i
    while(get_rightmostchild_index(p_ind) != None):
        minx = get_leftmostchild_index(p_ind)
        maxx = get_leftmostchild_index(p_ind)
        for j in range(get_leftmostchild_index(p_ind), get_rightmostchild_index(p_ind) + 1):
            if CMP_FUNCTION(DATA[j] , DATA[minx]) == -1:
                minx = j
            if CMP_FUNCTION(DATA[j] , DATA[maxx]) == 1:
                maxx = j
        if MIN_TOP:
            if CMP_FUNCTION(DATA[p_ind] , DATA[minx]) == 1:
                DATA[p_ind] , DATA[minx] = DATA[minx] , DATA[p_ind]
                p_ind = minx
            else:
                break 
        else:
            if CMP_FUNCTION(DATA[p_ind] , DATA[maxx]) == -1:
                DATA[p_ind] , DATA[maxx] = DATA[maxx] , DATA[p_ind]
                p_ind = maxx
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
    child_index = i
    p_ind = get_parent_index(child_index)
    if MIN_TOP:
        if (p_ind != None and CMP_FUNCTION(DATA[p_ind] , DATA[child_index]) == 1):
            while (p_ind > 0 and CMP_FUNCTION(DATA[p_ind] , DATA[child_index]) == 1 ):
                DATA[p_ind] , DATA[child_index] = DATA[child_index] , DATA[p_ind]
                child_index = p_ind
                p_ind = get_parent_index(child_index)
        else:
            restore_subtree(child_index)
    else:
        if (p_ind != None and CMP_FUNCTION(DATA[p_ind],DATA[child_index])==-1):
            while (p_ind > 0 and CMP_FUNCTION(DATA[p_ind], DATA[child_index])==-1):
                DATA[p_ind], DATA[child_index] = DATA[child_index], DATA[p_ind]
                child_index = p_ind
                p_ind = get_parent_index(child_index)
        else:
            restore_subtree(child_index)      
      

def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    p_ind = get_parent_index(size()-1)
    while(p_ind >= 0):
        restore_subtree(p_ind)
        p_ind = p_ind - 1


def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    DATA[i] , DATA[-1] = DATA[-1] , DATA[i]
    del DATA[-1]
    restore_subtree(i)


def pop():
    '''
    Pull the top element out of the heap
    '''
    element = DATA[0]
    remove(0)
    return element
   

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
    for i in lst:
        DATA.append(i)


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    DATA=[]


if __name__ == '__main__':
    pass