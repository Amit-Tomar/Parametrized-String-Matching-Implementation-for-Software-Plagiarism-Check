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
    CMP_FUNCTION = compare_fn
    EXP2 = arity_exp
    DATA = []


def size():
    '''
    Return the size of the heap
    '''
    return len(DATA)
    # Your code


def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    return 2<<(EXP2-1)
    # Your code
    
    
    
def get_item_at(i):
    '''
    Return the i-th element of the data list (DATA)
    '''
    global DATA
    return DATA[i]


def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    global DATA
    if child_index==0:
        return None
    else:
        return (child_index-1)/arity()
    # Your code


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    global DATA
    if (arity()*parent_index)+1<len(DATA):
        return (arity()*parent_index)+1
    # Your code


def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    global DATA
    if get_leftmostchild_index(parent_index)!=None:
        if (arity()*parent_index)+arity()<len(DATA):
            return (arity()*parent_index)+arity()
        else:
            return len(DATA)-1
    # Your code



def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    global DATA
    if get_leftmostchild_index(parent_index)!=None:
        new=DATA[get_leftmostchild_index(parent_index):get_rightmostchild_index(parent_index)+1]
        if MIN_TOP==False:
            return get_leftmostchild_index(parent_index)+new.index(max(new))
        else: 
            return get_leftmostchild_index(parent_index)+new.index(min(new))
    
    # Your code


def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    global DATA
    if MIN_TOP==False:
        if get_leftmostchild_index(i)!=None and i<size():
            temp = get_top_child(i)
            if DATA[temp]>DATA[i] and temp!=None:
                DATA[temp],DATA[i]=DATA[i],DATA[temp]
                restore_subtree(temp)
        
    else:
        if get_leftmostchild_index(i)!=None and i<size():
            temp = get_top_child(i)
            if DATA[temp]<DATA[i] and temp!=None:
                DATA[temp],DATA[i]=DATA[i],DATA[temp]
                restore_subtree(temp)
        
    # Your code
        
    # Your code

    
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    global DATA
    if MIN_TOP==False:
        if get_parent_index(i)!=None:
            if DATA[get_parent_index(i)]<DATA[i]:
                DATA[get_parent_index(i)],DATA[i]=DATA[i],DATA[get_parent_index(i)]
                restore_subtree(i)
                restore_heap(get_parent_index(i))
                
            else:
                restore_subtree(i)
    if MIN_TOP==True:
        if get_parent_index(i)!=None:
            if DATA[get_parent_index(i)]>DATA[i]:
                DATA[get_parent_index(i)],DATA[i]=DATA[i],DATA[get_parent_index(i)]
                restore_subtree(i)
                restore_heap(get_parent_index(i))
            else:
                restore_subtree(i)
                
            
    # Your code


def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    global MIN_TOP
    global EXP2
    if MIN_TOP==True or MIN_TOP==False:
        global DATA
        temp1=get_parent_index(len(DATA)-1)
        while(temp1>=0):
            restore_subtree(temp1)
            temp1=temp1-1
        
        
    
    
    # Your code


def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    global DATA
    DATA[i],DATA[len(DATA)-1]=DATA[len(DATA)-1],DATA[i]
    
    DATA.pop()
    heapify()
    
    
    # Your code


def pop():
    '''
    Pull the top element out of the heap
    '''
    global DATA
    
    heapify()
    a=DATA[0]
    del DATA[0]
    if size()>1:
        heapify()
    return a
    
    # Your code


def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    global DATA
    DATA.append(obj)
    return DATA
    # Your code


def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    global DATA
    for element in lst:
        DATA.append(element)
    return DATA
    
    # Your code


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    global DATA
    '''for i in range (0,len(DATA)-1):
        DATA.pop()'''
    DATA = []
    return DATA
    
    # Your code
if __name__ == '__main__':
    pass
    

    

