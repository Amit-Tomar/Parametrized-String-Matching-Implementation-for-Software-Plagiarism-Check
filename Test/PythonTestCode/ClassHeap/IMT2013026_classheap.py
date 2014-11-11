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
        self.data = []
        self.min_top = is_min
        self.exp2 = arity_exp
        self.cmp_function = compare_fn
    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        if index1 < index2:
            return -1
        elif index1 > index2:
            return 1
        else:
            return 0


    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        self.data[i] = val

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
        return 2**self.exp2
        
        
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
        parent = (child_index-1)>>self.exp2
        if parent < 0:
            return None
        else:
            return (child_index-1)>>self.exp2
    
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        child = (parent_index << self.exp2)+1
        if child > self.size()-1:
            return None
        return child
    
    
    def get_rightmostchild_index(self, parent_index): 
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        n = 1
        child = self.get_leftmostchild_index(parent_index)+1
        if child > self.size()-1:
            return None
        if child+1 > self.size()-1:
            return None
        while(n < self.arity()):
            if self.get_leftmostchild_index(parent_index)+n>self.size()-1:
                return self.get_leftmostchild_index(parent_index) + n-1
            n += 1
        return self.get_leftmostchild_index(parent_index) + n
    
    
    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        lchild = self.get_leftmostchild_index(parent_index)
        if lchild == None:
            return None
        rchild = self.get_rightmostchild_index(parent_index)
        if rchild == None:
            return lchild
        min_index = lchild
        max_index = lchild
        
        if self.min_top == True:
            min = self.data[lchild]
            for i in range(lchild, rchild):
                if self.cmp_function(self.data[i],min) == -1:
                    min = self.data[i]
                    min_index = i
            return min_index
        else:
            max = self.data[lchild]
            for i in range(lchild, rchild):
                if self.cmp_function(self.data[i],max) == 1:
                    max = self.data[i]
                    max_index = i
            return max_index
    
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        child = self.get_top_child(i)
        if child != None:
            if(self.min_top == True):
                if self.cmp_function(self.data[child], self.data[i]) == -1:
                    temp = self.data[i]
                    self.data[i] = self.data[child]
                    self.data[child] = temp
                self.restore_subtree(child)
            else:
                if self.cmp_function(self.data[child], self.data[i]) == 1:
                    temp = self.data[i]
                    self.data[i] = self.data[child]
                    self.data[child] = temp
                self.restore_subtree(child)
            
    def restore_heap(self, i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        count = 0
        n = 4
        initiali = i
        while (i > 0):  
            parent = self.get_parent_index(i)  
            if n > 0:
                if self.min_top == True:
                    if self.cmp_function(self.data[i],self.data[parent]) == -1:
                        count += 1
                        temp = self.DATA[i]
                        self.data[i] = self.data[parent]
                        self.data[i] = temp
                        i = parent
                    self.restore_subtree(i)
                else:
                    if self.cmp_function(self.data[i],self.data[parent]) == 1:
                        count += 1
                        temp = 0
                        temp = self.data[i]
                        self.data[i] = self.data[parent]
                        self.data[parent] = temp
                        i = parent
                    self.restore_subtree(i)
        if count == 0:
            self.restore_subtree(initiali)
                
    def heapify(self):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        position = self.get_parent_index(self.size()-1)
        while position >= 0:
            x = position
            self.restore_subtree(x)
            position -= 1
    
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        self.data[0] = self.data[self.size()-1]
        self.data.pop()
        self.restore_subtree(self.size()-1, self.data)
            
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        a = self.data[0]
        self.data.remove(a)
        self.heapify()
        return a
    
    def add(self, obj):
        '''
        Add an object 'obj' to the heap
        '''
        self.data.append(obj)
        self.heapify()
    
    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
        for i in lst:
            self.data.append(i)
    
    def clear(self):
        '''
        Clear the data in  the heap - initialize to empty list
        '''
        for i in self.data:
            print i
            self.data.pop()
    

if __name__ == '__main__':
    pass