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
#         if(index1<len(self.data) and index2<len(self.data)):
        if(self.min_top==True):
            if(self.cmp_function(self.data[index1] , self.data[index2])!=1):
                return True
        elif(self.min_top==False):
            if(self.cmp_function(self.data[index1] , self.data[index2])!=-1):
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
        # Your code
        return len(self.data)


    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
        # Your code
        return 2**self.exp2
        
        
    def get_item_at(self , i):
        '''
        Return the i-th element of the data list (data)
        '''
        return self.data[i]
    
    
    def get_parent_index(self , child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your code
        if(child_index!=0):
            return (child_index-1)//self.arity()
        else:
            return None
    def get_leftmostchild_index(self , parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        if((self.arity()*parent_index)+1<len(self.data)):
            return (self.arity()*parent_index)+1
        else:
            return None
    
    def get_rightmostchild_index(self , parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        rightc = self.arity()*parent_index+self.arity()
        if(self.get_leftmostchild_index(parent_index)==None):
            return None
        elif(len(self.data)>rightc):
            return rightc
        else:
            return len(self.data)-1    
    def get_top_child(self , parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        if(self.min_top==True):
            minheap = self.data[(self.arity()*parent_index)+1:((self.arity()*parent_index) + self.arity()+1)]
            i = 0
            minimum = minheap[i]
            while(i<len(minheap)):
                if(self.cmp_function(minheap[i] , minimum)!=1):
                    minimum = minheap[i]
                i += 1
            return self.arity()*parent_index+1+minheap.index(minimum)
        else:
            maxheap = self.data[(self.arity()*parent_index)+1:((self.arity()*parent_index)+self.arity()+1)]
            j = 0
            maximum = maxheap[j]
            while(i<len(maxheap)):
                if(self.cmp_function(minheap[i] , minimum)!=-1):
                    maximum = maxheap[i]
                i += 1
            return self.arity()*parent_index+1+maxheap.index(maximum)
    def restore_subtree(self , i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        
        if(self.arity()*i+1<self.size()):
            subheap = self.data[((self.arity()*(i))+1):((self.arity()*i)+self.arity()+1)]
            var = 0
            minimum = subheap[var]
            maximum = minimum
            while(var<len(subheap)):
                if(self.cmp_function(subheap[var] , minimum)!=1):
                    minimum = subheap[var]
                elif(self.cmp_function(subheap[var] , maximum)!=-1):
                    maximum = subheap[var]
                var += 1
            j = self.arity()*i+1+subheap.index(minimum)
            k = self.arity()*i+1+subheap.index(maximum)
            if(self.min_top==True):
                if(self.cmp_function(self.data[i] , self.data[j])==1):
                    self.data[i] , self.data[j] = self.swap(self.data[i] , self.data[j])
                    i = j
                    self.restore_subtree(i)
            elif(self.min_top==False):
                if(self.cmp_function(self.data[i] , self.data[k])==-1):
                    self.data[i] , self.data[k] = self.swap(self.data[i] , self.data[k])     
                    i = k
                    self.restore_subtree(i)
        
    def restore_heap(self , i):
        '''
        Restore the heap property for data assuming that it has been 'corrupted' at index i
        The rest of data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        if(i!=0):
            if(self.min_top==True):
                if(self.arity()*i+1<self.size()):
                    subheap = self.data[((self.arity()*(i))+1):((self.arity()*i)+self.arity()+1)]
                    var = 0
                    minimum = subheap[var]
                    maximum = minimum
                    while(var<len(subheap)):
                        if(self.cmp_function(subheap[var] , minimum)!=1):
                            minimum = subheap[var]
                        elif(self.cmp_function(subheap[var] , maximum)!=-1):
                            maximum = subheap[var]
                        var += 1
                    j = self.data.index(minimum)
                    parent_index = self.get_parent_index(i)
                    if(self.cmp_function(self.data[i] , self.data[parent_index])==-1):
                        self.data[i] , self.data[parent_index] = self.swap(self.data[i] , self.data[parent_index])
                        i = parent_index
                        self.restore_heap(i)
                    elif(self.cmp_function(self.data[i] , minimum)==1):
                        self.data[i] , self.data[j] = self.swap(self.data[i] , self.data[j])
                        i = j
                        self.restore_subtree(i)
                elif(self.arity()*i+1>self.size()):
                    parent_index = self.get_parent_index(i)
                    if(self.cmp_function(self.data[i] , self.data[parent_index])==-1):
                        self.data[i] , self.data[parent_index] = self.swap(self.data[i] , self.data[parent_index])
                        i = parent_index
                        self.restore_heap(i)
                else:
                    i -= 1 
            
                
            elif(self.min_top==False):
                if(self.arity()*i+1<self.size()):
                    subheap = self.data[((self.arity()*(i))+1):((self.arity()*i)+self.arity()+1)]
                    var = 0
                    minimum = subheap[var]
                    maximum = minimum
                    while(var<len(subheap)):
                        if(self.cmp_function(subheap[var] , minimum)!=1):
                            minimum = subheap[var]
                        elif(self.cmp_function(subheap[var] , maximum)!=-1):
                            maximum = subheap[var]
                        var += 1
                    k = self.data.index(maximum)
                    parent_index = self.get_parent_index(i)
                    if(self.cmp_function(self.data[i] , self.data[parent_index])==1):
                        self.data[i] , self.data[parent_index] = self.swap(self.data[i] , self.data[parent_index])
                        i = parent_index
                        self.restore_heap(i)
                    elif(self.cmp_function(self.data[i],maximum)==-1):
                        self.data[i] , self.data[k] = self.swap(self.data[i] , self.data[k])
                        i = k
                        self.restore_subtree(i)
                elif(self.arity()*i+1>=self.size()):
                    parent_index = self.get_parent_index(i)
                    if(self.cmp_function(self.data[i] , self.data[parent_index])==1):
                        self.data[i] , self.data[parent_index] = self.swap(self.data[i] , self.data[parent_index])
                        i = parent_index
                        self.restore_heap(i)
                else:
                    i -= 1
        else:
            self.restore_subtree(0)
    
    
    def heapify(self):
        '''
        Rearrange data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        i = self.size()-1
        while(i>=0):
            if(self.min_top==True):
                if((self.arity()*i)+1<self.size()):
                    subheap = self.data[((self.arity()*i)+1):(self.arity()*(i+1))+1]
                    var = 0
                    minimum = subheap[var]
                    maximum = minimum
                    while(var<len(subheap)):
                        if(self.cmp_function(subheap[var] , minimum)!=1):
                            minimum = subheap[var]
                        elif(self.cmp_function(subheap[var] , maximum)!=-1):
                            maximum = subheap[var]
                        var += 1
                    j = (self.arity()*i)+1+subheap.index(minimum)
                    if(self.cmp_function(self.data[i] , minimum)==1):
                        self.data[i] , self.data[j] = self.swap(self.data[i] , self.data[j] )
                        i = j
                    else:
                        i -= 1
                else:
                    i -= 1 
            elif(self.min_top==False):
                if((self.arity()*i)+1<self.size()):
                    subheap = self.data[(self.arity()*(i))+1:(self.arity()*(i+1))+1]
                    var = 0
                    minimum = subheap[var]
                    maximum = minimum
                    while(var<len(subheap)):
                        if(self.cmp_function(subheap[var] , minimum)!=1):
                            minimum = subheap[var]
                        elif(self.cmp_function(subheap[var] , maximum)!=-1):
                            maximum = subheap[var]
                        var += 1
                    k = (self.arity()*i)+1+subheap.index(maximum)
                    if(self.cmp_function(self.data[i] , maximum)==-1):
                        self.data[i] , self.data[k] = self.swap(self.data[i] , self.data[k] )
                        i = k
                    else:
                        i -= 1
                else:
                    i -= 1               
        return self.data                     
    def remove(self , i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        self.data[i] , self.data[-1] = self.swap(self.data[i] , self.data[-1])
        self.data.pop()
        self.restore_heap(i)
        
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        
        self.data.reverse()
        pop1 = self.data.pop()
        self.data.reverse()
        self.heapify()
        return pop1
    
    def add(self , obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data.append(obj)
        self.heapify()
        return self.data
    def import_list(self , lst):
        '''
        Add all the elements of the list 'lst' to data
        Make sure this does not modify the input list 'lst'
        '''
        # Your code
        i = 0
        while(i<len(lst)):
            self.data.append(lst[i])
            i += 1
      
    
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        # Your code
        self.data = []
    def swap(self , a_1 , b_1):
        a_1 , b_1 = b_1 , a_1
        return a_1 , b_1

    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

if __name__ == '__main__':
    pass
