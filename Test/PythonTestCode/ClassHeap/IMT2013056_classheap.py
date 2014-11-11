'''
Created on 22-Oct-2013

@author: Ujjwal
'''
class Heap(object):
    '''
    Heap class
    The methods specific to the class implementation are added here - the rest will be the same as the
    functions in the modheap module
    '''
    min_top = False
    exp2 = 1
    cmp_function = None
    data = []
    
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
        if(index1 >= 0 and index2 >= 0):
            if(self.cmp_function(self.data[index1], self.data[index2]) != 1 and self.min_top == True):
                return True
            elif(self.cmp_function(self.data[index1], self.data[index2]) != -1 and self.min_top == False):
                return True
            

                
    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        # Your code
        self.data[i] = val


    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class
    '''

'''
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
        return 2 ** self.exp2
        
        
        
    def get_item_at(self, i):
        '''
        Return the i-th element of the data list (DATA)
        '''
        if(i < self.size()-1):
            return self.data[i]
    
    
    def get_parent_index(self, child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your code
        parent_in = (child_index-1) >> self.exp2
        if (parent_in >= 0):
            return parent_in
        else : 
            return None
    
    
    def get_leftmostchild_index(self, parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        
        
        if((((self.arity()) * (parent_index)) + 1 )< self.size()):
            return ((self.arity()) * (parent_index)) + 1
        return None
    
    
    def get_rightmostchild_index(self, parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        rightmostchild_index = ((self.arity()) * parent_index) + (self.arity())
        
        if((self.get_leftmostchild_index(parent_index) == None)):
            return None
        elif(((self.arity()) * parent_index) + (self.arity()) >= self.size()):
            l_var = 1
            while(self.data[((self.arity()) * parent_index) + l_var] != self.data[-1]):
                l_var += 1
            return ((self.arity()) * parent_index) + l_var
            
        else:
            return rightmostchild_index
    
    
    def get_top_child(self, parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        if(self.min_top == True):
            m_var = 1
            count = 0
            while((self.size() > ((self.arity() * parent_index) + m_var))):
                count += 1
                m_var += 1
            if(count > 1):
                minn = self.data[self.arity() * (parent_index) + 1]
                minn1 = self.arity() * (parent_index) + 1
                i_var = 2
                if(((self.arity() * (parent_index)) + i_var) < self.size()):
                    while(i_var <= self.arity()):
                        if(self.data[((self.arity() * (parent_index)) + i_var)] <= minn):
                            minn = self.data[(self.arity() * (parent_index)) + i_var]
                            minn1 = (self.arity() * (parent_index)) + i_var
                        i_var += 1
                    return minn1
                else:
                    return None
                
            elif(count == 1):
                minn = self.arity() * (parent_index) + 1
                return minn
            elif(count == 0):
                return None
        
        else:
            m_var = 1
            count = 0
            while((self.size() > ((self.arity() * parent_index) + m_var))):
                count += 1
                m_var += 1
            if(count > 1):
                minn = self.data[self.arity() * (parent_index) + 1]
                minn1 = self.arity() * (parent_index) + 1
                i_var = 2
                if(((self.arity() * (parent_index)) + i_var) < self.size()):
                    while(i_var <= self.arity()):
                        if(self.data[((self.arity() * (parent_index)) + i_var)] >= minn):
                            minn = self.data[(self.arity() * (parent_index)) + i_var]
                            minn1 = (self.arity() * (parent_index)) + i_var
                        i_var += 1
                    return minn1
                else:
                    return None
                
            elif(count == 1):
                minn = self.arity() * (parent_index) + 1
                return minn
            elif(count == 0):
                return None            
    
    
    def restore_subtree(self, i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        self.heapify()
     
    def restore_heap(self, i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        parent = self.get_parent_index(i)
        flag = 0
        if parent != None:
            while(self.is_favoured(i, parent)):
                flag = 1
                self.data[i], self.data[parent] = self.data[parent], self.data[i]
                i = parent
                parent = self.get_parent_index(i)
                if(parent == None):
                    break
            while(self.is_favoured(i, parent)):
                flag = 1
                self.data[i], self.data[parent] = self.data[parent], self.data[i]
                i = parent
                parent = self.get_parent_index(i)
                if(parent == None):                    
                    break
        if(flag == 0):
            self.restore_subtree(i)
     
        'self.heapify()'    
    
    
    def heapify(self, ):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        import random
        global data
    
        if(self.min_top == True):
            def minm(list1):
                min1 = list1[0]
                for j in list1:
                    if(j < min1):
                        min1 = j
                return min1
    
            sample = []
            result = []
            if(len(self.data) != 0):
                result.append(minm(self.data))
            else:
                return
            noe = len(self.data)
            d_var = 1
        
            while(d_var < noe and len(self.data) != 0):
                x_var = 1
                while(2**d_var >= x_var and len(self.data) != 0):
                    self.data.remove(minm(self.data))
                    if(len(self.data)):
                        sample.append(minm(self.data))
                    x_var += 1
                i = 1
            
                while(2**d_var >= i and len(sample) != 0):
                    random_int = random.choice(sample)
                    sample.remove(random_int)
                    result.append(random_int)
                    i += 1
                d_var += 1
            self.data = []
            for i in result:
                self.data.append(i)
        
        else:
            def maxx(list2):
                max1 = list2[0]
            
                for j in list2:
                    if(j > max1):
                        max1 = j
            
                return max1
            
            sample = []
            result = []
            if(len(self.data) != 0):
                result.append(maxx(self.data))
            else:
                return
            noe = len(self.data)
            d_var = 1
            
            while(d_var < noe and len(self.data) != 0):
                x_var = 1
                while(2**d_var >= x_var and len(self.data) != 0):
                    self.data.remove(maxx(self.data))
                    if(len(self.data)):
                        sample.append(maxx(self.data))
                    x_var += 1
                i = 1
                
                while(2**d_var >= i and len(sample) != 0):
                    random_int = random.choice(sample)
                    sample.remove(random_int)
                    result.append(random_int)
                    i += 1
                d_var += 1
            self.data = []
            for i in result:
                self.data.append(i)
            
            
    def remove(self, i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        global data
        if i == 0 : 
            self.data[i], self.data[-1] = self.data[-1], self.data[i]
            k = self.data[-1]
            self.data = self.data[:-1]
            self.heapify()
            return k
        
    
    
    def pop(self,):
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
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        global data
        self.data = lst[:]
        
    
    
    def clear(self, ):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        # Your code
        
        while(len(self.data) != 0):
            self.data.remove()
            
if __name__ == '__main__':
    pass
