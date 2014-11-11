'''
Created on 22-Oct-2013

@author: raghavan
'''

class Heap(object):
    '''
    Heap class
    '''
    def __init__(self, is_min, arity_exp, compare_fn):
        self.min_top = is_min
        self.cmp_function = compare_fn
        self.exp2 = arity_exp
        self.data = []

#     def is_min_heap(self):
#         return self.min_top

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
        return (1 << self.exp2)
    
    
    def get_item_at(self, i):
        '''
        Return the i-th element of the data list (self.data)
        '''
        return self.data[i]

    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data list (self.data) to the value 'val'
        '''
        self.data[i] = val
    
    def get_parent_index(self, child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        Should return None if the child has no parent
        '''
        if (child_index <= 0):
            return None
        else:
            parent_index = (child_index - 1) >> self.exp2
            return (parent_index if (parent_index < child_index) else None)
    
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        Should return None if the parent has no child
        '''
        child_index = (parent_index << self.exp2) + 1
        return (child_index if (child_index < self.size()) else None)
    
    
    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        leftmostchild_index = self.get_leftmostchild_index(parent_index)
        return (None if (leftmostchild_index == None) else (min(self.size(), (leftmostchild_index + self.arity()))-1))
    
    
    def is_favoured(self, index1, index2):
        '''
        Might heap to have this helper function to check if the element elem1 if favoured (to move up) over elem2.
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        return ((not self.min_top and self.cmp_function(self.data[index1], self.data[index2]) >= 0) or
                (self.min_top and self.cmp_function(self.data[index1], self.data[index2]) <= 0))
    
    
    def get_top_child(self, parent_index):
        '''
        This returns the index of the child which is most favoured to move up the tree among all the childred on the
        element at parent_index
        '''
        min_index = self.get_leftmostchild_index(parent_index)
        if (min_index == None):
            return None
        max_index = min(self.size(), (min_index + self.arity()))
        child_index = min_index
        for i in range(min_index, max_index):
            if self.is_favoured(i, child_index):
                child_index = i
        return child_index
    
    
    def should_move_up(self, i):
        '''
        Return true if the element at index i needs to move up the tree
        '''
        parent_index = self.get_parent_index(i)
        return (False if (parent_index == None) else self.is_favoured(i, parent_index))
    
    
    def should_move_down(self, i):
        '''
        Return true if the element at index i needs to move down the tree
        '''
        child_index = self.get_top_child(i)
        return (False if (child_index == None) else self.is_favoured(child_index, i))
    
    
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        while (self.should_move_down(i)):
            child_index = self.get_top_child(i)
            self.data[i], self.data[child_index] = self.data[child_index], self.data[i]
            i = child_index
    
    
    def restore_heap(self, i):
        '''
        Restore the heap property for self.data assuming that it has been 'corrupted' at index i
        The rest of self.data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        moved_up = False
        while (self.should_move_up(i)):
            moved_up = True
            parent_index = self.get_parent_index(i)
            self.data[i], self.data[parent_index] = self.data[parent_index], self.data[i]
            i = parent_index
        if (not moved_up):
            self.restore_subtree(i)
            
    
    def heapify(self):
        '''
        Rearrange self.data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        last_nonleaf = self.get_parent_index(self.size() - 1)
        while (last_nonleaf >= 0):
            self.restore_subtree(last_nonleaf)
            last_nonleaf -= 1
    
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        if (i < (self.size() - 1)):
            self.data[i], self.data[-1] = self.data[-1], self.data[i]
        item = self.data.pop()
        if (i < (self.size() - 1)):
            self.restore_heap(i)
        return item
    
    
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
        self.restore_heap(self.size()-1)
    
    
    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to self.data
        Make sure this does not modify the input list 'lst'
        '''
        for elem in lst:
            self.data.append(elem)
    
    
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        self.data = []

if __name__ == '__main__':
    pass