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
        self.flag=0
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
        if(self.min_top==True and self.data[index1]<=self.data[index2]):
            return True
        elif(self.min_top==False and self.data[index1]>=self.data[index2]):
            return True


    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        # Your code
        val=self.data[i]
    
    
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
        return 1<<self.exp2
        
        
    def get_item_at(self,i):
        '''
        Return the i-th element of the data list (self.data)
        '''
        return self.data[i]
    
    
    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your code
        if (child_index>0):
            return ((child_index-1)>>self.exp2)
        return None
        
    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        # Your code
        if(parent_index == None):
            return None
        elif (((parent_index<<self.exp2)+1)<self.size()):
            return (parent_index<<self.exp2)+1
        else:
            return None    
    
    
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code
        if(((parent_index<<self.exp2)+self.arity()<self.size())):
            return((parent_index<<self.exp2)+self.arity())
        elif(self.get_leftmostchild_index==None):
            return None
        else:
            return (self.size()-1)
        
    
    
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        # Your code
        if(self.get_leftmostchild_index(parent_index)==None):
            return None
        temp=[]
        i=self.get_rightmostchild_index(parent_index)
        if(i!=None and self.min_top==True and i<self.size()-1):    
            temp=((self.data[self.get_leftmostchild_index(parent_index):i+1]))
            mini=temp[0]
            i=0
            while(i<len(temp)):
                if(self.cmp_function(mini,temp[i])!=-1):
                    mini=temp[i]
                i+=1
            k=temp.index(mini)
            return self.get_leftmostchild_index(parent_index)+k
        if(i!=None and self.min_top==True and i==self.size()-1):
            temp=((self.data[self.get_leftmostchild_index(parent_index):]))
            mini=temp[0]
            i=0
            while(i<len(temp)):
                if(self.cmp_function(mini,temp[i])!=-1):
                    mini=temp[i]
                i+=1
            k=temp.index(mini)
            return self.get_leftmostchild_index(parent_index)+k
        if(i!=None and self.min_top==False and i<self.size()-1):    
            temp=((self.data[self.get_leftmostchild_index(parent_index):i+1]))
            mini=temp[0]
            i=0
            while(i<len(temp)):
                if(self.cmp_function(mini,temp[i])!=1):
                    mini=temp[i]
                i+=1
            k=temp.index(mini)
            return self.get_leftmostchild_index(parent_index)+k
        if(i!=None and self.min_top==False and i==self.size()-1):
            temp=((self.data[self.get_leftmostchild_index(parent_index):]))
            mini=temp[0]
            i=0
            while(i<len(temp)):
                if(self.cmp_function(mini,temp[i])!=1):
                    mini=temp[i]
                i+=1
            k=temp.index(mini)
            return self.get_leftmostchild_index(parent_index)+k
        else:
            return None
        
        
    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        # Your code
        if (self.min_top==True):
            while (i!=None and i<self.size()):
                a=self.get_top_child(i)
                if a==None:
                    return None
                elif (self.cmp_function(self.data[i],self.data[a])==1):
                    self.data[i],self.data[a]=self.data[a],self.data[i]
                i=a
        if (self.min_top==False):
            while (i!=None and i<self.size()):
                a=self.get_top_child(i)
                if (a==None):
                    return None
                elif (self.cmp_function(self.data[i],self.data[a])==-1):
                    self.data[i],self.data[a]=self.data[a],self.data[i]
                i=a
    
        
    def restore_heap(self,i):
        '''
        Restore the heap property for self.data assuming that it has been 'corrupted' at index i
        The rest of self.data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        # Your code
        a=self.get_parent_index(i)
        self.flag
        if (a!=None and (self.cmp_function(self.data[i],self.data[a])==-1) and self.min_top==True):
            self.data[i],self.data[a]=self.data[a],self.data[i]
            self.flag+=1 
            self.restore_heap(a)
        elif (a!=None and (self.cmp_function(self.data[i],self.data[a])==1) and self.min_top==False):
            self.data[i],self.data[a]=self.data[a],self.data[i]
            self.flag+=1
            self.restore_heap(a)
        if (self.flag==0):
            self.restore_subtree(i)
    
    
    def heapify(self):
        '''
        Rearrange self.data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
        i=self.get_parent_index(self.size()-1)
        while(i>=0):
            self.restore_subtree(i)
            i-=1
        return self.data   
    
    
    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        # Your code
        last=self.size()-1
        self.data[i],self.data[last]=self.data[last],self.data[i]
        a=self.data.pop()
        self.heapify()
        return a
        
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        return self.remove(0)
    
    
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
        self.data
        self.data=lst[:]
    
    
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        # Your code
        self.data
        self.data=[]
    
    if __name__ == '__main__':
        pass