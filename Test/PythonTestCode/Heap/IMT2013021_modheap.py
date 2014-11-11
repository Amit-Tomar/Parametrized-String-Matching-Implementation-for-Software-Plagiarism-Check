
'''
Created on 28-Oct-2013

@author: raghavan
'''

MIN_TOP = True # Says whether the heap is a Min-Heap (True) or a Max-Heap(False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and returns 1 
# if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = lambda x, y : (1 if (x > y) else (-1 if (x < y) else 0))


# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA = []



def initialize_heap(is_min = True, arity_exp = 1, compare_fn = None):
    '''
    To initialize the elements in the beginning
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
    return 2 << (EXP2 - 1)
    
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
    if(child_index <= 0):
        return None
    
    return child_index >> EXP2

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    
    if(parent_index==None or int(parent_index << EXP2)+1 > size()):
        return None
    
    return int(parent_index << EXP2) + 1

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    
    if parent_index << EXP2 + arity() > size() - 1:
        return size() - 1
    
    return parent_index << EXP2 + arity()
    
def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
    
    l_m_c = get_leftmostchild_index(parent_index)
    
    if(not l_m_c):
        return None
    
    for count in range(len(DATA[l_m_c + 1:])):
        
        if((CMP_FUNCTION(DATA[count + l_m_c], DATA[l_m_c])==1
           and MIN_TOP) or (MIN_TOP == False 
           and CMP_FUNCTION(DATA[count + l_m_c], DATA[l_m_c]))): 
            
            l_m_c = count + get_leftmostchild_index(parent_index)
    
    return l_m_c

    
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    temp = get_parent_index(i)
    
    while(i!=None and temp >= 0 and i<size() ):
        
        if((( CMP_FUNCTION(DATA[temp], DATA[i]) != -1 and MIN_TOP) or 
            ( MIN_TOP == False and  CMP_FUNCTION(DATA[temp], DATA[i]) != 1))):
            
            DATA[i], DATA[temp] = DATA[temp], DATA[i]
        
        i = temp
        temp = get_parent_index(temp)
    
    return None    

def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (child_recur(i, top_child)i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code
    
    for index in range(size())[i:]:
        restore_subtree(index)

def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code 
    restore_heap(0)            

def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
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
    
    if(len(DATA) == 0):
        return None
    
    temp = DATA[0]
    DATA = DATA[1:]
    
    heapify()
    
    return temp

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
    for element in lst :
        DATA.append(element)
            
def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your codeleftmost_child <= rightmost_child
    global DATA    
    
    DATA = []

if __name__ == '__main__':
    pass