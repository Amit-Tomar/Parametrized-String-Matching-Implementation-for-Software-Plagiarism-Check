'''
Created on 10-Nov-2013

@author: vivek
'''
MIN_TOP = False# Says whether the heap is a Min-Heap (True) or a Max-Heap (False)
    
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
    return 2**EXP2
        
        
        
def get_item_at(i):
    '''
    Return the i-th element of the data list (new_heap)
    '''
    return DATA[i]
    
    
    
def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    if(child_index==0):
        return None
    else:
        return (child_index-1) >>EXP2
    
    
def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    if ((parent_index<<EXP2)+1) < size():
        return ((parent_index<<EXP2)+1)
    
    
    
def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    x = (parent_index << EXP2) + arity()
    if(get_leftmostchild_index==None):
        return None    
    if(x>size()):
        return len(DATA)-1
    else:
        return x
    
    
    
def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    x=[]
    childindex_start=(arity()*parent_index) +1
    childindex_end=(arity()*parent_index) + (arity()+1)
    if(childindex_end>size()):  
        x=x+DATA[childindex_start:]  
    else:
        x=x+DATA[childindex_start:childindex_end]
    if(childindex_start>=size()):
        return None
    if(MIN_TOP== False):
        val=max(x)
        a=x.index(val)
        return a+get_leftmostchild_index(parent_index)
    else:
        val=min(x)
        a=x.index(val)
        return a+get_leftmostchild_index(parent_index)
            
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    while(i!=None and i<size()):
        childindex=get_top_child(i)
        if(childindex==None):
            return None
        element=DATA[childindex]
        if(MIN_TOP==False):
            if(element>DATA[i]):
                DATA[i],DATA[childindex]=DATA[childindex],DATA[i]
        else:
            if(element<DATA[i]):
                DATA[i],DATA[childindex]=DATA[childindex],DATA[i]
        i=childindex
        
print restore_subtree(1)
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    if(MIN_TOP==True):
        while(i!=None and i>0):
            parentindex=get_parent_index(i)
            if(DATA[i]<DATA[parentindex]):
                DATA[i],DATA[parentindex]=DATA[parentindex],DATA[i]
            else:
                restore_subtree(i)
            i=parentindex
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
    i=(size()-1)    
    while(i>0):
        restore_heap(i)
        i-=1
               
        
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    #DATA[i],DATA[-1]=DATA[-1],DATA[i]
    swap(i,-1)
    var=DATA.pop()
    heapify()
    return var 
    
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
    heapify()
    
    
def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
        
    i=0
    while(i<len(lst)):
        DATA.append(lst[i])
        i=i+1
            
def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    
       
def swap(x,y):
    (DATA[x],DATA[y])=(DATA[y],DATA[x])        

if __name__ == '__main__':
    pass 