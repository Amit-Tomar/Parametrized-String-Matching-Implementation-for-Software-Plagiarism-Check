'''
Created on 28-Oct-2013

@author: raghavan
'''
MIN_TOP = True 
# Says whether the heap is a Min-Heap 
##(True) or a Max-Heap (False)

def compare_fn(num1, num2):
    if num1 >= num2:
        return 1
    else:
        return -1
# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments 
##and returns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = compare_fn

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
    parent = (child_index-1)>>EXP2
    if parent < 0:
        return None
    else:
        return (child_index-1)>>EXP2


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - 
    left shift n by m bits (written as n << m, in python)
    '''
    child = (parent_index<<EXP2)+1
    if child > size()-1:
        return None
    return child


def get_rightmostchild_index(parent_index): 
    '''
    Return the index of the rightmost child of the element at
     parent_index
    Should return None if the parent has no child
    '''
    n=1
    child = get_leftmostchild_index(parent_index)+1
    if child > size()-1:
        return None
    if child+1 > size()-1:
        return None
    while(n < arity()):
        if get_leftmostchild_index(parent_index)+n > size()-1:
            return get_leftmostchild_index(parent_index)+n-1
        n+=1
    return get_leftmostchild_index(parent_index)+n


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured 
    to move up the tree among all the children of the
    element at parent_index
    '''
    lchild = get_leftmostchild_index(parent_index)
    if lchild == None:
        return None
    rchild = get_rightmostchild_index(parent_index)
    if rchild == None:
        return lchild
    min_index = lchild
    max_index = lchild
    
    if MIN_TOP == True:
        min = DATA[lchild]
        for i in range(lchild, rchild):
            if CMP_FUNCTION(DATA[i], min) == -1:
                min = DATA[i]
                min_index = i
        return min_index
    else:
        max = DATA[lchild]
        for i in range(lchild, rchild):
            if CMP_FUNCTION(DATA[i], max) == 1:
                max = DATA[i]
                max_index = i
        return max_index

def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    child = get_top_child(i)
    if child != None:
        if(MIN_TOP == True):
            if CMP_FUNCTION(DATA[child], DATA[i]) ==- 1:
                temp = DATA[i]
                DATA[i] = DATA[child]
                DATA[child] = temp
            restore_subtree(child)
        else:
            if CMP_FUNCTION(DATA[child], DATA[i]) == 1:
                temp = DATA[i]
                DATA[i] = DATA[child]
                DATA[child] = temp
            restore_subtree(child)
        
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    count = 0
    n = 4
    initiali = i
    while (i>0):  
        parent = get_parent_index(i)  
        if n>0:
            if MIN_TOP == True:
                if CMP_FUNCTION(DATA[i],DATA[parent]) == -1:
                    count += 1
                    temp = DATA[i]
                    DATA[i] = DATA[parent]
                    DATA[i] = temp
                    i = parent
                restore_subtree(i)
            else:
                if CMP_FUNCTION(DATA[i], DATA[parent]) == 1:
                    count += 1
                    temp = 0
                    temp = DATA[i]
                    DATA[i] = DATA[parent]
                    DATA[parent] = temp
                    i = parent
                restore_subtree(i)
    if count == 0:
        restore_subtree(initiali)
            
def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    position = get_parent_index(size()-1)
    while position >= 0:
        x = position
        restore_subtree(x)
        position -= 1

def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    DATA[0] = DATA[size()-1]
    DATA.pop()
    restore_subtree(size()-1, DATA)
        
def pop():
    '''
    Pull the top element out of the heap
    '''
    a = DATA[0]
    DATA.remove(a)
    heapify()
    return a

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
    Clear the data in  the heap - initialize to empty list
    '''
    for i in DATA:
        print i
        DATA.pop()

if __name__ == '__main__':
    pass













