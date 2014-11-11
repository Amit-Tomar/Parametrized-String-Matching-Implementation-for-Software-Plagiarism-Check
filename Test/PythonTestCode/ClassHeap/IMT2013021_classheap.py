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
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        # Your code
        if (self.cmp_function(self.data[index1], self.data[index2])
             <= 0 and self.min_top):
            return True
        
        elif (self.cmp_function(self.data[index1], self.data[index2]) 
             >= 0 and not self.min_top):
            return True
        
        else:
            return False

    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        # Your code
        
        self.data[i] = val


    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class
    
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
        return 2 << (self.exp2 - 1)
        
    def get_item_at(self, i):
        '''
        Return the i-th element of the data list (data)
        '''
        
        return self.data[i]
    
    
    def get_parent_index(self, child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your code    
        if(child_index <= 0):
            return None
        
        return child_index >> self.exp2
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        
        if(parent_index==None or int(parent_index << self.exp2)+1
           > self.size()):
            
            return None
        
        return int(parent_index << self.exp2) + 1
    
    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        
        if parent_index << self.exp2 + self.arity() > self.size() - 1:
            return self.size() - 1
        
        return parent_index << self.exp2 + self.arity()
        
    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        
        l_m_c = self.get_leftmostchild_index(parent_index)
    
        if(not l_m_c):
            return None
        
        for count in range(len(self.data[l_m_c + 1:])):
            
            if((self.cmp_function(self.data[count + l_m_c], self.data[l_m_c])==1
               and self.min_top) or (self.min_top == False and
               self.cmp_function(self.data[count + l_m_c], self.data[l_m_c]))): 
                
                l_m_c = count + self.get_leftmostchild_index(parent_index)
        
        return l_m_c
    
        
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        
        temp = self.get_parent_index(i)
    
        while(i!=None and temp >= 0 and i < self.size() ):
            
            if(((self.cmp_function(self.data[temp], self.data[i]) != -1
                  and self.min_top) or (self.min_top == False and
                self.cmp_function(self.data[temp], self.data[i]) != 1))):
                
                self.data[i], self.data[temp] = self.data[temp], self.data[i]
            
            i = temp
            temp = self.get_parent_index(temp)
        
        return None    
    
    def restore_heap(self, i):
        '''
        Restore the heap property for data assuming that it has been 'corrupted' at index i
        The rest of data is assumed to already satisfy the heap property
        Algo: (child_recur(i, top_child)i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        
        for index in range(self.size())[i:]:
            self.restore_subtree(index)
    
    def heapify(self):
        '''
        Rearrange data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code 
        self.restore_heap(0)            
    
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        
        self.data = self.data[:i]+self.data[i+1:]
        
        self.restore_heap(self.get_parent_index(i))
        
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
                
        if(len(self.data) == 0):
            return None
        
        temp = self.data[0]
        self.data = self.data[1:]
        
        self.heapify()
        
        return temp
    
    def add(self, obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code    
        self.data.append(obj)    
        
        self.heapify()
            
    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to data
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        for element in lst :
            self.data.append(element)
                
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        # Your codeleftmost_child <= rightmost_child   
        
        self.data = []

if __name__ == '__main__':
    pass