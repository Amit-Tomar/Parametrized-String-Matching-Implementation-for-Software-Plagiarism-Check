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
        self.MIN_TOP = is_min
        self.CMP_FUNCTION = compare_fn
        self.EXP2 = arity_exp
        self.DATA = []

   def is_favoured(self, index1, index2):
        '''
        Return True if the element at index1 is favoured over the element at index2 --- 
        In other words a heap is a data structure which ensures that any node is favoured over any of its children
        Takes into account whether the heap is min or max and also the result of comparison between elem1 and elem2
        '''
        
        if(self.MIN_TOP==True):
            if((self.index1)>(self.index2)):
                return True
        else:
            return False
            

    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        
        self.DATA[i]=val
    def size(self):

    
        return len(self.DATA)

    def arity(self):
        '''
        Return the arity of the heap - max number of children that any internal node has
        Also only one internal node will have less children than the arity of the heap
        '''
    
        return 2**self.EXP2
    
    
    def get_item_at(self,i):
        '''
        Return the i-th element of the data list (DATA)
        '''
        return self.DATA[i]


    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
    
        if (child_index-1)>>self.EXP2 < 0:
            return None
        else:
            return (child_index-1)//self.arity()

    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
   
   
        if ((parent_index<<self.EXP2)+1) < self.size():
            return ((parent_index<<self.EXP2)+1)
  

    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
   
        if  (parent_index<<self.EXP2)+2**self.EXP2 < self.size():
            return (parent_index<<self.EXP2)+2**self.EXP2
        else:
            return self.size()-1
    
          

    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        #children = DATA[get_leftmostchild_index(parent_index):get_rightmostchild_index(parent_index)+1]
        get_leftmostchild_index(parent_index) = self.get_leftmostchild_index(parent_index)
        if self.MIN_TOP:
            if get_leftmostchild_index(parent_index)!=None:
                for i in range(self.get_leftmostchild_index(parent_index),self.get_rightmostchild_index(parent_index)+1):
                    if self.CMP_FUNCTION(self.DATA[m] , self.DATA [i])==1:
                        get_leftmostchild_index(parent_index) = i
                    return get_leftmostchild_index(parent_index)
        else:
            if get_leftmostchild_index(parent_index)!=None : 
                for i in range(self.get_leftmostchild_index(parent_index),self.get_rightmostchild_index(parent_index)+1):
                    if self.CMP_FUNCTION(self.DATA[get_leftmostchild_index(parent_index)] ,self.DATA [i])==-1:
                        get_leftmostchild_index(parent_index) = i
                    return get_leftmostchild_index(parent_index)
        #return DATA.index(max(children))

    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
  
        if(self.MIN_TOP==True):
            if(self.get_top_child(i)!=None):
                while(self.get_top_child(i) !=None and self.CMP_FUNCTION(self.DATA[i],self.DATA[self.get_top_child(i)]))==1:
                    self.DATA[i],self.DATA[self.get_top_child(i)]=self.DATA[self.get_top_child(i)],self.DATA[i]
                    i=self.get_top_child(i)
    
               
        
        else:
            if(self.get_top_child(i)!=None):
                while(self.get_top_child(i) !=None and self.CMP_FUNCTION(self.DATA[i],self.DATA[self.get_top_child(i)]))==-1:
                    self.DATA[i],self.DATA[self.get_top_child(i)]=self.DATA[self.get_top_child(i)],self.DATA[i]
                    i=self.get_top_child(i)  

              
   
        #def parentchild_indices(i):
        #return i/2,2*i,(2*i+1)

    
    def restore_heap(self,i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
    
        if(self.MIN_TOP==True ):
            if(i != None ):
                parent_index = self.get_parent_index(i)
                if parent_index != None and self.CMP_FUNCTION( self.DATA[i] , self.DATA[parent_index])==1:
                    while(i != None and parent_index != None  and self.CMP_FUNCTION( self.DATA[i] , self.DATA[parent_index]))==1:
                        self.DATA[i], self.DATA[parent_index]=self.DATA[parent_index],self.DATA[i]
                        i = parent_index
                        parent_index = self.get_parent_index(i)
            else:
                self.restore_subtree(i)
       
        else:
            if(i != None ):
                parent_index = self.get_parent_index(i)
                if parent_index != None and self.CMP_FUNCTION(self.DATA[parent_index]  , self.DATA[i])==-1:
                    while(i != None and parent_index != None and self.CMP_FUNCTION(self.DATA[parent_index]  , self.DATA[i]))==-1:
                        self.DATA[i],self.DATA[parent_index]=self.DATA[parent_index],self.DATA[i]
                        i = parent_index
                        parent_index = self.get_parent_index(i)
            else:
                self.restore_subtree(i)
        

   
   

    def heapify(self):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        i=self.get_parent_index(self.size()-1)
        while(i>=0):
            self.restore_subtree(i)
            i=i-1
        
    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
    
        self.DATA[i],self.DATA[-1]=self.DATA[-1],self.DATA[i]
        rem=self.DATA.pop()
        self.restore_heap(i)
        return rem



    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        rem = self.remove(0)
        return rem


    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        self.DATA.append(obj)
        self.restore_heap(self.size()-1)


    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
        for i in lst:
            self.DATA.append(i)
        #self.DATA = self.DATA + lst
    

    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        #remove(DATA)
        self.DATA=[]
    


    # Other methods will be the same as the functions in the modheap module -
    # add them here as methods of the Heap class

if __name__ == '__main__':
    pass
