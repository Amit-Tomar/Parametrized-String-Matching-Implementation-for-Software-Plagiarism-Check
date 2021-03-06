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
        if(self.min_top == True):
            if( self.data[index1] <= self.data[index2] ):
                return True
        else:
            if( self.data[index1] >= self.data[index2] ):
                return True

    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        self.data[i] = val

    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class
    def size(self):
        '''
        Return the size of the heap
        '''
        return len( self.data )
    
    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
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
        if child_index != 0:
            return (child_index-1)>>self.exp2
        else:
            return None
        
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        if((parent_index<<self.exp2)|1)<len(self.data):
            return (parent_index<<self.exp2)|1
        else:
            return None
        
    def get_rightmostchild_index(self , parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        if(self.get_leftmostchild_index(parent_index)>len(self.data)-1):
            return None
        elif((parent_index+1<<self.exp2)>len(self.data)-1):
            return len(self.data)-1
        else:
            return (parent_index+1<<self.exp2)
        
    def get_top_child(self , parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        r_index = self.get_rightmostchild_index(parent_index)
        l_index = self.get_leftmostchild_index(parent_index)
        minimum = self.get_leftmostchild_index(parent_index)
        maximum = self.get_rightmostchild_index(parent_index)
        if(self.min_top == True):
            for j in range(l_index , r_index+1):
                if self.cmp_function(self.data[j], self.data[minimum])==-1:
                    minimum = j
            return minimum
        else:
            for i in range(l_index , r_index+1):
                if self.cmp_function(self.data[i], self.data[maximum])==1:
                    maximum = i
            return maximum
        
    def restore_subtree(self , i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        if(self.min_top == True):
            while(self.get_leftmostchild_index(i) is not None):
                top_child = self.get_top_child(i)
                if(top_child is not None and self.cmp_function(self.data[i] , self.data[top_child]) == 1):
                    self.data[top_child] , self.data[i] = self.data[i] , self.data[top_child]
                    i = top_child
                else:
                    break    
            
        else:
            while(self.get_leftmostchild_index(i) is not None):
                top_child = self.get_top_child(i)
                if(top_child is not None and self.cmp_function(self.data[i] , self.data[top_child])==-1):
                    self.data[top_child] , self.data[i] = self.data[i] , self.data[top_child]
                    i = top_child
                else:
                    break
                
    def restore_heap(self , i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        res_heap = i
        if (self.min_top == True):
            while(res_heap>0 and res_heap is not None):
                res_heap = self.get_parent_index(i)
                if (self.cmp_function(self.data[res_heap] , self.data[i])==1):
                    self.data[res_heap] , self.data[i] = self.data[i] , self.data[res_heap]
                    res_heap = i
                else:
                    break
            self.restore_subtree(i)
        else:            
            while(res_heap>0 and res_heap is not None):
                res_heap = self.get_parent_index(i)
                if (self.cmp_function(self.data[res_heap] , self.data[i]) == -1):
                    self.data[res_heap] , self.data[i] = self.data[i] , self.data[res_heap]
                    res_heap = i
                else:
                    break
            self.restore_subtree(i)
             
    def heapify(self):
    
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        len_size = len(self.data)-1
        while(len_size > 0):
            self.restore_heap(len_size)
            len_size = len_size - 1
            
    def remove(self , i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        self.data[i] , self.data[len(self.data)-1] = self.data[len(self.data)-1] , self.data[i]
        ele = self.data.pop()
        self.heapify()
        return ele
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        ele = self.remove(0)
        return ele
    
    def add(self , obj):
        '''
        Add an object 'obj' to the heap
        '''
        self.data.append(obj)
        self.heapify()
    
    def import_list(self , lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
        for ele in lst:
            self.data.append(ele)
    
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        self.data = []
        
if __name__ == '__main__':
    pass