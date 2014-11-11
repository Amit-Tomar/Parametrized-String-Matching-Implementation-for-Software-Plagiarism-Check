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

# The list of elements organized as a noheap
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
    if child_index == 0: return None
    return child_index-1 >> EXP2

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    if parent_index == None: return None
    elif parent_index == 0 :return 1
    elif size() - parent_index <= arity() or (parent_index << EXP2) + 1 > size()-1: return None
    else: return (parent_index << EXP2) + 1 

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    lchild = get_leftmostchild_index(parent_index)
    if (lchild == None): return None
    elif lchild == size()-1 : return lchild
    elif size() - lchild < arity(): return size()-1
    else: return lchild + arity()-1
   
def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    child_index = get_leftmostchild_index(parent_index)
    top_child_index = child_index
    rchild_ind = get_rightmostchild_index(parent_index)
    if(MIN_TOP != True):
        if child_index != None:
            while(child_index <= rchild_ind):
                if(CMP_FUNCTION(DATA[top_child_index],DATA[child_index]) == -1):
                    top_child_index = child_index
                child_index = child_index + 1 
            return top_child_index
        return None
    else:
        if child_index != None : 
            while(child_index <= rchild_ind):
                if(CMP_FUNCTION(DATA[top_child_index],DATA[child_index]) == 1):
                    top_child_index = child_index
                child_index = child_index + 1      
            return top_child_index

def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    top_child_index = get_top_child(i)
    if MIN_TOP == False:
        while(top_child_index != None and CMP_FUNCTION(DATA[top_child_index],DATA[i]) == 1):
            DATA[top_child_index],DATA[i] = DATA[i],DATA[top_child_index]
            i = top_child_index
            top_child_index = get_top_child(i)
    else:
        while(top_child_index != None and CMP_FUNCTION(DATA[top_child_index],DATA[i]) == -1):
            DATA[top_child_index],DATA[i] = DATA[i],DATA[top_child_index]
            i = top_child_index
            top_child_index = get_top_child(i)   
                           
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    initial = i
    count = 0
    if(MIN_TOP == False):
        parent_ind = get_parent_index(i)
        while(parent_ind != None and CMP_FUNCTION(DATA[i],DATA[parent_ind]) == 1 ):
            DATA[i],DATA[parent_ind] = DATA[parent_ind],DATA[i]
            parent_ind = get_parent_index(parent_ind)
            i = get_top_child(parent_ind)
            count += 1
    else:
        parent_ind = get_parent_index(i)
        while(parent_ind != None and CMP_FUNCTION(DATA[i],DATA[parent_ind]) == -1):
            DATA[i],DATA[parent_ind] = DATA[parent_ind],DATA[i]
            parent_ind = get_parent_index(parent_ind)
            i = get_top_child(parent_ind)
            count += 1
    if count == 0: restore_subtree(initial)

def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    ind = get_parent_index(size()-1)
    while (ind  >= 0):
        restore_subtree(ind)
        ind = ind - 1
        
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    DATA[i],DATA[-1] = DATA[-1],DATA[i]
    element = DATA[size()-1] 
    DATA = DATA[:-1]
    restore_heap(i)
    return element

def pop():
    '''
    Pull the top element out of the heap
    '''
    element = DATA.pop(0)
    heapify()
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
    DATA.extend(lst)
    heapify()    

def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    DATA=[]

if __name__ == '__main__':
    pass
