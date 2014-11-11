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
        min_top = is_min
        cmp_function = compare_fn
        exp2 = arity_exp
        data = []
        # Your code

    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        # Your code


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
        return self.len(self.data)
    
    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        # Your code
        return 2**self.exp2
        
        
    def get_item_at(self,i):
        '''
        Return the i-th element of the data list (data)
        '''
        return self.data[i]

    def get_parent_index(self,child_index):
    
    # Your code
        if child_index == 0: 
            return None
        return child_index-1 >> self.exp2

    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        if parent_index == None: return None
        elif parent_index == 0 :return 1
        elif self.size() - parent_index <= self.arity() or (parent_index << self.exp2) + 1 > self.size()-1: return None
        else: return (parent_index << self.exp2) + 1 
    
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        lchild = self.get_leftmostchild_index(parent_index)
        
        if (lchild == None): return None
        elif lchild == self.size()-1 : return lchild
        elif self.size() - lchild < self.arity(): return self.size()-1
        else: return lchild + self.arity()-1
       
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        
        child_index = self.get_leftmostchild_index(parent_index)
        top_child_index = child_index
        rchild_ind = self.get_rightmostchild_index(parent_index)
        
        if(self.min_top != True):
            
            if child_index != None:
                while(child_index <= rchild_ind):
                    if(self.cmp_function(self.data[top_child_index],self.data[child_index]) == -1):
                        top_child_index = child_index
                    child_index = child_index + 1 
                
    #            if(data[top_child_index] > data[parent_index]):
                return top_child_index
            return None
        
        else:
            if child_index != None : 
                while(child_index <= rchild_ind):
                    if(self.cmp_function(self.data[top_child_index],self.data[child_index]) == 1):
                        top_child_index = child_index
                    child_index = child_index + 1
            
    #           if(data[top_child_index] < data[parent_index]):
                return top_child_index
        #return None
    
    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        top_child_index = self.get_top_child(i)
        if self.min_top == False:
            while(top_child_index != None and self.cmp_function(self.data[top_child_index],self.data[i]) == 1):
                self.data[top_child_index],self.data[i] = self.data[i],self.data[top_child_index]
                i = top_child_index
                top_child_index = self.get_top_child(i)
        else:
            while(top_child_index != None and self.cmp_function(self.data[top_child_index],self.data[i]) == -1):
                self.data[top_child_index],self.data[i] = self.data[i],self.data[top_child_index]
                i = top_child_index
                top_child_index = self.get_top_child(i)   
                               
    def restore_heap(self,i):
        '''
        Restore the heap property for data assuming that it has been 'corrupted' at index i
        The rest of data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code   
        initial = i
        count = 0
        if(self.min_top == False):
            parent_ind = self.get_parent_index(i)
            while(parent_ind != None and self.cmp_function(self.data[i],self.data[parent_ind]) == 1 ):
                self.data[i],self.data[parent_ind] = self.data[parent_ind],self.data[i]
                parent_ind = self.get_parent_index(parent_ind)
                i = self.get_top_child(parent_ind)
                count += 1
                
        else:
            parent_ind = self.get_parent_index(i)
            while(parent_ind != None and self.cmp_function(self.data[i],self.data[parent_ind]) == -1):
                self.data[i],self.data[parent_ind] = self.data[parent_ind],self.data[i]
                parent_ind = self.get_parent_index(parent_ind)
                i = self.get_top_child(parent_ind)
                count += 1
        
        if count == 0:
            self.restore_subtree(initial)
    
    def heapify(self):
        '''
        Rearrange data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        ind = self.get_parent_index(self.size()-1)
        
        while (ind  >= 0):
            self.restore_subtree(ind)
            ind = ind - 1
            
    
    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        self.data[i],self.data[-1] = self.data[-1],self.data[i]
        element = self.data[self.size()-1] 
        self.data = self.data[:-1]
        self.restore_heap(i)
        return element
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        element = self.data.pop(0)
        self.heapify()
        return element
        
    
    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data.append(obj)
        self.heapify()
    
    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to data
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        self.data.extend(lst)
        self.heapify()    
    
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        # Your code
        self.data=[]
if __name__ == '__main__':
    pass
