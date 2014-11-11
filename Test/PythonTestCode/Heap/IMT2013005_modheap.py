'''
Created on 28-Oct-2013

@author: raghavan
'''

MIN_TOP = True # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

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
    Return the i-th element of the data list (DATA)
    '''
    return DATA[i]


def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    # Your code
    if(child_index!=0):
        return (child_index-1)//arity()
    else:
        return None
def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    if((arity()*parent_index)+1<len(DATA)):
        return (arity()*parent_index)+1
    else:
        return None

def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    rightc = arity()*parent_index+arity()
    if(get_leftmostchild_index(parent_index)==None):
        return None
    elif(len(DATA)>rightc):
        return rightc
    else:
        return len(DATA)-1    
def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
    if(MIN_TOP==True):
        minheap = DATA[(arity()*parent_index)+1:((arity()*parent_index)+arity()+1)]
        i = 0
        minimum = minheap[i]
        while(i<len(minheap)):
            if(CMP_FUNCTION(minheap[i], minimum) != 1):
                minimum = minheap[i]
            i += 1
        return arity()*parent_index+1+minheap.index(minimum)
    else:
        maxheap = DATA[(arity()*parent_index)+1:((arity()*parent_index)+arity()+1)]
        j = 0
        maximum = maxheap[j]
        while(i<len(maxheap)):
            if(CMP_FUNCTION(minheap[i], minimum)!=-1):
                maximum = maxheap[i]
            i += 1
        return arity()*parent_index+1+maxheap.index(maximum)
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    
    if(arity()*i+1<size()):
        subheap = DATA[((arity()*(i))+1):((arity()*i)+arity()+1)]
        var = 0
        minimum = subheap[var]
        maximum = minimum
        while(var<len(subheap)):
            if(CMP_FUNCTION(subheap[var], minimum)!=1):
                minimum = subheap[var]
            elif(CMP_FUNCTION(subheap[var], maximum)!=-1):
                maximum = subheap[var]
            var += 1
        j = arity()*i+1+subheap.index(minimum)
        k = arity()*i+1+subheap.index(maximum)
        if(MIN_TOP==True):
            if(CMP_FUNCTION(DATA[i], DATA[j])==1):
                DATA[i], DATA[j] = swap(DATA[i], DATA[j])
                i = j
                restore_subtree(i)
        elif(MIN_TOP==False):
            if(CMP_FUNCTION(DATA[i], DATA[k])==-1):
                DATA[i], DATA[k] = swap(DATA[i], DATA[k])     
                i = k
                restore_subtree(i)
    
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code
    if(i!=0):
        if(MIN_TOP==True):
            if(arity()*i+1<size()):
                subheap = DATA[((arity()*(i))+1):((arity()*i)+arity()+1)]
                var = 0
                minimum = subheap[var]
                maximum = minimum
                while(var<len(subheap)):
                    if(CMP_FUNCTION(subheap[var] , minimum)!=1):
                        minimum = subheap[var]
                    elif(CMP_FUNCTION(subheap[var] , maximum)!=-1):
                        maximum = subheap[var]
                    var += 1
                j = DATA.index(minimum)
                parent_index = get_parent_index(i)
                if(CMP_FUNCTION(DATA[i] , DATA[parent_index])==-1):
                    DATA[i] , DATA[parent_index] = swap(DATA[i] , DATA[parent_index])
                    i = parent_index
                    restore_heap(i)
                elif(CMP_FUNCTION(DATA[i] , minimum)==1):
                    DATA[i] , DATA[j] = swap(DATA[i] , DATA[j])
                    i = j
                    restore_subtree(i)
            elif(arity()*i+1>size()):
                parent_index = get_parent_index(i)
                if(CMP_FUNCTION(DATA[i] , DATA[parent_index])==-1):
                    DATA[i] , DATA[parent_index] = swap(DATA[i] , DATA[parent_index])
                    i = parent_index
                    restore_heap(i)
            else:
                i -= 1
        
            
        elif(MIN_TOP==False):
            if(arity()*i+1<size()):
                subheap = DATA[((arity()*(i))+1):((arity()*i)+arity()+1)]
                var = 0
                minimum = subheap[var]
                maximum = minimum
                while(var<len(subheap)):
                    if(CMP_FUNCTION(subheap[var], minimum)!=1):
                        minimum = subheap[var]
                    elif(CMP_FUNCTION(subheap[var] , maximum)!=-1):
                        maximum = subheap[var]
                    var += 1
                k = DATA.index(maximum)
                parent_index = get_parent_index(i)
                if(DATA[i]>DATA[parent_index]):
                    DATA[i] , DATA[parent_index] = swap(DATA[i] , DATA[parent_index])
                    i = parent_index
                    restore_heap(i)
                elif(CMP_FUNCTION(DATA[i] , maximum)==-1):
                    DATA[i] , DATA[k] = swap(DATA[i] , DATA[k])
                    i = k
                    restore_subtree(i)
            elif(arity()*i+1>=size()):
                parent_index = get_parent_index(i)
                if(CMP_FUNCTION(DATA[i] , DATA[parent_index])==1):
                    DATA[i] , DATA[parent_index] = swap(DATA[i] , DATA[parent_index])
                    i = parent_index
                    restore_heap(i)
            else:
                i -= 1
    else:
        restore_subtree(0)


def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    i = size()-1
    while(i>=0):
        if(MIN_TOP==True):
            if((arity()*i)+1<size()):
                subheap = DATA[((arity()*i)+1):(arity()*(i+1))+1]
                var = 0
                minimum = subheap[var]
                maximum = minimum
                while(var<len(subheap)):
                    if(CMP_FUNCTION(subheap[var] , minimum)!=1):
                        minimum = subheap[var]
                    elif(CMP_FUNCTION(subheap[var] , maximum)!=-1):
                        maximum = subheap[var]
                    var += 1
                j = (arity()*i)+1+subheap.index(minimum)
                if(CMP_FUNCTION(DATA[i] , minimum)==1):
                    DATA[i] , DATA[j] = swap(DATA[i] , DATA[j] )
                    i = j
                else:
                    i -= 1
            else:
                i -= 1
        elif(MIN_TOP==False):
            if((arity()*i)+1<size()):
                subheap = DATA[(arity()*(i))+1:(arity()*(i+1))+1]
                var = 0
                minimum = subheap[var]
                maximum = minimum
                while(var<len(subheap)):
                    if(CMP_FUNCTION(subheap[var] , minimum)!=1):
                        minimum = subheap[var]
                    elif(CMP_FUNCTION(subheap[var] , maximum)!=-1):
                        maximum = subheap[var]
                    var += 1
                k = (arity()*i)+1+subheap.index(maximum)
                if(CMP_FUNCTION(DATA[i] , maximum)==-1):
                    DATA[i] , DATA[k] = swap(DATA[i] , DATA[k] )
                    i = k
                else:
                    i -= 1
            else:
                i -= 1               
    return DATA                     
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    DATA[i] , DATA[-1] = swap(DATA[i] , DATA[-1])
    DATA.pop()
    restore_heap(i)
    

def pop():
    '''
    Pull the top element out of the heap
    '''
    # Your code
    
    DATA.reverse()
    pop1 = DATA.pop()
    DATA.reverse()
    heapify()
    return pop1

def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    # Your code
    DATA.append(obj)
    heapify()
    return DATA
def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    # Your code
    i = 0
    while(i<len(lst)):
        DATA.append(lst[i])
        i += 1
  

def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    DATA = []
def swap(a_1 , b_1):
    a_1 , b_1 = b_1 , a_1
    return a_1 , b_1
    
if __name__ == '__main__':
    pass
# DATA=[20,12,5,6,7,8,4,0,1,2,3,0,6]
# #heapify()
# restore_subtree(2)
# print DATA