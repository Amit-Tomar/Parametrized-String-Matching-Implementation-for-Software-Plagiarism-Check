'''
Created on 28-Oct-2013

@author: raghavan
'''

MIN_TOP = True # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and returns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 2

# The list of elements organized as a heap
DATA = []

def initialize_heap(is_min = True, arity_exp = 1, compare_fn = None):
    '''
    Initializes the globals in the code
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
    return 2 >> (EXP2 - 1)
    
    
def get_item_at(i):
    '''
    Return the i-th element of the data list (DATA)
    '''
    global DATA
    if i >= size():
        if size() > 0:
            return DATA[size() - 1]
        else:
            return None
    if i == None:
        return None
    return DATA[i]


def swap(index_1, index_2):
    '''
    Swaps items at two given indices
    '''
    temp = DATA[index_1]
    DATA[index_1] = DATA[index_2]
    DATA[index_2] = temp


def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    # Your code
    if child_index <= 0:
        return None
    return (child_index - 1) >> EXP2


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    if parent_index == None:
        return 0
    elif ((parent_index << EXP2) + 1) < size():
        return (parent_index << EXP2) + 1
    else:
        return None
    
    
def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    start_index = get_leftmostchild_index(parent_index) 
    if start_index == None:
        return None
    else:
        end_index = (parent_index + 1) << EXP2
        while(end_index >= start_index):
            if end_index < size():
                return end_index
            end_index -= 1
            
def get_top_child(parent_index):
    '''
    Return the index of the child which is most favored to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code 
    global DATA
    temp_list = []
    start_index = get_leftmostchild_index(parent_index) 
    end_index = get_rightmostchild_index(parent_index)
    if(start_index == None):
        return None
    if start_index != None and end_index != None:
        for i in range (start_index, end_index + 1):
            temp_list.append(DATA[i])
    
    min_num = temp_list[0]
    max_num = temp_list[0]
    count = -1
    loc_min = loc_max = start_index
    for i in temp_list:
        count += 1
        if i < min_num:
            loc_min = start_index
            min_num = i
            loc_min += count
        if i > max_num:
            loc_max = start_index
            max_num = i
            loc_max += count  
            
    if MIN_TOP == False:
        return loc_max
    else:
        return loc_min
            
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code\
    parent_index = i
    if( parent_index == None ):
        return None
    top_child_index = get_top_child(i)
    if MIN_TOP == True :
        while(get_item_at(i) > get_item_at(top_child_index) and  top_child_index != None):
            j = top_child_index
            swap(i, j)
            i = j
            top_child_index = get_top_child(i)
            if( top_child_index == None):
                break
            
    else:
        while(get_item_at(i) < get_item_at(top_child_index) and  top_child_index != None):
            j = top_child_index
            swap(i, j)
            i = j
            top_child_index = get_top_child(i)
            if( top_child_index == None):
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
    flag = 0
    parent_index = get_parent_index(i)
    if( parent_index == None ):
        restore_subtree(i)
    if(MIN_TOP == True ):
        while(get_item_at(i) > get_item_at(parent_index) and parent_index != None):
            flag = 1
            swap(i, parent_index)
            i = parent_index
            parent_index = get_parent_index(i)
        if( flag == 0 ):
            restore_subtree(i)
    else:
        while(get_item_at(i) < get_item_at(parent_index) and parent_index != None):
            flag = 1
            swap(i, parent_index)
            i = parent_index
            parent_index = get_parent_index(i)
        if(flag == 0):
            restore_subtree(i)

def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    last_child = size() - 1
    parent = get_parent_index(last_child)
    while(parent >= 0):
        restore_subtree(parent)
        parent -= 1

def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    global DATA
    last_index = size() - 1
    swap(i, last_index)
    return_item = DATA.pop(-1)
    restore_heap(i)
    return return_item


def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    return remove(0)

def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    # Your code
    global DATA
    DATA.append(obj)
    heapify()


def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    # Your code
    global DATA
    DATA = lst[:]

def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    global DATA
    DATA = []

if __name__ == '__main__':
    pass