'''
Created on 01-Nov-2013

@author: Srinivasan
------------------------
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
    # Your code
    return EXP2 << 1
    
def get_item_at(i):
    '''
    Return the i-th element of the data list (DATA)
    '''
    if(i >= size()):
        return None
    return DATA[i]


def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    if(child_index <= 0):
        return None
    return int(child_index >> EXP2)


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    if(parent_index == None or int(parent_index << EXP2) + 1 > size()):
        return None
    return int(parent_index << EXP2)+1


def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    right = (int(parent_index << EXP2)+arity())
    while (right >= size()):
        right -= 1
    return right

def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    least = get_leftmostchild_index(parent_index)
    if(not least):
        return None
    for count in range(len(DATA[get_leftmostchild_index(parent_index)+1:])):
        child = get_leftmostchild_index(parent_index)
        if((DATA[count + child] < DATA[least] and MIN_TOP ) or ( MIN_TOP ==  False and DATA[count + child] > DATA[least])): 
            least = count+child
    return least

def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    while(i != None and get_parent_index(i) >= 0 and i < size()):
        if(( DATA[get_parent_index(i)] >= DATA[i] and MIN_TOP) or ( MIN_TOP ==  False and  DATA[get_parent_index(i)] <= DATA[i])):
            DATA[i], DATA[get_parent_index(i)] = DATA[get_parent_index(i)], DATA[i]
        i = get_parent_index(i)
    return None
        
        
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Also: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code
    for j in range(size())[i:]:
        restore_subtree(j)
            
def heapify():
    '''
    Rearrange DATA into a heap
    Also: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    restore_heap(0)

def remove(i):
    '''
    Remove an element (at index i) from the heap
    Also: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    global DATA
    DATA = DATA[:i]+DATA[i+1:]
    restore_heap(get_parent_index(i))

def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    global DATA
    if(DATA == []):
        return None
    pop1 = DATA[0]
    DATA = DATA[1:]
    heapify()
    return pop1


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
    return DATA

def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    DATA = []
    
if __name__ ==  '__main__':
    clear()
    LST = [26, 18, 18, 24, 8, 9, 21, 13, 13, 13, 3, 8, 10, 3, 4]
    initialize_heap(False, 2, CMP_FUNCTION)
    DATA = LST[:]
    print "parent ", get_parent_index(6)
    TEMP = []
    heapify()
    print "should be correct", DATA
    while(size()>0):
        TEMP.append(pop())
    LST.sort(reverse = False)
    print "popped : ", TEMP
    print (LST)
