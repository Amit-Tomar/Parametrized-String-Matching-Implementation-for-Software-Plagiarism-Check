'''
Created on 22-Oct-2013

@author: raghavan
'''
import math
class Heap(object):
    '''
    Heap class
    The methods specific to the class implementation are added here - the rest will be the same as the
    functions in the modheap module
    '''
    min_top = False
    # Says whether the heap is a Min-Heap (True) or a Max-Heap (False)

    # Comparison Function for the heap
    # Takes two elements - e1 , e1 - of the heap as arguments and retuns 1 if
    # e1 > e2 , -1 if e1 < e2 and 0 otherwise
    cmp_function = None
    
    # The arity (number of children for a parent) is taken to be 2^self.exp2
    exp2 = 1
    
    # The list of elements organized as a heap
    data = []
    
    def size(self):
        '''
        Return the size of the heap
        '''
        # Your code
        length = len(self.data)
        return length
        
    
    
    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        # Your code
        return 2**self.exp2
        
        
    def get_item_at(self , i):
        '''
        Return the i-th element of the self.data list (self.data)
        '''
        return self.data[i]
    
    
    def get_parent_index(self , child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m , in python)
        '''
        # Your code
        arit = self.arity()
        parent_index = (child_index-1)//arit
        if(parent_index >= 0):
            return parent_index
        else:
            return None
    
    def get_leftmostchild_index(self , parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m , in python)
        '''
        # Your code
        r_child = self.get_rightmostchild_index(parent_index)
        if(r_child == None):
            return None
        arit = self.arity()
        size = len(self.data)
        l_child = (arit*parent_index)+1
        if(l_child<size):
            return l_child
        else:
            return None
    
    def get_rightmostchild_index(self , parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        arit = self.arity()
        size = len(self.data)
        l_child = 0
        r_child = (arit*parent_index)+1
        if(r_child<size):
            l_child = r_child
        else:
            l_child = None
        size = len(self.data)
        r_child = (arit*parent_index)+arit
        while(r_child>l_child):
            if(r_child<size):
                return r_child
            else:
                arit -= 1
                r_child = (arit*parent_index)+arit
        return None
    
    
    def get_top_child(self , parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        l_child = self.get_leftmostchild_index(parent_index)
        r_child = self.get_rightmostchild_index(parent_index)
        if(self.min_top==False):
            i = l_child
            max_val = self.data[l_child]
            max_index = l_child
            while(i <= r_child):
                if self.data[i] > max_val:
                    max_val = self.data[i]
                    max_index = i
                i += 1
            return max_index
        else:
            i = l_child
            min_val = self.data[l_child]
            min_index = l_child
            while(i <= r_child):
                if self.data[i] < min_val and self.data[i] != -1:
                    min_val = self.data[i]
                    min_index = i
                i += 1
            return min_index
        
    def restore_subtree(self , i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        self.heapify()
        
    def restore_heap(self , i):
        '''
        Restore the heap property for self.data assuming that it has been 'corrupted' at index i
        The rest of self.data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes , swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up , then fix the subtree below this element 
        '''
        # Your code
        global data , min_top
        flag = 1
        length = len(self.data)
        arit = self.arity()
        while(length>0):
            if(length == 2):
                flag = 0
                self.data.append(-1)
                break
            length -= arit
        l_child , r_child = self.get_leftmostchild_index(i) , self.get_rightmostchild_index(i)
        if(l_child != None and r_child != None):
            if(self.min_top==False):
                j = self.get_top_child(i)
                while(self.data[i]<self.data[j]):
                    self.data[i] , self.data[j] = self.data[j] , self.data[i]
                    i = j
                    l_child , r_child = self.get_leftmostchild_index(i) , self.get_rightmostchild_index(i)
                    if(l_child == None or r_child == None):
                        break
                    else:
                        j = self.get_top_child(i)
            else:
                j = self.get_top_child(i)
                while(self.data[i] > self.data[j]):
                    self.data[i] , self.data[j] = self.data[j] , self.data[i]
                    i = j
                    l_child , r_child = self.get_leftmostchild_index(i) , self.get_rightmostchild_index(i)
                    if(l_child == None or r_child == None):
                        break
                    else:
                        j = self.get_top_child(i)
                    
                
        if(flag==0):
            self.data = self.data[:len(self.data)-1]
            
    def heapify(self):
        '''
        Rearrange self.data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        length = len(self.data)-1
        arit = self.arity()
        i = int(math.floor(length/arit))
        while(i>=0):
            self.restore_heap(i)
            i -= 1
              
    def remove(self , i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        length = len(self.data)-1
        self.data[i] , self.data[length] = self.data[length] , self.data[i]
        return self.data.pop()
    
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        self.data[0] , self.data[len(self.data)-1] = self.data[len(self.data)-1] , self.data[0]
        last_element = self.data.pop()
        self.heapify()
        return last_element
    
    
    def add(self , obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data.append(obj)
        self.heapify()
    def clear(self):
        '''
        Clear the self.data in the heap - initialize to empty list
        '''
        # Your code
        self.data=[]
    
    def import_list(self , lst):
        '''
        Add all the elements of the list 'lst' to self.data
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        for i in lst:
            self.data.append(i)
    def __init__(self , is_min , arity_exp , compare_fn):
        '''
        The Python convention is to have upper case name for global variables - that's why the globals
        in modheap were named in all caps
        Unlike the globals in heap module --- name the attributes as lower case variable names
        '''
        # Your code
        global min_top , cmp_function , exp2 , data
        self.min_top = is_min
        self.cmp_function = compare_fn
        self.exp2 = arity_exp
        self.data = []

    
    def is_favoured(self , index1 , index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a self.data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        # Your code
        if self.min_top == True:
            if self.data[index1] <= self.data[index2]:
                return True
            else:
                return False
        else:
            if self.data[index1] >= self.data[index2]:
                return True
            else:
                return False

    def set_item_at(self , i , val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        # Your code
        self.data[i] = val


    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

if __name__ == '__main__':
    pass