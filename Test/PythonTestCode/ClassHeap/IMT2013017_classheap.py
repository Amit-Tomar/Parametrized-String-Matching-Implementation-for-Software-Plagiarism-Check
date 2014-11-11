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
        self.min_top = is_min
        self.cmp_function = compare_fn
        self.exp2 = arity_exp
        self.data = []

    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        if(self.min_top==True):
            if( self.data[index1] <= self.data[index2] ):
                return True
        else:
            if( self.data[index1] >= self.data[index2] ):
                return True


    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        self.data[i]=val


        # Other methods will be the same as the functions in the modheap module -
        # add them here as methods of the Heap class
    def swap(self,x,y):
        (self.data[x],self.data[y])=(self.data[y],self.data[x])        
    
    def size(self):
        '''
        Return the size of the heap
        '''
        # Your code
        return len(self.data)
    
    
    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        # Your code
        return 2**self.exp2
        
        
        
    def get_item_at(self,i):
        '''
        Return the i-th element of the data list (new_heap)
        '''
        return self.data[i]
    
    
    
    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        if(child_index==0):
            return None
        else:
            return (child_index-1) >>self.exp2
    
    
    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        if ((parent_index<<self.exp2)+1) < self.size():
            return ((parent_index<<self.exp2)+1)
    
    
    
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        x = (parent_index << self.exp2) + self.arity()
        if(self.get_leftmostchild_index==None):
            return None    
        if(x>self.size()):
            return len(self.data)-1
        else:
            return x
    
    
    
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        x=[]
        childindex_start=(self.arity()*parent_index) +1
        childindex_end=(self.arity()*parent_index) + (self.arity()+1)
        if(childindex_end>self.size()):  
            x=x+self.data[childindex_start:]  
        else:
            x=x+self.data[childindex_start:childindex_end]
        if(childindex_start>=self.size()):
            return None
        if(self.min_top== False):
            val=max(x)
            a=x.index(val)
            return a+self.get_leftmostchild_index(parent_index)
        else:
            val=min(x)
            a=x.index(val)
            return a+self.get_leftmostchild_index(parent_index)
            
    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        while(i!=None and i<self.size()):
            childindex=self.get_top_child(i)
            if(childindex==None):
                return None
            element=self.data[childindex]
            if(self.min_top==False):
                if(element>self.data[i]):
                    self.data[i],self.data[childindex]=self.data[childindex],self.data[i]
            else:
                if(element<self.data[i]):
                    self.data[i],self.data[childindex]=self.data[childindex],self.data[i]
            i=childindex
        
        print self.restore_subtree(1)
    def restore_heap(self,i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        if(self.min_top==True):
            while(i!=None and i>0):
                parentindex=self.get_parent_index(i)
                if(self.data[i]<self.data[parentindex]):
                    #self.swap(self.data[i],self.data[parentindex])
                    self.data[i],self.data[parentindex]=self.data[parentindex],self.data[i]
                else:
                    self.restore_subtree(i)
                i=parentindex
            self.restore_subtree(0)
        else:
            while(i!=None and i>0):
                self.parent_index=self.get_parent_index(i)
                if(self.data[i]>self.data[self.parent_index]):
                    #self.swap(self.data[i],self.data[self.parent_index])
                    self.data[i],self.data[self.parent_index]=self.data[self.parent_index],self.data[i]
                else:
                    self.restore_subtree(i)
                i=self.parent_index
            self.restore_subtree(0)
            
        
                
    
    def heapify(self):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        i=(self.size()-1)    
        while(i>0):
            self.restore_heap(i)
            i-=1
               
        
    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        
        self.swap(i,-1)
        var=self.data.pop()
        self.heapify()
        return var 
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        return self.remove(0)
    
    
    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        self.data.append(obj)
        self.heapify()
    
    
    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
        
        i=0
        while(i<len(lst)):
            self.data.append(lst[i])
            i=i+1
            
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        self.data=[]
       
    #def swap(self,x,y):
     #   (self.data[x],self.data[y])=(self.data[y],self.data[x])        
    

if __name__ == '__main__':
    pass