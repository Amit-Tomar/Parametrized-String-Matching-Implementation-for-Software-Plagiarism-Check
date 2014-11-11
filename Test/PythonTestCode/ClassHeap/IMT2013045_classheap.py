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
        return 2**self.exp2
    
        
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
      
        child_index = ( parent_index << self.exp2 ) + 1
        if( child_index <= self.size()-1 ):
            return child_index
        else:
            return None
        
        
    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        
        rchild_index = ( parent_index << self.exp2 ) + self.arity()
        lchild_index = self.get_leftmostchild_index(parent_index)
        if( rchild_index <= self.size()-1 ):
            return rchild_index
        elif( lchild_index != None ):
            return self.size()-1    
        else:
            return None  
                    
    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        lchild_index = self.get_leftmostchild_index(parent_index)
        rchild_index = self.get_rightmostchild_index(parent_index)
        if( ( lchild_index != None ) and ( rchild_index != None ) ): 
            i = rchild_index
            temp_list = []
            while(i >= lchild_index):
                temp_list.append( ( self.data[i], i) )
                i -= 1
            if(self.min_top == False):
                pos = temp_list.index(max(temp_list))  
                return temp_list[pos][1]   
            else:
                pos = temp_list.index(min(temp_list))  
                return temp_list[pos][1]   
        elif(( lchild_index != None ) and ( rchild_index == self.size() - 1 )):
            return lchild_index
        else:
            return None
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        child_index = self.get_top_child(i)
        if( self.min_top == True ):
            while( child_index != None ):
                if( self.cmp_function( self.data[i] , self.data[child_index] ) == 1 ):
                    self.data[i] , self.data[child_index] = self.data[child_index] , self.data[i]
                    i = child_index
                    child_index = self.get_top_child(i)
                else:
                    lchild_index , rchild_index = self.get_leftmostchild_index(i) , self.get_rightmostchild_index(i)
                    if((lchild_index != None ) and (rchild_index != None)):
                        while( lchild_index <= rchild_index ):
                            self.restore_subtree(lchild_index)
                            lchild_index += 1
                    break
        else:
            while( child_index != None ):
                if( self.cmp_function( self.data[i] , self.data[child_index] ) == -1 ):
                    self.data[i] , self.data[child_index] = self.data[child_index] , self.data[i]
                    i = child_index
                    child_index = self.get_top_child(i)
                else:
                    lchild_index , rchild_index = self.get_leftmostchild_index(i) , self.get_rightmostchild_index(i)
                    if((lchild_index != None ) and (rchild_index != None)):
                        while( lchild_index <= rchild_index ):
                            self.restore_subtree(lchild_index)
                            lchild_index += 1
                    break
                    
    def restore_heap(self, i):
        '''
        Restore the heap property for data assuming that it has been 'corrupted' at index i
        The rest of data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        counter = 0
        initial = i
        if( self.min_top == True ):
            parent_index = self.get_parent_index(i)
            while( parent_index != None ):
                if( self.cmp_function( self.data[i] , self.data[parent_index] ) == -1 ):
                    self.data[i], self.data[parent_index] = self.data[parent_index], self.data[i]
                    i = parent_index
                    counter += 1  
                    parent_index = self.get_parent_index(i)
                else:
                    self.restore_subtree(i)
                    break
            if( counter == 0 ):
                self.restore_subtree(initial)
            else:
                self.restore_subtree(i)
        else:
            parent_index = self.get_parent_index(i)
            while( parent_index != None ):
                if( self.cmp_function( self.data[i] , self.data[parent_index] ) == 1 ):
                    self.data[i], self.data[parent_index] = self.data[parent_index], self.data[i]
                    i = parent_index
                    counter += 1  
                    parent_index = self.get_parent_index(i)
                else:
                    self.restore_subtree(i)
                    break
            if( counter == 0 ):
                self.restore_subtree(initial)
            else:
                self.restore_subtree(i)
    
    
    def heapify(self):
        '''
        Rearrange data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        i = self.size()-1
        while(i >=0 ):
            self.restore_heap(i)
            i -= 1       
    
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        self.data[i] , self.data[self.size()-1] = self.data[self.size()-1] , self.data[i]
        item_removed = self.data[self.size()-1]
        self.data = self.data[:self.size()-1]
        return item_removed
        
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        item = self.remove(0)
        self.heapify()
        return item
        
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
        length = len(lst)
        i = 0
        while(i < length):
            self.data.append(lst[i])
            i += 1
    
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        # Your code
        self.data = []

if __name__ == '__main__':
    pass