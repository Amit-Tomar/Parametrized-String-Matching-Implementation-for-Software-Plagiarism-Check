'''
Created on 28-Oct-2013

@author: raghavan
'''

MIN_TOP = False # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)
FLAG=0

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = lambda x, y : (1 if (x > y) else (-1 if (x < y) else 0))

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
    return 1<<EXP2
    
    
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
    if (child_index>0):
        return ((child_index-1)>>EXP2)
    return None
    
def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    if(parent_index == None):
        return None
    elif (((parent_index<<EXP2)+1)<size()):
        return (parent_index<<EXP2)+1
    else:
        return None    


def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    if(((parent_index<<EXP2)+arity()<size())):
        return((parent_index<<EXP2)+arity())
    elif(get_leftmostchild_index==None):
        return None
    else:
        return (size()-1)
    


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
#     if(get_leftmostchild_index(parent_index)==None):
#         return None
#     temp=[]
#     i=get_rightmostchild_index(parent_index)
#     if(i!=None and MIN_TOP==True and i<size()-1):    
#         temp=((DATA[get_leftmostchild_index(parent_index):i+1]))
#         mini=temp[0]
#         i=0
#         while(i<len(temp)):
#             if(CMP_FUNCTION(mini,temp[i])!=-1):
#                 mini=temp[i]
#             i+=1
#         k=temp.index(mini)
#         return get_leftmostchild_index(parent_index)+k
#     if(i!=None and MIN_TOP==True and i==size()-1):
#         temp=((DATA[get_leftmostchild_index(parent_index):]))
#         mini=temp[0]
#         i=0
#         while(i<len(temp)):
#             if(CMP_FUNCTION(mini,temp[i])!=-1):
#                 mini=temp[i]
#             i+=1
#         k=temp.index(mini)
#         return get_leftmostchild_index(parent_index)+k
#     if(i!=None and MIN_TOP==False and i<size()-1):    
#         temp=((DATA[get_leftmostchild_index(parent_index):i+1]))
#         mini=temp[0]
#         i=0
#         while(i<len(temp)):
#             if(CMP_FUNCTION(mini,temp[i])!=1):
#                 mini=temp[i]
#             i+=1
#         k=temp.index(mini)
#         return get_leftmostchild_index(parent_index)+k
#     if(i!=None and MIN_TOP==False and i==size()-1):
#         temp=((DATA[get_leftmostchild_index(parent_index):]))
#         mini=temp[0]
#         i=0
#         while(i<len(temp)):
#             if(CMP_FUNCTION(mini,temp[i])!=1):
#                 mini=temp[i]
#             i+=1
#         k=temp.index(mini)
#         return get_leftmostchild_index(parent_index)+k
#     else:
#         return None
    temp = []
    childindex_start = (arity()*parent_index) + 1
    childindex_end = (arity()*parent_index) + (arity()+1)
    if(childindex_end > size()):  
        temp = temp + DATA[childindex_start:]  
    else:
        temp = temp+DATA[childindex_start:childindex_end]
    if(childindex_start >= size()):
        return None
    if(MIN_TOP == False):
        val = max(temp)
        temp_index = temp.index(val)
        return  temp_index + get_leftmostchild_index(parent_index)
    else:
        val = min(temp)
        temp_index = temp.index(val)
        return  temp_index + get_leftmostchild_index(parent_index)
    
    
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    if (MIN_TOP==True):
        while (i!=None and i<size()):
            a=get_top_child(i)
            if a==None:
                return None
            elif (CMP_FUNCTION(DATA[i],DATA[a])==1):
                DATA[i],DATA[a]=DATA[a],DATA[i]
            i=a
    if (MIN_TOP==False):
        while (i!=None and i<size()):
            a=get_top_child(i)
            if (a==None):
                return None
            elif (CMP_FUNCTION(DATA[i],DATA[a])==-1):
                DATA[i],DATA[a]=DATA[a],DATA[i]
            i=a

    
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code
    a=get_parent_index(i)
    global FLAG
    if (a!=None and (CMP_FUNCTION(DATA[i],DATA[a])==-1) and MIN_TOP==True):
        DATA[i],DATA[a]=DATA[a],DATA[i]
        FLAG+=1 
        restore_heap(a)
    elif (a!=None and (CMP_FUNCTION(DATA[i],DATA[a])==1) and MIN_TOP==False):
        DATA[i],DATA[a]=DATA[a],DATA[i]
        FLAG+=1
        restore_heap(a)
    if (FLAG==0):
        restore_subtree(i)


def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    i=get_parent_index(size()-1)
    while(i>=0):
        restore_subtree(i)
        i-=1
    return DATA   


def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    last=size()-1
    DATA[i],DATA[last]=DATA[last],DATA[i]
    a=DATA.pop()
    heapify()
    return a
    
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
    global DATA
    DATA=lst[:]


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    global DATA
    DATA=[]

if __name__ == '__main__':
    pass
