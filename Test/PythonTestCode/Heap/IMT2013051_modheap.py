'''
Created on 28-Oct-2013

@author: imt2013051
'''

MIN_TOP = True # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA = []
def abc(a,b):
    if(a>b):
        return 1
    elif(a<b):
        return -1
    else:
        return 0

def initialize_heap(is_min = True, arity_exp = 1, compare_fn =abc):
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
    return pow(2,EXP2)
    
    
    
def get_item_at(i):
    '''
    Return the i-th element of the data list (DATA)
    '''
    if(i<len(DATA)):
        return DATA[i]
    else:
        return None


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
    x=((parent_index)<<EXP2)+1
    if(len(DATA)>x):
        return x
    else:
        return None


def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    if(len(DATA)-1>=(parent_index+1)<<EXP2):
        return (parent_index+1)<<EXP2
    elif(len(DATA)-1>=get_leftmostchild_index(parent_index)):
        return len(DATA)-1
    else:
        return None


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    j=0
    if(MIN_TOP==True):
        if((get_leftmostchild_index(parent_index))!=None):
            i=(parent_index<<EXP2)+1
            min_child=DATA[i]
            while(i<=get_rightmostchild_index(parent_index)):
                if(CMP_FUNCTION(DATA[i],min_child)==-1 or CMP_FUNCTION(DATA[i],min_child)==0):
                    min_child=DATA[i]
                    j=i
                i=i+1
            return j
        else:
            return None
    else:
        if((get_leftmostchild_index(parent_index))!=None):
            i=(parent_index<<EXP2)+1
            max_child=DATA[i]
            while(i<=get_rightmostchild_index(parent_index)):
                if(CMP_FUNCTION(DATA[i],max_child)==1 or CMP_FUNCTION(DATA[i],max_child)==0):
                    max_child=DATA[i]
                    j=i
                i=i+1
            return j
        else:
            return None
        
     
       
  
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    global DATA
    
    if(MIN_TOP==True):        
        if(get_top_child(i)!=None):                       
            x=get_top_child(i)
            if(CMP_FUNCTION(DATA[i],DATA[x])==1):                               
                DATA[i],DATA[x]=DATA[x],DATA[i]
                restore_subtree(x)
                
            
    else:
        
        if(get_top_child(i)!=None):                       
            x=get_top_child(i)
            if(CMP_FUNCTION(DATA[i],DATA[x])==-1):               
                DATA[i],DATA[x]=DATA[x],DATA[i]
                restore_subtree(x)
            

    
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    global DATA
    if(MIN_TOP==True):
        if(i!=0):
            if(CMP_FUNCTION(DATA[i],DATA[get_parent_index(i)])==-1):
                x=DATA[i]
                DATA[i]=DATA[get_parent_index(i)]
                DATA[get_parent_index(i)]=x
                restore_heap(get_parent_index(i))
        restore_subtree(i)
        
    else:
        if(i!=0):
            if(CMP_FUNCTION(DATA[i],DATA[get_parent_index(i)])==1):
                x=DATA[i]
                DATA[i]=DATA[get_parent_index(i)]
                DATA[get_parent_index(i)]=x
                restore_heap(get_parent_index(i))
        restore_subtree(i)


def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    global DATA
    i=get_parent_index(len(DATA)-1)
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
    if(i<len(DATA)):
        DATA[i],DATA[-1]=DATA[-1],DATA[i]
        x=DATA[-1]
        del DATA[-1]
        restore_heap(i)
        return x    
    
    
    
def pop():
    '''
    Pull the top element out of the heap
    '''
    x=remove(0)
    return x


def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    global DATA
    DATA.append(obj)
    heapify()
    

def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    global DATA
    DATA=DATA+lst


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    global DATA
    DATA = []

if __name__ == '__main__':
    pass
heapify()
print DATA