'''
Created on 22-Oct-2013

@author: raghavan
'''

class Heap(object):
    '''
    Heap class
    The methods specific to the class implementation are added here - 
    the rest will be the same as the
    functions in the modheap module
    '''
    def __init__(self, is_min, arity_exp, compare_fn):
        '''
        The Python convention is to have upper case name for global variables 
        - that's why the globals in modheap were named in all caps
        Unlike the globals in heap module --- name the attributes as lower 
        case variable names
        '''
        self.min_top = is_min
        self.cmp_function = compare_fn
        self.exp2 = arity_exp
        self.data = []
        # Your code

    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at
         index2 --- 
        In other words a heap is a data structure which ensures that any node
         is favoured over any of its children
        Takes into account whether the heap is min or max and also the result
         of comparison between elem1 and elem2
        '''
        if(self.cmp_function(self.get_item_at(index1), \
                    self.get_item_at(index2)) != 1 and self.min_top == True):
            return True
        if(self.cmp_function(self.get_item_at(index1), \
                    self.get_item_at(index2))!= -1 and self.min_top == False):
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
    
    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal
        node has
         Also only one internal node will have less children than the arity
         of the heap
        '''
        return 2**self.exp2
    
        
    def get_item_at(self, i):
        '''
        Return the i-th element of the data list (data)
        '''
        if (i > self.size()-1):
            return self.data[self.size()-1]
        return self.data[i]
    
    def get_parent_index(self, child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - 
        right shift n by m bits (written as n >> m, in python)
        '''
        if (child_index==0 or child_index==None):
            return None
        else:
            return ((child_index-1)>>self.exp2)
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift 
        n by m bits (written as n << m, in python)
        '''
        i = (parent_index<<self.exp2)+1
        if i > (self.size()-1):
            return None
        return i
    
    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if parent has no child from random import randrange
        '''
        return ((parent_index<<self.exp2)+self.arity())
    
    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the 
        tree among all the children of the
        element at parent_index
        '''
        initial_child = self.get_leftmostchild_index(parent_index)
        cmp_elem = self.data[initial_child]
        index = initial_child
        for children in range(0, self.arity()):
            position = initial_child+children
            if position < self.size():
                if (self.cmp_function(self.data[position], cmp_elem)==-1 \
                    and self.min_top==True):
                    cmp_elem = self.data[position]
                    index = position
                elif(self.cmp_function(self.data[position], cmp_elem)==1 \
                     and self.min_top==False):
                    cmp_elem = self.data[position]
                    index = position
        return index
    def swap(self, index1, index2):
        '''
        swap 2 elements
        '''
        temp = self.data[index1]
        self.data[index1] = self.data[index2]
        self.data[index2] = temp
    
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i
         as the root
        Assume that everything in the subtree other than possibly the root 
        satisfies the heap property
        '''
        left_child = self.get_leftmostchild_index(i)
        while((self.size() > left_child) and left_child!=None):
            child_index = self.get_top_child(i)
            if(self.cmp_function(self.data[child_index], self.data[i])==-1 \
               and self.min_top==True):
                self.swap(i, child_index)
                i = child_index
            elif(self.cmp_function(self.data[child_index], self.data[i])==1 \
                 and self.min_top==False):
                self.swap(i, child_index)
                i = child_index
            else:
                break
            left_child = self.get_leftmostchild_index(i)
            
    def restore_heap(self, i):
        '''
        Restore the heap property for data assuming that it has been 
        'corrupted' at index i
        The rest of data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree.
         If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        i += 1
        self.heapify()
        
    def heapify(self):
        '''
        Rearrange data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last
        element(ii) Restore the heap property for subtree rooted at at every 
        node starting from the last non-leaf node upto the root
        '''
        if self.size()!=0:
            index = self.get_parent_index(self.size()-1)
            higher_parent = self.get_parent_index(index)
            while(index!=None):
                if (higher_parent==None):
                    self.restore_subtree(0)
                else:
                    initial_child = self.get_leftmostchild_index(higher_parent)
                    final_child = self.get_rightmostchild_index(higher_parent)
                    for parent in range(initial_child, final_child+1):
                        if parent < self.size():
                            self.restore_subtree(parent)
                index = higher_parent
                if(index!=None):
                    higher_parent = self.get_parent_index(index)
        
        
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. 
        (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        self.data[i], self.data[-1] = self.data[-1], self.data[i]
        k = self.data.pop(-1)
        self.restore_heap(0)
        return k
    
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
        self.heapify()
    
    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to data
        Make sure this does not modify the input list 'lst'
        '''
        self.data = lst[:]
        # Other methods will be the same as the functions in the modheap module
        # add them here as methods of the Heap class

if __name__ == '__main__':
    pass