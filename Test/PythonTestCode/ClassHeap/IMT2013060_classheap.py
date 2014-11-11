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
        The Python convention is to have upper case name for  variables - that's why the s
        in modheap were named in all caps
        Unlike the s in heap module --- name the attributes as lower case variable names
        '''
        # Your code
        self.min_top = is_min
        self.cmp_function = compare_fn
        self.exp2 = arity_exp
        self.data = []

    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a self.data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        # Your code
        if(self.min_top==True and self.data[index1] <= self.data[index2]):
            return True
        if(self.min_top==False and self.data[index1] >= self.data[index2]):
            return True
        


    def set_item_at(self, i, val):
        '''
        Set the i-th element of the self.data to the value 'val'
        '''
        # Your code
        
    def size(self):
        '''
        Return the size of the heap
        '''
        
        return len(self.data)
        # Your code
    
    
    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        return 2<<(self.exp2-1)
        # Your code
        
        
        
    def get_item_at(self,i):
        '''
        Return the i-th element of the self.data list (self.data)
        '''
        self.data
        return self.data[i]
    
    
    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        self.data
        if child_index==0:
            return None
        else:
            
            return (child_index-1)/self.arity()
        # Your code
    
    
    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        self.data
        if (self.arity()*parent_index)+1<len(self.data):
            return (self.arity()*parent_index)+1
        # Your code
    
    
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        self.data
        if self.get_leftmostchild_index(parent_index)!=None:
            if (self.arity()*parent_index)+self.arity()<len(self.data):
                return (self.arity()*parent_index)+self.arity()
            else:
                return len(self.data)-1
        # Your code
    
    
    
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        self.data
        if self.get_leftmostchild_index(parent_index)!=None:
            new=self.data[self.get_leftmostchild_index(parent_index):self.get_rightmostchild_index(parent_index)+1]
            if self.min_top==False:
                return self.get_leftmostchild_index(parent_index)+new.index(max(new))
            else: 
                return self.get_leftmostchild_index(parent_index)+new.index(min(new))
        
        # Your code
    
    
    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        self.data
        if self.min_top==False:
            if self.get_leftmostchild_index(i)!=None and i<self.size():
                temp = self.get_top_child(i)
                if self.data[temp]>self.data[i] and temp!=None:
                    self.data[temp],self.data[i]=self.data[i],self.data[temp]
                    self.restore_subtree(temp)
            
        else:
            if self.get_leftmostchild_index(i)!=None and i<self.size():
                temp = self.get_top_child(i)
                if self.data[temp]<self.data[i] and temp!=None:
                    self.data[temp],self.data[i]=self.data[i],self.data[temp]
                    self.restore_subtree(temp)
            
        # Your code
            
        # Your code
    
        
    def restore_heap(self,i):
        '''
        Restore the heap property for self.data assuming that it has been 'corrupted' at index i
        The rest of self.data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        self.data
        if self.min_top==False:
            if self.get_parent_index(i)!=None:
                if self.data[self.get_parent_index(i)]<self.data[i]:
                    self.data[self.get_parent_index(i)],self.data[i]=self.data[i],self.data[self.get_parent_index(i)]
                    self.restore_subtree(i)
                    self.restore_heap(self.get_parent_index(i))
                    
                else:
                    self.restore_subtree(i)
        if self.min_top==True:
            if self.get_parent_index(i)!=None:
                if self.data[self.get_parent_index(i)]>self.data[i]:
                    self.data[self.get_parent_index(i)],self.data[i]=self.data[i],self.data[self.get_parent_index(i)]
                    self.restore_subtree(i)
                    self.restore_heap(self.get_parent_index(i))
                else:
                    self.restore_subtree(i)
                    
                
        # Your code
    
    
    def heapify(self):
        '''
        Rearrange self.data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        self.min_top
        self.exp2
        if self.min_top==True or self.min_top==False:
            self.data
            temp1=self.get_parent_index(len(self.data)-1)
            while(temp1>=0):
                self.restore_subtree(temp1)
                temp1=temp1-1
            
            
        
        
        # Your code
    
    
    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        self.data
        self.data[i],self.data[len(self.data)-1]=self.data[len(self.data)-1],self.data[i]
        
        self.data.pop()
        self.heapify()
        
        
        # Your code
    
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
    
        
        self.heapify()
        a=self.data[0]
        del self.data[0]
        if self.size()>1:
            self.heapify()
        return a
        
        # Your code
    
    
    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        self.data
        self.data.append(obj)
        return self.data
        # Your code
    
    
    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to self.data
        Make sure this does not modify the input list 'lst'
        '''
        self.data
        for element in lst:
            self.data.append(element)
        return self.data
        
        # Your code
    
    
    def clear(self):
        '''
        Clear the self.data in the heap - initialize to empty list
        '''
        self.data
        '''for i in range (0,len(self.data)-1):
            self.data.pop()'''
        self.data = []
        return self.data
        
        # Your code
    if __name__ == '__main__':
        pass