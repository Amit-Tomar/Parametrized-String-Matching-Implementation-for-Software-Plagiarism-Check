'''
Created on 7-Nov-2013

@author: satwik
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


def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    return 2<<(EXP2-1)
    
print arity()
    
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
    if(child_index!=0):
        return (child_index-1)>>EXP2
    else:
        return None

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    if(parent_index!=None and parent_index<=get_parent_index(len(DATA)-1)):
        return (parent_index<<EXP2)+1

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    if(parent_index==0):
        return arity()
    elif(parent_index<=get_parent_index(size()-1)):
        return (parent_index+1)<<EXP2


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    if(parent_index<=get_parent_index(size()-1)):
        i=1
        children_given_parent=[]
        if(parent_index==get_parent_index(len(DATA)-1)):
            while(get_rightmostchild_index(parent_index-1)is not None and i<=(size()-get_rightmostchild_index(parent_index-1)-1)):
                children_given_parent.append(DATA[get_rightmostchild_index(parent_index-1)+i])
                i+=1
        else:
            while(i<=arity()):
                children_given_parent.append(DATA[get_rightmostchild_index(parent_index-1)+i])
                i+=1
        if(MIN_TOP==True):
            return get_rightmostchild_index(parent_index-1)+children_given_parent.index(min(children_given_parent))+1
        else:
            return get_rightmostchild_index(parent_index-1)+children_given_parent.index(min(children_given_parent))+1


def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    present_parent_index=i
    if(MIN_TOP==True):
        while(get_top_child(present_parent_index)!=None and cmp(DATA[present_parent_index],DATA[get_top_child(present_parent_index)])==1):
            temp_variable=get_top_child(present_parent_index)
            DATA[present_parent_index],DATA[get_top_child(present_parent_index)]=DATA[get_top_child(present_parent_index)],DATA[present_parent_index]
            present_parent_index=temp_variable
    else:
        while(get_top_child(present_parent_index)!=None and cmp(DATA[present_parent_index],DATA[get_top_child(present_parent_index)])==-1):
            temp_variable=get_top_child(present_parent_index)
            DATA[present_parent_index],DATA[get_top_child(present_parent_index)]=DATA[get_top_child(present_parent_index)],DATA[present_parent_index]
            present_parent_index=temp_variable


def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    if(i==0):
        parent_index=i
    else:
        parent_index=get_parent_index(i)
    while(1):
        restore_subtree(parent_index)
        if(restore_subtree(parent_index)==None):
            restore_subtree(i)
            break
        parent_index=get_parent_index(parent_index)

def heapify():    
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    last_parent_index=get_parent_index(len(DATA)-1)
    lastlast_parent_index=get_parent_index(last_parent_index)
    range_elements_lastrow=last_parent_index-lastlast_parent_index
    i=0
    while(i<range_elements_lastrow):
        restore_heap(lastlast_parent_index+i)
        i+=1


def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    temp_variable=DATA[len(DATA)-1]
    DATA[len(DATA)-1]=DATA[i]
    DATA[i]=temp_variable
    DATA.remove(DATA[len(DATA)-1])
    restore_heap(i)
    


def pop():
    '''
    Pull the top element out of the heap
    '''
    '''temp_variable=DATA[len(DATA)-1]
    DATA[len(DATA)-1]=DATA[0]
    DATA[0]=temp_variable
    DATA.remove(DATA[len(DATA)-1])
    nextlevel_parent=0
    exchanged_element=get_top_child(nextlevel_parent)
    restore_subtree(nextlevel_parent)
    restore_subtree(exchanged_element)
    while(restore_subtree(exchanged_element)!=None):
        if(restore_subtree(exchanged_element==None)):
            break
        exchanged_element=get_top_child(exchanged_element)
        restore_subtree(exchanged_element)
    '''
    temp=DATA[0]
    remove(0)
    return temp

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
    i=0
    while(i<len(lst)):
        DATA.append(lst[i])
        i+=1


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    DATA=[]

if __name__ == '__main__':
    pass
    DATA=[2,4,1,0,9,6]
    heapify()
    print DATA
