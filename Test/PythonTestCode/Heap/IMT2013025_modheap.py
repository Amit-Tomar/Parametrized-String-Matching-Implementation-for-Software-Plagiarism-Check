'''
Created on 28-Oct-2013

@author: raghavan
'''

MIN_TOP = False
# Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and,
# retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA = []
# 2, 1, 5, 7, 15, 9, 14, 3, 10, 6, 23, 18, 11, 0, 24, 25, 16, 20, 22, 4, 12
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
    # Your code
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
    # Your codeget_parent_index(c
    if child_index <= 0:
        return None
    else:
        index = (child_index-1) >> EXP2
        return index


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of theget_parent_index(c element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    parent_index2 = parent_index << EXP2
    if ((parent_index2+1) >= size()):
        return None
    else:
        return (parent_index2+1)
    # Your code


def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    left_child = get_leftmostchild_index(parent_index)
    arity_heap = arity()
    if get_leftmostchild_index(parent_index) == None:
        return None
    if ((left_child + arity_heap -1) >= size()):
        return size() - 1
    else:
        return (left_child + arity_heap -1)


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code

    
    position = get_leftmostchild_index(parent_index)
    leftchild = get_leftmostchild_index(parent_index)
    rightchild = get_rightmostchild_index(parent_index)
    if leftchild == None and rightchild == None:
        return None
    temp =  DATA[get_leftmostchild_index(parent_index)]
    for i in range(leftchild, rightchild + 1):
        
        if MIN_TOP and DATA[i] < temp :
            position = i
            temp = DATA [i]
        elif not MIN_TOP and DATA[i] > temp :
            position = i
            temp = DATA [i]
            
    return position
            

    
    


def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
  
        
    topchild_index = get_top_child(i)
    if i > get_parent_index(size()-1) :
        return None
    while (topchild_index>0 and topchild_index != None):
        if MIN_TOP and DATA[i] > DATA[topchild_index]:
            DATA[i], DATA[topchild_index] = DATA[topchild_index], DATA[i]
        elif not MIN_TOP and DATA[i] < DATA[topchild_index]:
            DATA[i], DATA[topchild_index] = DATA[topchild_index], DATA[i]
        
        
        i = topchild_index
        topchild_index = get_top_child(topchild_index)

        
    return DATA

    
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
    if MIN_TOP:
        if parent_index != None and DATA[i] < DATA[parent_index]:
            while (parent_index != None and DATA[i] < DATA[parent_index]):
                DATA[i], DATA[parent_index] = DATA[parent_index], DATA[i]
                i = parent_index 
                parent_index = get_parent_index(i)    
                
        else:
            restore_subtree(i)
    else:
        if (parent_index != None and DATA[i] > DATA[parent_index]) :
            while parent_index != None and DATA[i] > DATA[parent_index]:
                DATA[i], DATA[parent_index] = DATA[parent_index], DATA[i]
                i = parent_index    
                parent_index = get_parent_index(i) 
            
        else:
            restore_subtree(i)
        


def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    last_node = get_parent_index(size()-1)
    while last_node >= 0:
        restore_subtree(last_node)
        last_node = last_node - 1
    

def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    DATA[i], DATA [size()-1] = DATA [size()-1], DATA[i]
    DATA.pop()
    heapify()
    


def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    
    top_element = DATA[0]
    remove(0)
    #DATA[0] = DATA [size()-1]
    #DATA = DATA[0:-1]
    #restore_subtree(0)
    return top_element

def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    # Your code
    DATA.append(obj)
    heapify()
    #restore_heap(size()-1)


def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    # Your code
    for i in lst:
        DATA.append(i)

def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    while len(DATA)>0:
        DATA.pop()

if __name__ == '__main__':
    pass
    #print size()
    #print arity()
    #restore_subtree(2)
    #print get_top_child(2)
    #print DATA
