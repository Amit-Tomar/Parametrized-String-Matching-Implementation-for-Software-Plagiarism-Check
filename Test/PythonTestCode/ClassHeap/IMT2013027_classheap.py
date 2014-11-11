'''
Created on 22-Oct-2013

@author: raghavan

Last modified on 14-Nov-2013

@modifier: Nigel Steven Fernandez (IMT2013027)
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
        if ((self.min_top and self.cmp_function(self.get_item_at(index2), self.get_item_at(index1)) < 0) or 
            (not self.min_top and self.cmp_function(self.get_item_at(index2), self.get_item_at(index1)) > 0)):
            return False
        else:
            return True


    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        if(i in range(0, self.size())):
            self.data[i] = val
            
        return None
    
    
# Other methods will be the same as the functions in the modheap module -
# add them here as methods of the Heap class    

    
    def size(self):
        '''
        Return the size of the heap
        '''
        return len(self.data)


    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        return 2 << (self.exp2 - 1)
    
        
    def get_item_at(self, i):
        '''
        Return the i-th element of the data list (DATA)
        '''
        if(i in range(0, self.size())):
            return self.data[i]
    
        return None


    def get_parent_index(self, child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        if(child_index == 0):
            return None
        else:
            return (child_index - 1) >> self.exp2


    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        leftmostchild_index = (parent_index << self.exp2) + 1
    
        if(leftmostchild_index > (self.size() - 1)):
            return None
        else:
            return leftmostchild_index


    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        #min() used to take care of incomplete heap
        rightmostchild_index = min([(parent_index << self.exp2) + self.arity(),
                                    self.size() - 1])
     
        if(self.get_leftmostchild_index(parent_index) == None):
            return None
        else:
            return rightmostchild_index


    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''    
        #stores a list of children of parent at index i
        children = self.data[self.get_leftmostchild_index(parent_index) :
                             self.get_rightmostchild_index(parent_index) + 1]
        
        children_sorted = children[:]
        children_sorted.sort(self.cmp_function)
        
        offset = self.get_leftmostchild_index(parent_index)
        
        return ((offset + children.index(children_sorted[0])) if self.min_top 
                else (offset + children.index(children_sorted[-1])))


    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        while(i <= self.get_parent_index(self.size() - 1) and 
              self.is_favoured(i, self.get_top_child(i)) == False):
            j = self.get_top_child(i)
            self.data[i], self.data[j] = self.data[j], self.data[i]
            i = j 

        return None


    def restore_heap(self, i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        flag = 0
        
        while(i > 0 and self.is_favoured(self.get_parent_index(i), i)==False): 
            self.data[i], self.data[self.get_parent_index(i)] = (
            self.data[self.get_parent_index(i)], self.data[i])
            i = self.get_parent_index(i)
            flag = 1
    
        if(flag == 0):
            self.restore_subtree(i)
    
        return None
        
    
    def heapify(self):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        i = self.get_parent_index(self.size() - 1)
        
        while(i >= 0):
            self.restore_subtree(i)
            i -= 1
    
        return None


    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        ''' 
        self.data[i], self.data[self.size() - 1] = (
        self.data[self.size() - 1], self.data[i])
           
        obj = self.data.pop()
        self.restore_subtree(i)    
        
        return obj


    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        return self.remove(0)


    def add(self, obj):
        '''
        Add an object 'obj' to the heap
        '''
        self.data.append(obj)
        i = self.size() - 1
        while(i != 0 and self.is_favoured(self.get_parent_index(i), i)==False): 
            self.data[i], self.data[self.get_parent_index(i)] = (
            self.data[self.get_parent_index(i)], self.data[i])
            i = self.get_parent_index(i)
    
        return None


    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''    
        self.data = lst[:]
        
        return None


    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        self.data = []
    
        return None


if __name__ == '__main__':
    pass
