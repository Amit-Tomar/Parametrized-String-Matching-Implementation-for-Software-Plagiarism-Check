'''
Created on 28-Oct-2013

@author: Ujjwal
'''
# Says whether the heap is a Min-Heap (True) or a Max-Heap (False)
MIN_TOP = False 


# Comparison Function for the heap
CMP_FUNCTION = None

# The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA = []

def initialize_heap(is_min = True, arity_exp = 1, compare_fn = None):
    '''
    xyz
    '''
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
    if(i<size()-1):
        return DATA[i]


def get_parent_index(child_index):
    '''
    Return the index of the parent given the child_index
    Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
    '''
    # Your code
    parent_in = (child_index-1) >> EXP2
    if (parent_in >= 0):
        return parent_in
    else : 
        return None


def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    # Your code
    
    
    if(((arity()) * (parent_index)) + 1 < size()):
        return ((arity()) * (parent_index)) + 1
    return None


def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    # Your code
    rightmostchild_index = ((arity()) * parent_index) + (arity())
    
    if((get_leftmostchild_index(parent_index) == None)):
        return None
    elif(((arity()) * parent_index) + (arity()) >= size()):
        l_var = 1
        while(DATA[((arity()) * parent_index) + l_var] != DATA[-1]):
            l_var += 1
        return ((arity()) * parent_index) + l_var
        
    else:
        return rightmostchild_index


def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    # Your code
    if(MIN_TOP == True):
        m_var = 1
        count = 0
        while((size() > ((arity() * parent_index) + m_var))):
            count += 1
            m_var += 1
        if(count > 1):
            minn = DATA[arity() * (parent_index) + 1]
            minn1 = arity() * (parent_index) + 1
            i_var = 2
            if(((arity() * (parent_index)) + i_var) < size()):
                while(i_var <= arity()):
                    if(DATA[((arity() * (parent_index)) + i_var)] <= minn):
                        minn = DATA[(arity() * (parent_index)) + i_var]
                        minn1 = (arity() * (parent_index)) + i_var
                    i_var += 1
                return minn1
            else:
                return None
            
        elif(count == 1):
            minn = arity() * (parent_index) + 1
            return minn
        elif(count == 0):
            return None
    
    else:
        m_var = 1
        count = 0
        while((size() > ((arity() * parent_index) + m_var))):
            count += 1
            m_var += 1
        if(count > 1):
            minn = DATA[arity() * (parent_index) + 1]
            minn1 = arity() * (parent_index) + 1
            i_var = 2
            if(((arity() * (parent_index)) + i_var) < size()):
                while(i_var <= arity()):
                    if(DATA[((arity() * (parent_index)) + i_var)] >= minn):
                        minn = DATA[(arity() * (parent_index)) + i_var]
                        minn1 = (arity() * (parent_index)) + i_var
                    i_var += 1
                return minn1
            else:
                return None
            
        elif(count == 1):
            minn = arity() * (parent_index) + 1
            return minn
        elif(count == 0):
            return None            


def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    # Your code
    heapify()
 
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    # Your code
    parent = get_parent_index(i)
    flag = 0
    if parent != None:
        while(CMP_FUNCTION(DATA[i], DATA[parent])==-1 and MIN_TOP==True):
            flag = 1
            DATA[i], DATA[parent] = DATA[parent], DATA[i]
            i = parent
            parent = get_parent_index(i)
            if(parent==None):
                break
        while(CMP_FUNCTION(DATA[i], DATA[parent])==1 and MIN_TOP==False):
            flag = 1
            DATA[i], DATA[parent] = DATA[parent], DATA[i]
            i = parent
            parent = get_parent_index(i)
            if(parent==None):
                break
    if(flag==0):
        restore_subtree(i)



def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    # Your code
    import random
    global DATA

    if(MIN_TOP==True):
        def minm(list1):
            '''
            giving the minimum value out of a list
            '''
            min1 = list1[0]
            for j in list1:
                if(j<min1):
                    min1 = j
            return min1

        sample = []
        result = []
        if(len(DATA)!=0):
            result.append(minm(DATA))
        else:
            return
        noe = len(DATA)
        d_var = 1
    
        while(d_var < noe and len(DATA) != 0):
            x_var = 1
            while(2**d_var >= x_var and len(DATA) != 0):
                DATA.remove(minm(DATA))
                if(len(DATA)):
                    sample.append(minm(DATA))
                x_var += 1
            i = 1
        
            while(2**d_var >= i and len(sample) != 0):
                random_int = random.choice(sample)
                sample.remove(random_int)
                result.append(random_int)
                i += 1
            d_var += 1
        DATA = []
        for i in result:
            DATA.append(i)
    
    else:
        def maxx(list2):
            '''
            giving the maximum value out of a list
            '''
            max1 = list2[0]
        
            for j in list2:
                if(j>max1):
                    max1 = j
        
            return max1
        
        sample = []
        result = []
        if(len(DATA)!=0):
            result.append(maxx(DATA))
        else:
            return
        noe = len(DATA)
        d_var = 1
        
        while(d_var < noe and len(DATA) != 0):
            x_var = 1
            while(2**d_var >= x_var and len(DATA) != 0):
                DATA.remove(maxx(DATA))
                if(len(DATA)):
                    sample.append(maxx(DATA))
                x_var += 1
            i = 1
            
            while(2**d_var >= i and len(sample) != 0):
                random_int = random.choice(sample)
                sample.remove(random_int)
                result.append(random_int)
                i += 1
            d_var += 1
        DATA = []
        for i in result:
            DATA.append(i)
        
        
def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    # Your code
    global DATA
    if i == 0 : 
        DATA[i], DATA[-1] = DATA[-1], DATA[i]
        k = DATA[-1]
        DATA = DATA[:-1]
        heapify()
        return k
    


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
    DATA = lst[:]
    


def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    # Your code
    
    while(len(DATA) != 0):
        DATA.remove()