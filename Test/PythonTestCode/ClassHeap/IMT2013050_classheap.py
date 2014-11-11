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
        if(self.min_top == True):
            
            if(self.data[index1] <= self.data[index2]):
                return True
        else :
            
            if(self.data[index1] >= self.data[index2]):
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
        return len(self.data)
    
    
    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        return 2 << (self.exp2 - 1)
    
        
        
    def get_item_at(self , i):
        '''
        Return the i-th element of the data list (DATA)
        '''
        return self.data[i]
    
    
    
    def get_parent_index(self , child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        if(child_index != 0):
            return (child_index - 1) >> self.exp2
        else:
            return None
        
        
    
    def get_leftmostchild_index(self , parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        
        leftmostchild_index = (parent_index << self.exp2) + 1
        
        if(self.size() > leftmostchild_index):
            return leftmostchild_index
        else:
            return None
        
            
            
    def get_rightmostchild_index(self , parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        
        if(self.get_leftmostchild_index(parent_index) == None):
            return None
        
        sum1 = (parent_index << self.exp2)
        sum2 = 2 << (self.exp2 - 1)
        rightmost_index = sum1 + sum2
        
        total_sum = self.size() - self.get_leftmostchild_index(parent_index)
        
        if(total_sum < self.arity()):
            return (self.get_leftmostchild_index(parent_index) - 1) + total_sum
        
        if(rightmost_index == self.get_leftmostchild_index(parent_index)):
            return None
        
        if(self.size() > rightmost_index):
            return rightmost_index
        else:
            return None
    
    
    def get_top_child(self , parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        rcindex = self.get_rightmostchild_index(parent_index)
        list_children = []
        dict_children = {}
        lcindex = self.get_leftmostchild_index(parent_index)
        
        if(lcindex == None):
            return None
        
        if(rcindex == None):
            final_rcindex = lcindex
        else:
            final_rcindex = rcindex
        
        for i in range(lcindex , final_rcindex + 1):
            dict_children[self.data[i]] = i
            list_children.append(self.data[i])
        
        if(self.min_top == True):
            minimum = min(list_children)
            favourable_index = dict_children[minimum]
        else:
            maximum = max(list_children)
            favourable_index = dict_children[maximum]
        
        return favourable_index
                
                
                
                
    def restore_subtree(self , i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        
        flag = 1
        index_child = self.get_top_child(i)
        
        if(self.min_top == True and index_child != None):
            minimum = self.data[index_child]
            if(minimum < self.data[i]):
                flag = 0
                
        elif(index_child != None):
            maximum = self.data[index_child]
            if(maximum > self.data[i]):
                flag = 0
        
        if(flag == 0):
            self.data[i], self.data[index_child] = self.data[index_child], self.data[i] 
            
            if(self.get_leftmostchild_index(index_child) != None):
                self.restore_subtree(index_child)
        
            
    def restore_heap(self , i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        org_parent = i
        pindex = self.get_parent_index(i)
        
        if(self.min_top == True):
            flag = 1
            
            if(pindex == None):
                flag = 0
            
            if(flag == 1):
                
                while(self.data[pindex] > self.data[i]):
    
                    self.data[pindex] , self.data[i] = self.data[i] , self.data[pindex]
                    i = pindex
                    pindex = self.get_parent_index(pindex)
                    
                    if(pindex == None):
                        break
                    
        self.restore_subtree(org_parent)
            
                
                
                
    def heapify(self):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
    
        pindex = self.get_parent_index(self.size() - 1)
        while(pindex >= 0):
            self.restore_subtree(pindex)
            pindex = pindex - 1
            
        
    def remove(self , i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
    
        self.data[self.size() - 1] , self.data[i] = self.data[i] , self.data[self.size() - 1]
        
        self.data.pop()
        if(i != self.size()):
            self.restore_subtree(i)
    
    
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        first_ele = self.data[0]
        self.remove(0)
        return first_ele
    
    
    
    def add(self , obj):
        '''
        Add an object 'obj' to the heap
        '''
    
        self.data.append(obj)
        self.heapify()
    
    
    
    def import_list(self , lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
       
        i = 0
        while(i < len(lst)):
            self.data.append(lst[i])
            i = i + 1
        
        
        
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        self.data = []
    

    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

if __name__ == '__main__':
    pass