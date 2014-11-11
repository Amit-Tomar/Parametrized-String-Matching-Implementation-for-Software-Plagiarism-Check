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
        self.min_top = is_min
        self.cmp_function = compare_fn
        self.exp2 = arity_exp
        self.data = []

    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a self.data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        # Your code
        if self.min_top :
            if self.data[index1] <= self.data[index2] :
                return True
           
        else:
            if self.data[index1] >= self.data[index2] :
                return True


    def set_item_at(self, i, val):
        '''
        Set the i-th element of the self.data to the value 'val'
        '''
        # Your code
        
    def size(self):
        '''
        Return the size of the heap
        '''
        return len(self.data)
        # Your code


    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        # Your code
        return 2**self.exp2
        
        
        
    def get_item_at(self, i):
        '''
        Return the i-th element of the self.data list (self.data)
        '''
        return self.data[i]
    
    
    
    def get_parent_index(self, child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your codeget_parent_index(c
        if child_index <= 0:
            return None
        else:
            index = (child_index-1) >> self.exp2
            return index
    
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of theget_parent_index(c element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        parent_index2 = parent_index << self.exp2
        if ((parent_index2+1) >= self.size()):
            return None
        else:
            return (parent_index2+1)
        # Your code
    
    
    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        left_child = self.get_leftmostchild_index(parent_index)
        arity_heap = self.arity()
        if self.get_leftmostchild_index(parent_index) == None:
            return None
        if ((left_child + arity_heap -1) >= self.size()):
            return self.size() - 1
        else:
            return (left_child + arity_heap -1)
    
    
    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
    
        
        position = self.get_leftmostchild_index(parent_index)
        leftchild = self.get_leftmostchild_index(parent_index)
        rightchild = self.get_rightmostchild_index(parent_index)
        if leftchild == None and rightchild == None:
            return None
        temp =  self.data[self.get_leftmostchild_index(parent_index)]
        for i in range(leftchild, rightchild + 1):
            
            if self.min_top and self.data[i] < temp :
                position = i
                temp = self.data [i]
            elif not self.min_top and self.data[i] > temp :
                position = i
                temp = self.data [i]
                
        return position
                
    
        
        
    
    
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
      
            
        topchild_index = self.get_top_child(i)
        if i > self.get_parent_index(self.size()-1) :
            return None
        while (topchild_index>0 and topchild_index != None):
            if self.min_top and self.data[i] > self.data[topchild_index]:
                self.data[i], self.data[topchild_index] = self.data[topchild_index], self.data[i]
            elif not self.min_top and self.data[i] < self.data[topchild_index]:
                self.data[i], self.data[topchild_index] = self.data[topchild_index], self.data[i]
            
            
            i = topchild_index
            topchild_index = self.get_top_child(topchild_index)
    
            
        return self.data
    
        
    def restore_heap(self, i):
        '''
        Restore the heap property for self.data assuming that it has been 'corrupted' at index i
        The rest of self.data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
      
        parent_index = self.get_parent_index(i)   
        if self.min_top:
            if parent_index != None and self.data[i] < self.data[parent_index]:
                while (parent_index != None and self.data[i] < self.data[parent_index]):
                    self.data[i], self.data[parent_index] = self.data[parent_index], self.data[i]
                    i = parent_index 
                    parent_index = self.get_parent_index(i)    
                    
            else:
                self.restore_subtree(i)
        else:
            if (parent_index != None and self.data[i] > self.data[parent_index]) :
                while parent_index != None and self.data[i] > self.data[parent_index]:
                    self.data[i], self.data[parent_index] = self.data[parent_index], self.data[i]
                    i = parent_index    
                    parent_index = self.get_parent_index(i) 
                
            else:
                self.restore_subtree(i)
            
    
    
    def heapify(self):
        '''
        Rearrange self.data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        last_node = self.get_parent_index(self.size()-1)
        while last_node >= 0:
            self.restore_subtree(last_node)
            last_node = last_node - 1
        
    
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        self.data[i], self.data [self.size()-1] = self.data [self.size()-1], self.data[i]
        self.data.pop()
        self.heapify()
        
    
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        
        top_element = self.data[0]
        self.remove(0)
        #self.data[0] = self.data [size()-1]
        #self.data = self.data[0:-1]
        #restore_subtree(0)
        return top_element
    
    def add(self, obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data.append(obj)
        self.heapify()
        #restore_heap(size()-1)
    
    
    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to self.data
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        for i in lst:
            self.data.append(i)
    
    def clear(self):
        '''
        Clear the self.data in the heap - initialize to empty list
        '''
        # Your code
        while len(self.data)>0:
            self.data.pop()
    


    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

if __name__ == '__main__':
    pass