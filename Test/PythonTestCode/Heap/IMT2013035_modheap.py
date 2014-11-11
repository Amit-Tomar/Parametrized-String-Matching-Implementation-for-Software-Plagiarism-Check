'''
Created on 13-Nov-2013

@author: Rishabh Manoj
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
    ar=2**EXP2
    return ar
    # Your code
    
    
    
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
    if child_index==0:
        return None
    
    return child_index-1 >> EXP2
    # Your code


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    if((parent_index<<EXP2)+1<len(DATA)):
        return (parent_index<<EXP2)+1
    else:
        return None 
    # Your code


def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    if (get_leftmostchild_index(parent_index)==None):
        return None
    elif (((parent_index<<EXP2)+2**EXP2)<len(DATA)):
        return ((parent_index<<EXP2)+2**EXP2)
    else:
        return len(DATA)-1
    # Your code


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
    
    x=get_leftmostchild_index(parent_index)
    y=get_rightmostchild_index(parent_index)
    if(x==None):
        return None
   
    new = []
    for i in range (x,y+1):
        new.append(DATA[i])
            
    if (MIN_TOP==True):
        a=min(new)
        b=new.index(a)
        return x+b
    if (MIN_TOP==False):     
        a=max(new)
        b=new.index(a)
        return x+b

   
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    if (MIN_TOP==True):
        if (i==None or get_top_child(i)==None):
            return None
    
        elif ((DATA[get_top_child(i)]) < DATA[i]):
            c=get_top_child(i)
            (DATA[i],DATA[c])=(DATA[c],DATA[i])
            restore_subtree(c)

        
    elif (MIN_TOP==False):
        if (i==None or get_top_child(i)==None):
            return None
    
        elif ((DATA[get_top_child(i)]) > DATA[i]):
            c=get_top_child(i)
            (DATA[i],DATA[c])=(DATA[c],DATA[i])
            restore_subtree(c)

    
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code
    heapify()
        
def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    lastparent_index=get_parent_index(len(DATA)-1)
    if (lastparent_index == None):
        return None
    else:
        for i in range(0,lastparent_index+1):
            restore_subtree(lastparent_index - i )


def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    l=DATA[i]
    DATA[i]=DATA[-1]
    DATA[-1]=l
    DATA.remove(DATA[-1])
    restore_heap(i)
    # Your code


def pop():
    '''
    Pull the top element out of the heap
    '''
    pop=DATA[-1]
    DATA.remove(DATA[-1])
    return pop
    # Your code


def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    l=size()
    DATA[l]=obj
    return DATA
    # Your code


def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    DATA=DATA + lst
    return DATA 
    # Your code


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    DATA=[]
    return DATA
    # Your code

if __name__ == '__main__':
    pass
