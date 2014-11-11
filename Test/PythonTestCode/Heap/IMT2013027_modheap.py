'''
Created on 28-Oct-2013

@author: raghavan

Last modified on 14-Nov-2013

@modifier: Nigel Steven Fernandez (IMT2013027)
'''

# Says whether the heap is a Min-Heap (True) or a Max-Heap (False)
MIN_TOP = False 
 
#Comparison Function for the heap
#Takes two elements - e1, e1 - of the heap as arguments and 
#retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise

CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA = []


def initialize_heap(is_min = True, arity_exp = 1, compare_fn = None):
    '''
    initializes heap characteristics
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
    return len(DATA)


def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    return 2 << (EXP2 - 1)
    
        
def get_item_at(i):
    '''
    Return the i-th element of the data list (DATA)
    '''
    if(i in range(0, size())):
        return DATA[i]
    
    return None


def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    if(child_index == 0):
        return None
    else:
        return (child_index - 1) >> EXP2


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    leftmostchild_index = (parent_index << EXP2) + 1
    
    if(leftmostchild_index > (size() - 1)):
        return None
    else:
        return leftmostchild_index


def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    #min() used to take care of incomplete heap
    rightmostchild_index = min( [ (parent_index << EXP2) + arity(), size() - 1])
     
    if(get_leftmostchild_index(parent_index) == None):
        return None
    else:
        return rightmostchild_index


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree 
    among all the children of the element at parent_index
    '''
    #stores a list of children of parent at index i
    children = (DATA[get_leftmostchild_index(parent_index) 
                : get_rightmostchild_index(parent_index) + 1])
    
    children_sorted = children[:] 
    children_sorted.sort(CMP_FUNCTION)
        
    offset = get_leftmostchild_index(parent_index)
    
    return ((offset + children.index(children_sorted[0])) if MIN_TOP else
            (offset + children.index(children_sorted[-1]))) 


def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    while(i <= get_parent_index(size()-1) and 
          not is_favoured(i, get_top_child(i))):
        j = get_top_child(i)
        DATA[i], DATA[j] = DATA[j], DATA[i]
        i = j 

    return None


def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    flag = 0
    while(i > 0 and is_favoured(get_parent_index(i), i) == False): 
        DATA[i], DATA[get_parent_index(i)] = DATA[get_parent_index(i)], DATA[i]
        i = get_parent_index(i)
        flag = 1
    
    if(flag == 0):
        restore_subtree(i)
    
    return None
        
    
def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    i = get_parent_index(size() - 1)
    while(i >= 0):
        restore_subtree(i)
        i -= 1
    
    return None


def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    DATA[i], DATA[size() - 1] = DATA[size() - 1], DATA[i]
    obj = DATA.pop()
    restore_subtree(i)    
    
    return obj


def pop():
    '''
    Pull the top element out of the heap
    '''
    return remove(0)


def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    DATA.append(obj)
    i = size() - 1
    while(i != 0 and is_favoured(get_parent_index(i), i) == False): 
        DATA[i], DATA[get_parent_index(i)] = DATA[get_parent_index(i)], DATA[i]
        i = get_parent_index(i)
    
    return None


def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    global DATA
    DATA = lst[:]
        
    return None


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    global DATA
    DATA = []
    
    return None

    
def is_favoured(i, j):
    '''
    Return True if the element at index1 is favoured over the element at index2 --- 
    In other words a heap is a data structure which ensures that any node is favoured over any of its children
    Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
    '''
    if ((MIN_TOP and CMP_FUNCTION(get_item_at(j), get_item_at(i)) < 0) or
        (not MIN_TOP and CMP_FUNCTION(get_item_at(j), get_item_at(i)) > 0)):
        return False
    else:
        return True
       
    
if __name__ == '__main__':
    pass
