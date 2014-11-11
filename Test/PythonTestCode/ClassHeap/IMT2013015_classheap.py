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
        if self.min_top == True :
            if self.data[index1] < self.data[index2]:
                return True
        else :
            if self.data[index1] > self.data[index2]:
                return True

    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        # Your code
        self.data[i] = val


    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class
    def is_validindex(self, i):
        if i in range(len(self.data)):
            return True
    
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
        
        
    def get_item_at(self, i):
        '''
        Return the i-th element of the data list (DATA)
        '''
        return self.data[i]
    
    
    def get_parent_index(self, child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your code
        if self.is_validindex((child_index-1)>>self.exp2)== True:
            return (child_index-1)>>self.exp2
        if child_index == 0 :
            return None
        else:
            return None
    
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        if self.is_validindex((parent_index<<self.exp2)+ 1)==True:
            return (parent_index<<self.exp2)+1
        else :
            return None
    
    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        if self.get_leftmostchild_index(parent_index) not in range(len(self.data)):
            return None
        elif self.is_validindex(parent_index<<self.exp2 + 2**self.exp2)==True:
            return (parent_index<<self.exp2)+2**self.exp2
        else :
            return len(self.data)-1
    
    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        if parent_index <= self.get_parent_index(len(self.data)-1):
            lcindex = self.get_leftmostchild_index(parent_index)
            rcindex = self.get_rightmostchild_index(parent_index)
            min_val = self.data[lcindex]
            min_val_index = self.get_leftmostchild_index(parent_index)
            max_val = self.data[lcindex]
            for x in range(lcindex, rcindex+1):
                elem = self.data[x]
                if self.min_top == True:
                    if cmp(elem, min_val) == -1 :
                        min_val = elem
                        min_val_index = self.data.index(elem)
                elif self.min_top == False:
                    if cmp(elem, max_val) == 1 :
                        max_val = elem
                        min_val_index = self.data.index(elem)
            return min_val_index
           
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        if i <= self.get_parent_index(len(self.data)-1) and i >= 0:
            j = self.get_top_child(i)
            if self.min_top == True:
                while i > self.get_parent_index(len(self.data)-1) and (self.data[i]>self.data[j]):
                    self.data[i] = self.data[j]
                    self.data[j] = self.data[i]
                    i = j
                    j = self.get_top_child(i)
    
                            
            if self.min_top == False:
                while i > self.get_parent_index(len(self.data)-1) and (self.data[i]<self.data[j]):
                    self.data[i] = self.data[j]
                    self.data[j] = self.data[i]
                    i = j
                    j = self.get_top_child(i)
    
                                   
    def restore_heap(self, i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
      
        parent_index = self.get_parent_index(i)   
        if self.min_top:
            if parent_index != None and self.cmp_function(self.data[i], self.data[parent_index]) == -1:
                while (parent_index != None and self.cmp_function(self.data[i], self.data[parent_index]) == -1):
                    self.data[i] = self.data[parent_index]
                    self.data[parent_index] = self.data[i]
                    i = parent_index 
                    parent_index = self.get_parent_index(i)    
                    
            else:
                self.restore_subtree(i)
        else:
            if (parent_index != None and self.cmp_function(self.data[i], self.data[parent_index]) == 1) :
                while parent_index != None and self.cmp_function(self.data[i], self.data[parent_index]) == 1:
                    self.data[i] = self.data[parent_index] 
                    self.data[parent_index] = self.data[i]
                    i = parent_index    
                    parent_index = self.get_parent_index(i) 
                
            else:
                self.restore_subtree(i)
                
    def heapify(self):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        nodeindex = self.get_parent_index(len(self.data)-1)
        while(nodeindex >= 0):
            self.restore_subtree(nodeindex)
            nodeindex -= 1
    
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        self.data[i] = self.data[len(self.data)-1]
        self.data[len(self.data)-1] = self.data[i]
        self.data.pop()
        self.restore_heap(i)
    
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        elem = self.data[0]
        self.remove(0)
        return elem
    
    
    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data.append(obj)
        self.restore_heap(len(self.data)-1)
                
    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        for x in lst:
            self.add(x)        
        
    def clear(self):
        '''
        Clear the dadef initialize_heap(is_min = True, arity_exp = 1, compare_fn = None):
        global MIN_TOP, CMP_FUNCTION, EXP2, DATA
        MIN_TOP = is_min
        CMP_FUNCTION = compare_fn
        EXP2 = arity_exp
        DATA = []ta in the heap - initialize to empty list
        '''
        # Your code
        self.data = []

if __name__ == '__main__':
    pass