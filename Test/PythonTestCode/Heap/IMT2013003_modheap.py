'''
Created on 09-Nov-2013

@author: aditya9509
'''

MIN_TOP = True # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap

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
   
    return 2<<(EXP2-1)


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
    if(child_index==0):
        return None
    else:
        
        parent_index = ((child_index-1)>>EXP2)
        return parent_index

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    
    leftmostchild_index= (parent_index<<EXP2)+1
    # Your code
    if(leftmostchild_index>=len(DATA)):
        return None
    else:
        return leftmostchild_index
    

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code

    left_index=get_leftmostchild_index(parent_index)
    if(left_index==None):
        return None
    
    else:
        ref=0
        while(ref<arity()):
            rightmost_index=left_index+ref
        
            if(rightmost_index>=len(DATA)-1):
                return rightmost_index
                break
                  
            else:
                ref=ref+1
        return rightmost_index 


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''

    # Your code
    temp_var=[]
    child_index_first=(arity()*parent_index) +1
    child_index_last=(arity()*parent_index) + (arity()+1)
    if(child_index_last>size()):  
        temp_var=temp_var+DATA[child_index_first:]  
    else:
        temp_var=temp_var+DATA[child_index_first:child_index_last]
    if(child_index_first>=size()):
        return None
    if(MIN_TOP== False):
        value=max(temp_var)
        ref_val=temp_var.index(value)
        return ref_val+get_leftmostchild_index(parent_index)
    else:
        value=min(temp_var)
        ref_val=temp_var.index(value)
        return ref_val+get_leftmostchild_index(parent_index)

def restore_subtree(i):
    while(i!=None and i<len(DATA)):
        topmost_child_index=get_top_child(i)
        if(topmost_child_index==None):
            return None
        topmost_child_value=DATA[topmost_child_index]
        if(MIN_TOP==False):
            if(topmost_child_value>DATA[i]):
                DATA[i],DATA[topmost_child_index]=DATA[topmost_child_index],DATA[i]
        else:
            if(topmost_child_value<DATA[i]):
                DATA[i],DATA[topmost_child_index]=DATA[topmost_child_index],DATA[i]
        i=topmost_child_index
    
                

def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element
    '''
    # Your code
    if(MIN_TOP==True):
        while(i!=None and i>0):
            parent_index=get_parent_index(i)
            if(DATA[i]<DATA[parent_index]):
                DATA[i],DATA[parent_index]=DATA[parent_index],DATA[i]
            else:
                restore_subtree(i)
            i=parent_index
        restore_subtree(0)
    else:
        while(i!=None and i>0):
            parent_index=get_parent_index(i)
            if(DATA[i]>DATA[parent_index]):
                DATA[i],DATA[parent_index]=DATA[parent_index],DATA[i]
            else:
                restore_subtree(i)
            i=parent_index
        restore_subtree(0) 

def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    
    firstnonleaf_index= get_parent_index(len(DATA)-1)
    
    while(firstnonleaf_index>=0):
        restore_subtree(firstnonleaf_index)
        firstnonleaf_index=firstnonleaf_index-1
       

def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    temp=DATA[len(DATA)-1]
    DATA[len(DATA)-1]=DATA[i]
    DATA[i]=temp
    element=DATA.pop()
    heapify()
    return element

def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    return remove(0)
    heapify()
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
    len_lst=len(lst)
    i=0
    while(i<len_lst):
        DATA.append(lst[i])
        i=i+1
    
    return DATA



def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    DATA=[]
    
if __name__ == '__main__':
    pass
