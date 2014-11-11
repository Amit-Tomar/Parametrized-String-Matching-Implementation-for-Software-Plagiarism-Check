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
        if self.min_top:
            if self.cmp_function (self.data[index1], self.data[index2]) <= 0 :
                return True
            else : return False
            
        else:
            if self.cmp_function (self.data[index1], self.data[index2] ) >= 0:
                return True
            else : return False

    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        # Your code  
        self.data[i] = val
        
    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class
    
    def swap(self, index_1, index_2):
        '''
        swapping 2 elements
        '''
        self.data[index_1], self.data[index_2] = self.data[index_2], self.data[index_1]
    
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
        return 2 << (self.exp2-1)
        
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
        if( (child_index-1)>>self.exp2 >= 0):
            return (child_index-1)>>self.exp2
        else : return None
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code        
        if ( (parent_index<<self.exp2) + 1 < self.size()):
            return (parent_index<<self.exp2)+1
        else :  return None      
    
    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        if ( (parent_index<<self.exp2)+self.arity() < self.size()) :
            return (parent_index<<self.exp2)+self.arity()
        elif ( self.get_leftmostchild_index(parent_index) != None):
            return self.size()-1
        else :
            return None        
        
    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code 
        leftmost_child  = self.get_leftmostchild_index(parent_index)    
        rightmost_child = self.get_rightmostchild_index(parent_index)
        top_child = leftmost_child
    
        if(leftmost_child!= None):
                   
            if(self.min_top == True):
                while(leftmost_child <= rightmost_child):
                    if( self.cmp_function ( self.data[top_child], self.data[leftmost_child]) == 1 ):
                        top_child = leftmost_child                
                    leftmost_child += 1
            
            elif(self.min_top==False):
                while(leftmost_child <= rightmost_child):
                    if( self.cmp_function ( self.data[top_child], self.data[leftmost_child]) == -1 ):
                        top_child = leftmost_child               
                    leftmost_child += 1  
            
            return top_child
        else:
            return None    
    
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        top_child = self.get_top_child(i)
        
        if top_child != None and i != None:
        
            if self.min_top:
                while self.cmp_function(self.data[i], self.data[top_child]) > 0:
                    i, top_child = self.child_recur(i, top_child)
                    if(top_child == None):
                        break
            else :
                while self.cmp_function(self.data[i], self.data[top_child]) < 0:
                    i, top_child = self.child_recur(i, top_child)
                    if(top_child == None):
                        break
                    
    def child_recur(self, i, top_child):
        '''
        To swap an element and its child
        '''
        self.swap(i, top_child)
        i = top_child
        top_child = self.get_top_child(i)
        return i, top_child                  
                        
    def parent_recur(self, i, parent_index): 
        '''
        To swap an element and its parent 
        '''
        self.swap(i, parent_index)
        i = parent_index    
        parent_index = self.get_parent_index(i)
        return i, parent_index
    
    def restore_heap(self, i):
        '''
        Restore the heap property for data assuming that it has been 'corrupted' at index i
        The rest of data is assumed to already satisfy the heap property
        Algo: (child_recur(i, top_child)i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        
        if i != None :
            parent_index = self.get_parent_index(i)
                   
        flag = 0      
           
        if(parent_index != None ): 
            
            if self.min_top:            
                while self.cmp_function(self.data[i], self.data[parent_index]) < 0:
                    flag = 1
                    i, parent_index = self.parent_recur(i, parent_index)
                    if parent_index == None :
                        break
                    
            else:                         
                while self.cmp_function(self.data[i], self.data[parent_index]) > 0:
                    flag = 1
                    i, parent_index = self.parent_recur(i, parent_index)
                    if parent_index == None:
                        break
                    
        if flag == 0 :
            self.restore_subtree(i)
             
    def heapify(self):
        '''
        Rearrange data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code 
        parent_index = self.get_parent_index(self.size()-1)
        
        if parent_index != None :
            while parent_index >= 0:
                self.restore_subtree(parent_index)
                parent_index -= 1             
    
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        self.swap (i, len(self.data)-1)
        self.data.pop()
        self.restore_heap(i)    
        
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        lenght = self.data[0]
        self.remove(0)
        return lenght
    
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
        for elem in lst :
            self.data.append(elem)
                
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''  
        self.data = []

if __name__ == '__main__':
    pass