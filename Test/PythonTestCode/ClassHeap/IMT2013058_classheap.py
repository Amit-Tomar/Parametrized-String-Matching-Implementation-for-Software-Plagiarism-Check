'''
Created on 22-Oct-2013

@author: raghavan
'''
import math
class Heap(object):
    '''
    Heap class
    The methods specific to the class implementation are added here - the rest will be the same as the
    functions in the modheap module
    '''
    MIN_TOP = False # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

    # Comparison Function for the heap
    # Takes two elements - e1, e1 - of the heap as arguments and retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
    CMP_FUNCTION = None
    
    # The arity (number of children for a parent) is taken to be 2^self.EXP2
    EXP2 = 1
    
    # The list of elements organized as a heap
    DATA = []
    
    def size(self):
        '''
        Return the size of the heap
        '''
        # Your code
        l=len(self.DATA)
        return l
        
    
    
    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        # Your code
        return 2**self.EXP2
        
        
    def get_item_at(self,i):
        '''
        Return the i-th element of the self.DATA list (self.DATA)
        '''
        return self.DATA[i]
    
    
    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your code
        ar=self.arity()
        a=(child_index-1)//ar
        if(a>=0):
            return a
        else:
            return None
    
    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        rc=self.get_rightmostchild_index(parent_index)
        if(rc==None):
            return None
        global DATA
        ar=self.arity()
        size=len(self.DATA)
        a=(ar*parent_index)+1
        if(a<size):
            return a
        else:
            return None
    
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        global DATA
        ar=self.arity()
        size=len(self.DATA)
        b=0
        a=(ar*parent_index)+1
        if(a<size):
            b=a
        else:
            b=None
        size=len(self.DATA)
        a=(ar*parent_index)+ar
        while(a>b):
            if(a<size):
                return a
            else:
                ar-=1
                a=(ar*parent_index)+ar
        return None
    
    
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        global DATA,MIN_TOP
        lc=self.get_leftmostchild_index(parent_index)
        rc=self.get_rightmostchild_index(parent_index)
        
        if(self.MIN_TOP==False):
            i=lc
            max_val=self.DATA[lc]
            max_index=lc
            while(i<=rc):
                if self.DATA[i]>max_val:
                    max_val=self.DATA[i]
                    max_index=i
                i+=1
            return max_index
        else:
            i=lc
            min_val=self.DATA[lc]
            min_index=lc
            while(i<=rc):
                if self.DATA[i]<min_val and self.DATA[i]!=-1:
                    min_val=self.DATA[i]
                    min_index=i
                i+=1
            return min_index
        
    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        self.heapify()
        
    def restore_heap(self,i):
        '''
        Restore the heap property for self.DATA assuming that it has been 'corrupted' at index i
        The rest of self.DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        global DATA,MIN_TOP
        a=1
        l=len(self.DATA)
        ar=self.arity()
        while(l>0):
            if(l==2):
                a=0
                self.DATA.append(-1)
                break
            l-=ar
        lc,rc=self.get_leftmostchild_index(i),self.get_rightmostchild_index(i)
        if(lc!=None and rc!=None):
            if(self.MIN_TOP==False):
                j=self.get_top_child(i)
                while(self.DATA[i]<self.DATA[j]):
                    self.DATA[i],self.DATA[j]=self.DATA[j],self.DATA[i]
                    i=j
                    lc,rc=self.get_leftmostchild_index(i),self.get_rightmostchild_index(i)
                    if(lc==None or rc==None):
                        break
                    else:
                        j=self.get_top_child(i)
            else:
                j=self.get_top_child(i)
                while(self.DATA[i]>self.DATA[j]):
                    self.DATA[i],self.DATA[j]=self.DATA[j],self.DATA[i]
                    i=j
                    lc,rc=self.get_leftmostchild_index(i),self.get_rightmostchild_index(i)
                    if(lc==None or rc==None):
                        break
                    else:
                        j=self.get_top_child(i)
                    
                
        if(a==0):
            self.DATA=self.DATA[:len(self.DATA)-1]
            
    def heapify(self):
        '''
        Rearrange self.DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        l=len(self.DATA)-1
        ar=self.arity()
        i=int(math.floor(l/ar))
        while(i>=0):
            self.restore_heap(i)
            i-=1
              
    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        self.DATA[i],self.DATA[len(self.DATA)-1]=self.DATA[len(self.DATA)-1],self.DATA[i]
        return self.DATA.pop()
    
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        global DATA
        self.DATA[0],self.DATA[len(self.DATA)-1]=self.DATA[len(self.DATA)-1],self.DATA[0]
        a=self.DATA.pop()
        self.heapify()
        return a
    
    
    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.DATA.append(obj)
        self.heapify()
    def clear(self):
        '''
        Clear the self.DATA in the heap - initialize to empty list
        '''
        # Your code
        self.DATA=[]
    
    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to self.DATA
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        for i in lst:
            self.DATA.append(i)
    def __init__(self, is_min, arity_exp, compare_fn):
        '''
        The Python convention is to have upper case name for global variables - that's why the globals
        in modheap were named in all caps
        Unlike the globals in heap module --- name the attributes as lower case variable names
        '''
        # Your code
        global MIN_TOP, CMP_FUNCTION, EXP2, DATA
        self.MIN_TOP = is_min
        self.CMP_FUNCTION = compare_fn
        self.EXP2 = arity_exp
        self.DATA = []

    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a self.DATA structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        # Your code
        if self.MIN_TOP==True:
            if self.DATA[index1]<=self.DATA[index2]:
                return True
            else:
                return False
        else:
            if self.DATA[index1]>=self.DATA[index2]:
                return True
            else:
                return False

    def set_item_at(self, i, val):
        '''
        Set the i-th element of the DATA to the value 'val'
        '''
        # Your code
        self.DATA[i]=val


    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

if __name__ == '__main__':
    pass