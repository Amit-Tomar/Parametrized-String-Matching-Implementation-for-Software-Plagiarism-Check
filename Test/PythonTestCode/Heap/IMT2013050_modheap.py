'''11111111
Created on 28-Oct-2013

@author: raghavan
'''
#from test.sortperf import randfloats

MIN_TOP = False 
# Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA = []


def initialize_heap(is_min = False, arity_exp = 1, compare_fn = None):
    
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
    return DATA[i]



def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    if(child_index != 0):
        return (child_index - 1) >> EXP2
    else:
        return None
    
    

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    
    leftmostchild_index = (parent_index << EXP2) + 1
    
    if(size() > leftmostchild_index):
        return leftmostchild_index
    else:
        return None
    
        
        
def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    
    if(get_leftmostchild_index(parent_index) == None):
        return None
    
    index1 = (parent_index<<EXP2)
    index2 = 2 << (EXP2 - 1)
    rightmost_index = index1 + index2
    
    final_index = size() - get_leftmostchild_index(parent_index)
    
    if(final_index < arity()):
        return (get_leftmostchild_index(parent_index) - 1) + final_index
    
    if(rightmost_index == get_leftmostchild_index(parent_index)):
        return None
    
    if(size() > rightmost_index):
        return rightmost_index
    else:
        return None


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
    rcindex = get_rightmostchild_index(parent_index)
    list_children = []
    dict_children = {}
    lcindex = get_leftmostchild_index(parent_index)
    
    if(lcindex == None):
        return None
    
    if(rcindex == None):
        final_rcindex = lcindex
    else:
        final_rcindex = rcindex
    
    for i in range(lcindex , final_rcindex + 1):
        dict_children[DATA[i]] = i
        list_children.append(DATA[i])
    
    if(MIN_TOP == True):
        minimum = min(list_children)
        favourable_index = dict_children[minimum]
    else:
        maximum = max(list_children)
        favourable_index = dict_children[maximum]
    
    return favourable_index
            
            
            
            
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    
    flag = 1
    index_child = get_top_child(i)
    
    if(MIN_TOP == True and index_child != None):
        minimum = DATA[index_child]
        if(minimum < DATA[i]):
            flag = 0
            
    elif(index_child != None):
        maximum = DATA[index_child]
        if(maximum > DATA[i]):
            flag = 0
    
    if(flag == 0):
        DATA[i] , DATA[index_child] = DATA[index_child] , DATA[i] 
        
        if(get_leftmostchild_index(index_child) != None):
            restore_subtree(index_child)
    
        
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    org_parent = i
    pindex = get_parent_index(i)
    
    if(MIN_TOP == True):
        flag = 1
        
        if(pindex == None):
            flag = 0
        
        if(flag == 1):
            
            while(DATA[pindex] > DATA[i]):

                DATA[pindex] , DATA[i] = DATA[i] , DATA[pindex]
                i = pindex
                pindex = get_parent_index(pindex)
                
                if(pindex == None):
                    break
                
    restore_subtree(org_parent)
        
            
            
            
def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''

    pindex = get_parent_index(size() - 1)
    while(pindex >= 0):
        restore_subtree(pindex)
        pindex = pindex - 1
        
    
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''

    DATA[size() - 1] , DATA[i] = DATA[i] , DATA[size() - 1]
    
    DATA.pop()
    if(i != size()):
        restore_subtree(i)



def pop():
    '''
    Pull the top element out of the heap
    '''
    first_ele = DATA[0]
    remove(0)
    return first_ele



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
   
    i = 0
    while(i < len(lst)):
        DATA.append(lst[i])
        i = i + 1
    
    
    
def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    global DATA
    DATA = []

if __name__ == '__main__':
    pass
   