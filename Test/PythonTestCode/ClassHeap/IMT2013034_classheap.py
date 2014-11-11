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
            if self.data[index1] <= self.data[index2]:
                return True
        else :
            if self.data[index1] >= self.data[index2]:
                return True


    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        # Your code
        self.data[i] = val
        
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
        Return the i-th element of the data list (self.data)
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
        else :
            return (child_index-1) >> self.exp2
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        left_child_index = (parent_index << self.exp2) + 1
        if self.size() > left_child_index :
            return left_child_index
        else :
            return None
        

    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        right_child_index = (parent_index + 1) << self.exp2
        if self.get_leftmostchild_index(parent_index)==None :
            return None
        elif self.size() > right_child_index :
            return right_child_index
        else : 
            return self.size() - 1

    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        top_child_index = self.get_leftmostchild_index(parent_index)
        right_child_index = self.get_rightmostchild_index(parent_index)
        if top_child_index == None :
            return None
        else :
            child_index = top_child_index
            if(self.min_top):
                while child_index <= right_child_index:
                    if self.cmp_function(self.data[child_index], self.data[top_child_index]) == -1:
                        top_child_index = child_index
                    child_index += 1
            else:
                while child_index <= right_child_index:
                    if self.cmp_function(self.data[child_index], self.data[top_child_index]) == 1:
                        top_child_index = child_index
                    child_index += 1
        return top_child_index
    
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
    
        fav_child = self.get_top_child(i)
        if self.min_top:
            while fav_child and self.cmp_function(self.get_item_at(fav_child), self.get_item_at(i)) == -1:
                self.data[fav_child], self.data[i] = self.data[i], self.data[fav_child]
                fav_child, i = self.get_top_child(fav_child), fav_child    
        else :
            while fav_child and self.cmp_function(self.get_item_at(fav_child), self.get_item_at(i)) == 1:
                self.data[fav_child], self.data[i] = self.data[i], self.data[fav_child]
                fav_child, i = self.get_top_child(fav_child), fav_child
            
    def restore_heap(self, i):
        '''
        Restore the heap property for self.data assuming that it has been 'corrupted' at index i
        The rest of self.data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        parent_index = self.get_parent_index(i)
        if i > 0 and ((self.min_top  and self.cmp_function(self.data[i], self.data[parent_index]) == -1) or 
                      (not self.min_top and self.cmp_function(self.data[i], self.data[parent_index]) == 1)):
            while i > 0 and ((self.min_top  and self.cmp_function(self.data[i], self.data[parent_index]) == -1) or 
                             (not self.min_top and self.cmp_function(self.data[i], self.data[parent_index]) == 1)):
                self.data[i], self.data[parent_index] = self.data[parent_index], self.data[i]
                i, parent_index = parent_index, self.get_parent_index(parent_index)
        else :
            self.restore_subtree(i)


    def heapify(self):
        '''
        Rearrange self.data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        node_index = self.get_parent_index(len(self.data)-1)
        while node_index >= 0 :
            self.restore_subtree(node_index)
            node_index -= 1
    

    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        final = self.size() - 1
        self.data[i], self.data[final] = self.data[final], self.data[i]
        self.data.pop()
        self.restore_subtree(i)

    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        max_min = self.data[0]
        self.remove(0)
        return max_min

    def add(self, obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data.append(obj)
        self.restore_heap(len(self.data)-1)
    
    
    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to self.data
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        i = 0
        while i < len(lst):
            self.data.append(lst[i])
            i += 1
        self.heapify()
    
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        # Your code
        while self.size() != 0:
            self.data.pop()


if __name__ == '__main__':
    pass