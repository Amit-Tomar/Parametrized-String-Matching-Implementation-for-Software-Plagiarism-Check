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
        self.exp2 = arity_exp
        self.cmp_function = compare_fn
        self.data = []
    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        if self.min_top:
            if self.data[index1] >= self.data[index2]:
                return 1
            else:
                return -1
        else:
            if self.data[index1] <= self.data[index2]:
                return 1
            else:
                return -1


    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        self.data[i] = val


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
    
        pIndex = (child_index - 1) >> self.exp2
        if child_index == 0:
            return None
        else:
            return pIndex
    
    def get_leftmostchild_index(self, parent_index):
    
        '''
    
        Return the index of the leftmost child of the element at parent_index
    
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
    
        '''
    
        lcIndex = (parent_index << self.exp2) + 1
        if lcIndex < self.size():
            return lcIndex
        else:
            return None
        
    def get_rightmostchild_index(self, parent_index):
    
        '''
    
        Return the index of the rightmost child of the element at parent_index
    
        Should return None if the parent has no child
    
        '''
    
        rcIndex = (parent_index + 1) << self.exp2
        if (parent_index << self.exp2) + 1 > self.size() - 1:
            return None
        elif rcIndex > (self.size() - 1):
            return self.size() - 1
        else:
            return rcIndex
    
    def get_top_child(self, parent_index):
    
        '''
    
        Return the index of the child which is most favoured to move up the tree among all the children of the
    
        element at parent_index
    
        '''
        topIndex = self.get_leftmostchild_index(parent_index)
        for i in range(topIndex , ((parent_index + 1) << self.exp2) + 1):
            if self.min_top:
                if self.cmp_function(self.data[i] , self.data[topIndex]) == -1:
                    topIndex = i
            else: 
                if self.cmp_function(self.data[i] , self.data[topIndex]) == 1:
                    topIndex = i
        return topIndex
    
    
    def restore_subtree(self, i):
        
        '''
    
        Restore the heap property for the subtree with the element at index i as the root
    
        Assume that everything in the subtree other than possibly the root satisfies the heap property
    
        '''
        
        while(self.get_rightmostchild_index(i) is not None):
            if self.get_rightmostchild_index( i) is None:
                break
            minchildIndex = self.get_leftmostchild_index( i)
            maxchildIndex = self.get_leftmostchild_index(i)
            for j in range(self.get_leftmostchild_index(i) , self.get_rightmostchild_index(i) + 1):
                if self.cmp_function(self.data[j] , self.data[minchildIndex]) == -1:
                    minchildIndex = j
                if self.cmp_function(self.data[j] , self.data[maxchildIndex]) == 1:
                    maxchildIndex = j   
            if self.min_top:
                if self.cmp_function(self.data[i] , self.data[minchildIndex]) == 1:
                    self.data[i] , self.data[minchildIndex] = self.data[minchildIndex] , self.data[i]
                    i = minchildIndex
                else:
                    break
            else:
                if self.cmp_function(self.data[i] , self.data[maxchildIndex]) == -1:
                    self.data[i] , self.data[maxchildIndex] = self.data[maxchildIndex] , self.data[i]
                    i = maxchildIndex
                else:
                    break
        
        
    def restore_heap(self, i):
    
        '''
    
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
    
        The rest of DATA is assumed to already satisfy the heap property
    
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
    
        Continue this till you do not need to move up anymore.
    
        (ii) If it has not moved up, then fix the subtree below this element
    
        '''
        
        if self.min_top:

            if (self.get_parent_index(i) != None and self.cmp_function(self.data[self.get_parent_index(i)],self.data[i])==1):

                while (self.cmp_function(self.data[self.get_parent_index(i)],self.data[i])==1 and self.get_parent_index(i)>0):
                    
                    self.data[self.get_parent_index(i)],self.data[i]= self.data[i],self.data[self.get_parent_index(i)]

                    i=self.get_parent_index(i)

            else:

                self.restore_subtree(i)

        else:

            if (self.get_parent_index(i) != None and self.data[self.get_parent_index(i)]< self.data[i]):

                while (self.cmp_function(self.data[self.get_parent_index(i)],self.data[i])==-1 and self.get_parent_index(i)>0):

                    self.data[self.get_parent_index(i)],self.data[i]=self.data[i],self.data[self.get_parent_index(i)]

                    i=self.get_parent_index(i)

            

            else:

                self.restore_subtree(i)            

            
    def heapify(self):
    
        '''
    
        Rearrange DATA into a heap
    
        Algo: (i) Start from the first nonleaf node - the parent of the last element
    
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
    
        '''
    
        parentIndex = self.get_parent_index(self.size() - 1)
        while(parentIndex >= 0):
            self.restore_subtree(parentIndex)
            parentIndex = parentIndex - 1
            
    def remove(self,i):
    
        '''
        Remove an element (at index i) from the heap
    
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
    
        (c) Restore the heap starting from i
        '''
        self.data[i] , self.data[-1] = self.data[-1] , self.data[i]
        self.data.pop()
        self.restore_subtree(i)
    
    def pop(self):
    
        '''
        Pull the top element out of the heap
        '''
        top = self.data[0]
        self.remove(0)
        return top
    
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
        self.heapify()
    
    def clear(self):
    
        '''
        Clear the data in the heap - initialize to empty list
        '''
        self.data = []

if __name__ == '__main__':

    pass