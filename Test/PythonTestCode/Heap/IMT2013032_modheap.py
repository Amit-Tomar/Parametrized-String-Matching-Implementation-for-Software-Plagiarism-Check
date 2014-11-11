'''
Created on 28-Oct-2013

@author: raghavan
'''
MIN_TOP = True # Says whether the heap is a Min-Heap (True) or a Max-Heap(False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and returns 1 
# if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION  = None

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

def swap(index_1, index_2):
    '''
    swapping 2 elements
    '''
    DATA[index_1], DATA[index_2] = DATA[index_2], DATA[index_1]

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
    return 2 << (EXP2-1)
    
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
    if( (child_index-1) >> EXP2 >= 0):
        return (child_index-1) >> EXP2
    else : return None

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    
    if ( (parent_index << EXP2) + 1 < size()):
        return (parent_index << EXP2 ) + 1
    else :  return None      

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    if ( (parent_index << EXP2) + arity() < size()) :
        return (parent_index << EXP2) + arity()
    elif ( get_leftmostchild_index(parent_index) != None):
        return size() - 1
    else :
        return None    
    
def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code        
    leftmost_child = get_leftmostchild_index(parent_index)    
    rightmost_child = get_rightmostchild_index(parent_index)
    top_child = leftmost_child
    
    if(leftmost_child != None):
                   
        if(MIN_TOP == True):
            while(leftmost_child <= rightmost_child):
                if( CMP_FUNCTION ( DATA[top_child], DATA[leftmost_child]) == 1):
                    top_child = leftmost_child                
                leftmost_child += 1
        
        elif(MIN_TOP==False):
            while(leftmost_child <= rightmost_child):
                if(CMP_FUNCTION ( DATA[top_child], DATA[leftmost_child]) == -1):
                    top_child = leftmost_child               
                leftmost_child += 1  
        
        return top_child
    else:
        return None

def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code    
    top_child = get_top_child(i)
    
    if top_child != None and i != None:
    
        if MIN_TOP:
            while CMP_FUNCTION (DATA[i], DATA[top_child]) == 1 :
                i, top_child = child_recur(i, top_child)
                if(top_child == None):
                    break
        else :
            while CMP_FUNCTION (DATA[i], DATA[top_child]) == -1 : 
                i, top_child = child_recur(i, top_child)
                if(top_child == None):
                    break
                
def child_recur(i, top_child):
    '''
    To swap an element and its child
    '''
    swap(i, top_child)
    i = top_child
    top_child = get_top_child(i)
    return i, top_child                  
                    
def parent_recur(i, parent_index): 
    '''
    To swap an element and its parent 
    '''
    swap(i, parent_index)
    i = parent_index    
    parent_index = get_parent_index(i)
    return i, parent_index

def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (child_recur(i, top_child)i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code    
    if i != None :
        parent_index = get_parent_index(i)
               
    flag = 0      
       
    if(parent_index != None ): 
        
        if MIN_TOP:            
            while CMP_FUNCTION (DATA[i], DATA[parent_index]) == -1:
                flag = 1
                i, parent_index = parent_recur(i, parent_index)
                if parent_index == None :
                    break
                
        else:                         
            while CMP_FUNCTION (DATA[i], DATA[parent_index]) == 1 :
                flag = 1
                i, parent_index = parent_recur(i, parent_index)
                if parent_index == None:
                    break
    
    if (flag == 0 ) :
        restore_subtree(i)
        
def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code 
    parent_index = get_parent_index(size() - 1)
    
    if parent_index != None :
        while parent_index >= 0:
            restore_subtree(parent_index)
            parent_index -= 1 
    
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    swap (i, len(DATA)-1)
    DATA.pop()
    restore_heap(0)
    
def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    length = DATA[0] 
    remove(0)
    return length

def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    # Your code    
    DATA.append(obj)    
    restore_heap(size()-1)
    
def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    # Your code
    for elem in lst :
        DATA.append(elem)
            
def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your codeleftmost_child <= rightmost_child
    global DATA    
    DATA = []

if __name__ == '__main__':
    pass    