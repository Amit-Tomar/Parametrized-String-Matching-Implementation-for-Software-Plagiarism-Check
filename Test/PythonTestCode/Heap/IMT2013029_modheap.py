MIN_TOP = False # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA = [2,3,4,5,1,2,5,7,8,9]

def swap(x,y):
    x,y=y,x

def initialize_heap(is_min = True, arity_exp = 1, compare_fn = None):
    global MIN_TOP, CMP_FUNCTION, EXP2, DATA
    MIN_TOP = is_min
    CMP_FUNCTION = compare_fn
    EXP2 = arity_exp
    DATA = [2,3,4,5,1,2,5,7,8,9]


def size():
    '''
    Return the size of the heap
    '''
    global DATA
    return len(DATA)


def arity():
    '''
    Return the arity of the heap - max number of children that any internal node has
    Also only one internal node will have less children than the arity of the heap
    '''
    global EXP2
    return 2**EXP2
 
    
def get_item_at(i):
    '''
    Return the i-th element of the data list (DATA)
    '''
    global DATA
    return DATA[i]


def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    global DATA
    if(child_index == 0):
        return None
    else:
        return (child_index-1)/(arity())

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''    # Your code
    global DATA
    l=size()
    x=(arity()*parent_index)+1
    if(x>=l):
        return None
    else:
        return x

        
def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    global DATA
    l=size()
    if(get_leftmostchild_index(parent_index) == None):
        return None
    x=arity()*(parent_index+1)
    if(x>=l):
        return size()-1
    else:
        return x
    


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    global DATA
    l=size()
    x=arity()*parent_index+1
    if(x>=l):
        return None
    else:
        if(MIN_TOP==True):
            return DATA.index(min(DATA[x:arity()*parent_index+arity()+1]))
        else:
            return DATA.index(max(DATA[x:arity()*parent_index+arity()+1]))


def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''         
    if (MIN_TOP == True):
        if (len(DATA)> 0 and get_top_child(i)):
            temp=get_top_child(i)
            if (DATA[get_top_child(i)] > DATA[i]):
                DATA[i],DATA[get_top_child[i]]=DATA[get_top_child[i]],DATA[i]
                
                restore_subtree(temp)
            elif (DATA[i] > DATA[get_top_child(i)]):
                return None
                
    elif (MIN_TOP == False):
        if (len(DATA)> 0 and get_top_child(i)):
            temp = get_top_child(i)
            if (DATA[get_top_child(i)] < DATA[i]):
                DATA[i],DATA[get_top_child(i)]=DATA[get_top_child(i)],DATA[i]
                restore_subtree(temp)
            elif (DATA[i] < DATA[get_top_child(i)]):
                return None

    
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    x=len(DATA)
    while(x>0):
        restore_subtree(x)
        x-=1

def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    x=len(DATA)
    while(x>=0):
        restore_subtree(x)
        x = x - 1
        
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    global DATA
    DATA[i] , DATA[-1] = DATA[-1] , DATA[i]
    DATA.remove(size()-1)
    heapify()


def pop():
    '''
    Pull the top element out of the heap
    '''
    global DATA
    popelmnt = get_item_at(0)
    return popelmnt


def add(obj):
    '''
    Add an object 'obj' to the heaarity()p
    '''
    global DATA
    DATA = DATA + [obj]
    return DATA


def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    global DATA
    for i in range (0,len(lst)):
        DATA += [lst[i]]
    


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    global DATA
    DATA=[]

if __name__ == '__main__':
    pass

