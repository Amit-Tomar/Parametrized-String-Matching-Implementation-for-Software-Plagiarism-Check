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

        
        # Your code

    
    def is_favoured(self , index1 , index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
	    '''
        
        if(self.min_top == True):
            if(self.cmp_function( self.data[index1], self.data[index2]) != 1 ):
                return True
            else:
                return False
     
        else:
            if(self.cmp_function( self.data[index1], self.data[index2]) != -1 ):
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
    # Your code


    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        return 2 << (self.exp2-1)
        # Your code
        
        
        
    def get_item_at(self,i):
        '''
        Return the i-th element of the data list (self.data)
        '''
        return self.data[i]
    
    
    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        
        c_index = (child_index-1) >> self.exp2
        if(c_index >= 0):
            return c_index
        else:
            return None
        # Your code
    
    
    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        first_child = (parent_index << self.exp2)+1
        if(first_child < self.size()):
            return first_child
        else:
            return None
        # Your code
    
    
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        first_child = self.get_leftmostchild_index(parent_index)
        if(first_child == None ):
            return None
        else:
            last_child = (parent_index+1) << self.exp2
            while(first_child <= last_child):
                if(last_child < self.size()):
                    return last_child
                last_child -= 1
        
        # Your code
    
    
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        
       
        req_child_index = self.get_leftmostchild_index(parent_index)
        i = req_child_index
        j = self.get_rightmostchild_index(parent_index)
       
        
        if(i != None):
           
            if(self.min_top == True):
                while(i <= j):
                    if( self.cmp_function( self.get_item_at(req_child_index), self.get_item_at(i)) == 1 ):
                        req_child_index = i
                    
                    i += 1
            
            elif(self.min_top == False):
                while(i <= j):
                    if( self.cmp_function ( self.get_item_at(req_child_index), self.get_item_at(i)) == -1):
                        req_child_index = i
                    
                    i += 1
       
            
            return req_child_index
        else:
            return None
        # Your code
    
    
    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        
        j = self.get_top_child(i)
        
        if( i != None and j != None):
        
            if(self.min_top == True):
                
                while(self.cmp_function (self.data[i] , self.data[j]) == 1):
                    self.data[i], self.data[j] = self.data[j], self.data[i]
                    i = j
                    j = self.get_top_child(i)
                    if(j == None):
                        break
            
            elif(self.min_top == False):
                while(self.cmp_function (self.data[i] , self.data[j]) == -1):
                    self.data[i], self.data[j] = self.data[j], self.data[i]
                    i = j
                    j = self.get_top_child(i)
                    if(j == None):
                        break
        
        
        # Your code
    
        
    def restore_heap( self, i ):
        '''
        Restore the heap property for self.data assuming that it has been 'corrupted' at index i
        The rest of self.data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element
        '''
        if(i != None):
            p_index = self.get_parent_index(i)
        
            if(p_index != None):
            
                if(self.min_top == True):    
                    if(self.cmp_function (self.data[i] , self.data[p_index]) == -1):  
                        while(self.cmp_function (self.data[i] , self.data[p_index]) == -1 ):
                            self.data[i], self.data[p_index] = self.data[p_index], self.data[i]
                            i = p_index
                            p_index = self.get_parent_index(i)
                            if(p_index == None):
                                break
                
                    else:
                        self.restore_subtree(i)
                
                elif(self.min_top == False):    
                    if( self.cmp_function( self.data[i] , self.data[p_index]) == 1):  
                        while(self.cmp_function (self.data[i] , self.data[p_index]) == 1 ):
                            self.data[i], self.data[p_index] = self.data[p_index], self.data[i]
                            i = p_index
                            p_index = self.get_parent_index(i)
                            if(p_index == None):
                                break
                
                    else:
                        self.restore_subtree(i)        
            else:
                self.restore_subtree(i)
        # Your code
    
    
    def heapify(self):
        '''
        Rearrange self.data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        length = self.size()-1
        i = self.get_parent_index(length)
        if(i != None):
            while(i >= 0):
                self.restore_subtree(i)
                i -= 1
        
        # Your code
    
    
    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        length = self.size() - 1
        self.data[i], self.data[length]=self.data[length], self.data[i]
        self.data.pop()
        self.restore_heap(i)
        # Your code
    
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        length = self.size() - 1
        self.data[0], self.data[length]=self.data[length], self.data[0]
        top = self.data.pop()
        self.restore_subtree(0)
        return top
        # Your code
    

    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        self.data.append(obj)
        self.restore_heap(self.size() - 1)
        # Your code


    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to self.data
        Make sure this does not modify the input list 'lst'
        '''
        for elem in lst:
            self.data.append(elem)
        
        # Your code
    
    
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        self.data = []
        # Your code
        
        
        # Other methods will be the same as the functions in the modheap module -
        # add them here as methods of the Heap class

if __name__ == '__main__':
    pass
