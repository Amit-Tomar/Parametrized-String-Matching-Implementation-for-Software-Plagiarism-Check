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
        self.min_top=is_min
        self.cmp_function=compare_fn
        self.exp2=arity_exp
        self.data=[]
    
    def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a self.self.data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        # Your code
        if(self.min_top==True and self.data[index1] <= self.data[index2]):
            return True
        elif(self.min_top==False and self.data[index1] >= self.data[index2]):
            return True
        else:
            return False

    def set_item_at(self, i, val):
        '''
        Set the i-th element of the self.self.data to the value 'val'
       , '''
        # Your code
        self.data[i]=val
    
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
   
        return 2<<(self.exp2-1)
    


    def get_item_at(self,i):
        '''
        Return the i-th element of the self.self.data list (self.self.data)
        '''
        return self.self.data[i]


    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        # Your code
        if(child_index==0):
            return None
        else:
        
            parent_index = ((child_index-1)>>self.exp2)
            return parent_index

    def get_leftmostchild_index(self,parent_index):
        '''
         Return the index of the leftmost child of the element at parent_index
         Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
    
        leftmostchild_index= (parent_index<<self.exp2)+1
        # Your code
        if(leftmostchild_index>=len(self.data)):
            return None
        else:
            return leftmostchild_index
    

    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        # Your code

      
        left_index=self.get_leftmostchild_index(parent_index)
        if(left_index==None):
            return None
    
        else:
            ref=0
            while(ref<self.arity()):
                rightmost_index=left_index+ref
        
                if(rightmost_index>=len(self.data)-1):
                    return rightmost_index
                    break
                  
                else:
                    ref=ref+1
            return rightmost_index 
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''

        # Your code
        temp_var=[]
        child_index_first=(self.arity()*parent_index) +1
        child_index_last=(self.arity()*parent_index) + (self.arity()+1)
        if(child_index_last>self.size()):  
            temp_var=temp_var+self.data[child_index_first:]  
        else:
            temp_var=temp_var+self.data[child_index_first:child_index_last]
        if(child_index_first>=self.size()):
            return None
        if(self.min_top== False):
            value=max(temp_var)
            ref_val=temp_var.index(value)
            return ref_val+self.get_leftmostchild_index(parent_index)
        else:
            value=min(temp_var)
            ref_val=temp_var.index(value)
            return ref_val+self.get_leftmostchild_index(parent_index)

    def restore_subtree(self,i):
            while(i!=None and i<len(self.data)):
                topmost_child_index = self.get_top_child(i)
                if(topmost_child_index==None):
                    return None
                topmost_child_value=self.data[topmost_child_index]
                if(self.min_top==False):
                    if(topmost_child_value>self.data[i]):
                        self.data[i],self.data[topmost_child_index]=self.data[topmost_child_index],self.data[i]
                else:
                    if(topmost_child_value<self.data[i]):
                        self.data[i],self.data[topmost_child_index]=self.data[topmost_child_index],self.data[i]
                i=topmost_child_index
    


    def restore_heap(self,i):
        '''
        Restore the heap property for self.self.data assuming that it has been 'corrupted' at index i
        The rest of self.self.data is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element
        '''
        # Your code
        if(self.min_top==True):
            while(i!=None and i>0):
                parent_index=self.get_parent_index(i)
                if(self.data[i]<self.data[parent_index]):
                    self.data[i],self.data[parent_index]=self.data[parent_index],self.data[i]
                else:
                    self.restore_subtree(i)
                i=parent_index
            self.restore_subtree(0)
        else:
            while(i!=None and i>0):
                parent_index=self.get_parent_index(i)
                if(self.data[i]>self.data[parent_index]):
                    self.data[i],self.data[parent_index]=self.data[parent_index],self.data[i]
                else:
                    self.restore_subtree(i)
                i=parent_index
            self.restore_subtree(0) 
            

    def heapify(self):
        '''
        Rearrange self.self.data into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        # Your code
    
        firstnonleaf_index= self.get_parent_index(len(self.data)-1)
    
        while(firstnonleaf_index>=0):
            self.restore_subtree(firstnonleaf_index)
            firstnonleaf_index=firstnonleaf_index-1
       

    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        temp=self.data[len(self.data)-1]
        self.data[len(self.data)-1]=self.data[i]
        self.data[i]=temp
        element=self.data.pop()
        self.heapify()
        return element

    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        # Your code
        return self.remove(0)
        self.heapify()
    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        # Your code
        self.data.append(obj)
        self.heapify()



    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to self.self.data
        Make sure this does not modify the input list 'lst'
    
        '''
        # Your code
        len_lst=len(lst)
        i=0
        while(i<len_lst):
            self.data.append(lst[i])
            i=i+1
    
        return self.data



def clear():
    '''
    Clear the self.self.data in the heap - initialize to empty list
    '''
    # Your code
    self.self.data=[]
    

    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

if __name__ == '__main__':
    pass