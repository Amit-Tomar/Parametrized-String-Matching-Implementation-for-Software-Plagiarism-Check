'''
Created on 28-Oct-2013

@author: raghavan

'''

MIN_TOP = True # Says whether the heap is a Min-Heap(True) or a Max-Heap(False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and retuns 1 if 
#e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA = []

def initialize_heap(is_min = True, arity_exp = 1, compare_fn = None):
    '''
    function to initialize all values
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
    return len( DATA)
# Your code


def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    return 2 << ( EXP2-1)
    # Your code
    
    
    
def get_item_at(  i):
    '''
    Return the i-th element of the data list ( DATA)
    '''
    return  DATA[i]


def get_parent_index(  child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    
    c_index = (child_index-1) >>  EXP2
    if(c_index >= 0):
        return c_index
    else:
        return None
    # Your code


def get_leftmostchild_index(  parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    first_child = (parent_index <<  EXP2)+1
    if(first_child <  size()):
        return first_child
    else:
        return None
    # Your code


def get_rightmostchild_index(  parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    first_child =  get_leftmostchild_index(parent_index)
    if(first_child == None ):
        return None
    else:
        last_child = (parent_index+1) <<  EXP2
        while(first_child <= last_child):
            if(last_child <  size()):
                return last_child
            last_child -= 1
    
    # Your code


def get_top_child(  parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    
   
    req_child_index =  get_leftmostchild_index(parent_index)
    i = req_child_index
    j =  get_rightmostchild_index(parent_index)
   
    
    if(i != None):
       
        if( MIN_TOP == True):
            while(i <= j):
                if(  CMP_FUNCTION(  get_item_at(req_child_index),  get_item_at(i)) == 1 ):
                    req_child_index = i
                
                i += 1
        
        elif( MIN_TOP == False):
            while(i <= j):
                if(  CMP_FUNCTION (  get_item_at(req_child_index),  get_item_at(i)) == -1):
                    req_child_index = i
                
                i += 1
   
        
        return req_child_index
    else:
        return None
    # Your code


def restore_subtree(  i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    
    j =  get_top_child(i)
    
    if( i != None and j != None):
    
        if( MIN_TOP == True):
            
            while( CMP_FUNCTION ( DATA[i] ,  DATA[j]) == 1):
                DATA[i],  DATA[j] =  DATA[j],  DATA[i]
                i = j
                j =  get_top_child(i)
                if(j == None):
                    break
        
        elif( MIN_TOP == False):
            while( CMP_FUNCTION ( DATA[i] ,  DATA[j]) == -1):
                DATA[i],  DATA[j] =  DATA[j],  DATA[i]
                i = j
                j =  get_top_child(i)
                if(j == None):
                    break
    
    
    # Your code

    
def restore_heap(    i ):
    '''
    Restore the heap property for  DATA assuming that it has been 'corrupted' at index i
    The rest of  DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element
    '''
    if(i != None):
        p_index =  get_parent_index(i)
    
        if(p_index != None):
        
            if( MIN_TOP == True):    
                if( CMP_FUNCTION ( DATA[i] ,  DATA[p_index]) == -1):  
                    while( CMP_FUNCTION ( DATA[i] ,  DATA[p_index]) == -1 ):
                        DATA[i],  DATA[p_index] =  DATA[p_index],  DATA[i]
                        i = p_index
                        p_index =  get_parent_index(i)
                        if(p_index == None):
                            break
            
                else:
                     restore_subtree(i)
            
            elif( MIN_TOP == False):    
                if(  CMP_FUNCTION(  DATA[i] ,  DATA[p_index]) == 1):  
                    while( CMP_FUNCTION ( DATA[i] ,  DATA[p_index]) == 1 ):
                        DATA[i],  DATA[p_index] =  DATA[p_index],  DATA[i]
                        i = p_index
                        p_index =  get_parent_index(i)
                        if(p_index == None):
                            break
            
                else:
                     restore_subtree(i)        
        else:
             restore_subtree(i)
    # Your code


def heapify():
    '''
    Rearrange  DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    length =  size()-1
    i =  get_parent_index(length)
    if(i != None):
        while(i >= 0):
            restore_subtree(i)
            i -= 1
    
    # Your code


def remove(  i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    length =  size() - 1
    DATA[i],  DATA[length]= DATA[length],  DATA[i]
    DATA.pop()
    restore_heap(i)
    # Your code


def pop():
    '''
    Pull the top element out of the heap
    '''
    length =  size() - 1
    DATA[0],  DATA[length]= DATA[length],  DATA[0]
    top =  DATA.pop()
    restore_subtree(0)
    return top
    # Your code


def add( obj):
    '''
    Add an object 'obj' to the heap
    '''
    DATA.append(obj)
    restore_heap( size() - 1)
    # Your code


def import_list(  lst):
    '''
    Add all the elements of the list 'lst' to  DATA
    Make sure this does not modify the input list 'lst'
    '''
    for elem in lst:
        DATA.append(elem)
    
    # Your code


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    DATA = []
    # Your code
    
    
    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

if __name__ == '__main__':
    pass