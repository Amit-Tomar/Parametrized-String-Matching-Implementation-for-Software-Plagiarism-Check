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
        
    def max_of_child (self, leftchild_index , rightchild_index ) :
        #Return the index of the maximum value at index1 and index2
        max_index = self.data[leftchild_index : rightchild_index+1].index(max(self.data[leftchild_index : rightchild_index+1]))
        return leftchild_index + max_index
    
    def min_of_child (self, leftchild_index , rightchild_index) :
        #Return the index of the minimum value at index1 and index2
        min_index = self.data[leftchild_index : rightchild_index+1].index(min(self.data[leftchild_index : rightchild_index+1]))
        return leftchild_index + min_index
    
    def put_item_at(self, i, obj):
        self.data[i] = obj
        
    def swap_element (self, index1 , index2):
        temp_data1 = self.get_item_at(index1)
        temp_data2 = self.get_item_at(index2)
        self.put_item_at(index1 , temp_data2)
        self.put_item_at(index2 , temp_data1)
        
    def size(self):
        '''
        Return the size of the heap
        '''
        # Your code
        size_heap = len(self.data)
        return size_heap
        
    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        # Your code
        if(self.min_top == True):
            if(cmp(self.get_item_at(index1),self.get_item_at(index2)) != 1):
                return True
        else:
            if(cmp(self.get_item_at(index1),self.get_item_at(index2)) != -1):
                return True
        
    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        # Your code
        self.data[i] = val
    
    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        # Your code
        arity_of_heap = 1 << self.exp2
        return arity_of_heap
    
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
        if child_index == 0:
            return None
        parent_index = (child_index-1) >> self.exp2
        return parent_index
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        leftchild_index = (parent_index<<self.exp2)+1
        heap_size = self.size()
        if(cmp(leftchild_index , heap_size) == -1):
            return leftchild_index
        else:
            return None
    
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        arity_heap = self.arity()
        leftchild_index = self.get_leftmostchild_index(parent_index)
        if(leftchild_index == None):
            return None
        rightchild_index = leftchild_index + arity_heap -1
        heap_size = self.size()
        if(cmp(rightchild_index , heap_size) == -1):
            return rightchild_index
        else:
            return heap_size-1
    
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        leftchild_index  = self.get_leftmostchild_index(parent_index) 
        rightchild_index = self.get_rightmostchild_index(parent_index)
        if(rightchild_index == None):
            return None
        if self.min_top == False :
            return self.max_of_child(leftchild_index , rightchild_index)
        else:
            return self.min_of_child(leftchild_index , rightchild_index)


    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        size_heap = self.size()
        parent_index = i
        fav_child = self.get_top_child(parent_index)
        if( parent_index == None  or parent_index >= size_heap):
            return None
        if self.min_top == True :
            while(fav_child != None and (self.cmp_function( self.get_item_at(i) , self.get_item_at(fav_child)) == 1 )):
                self.swap_element (i , fav_child)
                i = fav_child
                parent_index = i
                fav_child = self.get_top_child(parent_index)
        else :
            while(fav_child != None and (self.cmp_function( self.get_item_at(i) , self.get_item_at(fav_child)) == -1 )):
                self.swap_element (i , fav_child)
                i = fav_child
                parent_index = i
                fav_child = self.get_top_child(parent_index)
            
            
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
        if(self.min_top == True ):
            while(parent_index != None and self.cmp_function( self.get_item_at(i) , self.get_item_at(parent_index)) == -1 ):
                count += 1
                self.swap_element (i , parent_index)
                i = parent_index
                parent_index = self.get_parent_index(i)
            if(count == 0 ):
                self.restore_subtree(i)
        else:
            while(parent_index != None and self.cmp_function( self.get_item_at(i) , self.get_item_at(parent_index)) == 1 ):
                count += 1
                self.swap_element (i , parent_index)
                i = parent_index
                parent_index = self.get_parent_index(i)
            if(count == 0):
                self.restore_subtree(i)

    def heapify(self):
        '''
        Rearrange DATA into a heapDATA
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        index = self.size() - 1
        index = self.get_parent_index(index)
        while(index >= 0):
            self.restore_subtree(index)
            index -= 1


    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        size_of_heap = self.size()
        self.swap_element (i , size_of_heap-1)
        self.data[size_of_heap-1:size_of_heap] = []
        self.restore_heap(i)
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        if(self.size() == 0):
            return None
        pop_index = 0
        pop_element = self.get_item_at(0)
        self.remove(pop_index)
        return pop_element
    
    
    def add(self, obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data += [obj]
        self.restore_heap(self.size()-1)
    
    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        length_of_list = len(lst)
        for index in range(0, length_of_list):
            self.add(lst[index])
        
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        # Your code
        self.data = []
    
        # Other methods will be the same as the functions in the modheap module -
        # add them here as methods of the Heap class

if __name__ == '__main__':
    pass