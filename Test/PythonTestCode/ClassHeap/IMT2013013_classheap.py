'''
Created on Oct 31, 2013

@author: imt2013013
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
        
            if self.min_top:
                if self.data[index1]<=self.data[index2]:
                    return 1
                else:
                    return -1
            else:
                if self.data[index1]>=self.data[index2]:
                    return 1
                else:
                    return -1
    
    
    def set_item_at(self, i, val):
            '''
            Set the i-th element of the data to the value 'val'
            '''
            # Your code
            self.data[i] = val
            
    
    
    def initialize_heap(self,is_min = True, arity_exp = 1, compare_fn = None):
        self.min_top = is_min
        self.cmp_function = compare_fn
        self.exp2 = arity_exp
        self.data = []
    
    
    def size(self):
        '''#
        Return the size of the heap
        '''
        return len(self.data)
    
    
    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        arity=2**self.exp2
        return arity
       
       
    def get_item_at(self,i):
        '''
        Return the i-th element of the data list (data)
        '''
        if(i >= self.size()):
            return None
        else:
            return self.data[i]
    
    
    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        if(child_index <= 0 or child_index > self.size()):
            return None
        else:
            return ((child_index-1) >> self.exp2)
    
    
    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        #if(min_top):
        if (parent_index is None):
            return None
        else:
            if((parent_index << self.exp2)+1 >= self.size()):
                return None
            else:
                return (parent_index << self.exp2)+1

       
    
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        if(parent_index is None or self.get_leftmostchild_index is None):
            return None
        elif (((parent_index) << self.exp2) + self.arity()) <= (self.size()-1):
            return ((parent_index << self.exp2) + self.arity())
        else:
            return self.size()-1
    
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        a=self.get_leftmostchild_index(parent_index)
        b=self.get_rightmostchild_index(parent_index)
        minx=a
        maxx=a
        if a is None:
            return None
        else:
            if(self.min_top):
                for x in range(a,b+1):
                    if(self.cmp_function(self.data[minx],self.data[x]) is 1):
                        minx=x
                return minx
            else:
                for y in range(a,b+1):
                    if(self.cmp_function(self.data[maxx],self.data[y] is -1)):
                        maxx=y
                return maxx
              
    
    def restore_subtree(self,i):
        
        ''' Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property'''
        
        a=self.get_leftmostchild_index(i)
        b=self.get_top_child(i)
        #if a is None:
        #   return None
        #else:
        if(self.min_top):
                while(a is not None and i is not None and b is not None):
                    if(self.cmp_function(self.data[i],self.data[b] is 1)):
                        self.data[b],self.data[i]=self.data[i],self.data[b]
                        i=b
                        a=self.get_leftmostchild_index(i)
                        b=self.get_top_child(i)
                    else:
                        break
        else:
                while(a is not None and i is not None and b is not None):
                    if(self.cmp_function(self.data[i],self.data[b] is -1)):
                        self.data[b],self.data[i]=self.data[i],self.data[b]
                        i=b
                        a=self.get_leftmostchild_index(i)
                        b=self.get_top_child(i)
                    else:
                        break
           
    def restore_heap(self,i):
        
        '''Restore the heap property for data assuming that it has been 'corrupted' at index i
        The rest of data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element
        '''
        p=self.get_parent_index(i)
        if self.min_top:
            if p is not None and i is not None and (self.cmp_function(self.data[p],self.data[i]) is 1):
                while(p>0 and self.cmp_function(self.data[p],self.data[i] is 1)):
                    self.data[i],self.data[p]=self.data[p],self.data[i]
                    i=p
                    p=self.get_parent_index(i)
            else:
                self.restore_subtree(i)
        else:
            if p is not None and i is not None and (self.cmp_function(self.data[p],self.data[i]) is -1):
                while(p>0 and self.cmp_function(self.data[p],self.data[i]) is -1):
                    self.data[i],self.data[p]=self.data[p],self.data[i]
                    i=p
                    p=self.get_parent_index(i)
            else:
                self.restore_subtree(i)
       
               
    def heapify(self):
        '''
        Rearrange data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
    
        a=self.get_parent_index(len(self.data)-1)
        while(a>=0):
            self.restore_subtree(a)
            a=a-1
        
    
    
    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        #a=len(self.data)-1
        c = self.data[i]
        self.data[-1],self.data[i]=self.data[i],self.data[-1]
        del self.data[-1]
        self.heapify()
        return c
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        return self.remove(0)
       
    
    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        self.data.append(obj)
        #i=self.data.index(obj)
        #self.restore_heap(i)
        self.heapify()
        
    
    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to data
        Make sure this does not modify the input list 'lst'
        '''
        
        for i in range(0,len(lst)):
            self.data.append(lst[i])
    
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        self.data=[]
    
    if __name__ == '__main__':
        #initialize_heap()
        #print get_rightmostchild_index(2)
        #print restore_heap(2)
        #print data
        #print get_top_child(1)
        #print get_leftmostchild_index(2)
        #print data
        pass