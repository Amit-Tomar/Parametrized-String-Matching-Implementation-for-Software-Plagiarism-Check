'''
Created on 28-Oct-2013

@author: raghavan
'''

MIN_TOP = False # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise

CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2

EXP2 = 2

# The list of elements organized as a heap

DATA = []

def initialize_heap( is_min = True, arity_exp = 1, compare_fn = None ) :
    global MIN_TOP, CMP_FUNCTION, EXP2, DATA
    MIN_TOP = is_min
    CMP_FUNCTION = compare_fn
    EXP2 = arity_exp
    DATA = []
    
    
def size():
    
    '''
    Return the size of the heap
    '''
    
    global DATA
    return len(DATA)


def arity():
    
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    
    global DATA
    return 2 << (EXP2-1)


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
    parent_index = ( child_index - 1 ) / ( 2 << ( EXP2 - 1 ) )
    if parent_index < 0 :
        return None
    else:
        return parent_index
 
 
def get_leftmostchild_index(parent_index):
    
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    
    global DATA
    left_child = ( parent_index * arity() ) + 1
    if left_child > size()-1 :
        return None
    else:
        return left_child
    
    
def get_rightmostchild_index(parent_index):
    
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    
    global DATA
    right_child = None
    if get_leftmostchild_index == None:
        return None
    else:
        i=1
        while i <= arity() :
            temp = ( parent_index * arity() ) + i
            if temp > ( size() - 1 ) :
                break
            i += 1
            right_child = temp
        return right_child


def get_top_child(parent_index):
    
    '''
    Return the index of the child which is most favored to move up the tree among all the children of the
    element at parent_index
    '''
    
    global DATA
    child_index = ( parent_index << EXP2 ) + 1
    if(child_index < size()):
        i = child_index
        top_child = DATA[child_index]
        if MIN_TOP == True:
            while child_index <= i + arity() - 1 and child_index < size() :
                if ( DATA[child_index] <= top_child ):
                    top_index = child_index
                    top_child = DATA[top_index]
                child_index = child_index + 1
            return top_index
    
        else:
            while child_index <= i + arity() - 1 and child_index < size() :
                if DATA[child_index] >= top_child:
                    top_index = child_index
                    top_child = DATA[top_index]
                child_index = child_index + 1
            return top_index
    else:
        return None


def restore_subtree(i):
    '''
    global MIN_TOP, CMP_FUNCTION, EXP2, DATA
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    
    global DATA  
    
    child_index = get_top_child(i)
    if child_index != None :
        if MIN_TOP == False :
            if CMP_FUNCTION(DATA[i] , DATA[child_index]) == -1 :
                DATA[i] , DATA[child_index] = DATA[child_index] , DATA[i]
                restore_subtree(child_index)
        else:
            if CMP_FUNCTION(DATA[i] , DATA[child_index]) == 1 :
                DATA[i] , DATA[child_index] = DATA[child_index] , DATA[i]
                restore_subtree(child_index)
    
             
def restore_heap(i):    
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code
    global DATA
    parent_index = get_parent_index(i)
    count_restore = 0
    i_copy = i
    if MIN_TOP==True:
        while  i != 0 :
            
            parent_index = get_parent_index(i)
            if CMP_FUNCTION(DATA[i] , DATA[parent_index]) == -1  :
                DATA[i] , DATA[parent_index] = DATA[parent_index] , DATA[i]
                count_restore += 1
                i = parent_index
            
            else:
                restore_subtree(i)
                break
    
    else:
        while  i!=0 :
            parent_index = get_parent_index(i)
            if CMP_FUNCTION(DATA[i] , DATA[parent_index]) == 1 :
                DATA[i] , DATA[parent_index] = DATA[parent_index] , DATA[i]
                count_restore += 1
                i = parent_index
            else:
                break      
        restore_subtree(i)             
   
    if count_restore == 0:
        restore_subtree(i_copy)
         
def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    global DATA
    parent_index = ( size() - 2 ) >> EXP2
    
    while parent_index >= 0:
        restore_subtree( parent_index )
        parent_index -= 1
            
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    global DATA
    DATA[i],DATA[size()-1]=DATA[size()-1],DATA[i]
    removed_element = DATA[ size()-1 ]
    DATA=DATA[ 0 : size()-1 ]
    return removed_element
    
    
def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    global DATA
    
    pop_element = remove(0)
    heapify()
    return pop_element

def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    # Your code
    global DATA
    
    DATA.append(obj)
    heapify()
    return DATA
    
def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    # Your code
    global DATA
    for i in lst:
        DATA.append(i)

def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    global DATA
    DATA = []
  
if __name__ == "__main__":
    pass    