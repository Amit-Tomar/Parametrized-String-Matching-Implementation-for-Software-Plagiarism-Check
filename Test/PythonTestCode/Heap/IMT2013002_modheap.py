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
    # Your code
    return len(DATA)

def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    # Your code
    return 1 << EXP2
    
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
    if child_index == 0:
        return None
    else:
        return (child_index - 1 ) >> EXP2

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    child_index = (parent_index << EXP2) + 1
    if child_index > size() - 1:
        return None
    else:
        return child_index
def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    child_index = (parent_index << EXP2) + arity()
    if get_leftmostchild_index(parent_index) == None:
        return None
    elif child_index > size() - 1:
        return size()-1
    else:
        return child_index

def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    
    i = get_rightmostchild_index (parent_index)
    temp = []
    if (MIN_TOP == True):
        if i == None:
            return None
        elif (i < (size()-1)):
            temp = DATA[get_leftmostchild_index(parent_index):i+1]
            a = min(temp) 
            temp_index = temp.index(a)
            return get_leftmostchild_index(parent_index) + temp_index
        elif (i == size()-1):
            temp = DATA[get_leftmostchild_index(parent_index):]
            a=min(temp) 
            temp_index=temp.index(a)
            return get_leftmostchild_index(parent_index)+temp_index
     
    if MIN_TOP == False:
        if i == None:
            return None
        elif i<size()-1:
            temp=DATA[get_leftmostchild_index(parent_index):i+1]
            a=max(temp) 
            temp_index=temp.index(a)
            return get_leftmostchild_index(parent_index)+temp_index
        elif i == size()-1:
            temp=DATA[get_leftmostchild_index(parent_index):i+1]
            a=max(temp) 
            temp_index=temp.index(a)
            return get_leftmostchild_index(parent_index)+temp_index
     

def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code

    if MIN_TOP == True:
        while (i!=None and i < size()):
            child_index = get_top_child(i)
            if child_index==None:
                return None
            elif CMP_FUNCTION(DATA[i], DATA[child_index])==1 :
                DATA[i], DATA[child_index] = DATA[child_index], DATA[i]
            i=child_index
            
    if MIN_TOP == False:
        while (i!=None and i < size()):
            child_index = get_top_child(i)
            if child_index == None:
                return None
            elif CMP_FUNCTION(DATA[i] , DATA[child_index]) == -1:
                DATA[i], DATA[child_index] = DATA[child_index], DATA[i]
            i=child_index


    
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code
    if MIN_TOP == True:
        while (i>0 and i!=None):
            if CMP_FUNCTION(DATA[get_parent_index(i)] , DATA[i]) == 1:
                DATA[get_parent_index(i)], DATA[i] = DATA[i], DATA[get_parent_index(i)]
    
            else:
                restore_subtree(i)
            i=get_parent_index(i)
        restore_subtree(0)
        
    if MIN_TOP == False:
        while (i>0 and i!=None):
            if CMP_FUNCTION(DATA[get_parent_index(i)] , DATA[i]) == -1:
                DATA[get_parent_index(i)], DATA[i] = DATA[i], DATA[get_parent_index(i)]
            else:
                restore_subtree(i)
            i=get_parent_index(i)
        restore_subtree(0)


def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    
    i=size()-1
    while i>0:
        restore_heap(i)
        i-=1

def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    DATA[i], DATA[size()-1]=DATA[size()-1], DATA[i]
    element=DATA.pop()
    heapify()
    return element
    

def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    return remove(0)


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
    i=0
    while i<len(lst):
        DATA.append(lst[i])
        i+=1
    
def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    DATA=[]
    

if __name__ == '__main__':
    pass
    
#     self.assertEqual(lst[-1], modheap.pop())
#     self.assertEqual(lst[-2], modheap.pop())