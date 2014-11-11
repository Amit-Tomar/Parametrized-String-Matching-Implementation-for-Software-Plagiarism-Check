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
    
    data  =  [] 
    exp2 = 1
    min_top = False
    
    def __init__(self,  is_min,  arity_exp,  compare_fn):
        '''
        The Python convention is to have upper case name for global variables - that's why the globals
        in modheap were named in all caps
        Unlike the globals in heap module --- name the attributes as lower case variable names
        '''
        # Your code
        self.min_top  =  is_min
        self.cmp_function  =  compare_fn
        self.exp2  =  arity_exp
        self.data = []

    
    def is_favoured(self,  index1,  index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        # Your code
        if(( self.data[index2]>= self.data[index1] and self.min_top) or ( self.min_top  ==  False and  self.data[index2]<= self.data[index1])):
            return True


    def set_item_at(self,  i,  val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        # Your code
        self.data[i] = val


    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class
    
      
    
    def size(self, ):
        '''
        Return the size of the heap
        '''
        return len(self.data) 
    
    
    def arity(self, ):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        # Your code
        return self.exp2 << 1
        
    def get_item_at(self, i):
        '''
        Return the i-th element of the data list (self.data)
        '''
        if(i>= self.size()):
            return None
        return self.data[i]
    
    
    def get_parent_index(self, child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m,  in python)
        '''
        if(child_index<= 0):
            return None
        return int(child_index >> self.exp2)
    
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m,  in python)
        '''
        if(parent_index == None or int(parent_index << self.exp2) + 1 >self.size()):
            return None
        return int(parent_index << self.exp2) + 1
    
    
    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        right = (int(parent_index << self.exp2) + self.arity())
        while (right>= self.size()):
            right -= 1
        return right
    
    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        least = self.get_leftmostchild_index(self, parent_index)
        if(not least):
            return None
        for count in range(len(self.data[self.get_leftmostchild_index(parent_index) + 1:])):
            temp = self.get_leftmostchild_index(parent_index)
            if(self.is_favoured(least, count + temp)): 
                least = count + temp
        return least
    
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        while(i != None and self.get_parent_index(i)>= 0 and i<self.size()):
            temp = self.get_parent_index(i)
            if(self.is_favoured(i, temp)):
                self.data[i], self.data[temp] = self.data[temp], self.data[i]
            i = self.get_parent_index(i)            
        return False
    
    def restore_heap(self, i):
        '''
        Restore the heap property for self.data assuming that it has been 'corrupted' at index i
        The rest of self.data is assumed to already satisfy the heap property
        Also: (i) Check if the element at i needs to move up the tree. If yes,  swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up,  then fix the subtree below this element 
        '''
        # Your code
        for j in range(self.size())[i:]:
            self.restore_subtree(j)
        
    
    
    def heapify(self, ):
        '''
        Rearrange self.data into a heap
        Also: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        self.restore_heap(0)
    
    
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Also: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        self.data = self.data[:i] + self.data[i + 1:]
        self.restore_heap(self.get_parent_index(i))
    
    
    def pop(self, ):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        pop1 = self.data[0]
        self.data = self.data[1:]
        self.heapify()
        return pop1
    
    
    def add(self, obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data.append(obj)
        self.heapify()
    
    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to self.data
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        for i in lst:
            self.data.append(i)
        return self.data
    
    
    def clear(self, ):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        # Your code
        self.data = []
        

if __name__  ==  '__main__':
    pass