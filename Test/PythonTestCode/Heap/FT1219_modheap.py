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
    if (compare_fn != None):
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
    return (1 << EXP2)


def get_item_at(i):
    '''
    Return the i-th element of the data list (DATA)
    '''
    return DATA[i]


def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    Should return None if the child has no parent
    '''
    if (child_index <= 0):
        return None
    else:
        parent_index = (child_index - 1) >> EXP2
        return (parent_index if (parent_index < child_index) else None)


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    Should return None if the parent has no child
    '''
    child_index = (parent_index << EXP2) + 1
    return (child_index if (child_index < size()) else None)


def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    leftmostchild_index = get_leftmostchild_index(parent_index)
    return (None if (leftmostchild_index == None) else (min(size(), (leftmostchild_index + arity()))-1))


def is_favoured(index1, index2):
    '''
    Might heap to have this helper function to check if the element elem1 if favoured (to move up) over elem2.
    Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
    '''
    return ((not MIN_TOP and CMP_FUNCTION(DATA[index1], DATA[index2]) >= 0) or
            (MIN_TOP and CMP_FUNCTION(DATA[index1], DATA[index2]) <= 0))


def get_top_child(parent_index):
    '''
    This returns the index of the child which is most favoured to move up the tree among all the childred on the
    element at parent_index
    '''
    min_index = get_leftmostchild_index(parent_index)
    if (min_index == None):
        return None
    max_index = min(size(), (min_index + arity()))
    child_index = min_index
    for i in range(min_index, max_index):
        if is_favoured(i, child_index):
            child_index = i
    return child_index


def should_move_up(i):
    '''
    Return true if the element at index i needs to move up the tree
    '''
    parent_index = get_parent_index(i)
    return (False if (parent_index == None) else is_favoured(i, parent_index))


def should_move_down(i):
    '''
    Return true if the element at index i needs to move down the tree
    '''
    child_index = get_top_child(i)
    return (False if (child_index == None) else is_favoured(child_index, i))


def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    global DATA
    while (should_move_down(i)):
        child_index = get_top_child(i)
        DATA[i], DATA[child_index] = DATA[child_index], DATA[i]
        i = child_index


def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    global DATA
    moved_up = False
    while (should_move_up(i)):
        moved_up = True
        parent_index = get_parent_index(i)
        DATA[i], DATA[parent_index] = DATA[parent_index], DATA[i]
        i = parent_index
    if (not moved_up):
        restore_subtree(i)
        

def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    last_nonleaf = get_parent_index(size() - 1)
    while (last_nonleaf >= 0):
        restore_subtree(last_nonleaf)
        last_nonleaf -= 1

def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    global DATA
    if (i < (size() - 1)):
        DATA[i], DATA[-1] = DATA[-1], DATA[i]
    item = DATA.pop()
    if (i < (size() - 1)):
        restore_heap(i)
    return item


def pop():
    '''
    Pull the top element out of the heap
    '''
    return remove(0)


def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    global DATA
    DATA.append(obj)
    restore_heap(size()-1)


def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    for elem in lst:
        DATA.append(elem)


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    global DATA
    DATA = []


if __name__ == '__main__':
    initialize_heap()
    import_list([9,10,4,5,20,14,13,6,8,9])