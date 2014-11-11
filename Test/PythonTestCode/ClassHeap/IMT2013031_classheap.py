'''
Created on Nov 14, 2013

@author: imt2013031
'''
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
    def __init__(self, is_min , arity_exp , compare_fn):
        '''
        The Python convention is to have upper case name for global variables - that's why the globals
        in modheap were named in all caps
        Unlike the globals in heap module --- name the attributes as lower case variable names
        '''   
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
        if(self.min_top==True):
            if( self.data[index1] <= self.data[index2] ):
                return True
            else:
                return False
        else:
            if( self.data[index1] >= self.data[index2] ):
                return True
            else:
                return False
    def set_item_at(self, i, val):
        '''
        Set the i-th element of the data to the value 'val'
        '''
        self.data[i]=val
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
        return 2**self.exp2

    def get_item_at(self,i):
        '''
        Return the i-th element of the data list (DATA)
        '''
        return self.data[i]
    def get_parent_index(self,child_index):
        '''
        Return the index of the parent given the child_index
        Use bit operators here - to divide say n by 2^m - right shift n by m bits (written as n >> m, in python)
        '''
        limit=self.size()-1
        if(child_index>0 and child_index<=limit):
            return (child_index-1)>>self.exp2
        else:
            return None

    def get_leftmostchild_index(self,parent_index):
        '''
        Return the index of the leftmost child of the element at parent_index
        Use bit operators here - to multiply say n by 2^m - left shift n by m bits (written as n << m, in python)
        '''
        if((self.size()-1)%self.arity()==0):
            if(parent_index>=0 and parent_index<(self.size()-1)/self.arity()):
                return (parent_index<<self.exp2)+1
            else:
                return None
        if((self.size()-1)%self.arity()!=0):
            if(parent_index>=0 and parent_index<=(self.size()-1)/self.arity()):
                return (parent_index<<self.exp2)+1
            else:
                return None
    def get_rightmostchild_index(self,parent_index):
        '''
        Return the index of the rightmost child of the element at parent_index
        Should return None if the parent has no child
        '''
        if((self.size()-1)%self.arity()==0):
            if(parent_index>=0 and parent_index<(self.size()-1)/self.arity()):
                if(parent_index!=(self.get_parent_index(self.size()-1))):
                    return (parent_index<<self.exp2)+self.arity()
                else:
                    if((self.size()-self.get_leftmostchild_index(parent_index))==1):
                        return None
                    if((self.size()-self.get_leftmostchild_index(parent_index))>1 and (self.size()-self.get_leftmostchild_index(parent_index))<self.arity()):
                        return self.size()-1
        if((self.size()-1)%self.arity()!=0):
            if(parent_index>=0 and parent_index<=(self.size()-1)/self.arity()):
                if(parent_index!=self.get_parent_index(self.size()-1)):
                    return (parent_index<<self.exp2)+self.arity()
                else:
                    if((self.size()-self.get_leftmostchild_index(parent_index))==1):
                        return None
                    if((self.size()-self.get_leftmostchild_index(parent_index))>1 and (self.size()-self.get_leftmostchild_index(parent_index))<self.arity()):
                        return self.size()-1
           
    def get_top_child(self,parent_index):
        '''
        Return the index of the child which is most favoured to move up the tree among all the children of the
        element at parent_index
        '''
        if((self.size()-1)%self.arity()==0):
            if(parent_index>=0 and parent_index<(self.size()-1)/self.arity()):
                list1=[]
                lci=self.get_leftmostchild_index(parent_index)
                rci=self.get_rightmostchild_index(parent_index)
                if(rci==None):
                    rci=self.size()-1
                while(lci<=rci):
                    list1.append(self.data[lci])
                    lci=lci+1
                if(self.min_top==True):
                    a=min(list1)
                if(self.min_top==False):
                    a=max(list1)
                m=0
                while(m<=self.size()-1):
                    if(self.data[m]==a):
                        return m
                    m=m+1
            else:
                return None
        if((self.size()-1)%self.arity()!=0):
            if(parent_index>=0 and parent_index<=(self.size()-1)/self.arity()):
                list1=[]
                lci=self.get_leftmostchild_index(parent_index)
                rci=self.get_rightmostchild_index(parent_index)
                if(rci==None):
                    rci=self.size()-1
                while(lci<=rci):
                    list1.append(self.data[lci])
                    lci=lci+1
                if(self.min_top==True):
                    a=min(list1)
                if(self.min_top==False):
                    a=max(list1)
                m=0
                while(m<=self.size()-1):
                    if(self.data[m]==a):
                        return m
                    m=m+1
            else:
                return None
    def restore_subtree(self,i):
        '''
        Restore the heap property for the subtree with the element at index i as the root
        Assume that everything in the subtree other than possibly the root satisfies the heap property
        '''
        gtc1=self.get_top_child(i)
        if(self.min_top==True):
            while(gtc1!=None and self.data[gtc1]<self.data[i]):
                self.data[i],self.data[gtc1]=self.data[gtc1],self.data[i]
                i,gtc1=gtc1,i
                gtc1=self.get_top_child(i)
        if(self.min_top==False):
            while(gtc1!=None and self.data[gtc1]>self.data[i]):
                self.data[i],self.data[gtc1]=self.data[gtc1],self.data[i]
                i,gtc1=gtc1,i
                gtc1=self.get_top_child(i)
    def restore_heap(self,i):
        '''
        Restore the heap property for DATA assuming that it has been 'corrupted' at index i
        The rest of DATA is assumed to already satisfy the heap property
        Algo: (i) Check if the element at i needs to move up the tree. If yes, swap this element with its parent.
        Continue this till you do not need to move up anymore.
        (ii) If it has not moved up, then fix the subtree below this element 
        '''
        if(self.min_top==True):
            a=self.get_parent_index(i)
            while(a!=None and self.data[i]<self.data[a]):
                self.data[i],self.data[a]=self.data[a],self.data[i]
                i,a=a,i
                a=self.get_parent_index(i)
            self.restore_subtree(i)
        if(self.min_top==False):
            a=self.get_parent_index(i)
            while(a!=None and self.data[i]>self.data[a]):
                self.data[i],self.data[a]=self.data[a],self.data[i]
                i,a=a,i
                a=self.get_parent_index(i)
            self.restore_subtree(i)
    
    def heapify(self):
        '''
        Rearrange DATA into a heap
        Algo: (i) Start from the first nonleaf node - the parent of the last element
        (ii) Restore the heap property for subtree rooted at at every node starting from the last non-leaf node upto the root
        '''
        if(self.min_top==True):
            k=self.size()-1
            m=self.get_parent_index(k)
            while(m>=0):
                gtc1=self.get_top_child(m)
                while(gtc1!=None and self.data[gtc1]<self.data[m]):
                    self.data[m],self.data[gtc1]=self.data[gtc1],self.data[m]
                    m,gtc1=gtc1,m
                    gtc1=self.get_top_child(m)
                m=m-1
            return self.data
        if(self.min_top==False):
            k=self.size()-1
            m=self.get_parent_index(k)
            if(m==None):
                return None
            while(m>=0):
                gtc1=self.get_top_child(m)
                while(gtc1!=None and self.data[gtc1]>self.data[m]):
                    self.data[m],self.data[gtc1]=self.data[gtc1],self.data[m]
                    m,gtc1=gtc1,m
                    gtc1=self.get_top_child(m)
                m=m-1
        return self.data
    
    def remove(self,i):
        '''
        Remove an element (at index i) from the heap
        Algo: (a) Swap the element at i with the last element. (b) Discard the last element.
        (c) Restore the heap starting from i
        '''
        l=self.size()
        global data
        self.data[i],self.data[l-1]=self.data[l-1],self.data[i]
        self.data=self.data[:-1]
        self.restore_heap(i)
    
    def pop(self):
        '''
        Pull the top element out of the heap
        '''
        global data
        self.heapify()
        ret=self.data[0]
        self.remove(0)
        return ret
        
    def add(self,obj):
        '''
        Add an object 'obj' to the heap
        '''
        global data
        self.data=self.data+[obj]
    def import_list(self,lst):
        '''
        Add all the elements of the list 'lst' to DATA
        Make sure this does not modify the input list 'lst'
        '''
        self.heapify()
        global data
        h=0
        while(h<=(len(lst)-1)):
            self.data=self.data+[lst[h]]
            h=h+1
        return self.data
    def clear(self):
        '''
        Clear the data in the heap - initialize to empty list
        '''
        self.data=[]
            
    
    
        # Other methods will be the same as the functions in the modheap module -
        # add them here as methods of the Heap class
        

if __name__ == '__main__':
    pass