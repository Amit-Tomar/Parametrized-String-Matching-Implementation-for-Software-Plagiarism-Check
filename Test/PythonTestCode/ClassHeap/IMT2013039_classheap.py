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
        Set the i-th element of the data to the value 'val'
        '''
        # Your code
        

    


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
        return 2<<self.exp2-1
        
        
    def get_item_at(self,i):
        '''
        Return the i-th element of the data list (self.data)
        '''
        self.data
        return self.data[i]
    
    
    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your code
        if child_index==0:
            return None
        else:
            return child_index >> self.exp2
    
    
    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        right_mostchild=self.get_rightmostchild_index(parent_index)
        if(right_mostchild==None):
            return None
        left_mostchild = self.arity()*parent_index+1
        if (left_mostchild <= len(self.data)-1):
            return left_mostchild
        else :
            return None
    
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        right_mostchild = self.arity()*parent_index + self.arity()
        left_mostchild = self.arity()*parent_index + 1
        if (right_mostchild <= len(self.data)-1):
            return right_mostchild
        elif (right_mostchild - left_mostchild < self.arity()):
            return len(self.data)-1
    
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        var = []
        child_left = self.arity()*parent_index + 1
        child_right = self.arity()*parent_index + self.arity()+1
        if(child_right > self.size()):  
            var = var + self.data[child_left:]  
        else:
            var = var + self.data[child_left:child_right]
        if(child_left >= self.size()):
            return None
        
        
        if(self.min_top== False):
            value = max(var)
            a = var.index(value)
            return a+self.get_leftmostchild_index(parent_index)
        else:
            value = min(var)
            a = var.index(value)
            return a+self.get_leftmostchild_index(parent_index)
                  
           
    def restore_subtree(self,i):
       
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        if (self.min_top == True):
            if (i < len(self.data) and i< self.get_top_child(i)):
                if (self.data[self.get_top_child(i)] < self.data[i]):
                    index = self.get_top_child(i)
                    self.data[index],self.data[i] = self.data[i],self.data[index]
                    self.restore_subtree(index)
                
            else :
                return None   
            
        elif (self.min_top == False):
            if (i < len(self.data) and i< self.get_top_child(i)):
                if (self.data[self.get_top_child(i)] > self.data[i]):
                    index = self.get_top_child(i)
                    self.data[self.get_top_child(i)],self.data[i] = self.data[i],self.data[self.get_top_child(i)]
                    self.restore_subtree(index)
               
            else :
                return None
                
    def restore_heap(self,i):
        '''
        Restore the heap property for self.data assuming that it has been 'corrupted' at index i
        The rest of self.data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        k=self.get_parent_index((len(self.data))-1)
        while(k>=0):
            self.restore_subtree(k)
            k=k-1
            
    def heapify(self):
        '''
        Rearrange self.data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        k=self.get_parent_index((len(self.data))-1)
        while(k>=0):
            self.restore_subtree(k)
            k=k-1
                 
     
    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        self.data[i],self.data[len(self.data)-1] = self.data[len(self.data)-1],self.data[i] 
        self.data = self.data.reverse()
        self.data = self.data.pop()
        self.data = self.data.reverse()
        return self.restore_heap(i)
         
     
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        self.data[0],self.data[len(self.data)-1]=self.data[len(self.data)-1],self.data[0]
        a=self.data.pop()
        self.heapify()
        return a
     
    
     
    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data.append(obj)
        self.heapify()
     
     
    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to self.data
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        for i in lst:
            self.data.append(i)
            
        return self.data
     
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        # Your code
        Empty = []
        Heap = Empty
        return Heap
    if __name__ == '__main__':
        pass
   
    
        # Other methods will be the same as the functions in the modheap module -
        # add them here as methods of the Heap class
    
    