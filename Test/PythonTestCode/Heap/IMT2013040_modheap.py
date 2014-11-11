'''

Created on 28-Oct-2013

@author: raghavan

'''


MIN_TOP = False 

CMP_FUNCTION = None

EXP2 = 1

DATA = []

def initialize_heap(is_min = True , arity_exp = 1 , compare_fn = None):

    global MIN_TOP , CMP_FUNCTION , EXP2 , DATA
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

    pIndex = (child_index - 1) >> EXP2
    if child_index == 0:
        return None
    else:
        return pIndex

def get_leftmostchild_index(parent_index):

    '''

    Return the index of the leftmost child of the element at parent_index

    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)

    '''

    lcIndex = (parent_index << EXP2) + 1
    if lcIndex < size():
        return lcIndex
    else:
        return None
    
def get_rightmostchild_index(parent_index):

    '''

    Return the index of the rightmost child of the element at parent_index

    Should return None if the parent has no child

    '''

    rcIndex = (parent_index + 1) << EXP2
    if (parent_index << EXP2) + 1 > size() - 1:
        return None
    elif rcIndex > (size() - 1):
        return size() - 1
    else:
        return rcIndex

def get_top_child(parent_index):

    '''

    Return the index of the child which is most favoured to move up the tree among all the children of the

    element at parent_index

    '''
    topIndex = get_leftmostchild_index(parent_index)
    for i in range(topIndex , ((parent_index + 1) << EXP2) + 1):
        if MIN_TOP:
            if CMP_FUNCTION (DATA[i] , DATA[topIndex]) == -1:
                topIndex = i
        else: 
            if CMP_FUNCTION (DATA[i] , DATA[topIndex]) == 1:
                topIndex = i
    return topIndex


def restore_subtree(i):
    
    '''

    Restore the heap property for the subtree with the element at index i as the root

    Assume that everything in the subtree other than possibly the root satisfies the heap property

    '''
    
    while(get_rightmostchild_index(i) is not None):
        if get_rightmostchild_index(i) is None:
            break
        minchildIndex = get_leftmostchild_index(i)
        maxchildIndex = get_leftmostchild_index(i)
        for j in range(get_leftmostchild_index(i) , get_rightmostchild_index(i) + 1):
            if CMP_FUNCTION(DATA[j] , DATA[minchildIndex]) == -1:
                minchildIndex = j
            if CMP_FUNCTION(DATA[j] , DATA[maxchildIndex]) == 1:
                maxchildIndex = j   
        if MIN_TOP:
            if CMP_FUNCTION(DATA[i] , DATA[minchildIndex]) == 1:
                DATA[i] , DATA[minchildIndex] = DATA[minchildIndex] , DATA[i]
                i = minchildIndex
            else:
                break
        else:
            if CMP_FUNCTION(DATA[i] , DATA[maxchildIndex]) == -1:
                DATA[i] , DATA[maxchildIndex] = DATA[maxchildIndex] , DATA[i]
                i = maxchildIndex
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
        if (get_parent_index(i) != None and CMP_FUNCTION(DATA[get_parent_index(i)] , DATA[i]) == 1 and get_parent_index(i) > 0):
            while (CMP_FUNCTION ( DATA[get_parent_index(i) ] , DATA[i]) ==  1 and get_parent_index() >= 0):
                DATA[get_parent_index(i)] , DATA[i] = DATA[i] , DATA[get_parent_index(i)]
                i = get_parent_index(i)
        else:
            restore_subtree(i)
    else:
        if(get_parent_index(i) != None and CMP_FUNCTION(DATA[get_parent_index(i)] , DATA[i]) == -1 and get_parent_index(i) > 0):
            while (CMP_FUNCTION(DATA[get_parent_index(i)] , DATA[i]) == -1 and get_parent_index(i) > 0):
                DATA[get_parent_index(i)] , DATA[i] = DATA[i] , DATA[get_parent_index(i)]
                i = get_parent_index(i)

        else:
            restore_subtree(i)
        
def heapify():

    '''

    Rearrange DATA into a heap

    Algo: (i) Start from the first nonleaf node - the parent of the last element

    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root

    '''

    parentIndex = get_parent_index(size() - 1)
    while(parentIndex >= 0):
        restore_subtree(parentIndex)
        parentIndex = parentIndex - 1
        
def remove(i):

    '''
    Remove an element (at index i) from the heap

    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.

    (c) Restore the heap starting from i
    '''
    DATA[i] , DATA[-1] = DATA[-1] , DATA[i]
    DATA.pop()
    restore_subtree(i)

def pop():

    '''
    Pull the top element out of the heap
    '''
    top = DATA[0]
    remove(0)
    return top

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
    heapify()

def clear():

    '''
    Clear the data in the heap - initialize to empty list
    '''
    DATA = []

if __name__ == '__main__':

    pass
