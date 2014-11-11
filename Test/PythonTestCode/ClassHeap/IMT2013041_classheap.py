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
    
    def __init__(self, is_min = True, arity_exp = 1, compare_fn = None):
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
        In other words a heap is a self.data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        # Your code
        if self.min_top == True:
            if self.get_item_at(index1) > self.get_item_at(index2):
                return False
            else:
                return True
        else:
            if self.get_item_at(index1) < self.get_item_at(index2):
                return False
            else:
                return True
        

    def set_item_at(self, i, val):
        '''
        Set the i-th element of the self.data to the value 'val'
        '''
        # Your code
        self.data[i] = val

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
        return 2 >> (self.exp2 - 1)
        
        
    def get_item_at(self, i):
        '''
        Return the i-th element of the self.data list (self.data)
        '''
        if i >= self.size():
            if self.size() > 0:
                return self.data[self.size() - 1]
            else:
                return None
        if i == None:
            return None
        return self.data[i]
    
    def swap(self, index_1, index_2):
        '''
        Swaps the elements at given indices
        '''
        
        temp = self.data[index_1]
        self.data[index_1] = self.data[index_2]
        self.data[index_2] = temp
    
    
    def get_parent_index(self, child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your code
        if child_index <= 0:
            return None
        return (child_index - 1) >> self.exp2
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        if parent_index == None:
            return 0
        elif ((parent_index << self.exp2) + 1) < self.size():
            return (parent_index << self.exp2) + 1
        else:
            return None
    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        start_index = self.get_leftmostchild_index(parent_index) 
        if start_index == None:
            return None
        else:
            end_index = (parent_index + 1) << self.exp2
            while(end_index >= start_index):
                if end_index < self.size():
                    return end_index
                end_index -= 1
                
    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favored to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code 
        temp_list = []
        start_index = self.get_leftmostchild_index(parent_index) 
        end_index = self.get_rightmostchild_index(parent_index)
        if(start_index == None):
            return None
        if start_index != None and end_index != None:
            for i in range (start_index, end_index + 1):
                temp_list.append(self.data[i])
        
        min_num = temp_list[0]
        max_num = temp_list[0]
        count = -1
        loc_min = loc_max = start_index
        for i in temp_list:
            count += 1
            if i < min_num:
                loc_min = start_index
                min_num = i
                loc_min += count
            if i > max_num:
                loc_max = start_index
                max_num = i
                loc_max += count  
                
        if self.min_top == False:
            return loc_max
        else:
            return loc_min
                
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code\
        parent_index = i
        if( parent_index == None ):
            return None
        top_child_index = self.get_top_child(i)
        if self.min_top == True :
            while(self.get_item_at(i) > self.get_item_at(top_child_index) and  top_child_index!=None):
                j = top_child_index
                self.swap(i, j)
                i = j
                top_child_index = self.get_top_child(i)
                if( top_child_index == None):
                    break
                
        else:
            while(self.get_item_at(i) < self.get_item_at(top_child_index) and  top_child_index!=None):
                j = top_child_index
                self.swap(i, j)
                i = j
                top_child_index = self.get_top_child(i)
                if( top_child_index == None):
                    break
        
                                             
    def restore_heap(self, i):
        '''
        Restore the heap property for self.data assuming that it has been 'corrupted' at index i
        The rest of self.data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        flag = 0
        parent_index = self.get_parent_index(i)
        if( parent_index == None ):
            self.restore_subtree(i)
        if(self.min_top == True ):
            while(self.get_item_at(i) > self.get_item_at(parent_index) and parent_index != None):
                flag = 1
                self.swap(i, parent_index)
                i = parent_index
                parent_index = self.get_parent_index(i)
            if( flag == 0 ):
                self.restore_subtree(i)
        else:
            while(self.get_item_at(i) < self.get_item_at(parent_index) and parent_index != None):
                flag = 1
                self.swap(i, parent_index)
                i = parent_index
                parent_index = self.get_parent_index(i)
            if(flag == 0):
                self.restore_subtree(i)
    
    def heapify(self):
        '''
        Rearrange self.data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        last_child = self.size() - 1
        parent = self.get_parent_index(last_child)
        while(parent >= 0):
            self.restore_subtree(parent)
            parent -= 1
    
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        last_index = self.size() - 1
        self.swap(i, last_index)
        return_item = self.data.pop(-1)
        self.restore_heap(i)
        return return_item
    
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        return self.remove(0)
    
    def add(self, obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data.append(obj)
        self.heapify()
    
    
    def import_list(self, lst):
        '''
        Add all the elements of the list 'lst' to self.data
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        self.data = lst[:]
    
    def clear(self):
        '''
        Clear the self.data in the heap - initialize to empty list
        '''
        # Your code
        self.data = []

if __name__ == '__main__':
    pass