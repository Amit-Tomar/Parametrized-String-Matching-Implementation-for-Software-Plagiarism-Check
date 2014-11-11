'''
Created on 13-Nov-2013

@author: k.vasundhara
'''
'''
Created on 22-Oct-2013

@author: raghavan
'''

class Heap(object):
    '''
    Heap class
    The methods specific to the class implementation are added here - the rest will be the same as the
    functions in the modheap module
    '''
    def __init__(self, is_min, arity_exp, compare_fn):
        '''
        The Python convention is to have upper case name for global variables - that's why the globals
        in modheap were named in all caps
        Unlike the globals in heap module --- name the attributes as lower case variable names
        '''
        # Your code
        self.MIN_TOP = is_min
        self.CMP_FUNCTION = compare_fn
        self.EXP2 = arity_exp
        self.DATA = []
    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a DATA structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        # Your code
        if self.MIN_TOP:
            if self.DATA[index1]>=self.DATA[index2]:
                return 1
            else: 
                return -1
        else:
            if self.DATA[index1]<=self.DATA[index2]:
                return 1
            else:
                return -1

    def set_item_at(self, i, val):
        '''
        Set the i-th element of the DATA to the value 'val'
        '''
        # Your code
        self.DATA[i]=val
        
    def size(self):
        '''
        Return the size of the heap
        '''
        # Your code
        return len(self.DATA)

    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        # Your code
        return 2<<self.EXP2
    
    
    def get_item_at(self,i):
        '''
        Return the i-th element of the DATA list (DATA)
        '''
        return self.DATA[i]


    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your code
        if child_index==0:
            return None
        return ((child_index-1)>>self.EXP2)


    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        if ((parent_index<<self.EXP2)+1)<len(self.DATA):
            return (parent_index<<self.EXP2)+1
        else:
            return None
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        if ((parent_index<<self.EXP2)+1)>=len(self.DATA):
            return None
        elif ((parent_index+1)<<self.EXP2)<len(self.DATA):
            return (parent_index+1)<<self.EXP2
        else:
            return (len(self.DATA)-1)

    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        if self.MIN_TOP:
            minx=self.get_leftmostchild_index(parent_index)
            if(self.get_rightmostchild_index(parent_index) is not None):
                for i in range((parent_index<<self.EXP2)+1,self.get_rightmostchild_index(parent_index)+1):
                    if self.CMP_FUNCTION(self.DATA[i],self.DATA[minx])==-1:
                        minx=i
                return minx
            else:
                return None
        else:
            maxx=self.get_leftmostchild_index(parent_index)
            if(self.get_rightmostchild_index(parent_index) is not None):
                for i in range((parent_index<<self.EXP2)+1,self.get_rightmostchild_index(parent_index)+1):
                    if self.CMP_FUNCTION(self.DATA[i],self.DATA[maxx])==1:
                        maxx=i
                return maxx
            else:
                return None
    
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        p=self.get_top_child(i)
        if self.MIN_TOP:
            while(p is not None):
                if self.CMP_FUNCTION(self.DATA[p],self.DATA[i])==-1:
                    self.DATA[i],self.DATA[p]=self.DATA[p],self.DATA[i]
            
                else:
                    break
                i=p
                p=self.get_top_child(i)
    

        else:
            while(p is not None):
                if self.CMP_FUNCTION(self.DATA[p],self.DATA[i])==1:
                    self.DATA[i],self.DATA[p]=self.DATA[p],self.DATA[i]
            
                else:
                    break
                i=p
                p=self.get_top_child(i)
        
    def restore_heap(self,i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        k=i
        p=self.get_parent_index(i)
        if self.MIN_TOP:
            while(p is not None):
                if self.CMP_FUNCTION(self.DATA[k],self.DATA[p])==-1:
                    self.DATA[k],self.DATA[p]=self.DATA[p],self.DATA[k]
                
                else:
                    break
                k=p
                p=self.get_parent_index(k)
            self.restore_subtree(i)
        else:
            while(p is not None):
                if self.CMP_FUNCTION(self.DATA[k],self.DATA[p])==1:
                    self.DATA[k],self.DATA[p]=self.DATA[p],self.DATA[k]
                
                else:
                    break
                k=p
                p=self.get_parent_index(k)
            self.restore_subtree(i)
        

    def heapify(self):
    
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        
        i=len(self.DATA)-1
        p=self.get_parent_index(i)
        while(p>=0):
            self.restore_subtree(p)
            p-=1

    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        self.DATA[i], self.DATA[len(self.DATA)-1]=self.DATA[len(self.DATA)-1], self.DATA[i]
        self.DATA.remove(self.DATA[len(self.DATA)-1])
        self.restore_heap(i)
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code

        c=self.DATA[0]
        self.remove(0)
        return c
    

    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.DATA.append(obj)
        self.restore_heap(len(self.DATA)-1)

    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        i=0
        while(i<len(lst)):
            self.add(lst[i])
            i+=1

    def clear(self):
        '''
        Clear the DATA in the heap - initialize to empty list
        '''
        # Your code
        self.DATA=[]


    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

if __name__ == '__main__':
    pass
