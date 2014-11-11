'''
Created on 28-Oct-2013

@author: raghavan
'''

MIN_TOP = False 
# Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and 
#retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA = []

def max_of_child ( leftchild_index , rightchild_index ) :
#Return the index of the maximum value at index1 and index2
    max_index = DATA[leftchild_index : rightchild_index+1].index(max(DATA[leftchild_index : rightchild_index+1]))
    return leftchild_index + max_index
    
def min_of_child ( leftchild_index , rightchild_index) :
#Return the index of the minimum value at index1 and index2
    min_index = DATA[leftchild_index : rightchild_index+1].index(min(DATA[leftchild_index : rightchild_index+1]))
    return leftchild_index + min_index

def swap_element ( index1 , index2):
    temp_data1 = get_item_at(index1)
    temp_data2 = get_item_at(index2)
    put_item_at(index1 , temp_data2)
    put_item_at(index2 , temp_data1)
    

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
    size_heap = len(DATA)
    return size_heap


def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    # Your code
    arity_of_heap = 1 << EXP2
    return arity_of_heap

def put_item_at(i, obj):
    DATA[i] = obj
     
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
    parent_index = (child_index-1) >> EXP2
    return parent_index


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    leftchild_index = (parent_index<<EXP2)+1
    heap_size = size()
    if(cmp(leftchild_index , heap_size) == -1):
        return leftchild_index
    else:
        return None


def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    arity_heap = arity()
    leftchild_index = get_leftmostchild_index(parent_index)
    if(leftchild_index == None):
        return None
    rightchild_index = leftchild_index + arity_heap -1
    heap_size = size()
    if(cmp(rightchild_index , heap_size) == -1):
        return rightchild_index
    else:
        return heap_size-1


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
    leftchild_index  = get_leftmostchild_index(parent_index) 
    rightchild_index = get_rightmostchild_index(parent_index)
    if(rightchild_index == None):
        return None
    if MIN_TOP == False :
        return max_of_child(leftchild_index , rightchild_index)
    else:
        return min_of_child(leftchild_index , rightchild_index)


def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    size_heap = size()
    parent_index = i
    fav_child = get_top_child(parent_index)
    if( parent_index == None  or parent_index >= size_heap):
        return None
    if MIN_TOP == True :
        while(fav_child != None and (CMP_FUNCTION( get_item_at(i) , get_item_at(fav_child)) == 1 )):
            swap_element (i , fav_child)
            i = fav_child
            parent_index = i
            fav_child = get_top_child(parent_index)
    else :
        while(fav_child != None and (CMP_FUNCTION( get_item_at(i) , get_item_at(fav_child)) == -1 )):
            swap_element (i , fav_child)
            i = fav_child
            parent_index = i
            fav_child = get_top_child(parent_index)
            
            
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
    if(MIN_TOP == True ):
        while(parent_index != None and CMP_FUNCTION( get_item_at(i) , get_item_at(parent_index)) == -1 ):
            count += 1
            swap_element (i , parent_index)
            i = parent_index
            parent_index = get_parent_index(i)
        if(count == 0 ):
            restore_subtree(i)
    else:
        while(parent_index != None and CMP_FUNCTION( get_item_at(i) , get_item_at(parent_index)) == 1 ):
            count += 1
            swap_element (i , parent_index)
            i = parent_index
            parent_index = get_parent_index(i)
        if(count == 0):
            restore_subtree(i)

def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    index = size() - 1
    index = get_parent_index(index)
    while(index >= 0):
        restore_subtree(index)
        index -= 1


def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    size_of_heap = size()
    swap_element (i , size_of_heap-1)
    DATA[size_of_heap-1:size_of_heap] = []
    restore_heap(i)
    
def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    if(size() == 0):
        return None
    pop_index = 0
    pop_element = get_item_at(0)
    remove(pop_index)
    return pop_element


def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    # Your code
    global DATA
    DATA += [obj]
    restore_heap(size()-1)
    
def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    # Your code
    length_of_list = len(lst)
    for index in range(0, length_of_list):
        add(lst[index])

def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    DATA = []
    
if __name__ == '__main__':
    pass
