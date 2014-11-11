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
        self.MIN_TOP = is_min
        self.CMP_FUNCTION = compare_fn
        self.EXP2 = arity_exp
        self.DATA = []

        # Your code

    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        if self.MIN_TOP:
            if self.DATA[index1] > self.DATA[index2]:
                return index1
            else:
                return index2
        else:
            if self.DATA[index1] < self.DATA[index2]:
                return index1
            else:
                return index2
        # Your code


    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        self.DATA[i] = val
        # Your code
    
    
    def size(self):
        '''
        Return the size of the heap
        '''
        return len(self.DATA)
        # Your code
        
        
    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        return 2**self.EXP2
        # Your code
        
        
    def get_parent_index(self , child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        if child_index == 0:
            return None
        else:
            return (child_index-1)>>self.EXP2
        # Your code
        
        
    def get_leftmostchild_index(self , parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        child_index = (parent_index<<self.EXP2)+1
        if child_index < self.size():
            return (parent_index<<self.EXP2)+1
        else:
            return None
        # Your code

    
    def get_rightmostchild_index(self , parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        child_index = ((parent_index<<self.EXP2)+1)
        if (child_index > (self.size()-1)):
            return None
        elif (((parent_index+1)<<self.EXP2))>(self.size()-1):
            return (self.size()-1)
        else:
            return (parent_index+1)<<self.EXP2
        # Your code
    

    def import_list(self , lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''    
        for i in lst:
            self.DATA.append(i)
        # Your code


    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        par_ind = i
        while(self.get_rightmostchild_index(par_ind) != None):
            minx = self.get_leftmostchild_index(par_ind)
            maxx = self.get_leftmostchild_index(par_ind)
    
            for j in range(self.get_leftmostchild_index(par_ind),self.get_rightmostchild_index(par_ind) + 1):
                
                if self.CMP_FUNCTION(self.DATA[j] , self.DATA[minx]) == -1:
                    minx = j
                if self.CMP_FUNCTION(self.DATA[j] , self.DATA[maxx]) == 1:
                    maxx = j
            if self.MIN_TOP:
                if self.CMP_FUNCTION(self.DATA[par_ind] , self.DATA[minx]) == 1:
                    self.DATA[par_ind] , self.DATA[minx] = self.DATA[minx] , self.DATA[par_ind]
                    
                    par_ind = minx
                else:
                    break 
            else:
                if self.CMP_FUNCTION(self.DATA[par_ind], self.DATA[maxx]) == -1:
                    self.DATA[par_ind] , self.DATA[maxx] = self.DATA[maxx] , self.DATA[par_ind]
                    
                    par_ind = maxx
                else:
                    break
        # Your code

    
    def restore_heap(self , i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        child_index = i
        par_ind = self.get_parent_index(child_index)
        if self.MIN_TOP:
            if (par_ind != None and self.CMP_FUNCTION (self.DATA[par_ind] , self.DATA[child_index]) == 1):
                
                while (par_ind > 0 and self.CMP_FUNCTION (self.DATA[par_ind] , self.DATA[child_index]) == 1 ):
                    
                    self.DATA[par_ind] , self.DATA[child_index] = self.DATA[child_index] , self.DATA[par_ind]
                    
                    child_index = par_ind
                    par_ind = self.get_parent_index(child_index)
            else:
                self.restore_subtree(child_index)
        else:
            if (par_ind != None and self.CMP_FUNCTION (self.DATA[par_ind], self.DATA[child_index]) == -1):
                
                while (par_ind > 0 and self.CMP_FUNCTION (self.DATA[par_ind], self.DATA[child_index]) == -1):
                    
                    self.DATA[par_ind], self.DATA[child_index] = self.DATA[child_index],self.DATA[par_ind]
                    child_index = par_ind
                    par_ind = self.get_parent_index(child_index)
            else:
                self.restore_subtree(child_index)      
        # Your code
      
        

    def heapify(self):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        par_ind = self.get_parent_index(self.size()-1)
        while(par_ind >= 0):
            self.restore_subtree(par_ind)
            par_ind = par_ind - 1
        # Your code


    def remove(self , i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        self.DATA[i] , self.DATA[-1] = self.DATA[-1] , self.DATA[i]
        del self.DATA[-1]
        self.restore_subtree(i)
        # Your code
  

    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        element = self.DATA[0]
        self.remove(0)
        return element
        # Your code
   

    def add(self , obj):
        '''
        Add an object 'obj' to the heap
        '''
        self.DATA.append(obj)
        self.heapify()
        # Your code


    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

if __name__ == '__main__':
    pass