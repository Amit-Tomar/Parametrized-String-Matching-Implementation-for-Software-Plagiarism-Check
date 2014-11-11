'''
Created on 13-Nov-2013

@author: Rishabh Manoj
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
    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        if self.MIN_TOP:
            if self.DATA[index1] <= self.DATA[index2]:
                return 1
            else:
                return -1
        else:
            if self.DATA[index1] >= self.DATA[index2]:
                return 1
            else:
                return -1

    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        self.DATA[i] = val
    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

    def size(self):
        '''
        Return the size of the heap
        '''
        return len(self.DATA)

    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        ar=2**(self.EXP2)
        return ar
    
    def get_item_at(self, i):
        '''
        Return the i-th element of the data list (DATA)
        '''
        return self.DATA[i]

    def get_parent_index(self, child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''    
        if child_index == 0:
            return None
        return child_index-1 >> self.EXP2

    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        if((parent_index<<self.EXP2)+1<len(self.DATA)):
            return (parent_index<<self.EXP2)+1
        else:
            return None 
    
    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''    
        if (get_leftmostchild_index(self,parent_index)==None):
             return None
        elif (((parent_index<<self.EXP2)+2**self.EXP2)<len(self.DATA)):
             return ((parent_index<<self.EXP2)+2**self.EXP2)
        else:
             return len(self.DATA)-1

    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        child = (parent_index<<self.exp2)+1
        for i in range((parent_index<<self.exp2)+1, ((parent_index+1)<<self.exp2)+1 ):
            if self.min_top:
                if self.cmp_function(self.data[i], self.data[child])==-1:
                    child = i
            else:
                if self.cmp_function(self.data[i], self.data[child])==1:
                    child = i
            return child

    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        while(self.get_rightmostchild_index(i) is not None):
            minimum = self.get_leftmostchild_index(i)
            maximum = self.get_leftmostchild_index(i)
    
            for j in range(self.get_leftmostchild_index(i), self.get_rightmostchild_index(i)+1):
                if self.cmp_function(self.data[j], self.data[minimum]) == -1:
                    minimum = j
                if self.cmp_function(self.data[j], self.data[maximum]) == 1:
                    maximum = j
            if self.min_top:
                if self.cmp_function(self.data[i], self.data[minimum]) == 1:
                    self.data[i], self.data[minimum] = self.data[minimum], self.data[i]
                    minimum = i
                else:
                    break 
            else:
                if self.cmp_function(self.data[i], self.data[maximum]) == -1:
                    self.data[i], self.data[maximum] = self.data[maximum], self.data[i]
                    maximum = i
                else:
                    break

     def heapify(self):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        parent = self.get_parent_index(len(self.data)-1)
        while(parent > -1):
            self.restore_subtree(parent)
            parent = parent-1 
     
    def restore_heap(self, i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        self.heapify()

    
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        l=self.DATA[i]
        self.DATA[i]=self.DATA[-1]
        self.DATA[-1]=l
        self.pop()
        self.restore_heap(i)
    # Your code
        
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        self.DATA.remove(self.DATA[-1])
    
    def add(self, obj):
        '''
        Add an object 'obj' to the heap
        '''
        l=self.size()
        self.DATA[l]=obj
        return self.DATA

    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
        self.DATA=self.DATA + lst
        return self.DATA
    
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        self.DATA = []

if __name__ == '__main__':
    pass
    CMP_FUNCTION = lambda x, y : (1 if (x > y) else (-1 if (x < y) else 0))
    heap = Heap(False, 1, CMP_FUNCTION)
    heap.DATA=[2,4,3,5,6]
    heap.restore_subtree(0)
    print heap.DATA
    print heap.pop()
