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
        
        if self.min_top:
            if self.data[index2]>=self.data[index1]:
                return 1
            else:
                return -1
        else:
            if self.data[index2]<=self.data[index1]:
                return 1
            else:
                return -1# Your code


    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        # Your code
        
        self.data[i]=val
        #return self.data
    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

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
        return 2**self.exp2
    
    
    def get_item_at(self,i):
        '''
        Return the i-th element of the data list (DATA)
        '''
#     self.i=i
        return self.data[i]

    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your code
    
        if child_index==0:
            return None
        return (child_index-1)>>self.exp2

    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
    # Your code
    
        if (parent_index<<self.exp2)+1<len(self.data):
            return (parent_index<<self.exp2)+1
        return None
    
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
    # Your code
    
        if ((parent_index<<self.exp2)+1) > (len(self.data)-1):
            return None
        elif (((parent_index+1)<<self.exp2))>(len(self.data)-1):
            return len(self.data)-1
        else:
            return (parent_index+1)<<self.exp2

            
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
    # Your code
    
        minimum = (parent_index<<self.exp2)+1
        for i in range((parent_index<<self.exp2)+1, ((parent_index+1)<<self.exp2)+1):
            if self.min_top:
                if self.cmp_function(self.data[i],self.data[minimum])==-1:
                    minimum = i
            else:
                if self.cmp_function(self.data[i],self.data[minimum])==1:
                    minimum = i
            return minimum

    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
    # Your code
        pos = i
        while(self.get_rightmostchild_index(pos) is not None):
            minvar = self.get_leftmostchild_index(pos)
            maxvar = self.get_leftmostchild_index(pos)
    
            for j in range(self.get_leftmostchild_index(pos),self.get_rightmostchild_index(pos)+1):
                if self.cmp_function(self.data[j],self.data[minvar]) == -1:
                    minvar = j
                if self.cmp_function(self.data[j],self.data[maxvar]) == 1:
                    maxvar = j
            if self.min_top:
                if self.cmp_function(self.data[pos],self.data[minvar]) == 1:
                    self.data[pos],self.data[minvar] = self.data[minvar],self.data[pos]
                    minvar = pos
                else:
                    break 
            else:
                if self.cmp_function(self.data[pos],self.data[maxvar]) == -1:
                    self.data[pos],self.data[maxvar]=self.data[maxvar],self.data[pos]
                    maxvar = pos
                else:
                    break
        
    
    def restore_heap(self,i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
    # Your code
        c=i
        if self.min_top:
            if (self.get_parent_index(c) is not None and self.cmp_function(self.data[self.get_parent_index(c)],self.data[c]) ==1 ):
                while (self.cmp_function(self.data[self.get_parent_index(c)],self.data[c]) == 1 and self.get_parent_index(c)>0):
                    self.data[self.get_parent_index(c)],self.data[c]=self.data[c],self.data[self.get_parent_index(c)]
                    c=self.get_parent_index(c)
            else:
                self.restore_subtree(c)
        else:
            if (self.get_parent_index(c) is not None and self.data[self.get_parent_index(c)]<self.data[c]):
                while (self.cmp_function(self.data[self.get_parent_index(c)],self.data[c]) == -1 and self.get_parent_index(c)>0):
                    self.data[self.get_parent_index(c)],self.data[c]=self.data[c],self.data[self.get_parent_index(c)]
                    c=self.get_parent_index(c)
            
            else:
                self.restore_subtree(c)            
        

    def heapify(self):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
    # Your code
        p=self.get_parent_index(len(self.data)-1)
        while(p>-1):
            self.restore_subtree(p)
            p=p-1
    
    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
    # Your code
        c=self.data[i]
        self.heapify()
        self.data[i],self.data[-1]=self.data[-1],self.data[i]
        self.data.pop(-1)
        self.restore_subtree(i)
        return c
        
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
    # Your code
    
        c=self.data[0]
        self.remove(0)
        return c
    

    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
    # Your code
        (self.data).append(obj)
        self.heapify()



    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
    # Your code
    
        for i in lst:
            (self.data).append(i)
        self.heapify()
    

    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        self.data=[]

if __name__ == '__main__':
    pass
    
