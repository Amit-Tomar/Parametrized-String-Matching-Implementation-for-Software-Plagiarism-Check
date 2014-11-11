'''
Created on 28-Oct-2013

@author: raghavan
'''
#from python.test_heap import CMP_FUNCTION

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
    DATA=[]


def size():
    '''
    Return the size of the heap
    '''
    # Your code
    size=len(DATA)
    return size

def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    # Your code
    arity= 2**EXP2
    return arity 
    
    
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
    if(0<child_index<size()):
        parent_index=(child_index-1)>>EXP2
        return parent_index
    return None


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    left_c_index=(parent_index<<EXP2)+1
    if(left_c_index>=size()):
        return None 
    else:
        
        return left_c_index
    

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    right_c_index=((parent_index+1)<<EXP2)
    if(get_leftmostchild_index(parent_index)>=size()):
        return None
    else:
        return min(size()-1,right_c_index)
    
def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
    mini = get_leftmostchild_index(parent_index)
    if mini == None:
        return None
    if MIN_TOP:
        for c in range(get_leftmostchild_index(parent_index),get_rightmostchild_index(parent_index)+1):
            if CMP_FUNCTION(DATA[mini] , DATA[c]) == 1 :
                mini = c
        return mini
    else:
        for c in range(get_leftmostchild_index(parent_index),get_rightmostchild_index(parent_index)+1):
            if CMP_FUNCTION(DATA[mini] , DATA[c]) == -1 :
                mini = c
        return mini
        
            
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    if(MIN_TOP):
        while(get_leftmostchild_index(i) is not None):
            minm=get_top_child(i)
            if(minm is not None and CMP_FUNCTION(DATA[minm],DATA[i]) == -1):
                DATA[minm],DATA[i]=DATA[i],DATA[minm]
                i=minm
            else:
                break
    else:
        while(get_leftmostchild_index(i) is not None):
            minm=get_top_child(i)
            if(minm is not None and CMP_FUNCTION(DATA[minm],DATA[i])== 1):
                DATA[i],DATA[minm]=DATA[minm],DATA[i]
                i=minm
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
    # Your code

    parent=get_parent_index(i)
    if MIN_TOP:
        if parent is not None and i is not None and CMP_FUNCTION(DATA[parent],DATA[i]) == 1:
            while(parent>0 and CMP_FUNCTION(DATA[parent],DATA[i])== 1):
                DATA[i],DATA[parent]=DATA[parent],DATA[i]
                i=parent
                parent=get_parent_index(i)
        else:
            restore_subtree(i)
    else:
        if parent is not None and i is not None and CMP_FUNCTION(DATA[parent],DATA[i]) == -1:
            while(parent>0 and CMP_FUNCTION(DATA[parent],DATA[i]) == -1):
                DATA[i],DATA[parent]=DATA[parent],DATA[i]
                i=parent
                parent=get_parent_index(i)
        else:
            restore_subtree(i)
    return DATA
def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code

    p=get_parent_index(len(DATA)-1)
    while(p>-1):
        restore_subtree(p)
        p=p-1

def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    ele = DATA[i]
    DATA[i], DATA[-1] = DATA[-1], DATA[i]
    del DATA[-1]
    restore_heap(i)
    return ele
    


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
    DATA.append(obj)
    heapify()
    
def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    # Your code
    global DATA
    for i in lst:
        add(i)
    
def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    global DATA
    DATA=[]

if __name__ == '__main__':
    pass