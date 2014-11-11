'''
Created on Nov 7, 2013

@author: Rishabh
'''


MIN_TOP = False # Says whether the heap is a Min-Heap(True) or a Max-Heap(False)

# Comparison Function for the heap

CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA = []

def initialize_heap(is_min = False, arity_exp = 1, compare_fn = None):
    '''
    initializes variables
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
    # Your code
    return len(DATA)


def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    # Your code
    return 2 << (EXP2-1)
    
    
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
    else :
        return (child_index-1) >> EXP2
    
def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    left_child_index = (parent_index << EXP2) + 1
    if size() > left_child_index :
        return left_child_index
    else :
        return None
        

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    right_child_index = (parent_index + 1) << EXP2
    if get_leftmostchild_index(parent_index)==None :
        return None
    elif size() > right_child_index :
        return right_child_index
    else :
        return size() - 1

def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
    top_child_index = get_leftmostchild_index(parent_index)
    right_child_index = get_rightmostchild_index(parent_index)
    if top_child_index == None :
        return None
    else :
        child_index = top_child_index
        if(MIN_TOP):
            while child_index <= right_child_index:
                if CMP_FUNCTION(get_item_at(child_index), get_item_at(top_child_index)) == -1:
                    top_child_index = child_index
                child_index += 1
        else:
            while child_index <= right_child_index:
                if CMP_FUNCTION(get_item_at(child_index), get_item_at(top_child_index)) == 1:
                    top_child_index = child_index
                child_index += 1
        return top_child_index
    
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    
    fav_child = get_top_child(i)
    if MIN_TOP:
        while fav_child and CMP_FUNCTION(get_item_at(fav_child), get_item_at(i)) == -1:
            DATA[fav_child], DATA[i] = DATA[i], DATA[fav_child]
            fav_child, i = get_top_child(fav_child), fav_child    
    else :
        while fav_child and CMP_FUNCTION(get_item_at(fav_child), get_item_at(i)) == 1:
            DATA[fav_child], DATA[i] = DATA[i], DATA[fav_child]
            fav_child, i = get_top_child(fav_child), fav_child
            
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code
    parent_index = get_parent_index(i)
    if i > 0 and ((MIN_TOP  and CMP_FUNCTION(get_item_at(i), get_item_at(parent_index)) == -1) or 
                  (not MIN_TOP and CMP_FUNCTION(get_item_at(i), get_item_at(parent_index)) == 1)):
        while i > 0 and ((MIN_TOP  and CMP_FUNCTION(get_item_at(i), get_item_at(parent_index)) == -1) or 
                                   (not MIN_TOP and CMP_FUNCTION(get_item_at(i), get_item_at(parent_index)) == 1)):
            DATA[i], DATA[parent_index] = DATA[parent_index], DATA[i]
            i, parent_index = parent_index, get_parent_index(parent_index)
    else :
        restore_subtree(i)


def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    node_index = get_parent_index(len(DATA)-1)
    while node_index >= 0 :
        restore_subtree(node_index)
        node_index -= 1
    

def remove(i):
    
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    final = size() - 1
    DATA[i], DATA[final] = DATA[final], DATA[i]
    DATA.pop()
    restore_subtree(i)

def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    max_min = DATA[0]
    remove(0)
    return max_min

def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    # Your code
    DATA.append(obj)
    restore_heap(len(DATA)-1)
    
    
def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    # Your code
    i = 0
    while i < len(lst):
        DATA.append(lst[i])
        i += 1
    heapify()
    
def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    while size() != 0:
        DATA.pop()
        
        
    
if __name__ == '__main__':
    pass

    
