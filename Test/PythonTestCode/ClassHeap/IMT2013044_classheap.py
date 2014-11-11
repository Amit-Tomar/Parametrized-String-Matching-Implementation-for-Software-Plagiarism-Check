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
        # Your code
        self.data[i] = val

    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class
    
    def size(self):
        '''
        Return the size of the heap
        '''
        # Your code
        return len( self.data )

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
        parent_index = ( child_index - 1 ) >> self.exp2
        if( parent_index >= 0):
            return parent_index
        else:
            return None
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        leftmost_child = ( parent_index << self.exp2 ) + 1
        if ( leftmost_child < self.size() ):
            return leftmost_child
        else:
            return None

    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        count = 1
        leftmost_child = self.get_leftmostchild_index(parent_index)
        if ( leftmost_child !=None ):
            while ( count < self.arity() ):
                rightmost_child = leftmost_child + 1
                if ( rightmost_child >= self.size() ):
                    return leftmost_child
                else:
                    leftmost_child = rightmost_child
                count = count + 1
        else:
            return None
        if(count==self.arity()):
            return rightmost_child

    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favored to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        child_index = ( parent_index << self.exp2 ) + 1
        if(child_index < self.size()):
            count = child_index
            min_child = self.data[child_index]
            max_child = self.data[child_index]
            if ( self.min_top==True ):
                while ( child_index <= count + self.arity() - 1 \
                        and child_index < self.size()):
                    if ( self.cmp_function(self.data[child_index], min_child)==0 \
                         or self.cmp_function(self.data[child_index], min_child)==-1 ):
                        min_index = child_index
                        min_child = self.data[min_index]
                    child_index = child_index + 1
                return min_index
        
            else:
                while ( child_index <= count + self.arity() - 1 \
                        and child_index < self.size()):
                    if ( self.cmp_function(self.data[child_index], max_child)==0 \
                         or self.cmp_function(self.data[child_index], max_child)==1 ):
                        max_index = child_index
                        max_child = self.data[max_index]
                    child_index = child_index + 1
                return max_index
        else:
            return None

    def restore_subtree(self, i):
        '''global MIN_TOP, CMP_FUNCTION, EXP2, DATA
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        child_index = self.get_top_child(i)
        if ( child_index!=None ):
            if ( self.min_top==True ):
                if ( self.cmp_function(self.data[i], self.data[child_index])==1 ):
                    self.data[i] , self.data[child_index] = self.data[child_index] , self.data[i]
                self.restore_subtree(child_index)
            else:
                if ( self.cmp_function(self.data[i], self.data[child_index])==-1 ):
                    self.data[i] , self.data[child_index] = self.data[child_index] , self.data[i]
                self.restore_subtree(child_index)
            
    def restore_heap(self, i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        count = 0
        parent_index = self.get_parent_index(i)
        original_i = i
        if ( self.min_top==True ):
            while ( i!=0 ):
                parent_index = self.get_parent_index(i)
                if ( self.cmp_function(self.data[i], self.data[parent_index])==-1 ):
                    self.data[i] , self.data[parent_index] = self.data[parent_index] , self.data[i]
                    count = count + 1
                    i = parent_index
                else:
                    break
            self.restore_subtree(i)
        else:
            while ( i!=0 ):
                parent_index = self.get_parent_index(i)
                if ( self.cmp_function(self.data[i], self.data[parent_index])==1 ):
                    self.data[i] , self.data[parent_index] = self.data[parent_index] , self.data[i]
                    count = count + 1
                    i = parent_index
                else:
                    break
            self.restore_subtree(i)       
        if ( count == 0 ):
            self.restore_subtree(original_i)
             
    def heapify(self):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        parent_index = ( self.size() - 1 - 1 ) >> self.exp2
        while (parent_index >= 0):
            self.restore_subtree(parent_index)
            parent_index = parent_index - 1
        
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        self.data[i], self.data[self.size()-1] = self.data[self.size()-1], self.data[i]
        element = self.data[self.size()-1]
        self.data = self.data[:self.size()-1]
        return element
        
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        element = self.remove(0)
        self.heapify()
        return element

    def add(self, obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data.append(obj)
        self.heapify()
        
    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        for i in lst:
            self.data.append(i)
    
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        # Your code
        self.data = []  

if __name__ == '__main__':
    pass