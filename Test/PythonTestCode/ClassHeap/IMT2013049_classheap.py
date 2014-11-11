'''
Created on 22-Oct-2013

@author: Sulekha
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
        # Your code

    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        if self.min_top:
            if self.data[index1] <= self.data[index2]:
                return True
            else:
                return False
        else:
            if self.data[index1] >= self.data[index2]:
                return True
            else:
                return False
        # Your code


    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        self.data[i] = val
        # Your code

    def size(self):
        '''
        Return the size of the heap
        '''
        return len(self.data)

    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        return pow(2, self.exp2)
    
    def get_item_at(self,i):
        '''
        Return the i-th element of the data list (data)
        '''
        return self.data[i]
   


    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
    
        parent_index = (child_index-1) >> self.exp2
        if parent_index >= 0: 
            return parent_index
        else:
            return None
    

    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
    
        last_index = len(self.data)-1
        last_parent_index = self.get_parent_index(last_index)
    
        if(parent_index>last_parent_index):
            return None
        else:
            leftmostchild_index = (parent_index << self.exp2)+1
            return leftmostchild_index
    
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        temparity = self.arity()
        parent = parent_index
    
        if(self.get_leftmostchild_index(parent)==None):
            return None
       
        left = self.get_leftmostchild_index(parent)
        rightmostchild_index = left + (temparity-1)
    
        if(rightmostchild_index > self.size()-1):
            return self.size()-1
        else:
            return rightmostchild_index
    
    def get_top_child(self,parent_index):
        '''
    	Return the index of the child which is most favoured to move up the tree among all the children of the
    	element at parent_index
    	'''
        parent = parent_index
    
        last_index = len(self.data)-1
        last_parent_index = self.get_parent_index(last_index)
        if(parent>last_parent_index):
            return None
        else:
            left = self.get_leftmostchild_index(parent)
            right = self.get_rightmostchild_index(parent)
            top_child_index = left
            for i in range(left, right+1):
                if self.min_top:
                    if(self.cmp_function(self.data[i], self.data[top_child_index]) == -1):
                        top_child_index = i
                else:
                    if(self.cmp_function(self.data[i], self.data[top_child_index]) == 1):
                        top_child_index = i
            return top_child_index 
        
    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        cindex = self.get_top_child(i)
        while cindex :
            if self.min_top:
                if self.cmp_function(self.data[i] , self.data[cindex])==1:
                    self.data[i] , self.data[cindex] = self.data[cindex] , self.data[i]
            else:
                if self.cmp_function(self.data[i], self.data[cindex])== -1:
                    self.data[i] , self.data[cindex] = self.data[cindex] , self.data[i]
            i = cindex
            cindex = self.get_top_child(i)
        return self.data 
    
    def restore_heap(self,i):
        '''
        Restore the heap property for data assuming that it has been 'corrupted' at index i
        The rest of data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        
        parent_index = self.get_parent_index(i)
        if self.min_top:
            if parent_index != None and self.cmp_function(self.data[i], self.data[parent_index]) == -1:
                while(parent_index != None and self.cmp_function(self.data[i], self.data[parent_index])== -1 and i != None):
                    self.data[i], self.data[parent_index] = self.data[parent_index], self.data[i]
                    i = parent_index
                    parent_index = self.get_parent_index(i)          
            else:
                self.restore_subtree(i)
        else:
            if parent_index != None and self.cmp_function(self.data[i], self.data[parent_index]) == 1:
                while(parent_index != None and self.cmp_function(self.data[i], self.data[parent_index]) == 1 and i != None):
                    self.data[i], self.data[parent_index] = self.data[parent_index], self.data[i]
                    i = parent_index        
                    parent_index = self.get_parent_index(i)    
            else:
                self.restore_subtree(i)
        
    
        return self.data
    
      
    
    def heapify(self):
        '''
        Rearrange data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        i = self.get_parent_index(self.size()-1)
        while(i>=0):
            self.restore_subtree(i)
            i = i-1      
    
    


    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
    
        self.data[i] , self.data[-1] = self.data[-1] , self.data[i]
        del self.data[-1]     
        self.restore_heap(i)
    


    def pop(self):
        '''Pull the top element out of the heap'''
        if self.size():
            top_element = self.data[0]
            self.data[0] , self.data[-1] = self.data[-1] , self.data[0]
            del self.data[-1]     
            self.restore_heap(0)
        return top_element
    


    def add(self , obj):
        '''
        Add an object 'obj' to the heap
        '''
        self.data.append(obj)
        self.restore_heap(self.size()-1)
    

    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
    
        self.data = []
   

    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to data
        Make sure this does not modify the input list 'lst'
        '''
        self.data = self.data + lst

    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

if __name__ == '__main__':
    pass