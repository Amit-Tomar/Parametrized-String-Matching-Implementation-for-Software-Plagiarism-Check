'''
Created on 28-Oct-2013

@author: PUVVADA NIKHILESH(IMT2013031)
'''

MIN_TOP = False # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

# Comparison Function for the heap
# Takes two elements - e1, e1 - of the heap as arguments and retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
#CMP_FUNCTION = None

#     The arity (number of children for a parent) is taken to be 2^EXP2
EXP2 = 1

# The list of elements organized as a heap
DATA=[]
def CMP_FUNCTION(e1,e2):
    if(e1>e2):
        return 1
    if(e1<e2):
        return -1
    if(e1==e2):
        return 0
    
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
    limit=size()-1
    if(child_index>0 and child_index<=limit):
        return (child_index-1)>>EXP2
    else:
        return None

def get_leftmostchild_index(parent_index):
    '''
    Return the index of the leftmost child of the element at parent_index
    Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    '''
    if((size()-1)%arity()==0):
        if(parent_index>=0 and parent_index<(size()-1)/arity()):
            return (parent_index<<EXP2)+1
        else:
            return None
    if((size()-1)%arity()!=0):
        if(parent_index>=0 and parent_index<=(size()-1)/arity()):
            return (parent_index<<EXP2)+1
        else:
            return None
def get_rightmostchild_index(parent_index):
    '''
    Return the index of the rightmost child of the element at parent_index
    Should return None if the parent has no child
    '''
    if((size()-1)%arity()==0):
        if(parent_index>=0 and parent_index<(size()-1)/arity()):
            if(parent_index!=(get_parent_index(size()-1))):
                return (parent_index<<EXP2)+arity()
            else:
                if((size()-get_leftmostchild_index(parent_index))==1):
                    return None
                if((size()-get_leftmostchild_index(parent_index))>1 and (size()-get_leftmostchild_index(parent_index))<arity()):
                    return size()-1
    if((size()-1)%arity()!=0):
        if(parent_index>=0 and parent_index<=(size()-1)/arity()):
            if(parent_index!=get_parent_index(size()-1)):
                return (parent_index<<EXP2)+arity()
            else:
                if((size()-get_leftmostchild_index(parent_index))==1):
                    return None
                if((size()-get_leftmostchild_index(parent_index))>1 and (size()-get_leftmostchild_index(parent_index))<arity()):
                    return size()-1
           
def get_top_child(parent_index):
    '''
    Return the index of the child which is most favoured to move up the tree among all the children of the
    element at parent_index
    '''
    if((size()-1)%arity()==0):
        if(parent_index>=0 and parent_index<(size()-1)/arity()):
            list1=[]
            lci=get_leftmostchild_index(parent_index)
            rci=get_rightmostchild_index(parent_index)
            if(rci==None):
                rci=size()-1
            while(lci<=rci):
                list1.append(DATA[lci])
                lci=lci+1
            if(MIN_TOP==True):
                a=min(list1)
            if(MIN_TOP==False):
                a=max(list1)
            m=0
            while(m<=size()-1):
                if(DATA[m]==a):
                    return m
                m=m+1
        else:
            return None
    if((size()-1)%arity()!=0):
        if(parent_index>=0 and parent_index<=(size()-1)/arity()):
            list1=[]
            lci=get_leftmostchild_index(parent_index)
            rci=get_rightmostchild_index(parent_index)
            if(rci==None):
                rci=size()-1
            while(lci<=rci):
                list1.append(DATA[lci])
                lci=lci+1
            if(MIN_TOP==True):
                a=min(list1)
            if(MIN_TOP==False):
                a=max(list1)
            m=0
            while(m<=size()-1):
                if(DATA[m]==a):
                    return m
                m=m+1
        else:
            return None
def restore_subtree(i):
    '''
    Restore the heap property for the subtree with the element at index i as the root
    Assume that everything in the subtree other than possibly the root satisfies the heap property
    '''
    gtc1=get_top_child(i)
    if(MIN_TOP==True):
        while(gtc1!=None and CMP_FUNCTION(DATA[gtc1],DATA[i])==-1):
            DATA[i],DATA[gtc1]=DATA[gtc1],DATA[i]
            i,gtc1=gtc1,i
            gtc1=get_top_child(i)
    if(MIN_TOP==False):
        while(gtc1!=None and CMP_FUNCTION(DATA[gtc1],DATA[i])==1):
            DATA[i],DATA[gtc1]=DATA[gtc1],DATA[i]
            i,gtc1=gtc1,i
            gtc1=get_top_child(i)
def restore_heap(i):
    '''
    Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    The rest of DATA is assumed to already satisfy the heap property
    Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    Continue this till you do not need to move up anymore.
    (ii) If it has not moved up, then fix the subtree below this element 
    '''
    if(MIN_TOP==True):
        a=get_parent_index(i)
        while(a!=None and CMP_FUNCTION(DATA[i],DATA[a])==-1):
            DATA[i],DATA[a]=DATA[a],DATA[i]
            i,a=a,i
            a=get_parent_index(i)
        restore_subtree(i)
    if(MIN_TOP==False):
        a=get_parent_index(i)
        while(a!=None and CMP_FUNCTION(DATA[i],DATA[a])==1):
            DATA[i],DATA[a]=DATA[a],DATA[i]
            i,a=a,i
            a=get_parent_index(i)
        restore_subtree(i)

def heapify():
    '''
    Rearrange DATA into a heap
    Algo: (i) Start from the first nonleaf node - the parent of the last element
    (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    '''
    if(MIN_TOP==True):
        k=size()-1
        m=get_parent_index(k)
        while(m>=0):
            gtc1=get_top_child(m)
            while(gtc1!=None and CMP_FUNCTION(DATA[gtc1],DATA[m])==-1):
                DATA[m],DATA[gtc1]=DATA[gtc1],DATA[m]
                m,gtc1=gtc1,m
                gtc1=get_top_child(m)
            m=m-1
        return DATA
    if(MIN_TOP==False):
        k=size()-1
        m=get_parent_index(k)
        if(m==None):
            return None
        while(m>=0):
            gtc1=get_top_child(m)
            while(gtc1!=None and CMP_FUNCTION(DATA[gtc1],DATA[m])==1):
                DATA[m],DATA[gtc1]=DATA[gtc1],DATA[m]
                m,gtc1=gtc1,m
                gtc1=get_top_child(m)
            m=m-1

def remove(i):
    '''
    Remove an element (at index i) from the heap
    Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    (c) Restore the heap starting from i
    '''
    l=size()
    global DATA
    DATA[i],DATA[l-1]=DATA[l-1],DATA[i]
    DATA=DATA[:-1]
    restore_heap(i)

def pop():
    '''
    Pull the top element out of the heap
    '''
    global DATA
    heapify()
    ret=DATA[0]
    remove(0)
    return ret
    
def add(obj):
    '''
    Add an object 'obj' to the heap
    '''
    global DATA
    DATA=DATA+[obj]
def import_list(lst):
    '''
    Add all the elements of the list 'lst' to DATA
    Make sure this does not modify the input list 'lst'
    '''
    heapify()
    global DATA
    h=0
    while(h<=(len(lst)-1)):
        DATA=DATA+[lst[h]]
        h=h+1
    return DATA
def clear():
    '''
    Clear the data in the heap - initialize to empty list
    '''
    DATA=[]

if __name__ == '__main__':
    pass
    
   