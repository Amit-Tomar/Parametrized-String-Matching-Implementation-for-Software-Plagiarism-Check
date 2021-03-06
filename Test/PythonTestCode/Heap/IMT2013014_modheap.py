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
    return len(DATA)

def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
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
    
    if (child_index-1)>>EXP2 < 0:
        return None
    else:
        return (child_index-1)//arity()

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
   
    if  (parent_index<<EXP2)+2**EXP2 < size():
        return (parent_index<<EXP2)+2**EXP2
    else:
        return size()-1
    
          

def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    #children = DATA[get_leftmostchild_index(parent_index):get_rightmostchild_index(parent_index)+1]
    get_leftmostchild_index(parent_index)
    if MIN_TOP:
        if get_leftmostchild_index(parent_index)!=None:
            for i in range(get_leftmostchild_index(parent_index),get_rightmostchild_index(parent_index)+1):
                if CMP_FUNCTION(DATA[get_leftmostchild_index(parent_index)] , DATA [i])==1:
                    get_leftmostchild_index(parent_index) = i
        return get_leftmostchild_index(parent_index)
    else:
        if get_leftmostchild_index(parent_index)!=None : 
            for i in range(get_leftmostchild_index(parent_index),get_rightmostchild_index(parent_index)+1):
                if CMP_FUNCTION(DATA[get_leftmostchild_index(parent_index)] , DATA [i])==-1:
                    get_leftmostchild_index(parent_index) = i
        return get_leftmostchild_index(parent_index)
        #return DATA.index(max(children))

def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
 
    if(MIN_TOP==True):
            if(get_top_child(i)!=None):
                while(get_top_child(i) !=None and CMP_FUNCTION(DATA[i],DATA[get_top_child(i)]))==1:
                    DATA[i],DATA[get_top_child(i)]=DATA[get_top_child(i)],DATA[i]
                    i=get_top_child(i)
    
               
        
    else:
            if(get_top_child(i)!=None):
                while(get_top_child(i) !=None and CMP_FUNCTION(DATA[i],DATA[get_top_child(i)]))==-1:
                    DATA[i],DATA[get_top_child(i)]=DATA[get_top_child(i)],DATA[i]
                    i=get_top_child(i)  

              
   
#def parentchild_indices(i):
        #return i/2,2*i,(2*i+1)

    
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    
    if(MIN_TOP==True ):
        if(i != None ):
            parent_index = get_parent_index(i)
            if parent_index != None and CMP_FUNCTION( DATA[i] , DATA[parent_index])==1:
                while(i != None and parent_index != None  and CMP_FUNCTION( DATA[i] , DATA[parent_index]))==1:
                    DATA[i], DATA[parent_index]=DATA[parent_index],DATA[i]
                    i = parent_index
                    parent_index = get_parent_index(i)
            else:
                restore_subtree(i)
       
    else:
        if(i != None ):
            parent_index = get_parent_index(i)
            if parent_index != None and CMP_FUNCTION(DATA[parent_index]  , DATA[i])==-1:
                while(i != None and parent_index != None and CMP_FUNCTION(DATA[parent_index]  , DATA[i]))==-1:
                    DATA[i],DATA[parent_index]=DATA[parent_index],DATA[i]
                    i = parent_index
                    parent_index = get_parent_index(i)
            else:
                restore_subtree(i)
        

   
   

def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    i=get_parent_index(size()-1)
    while(i>=0):
        restore_subtree(i)
        i=i-1
        
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    global DATA
    DATA[i],DATA[-1]=DATA[-1],DATA[i]
    rem=DATA.pop()
    restore_heap(i)
    return rem



def pop():
    '''
    Pull the top element out of the heap
    '''
    rem = remove(0)
    return rem


def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    DATA.append(obj)
    restore_heap(size()-1)


def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    for i in lst:
        DATA.append(i)
    

def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    #remove(DATA)
    DATA=[]
    

if __name__ == '__main__':
    initialize_heap(False)
    lst=[2,4,1,0,9,6]
    import_list(lst)    
    heapify()
    print DATA