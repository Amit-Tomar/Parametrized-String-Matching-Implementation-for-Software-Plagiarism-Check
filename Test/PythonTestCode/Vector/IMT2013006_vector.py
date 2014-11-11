'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 50

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    # Your Code
    count=0
    if len(lst)>SIZE_THRESHOLD :
        for element in lst:
            if(zero_test(element))==True :
                count+=1
        if (float(count)/len(lst))>DENSITY_THRESHOLD :
            return True                                    #if its worth using sparse vector ten true
    return False            

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    if (is_long_and_sparse(data, zero_test)):
        non_zero_elem, elem_index, i= [], [], 0
        while(i<len(data)):
            if (data[i]!=0):
                non_zero_elem.append(data[i])
                elem_index.append(i)
            i+=1    
        return SparseVector (non_zero_elem, elem_index, len(data), zero_test)
    return FullVector (data, zero_test)
                

    
class Vector(object):
    '''
    Base Vector class - implements a number of the common methods required for a Vector
    '''
    def __init__(self, lst, zero_test = lambda x : (x == 0)):
        '''
        Have a data attribute that is initialized to the list of elements given in the argument 'lst'
        zero_test is a function that tests if a given element is zero (remember you could potentially
        have a vector of complex numbers, even a vector of functions, ... not just numbers 
        '''
        # Your Code
        self.lst=lst
        self.zero_test=zero_test
        
    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        # Your Code
        return len(self.lst)


    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        # Your Code
        return self.lst[i]
    

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        # Your Code
        self[i]=val
        

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        # Your Code
        for i in self.lst:
            if(i!=0):
                return False
        return True    


    def components(self):
        '''
        Allows one to iterate through the elements of the vector as shown below
        for elem in vector.components(): (vector is an object of type Vector or any of its derived classes)
        '''
        for i in xrange(len(self)):
            yield self[i]


    def __eq__(self, vector):
        '''
        Check if this vector is identical to another 'vector' (allows use of operator == to compare vectors)
        '''
        # Your Code
        if(len(self)!=len(vector)):
            return False
        for i in range(0,len(self)):
                if self[i]!=vector[i]:
                    return False
        return True        


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        if(len(self)!=len(vector)):
            return None
        multiplied_vector=0
        for i in range(0,len(self)):
            multiplied_vector+=self[i]*vector[i]
        return multiplied_vector    
            


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        if(len(self)!=len(vector)):
            return None
        added_vector=[]
        for i in range(0,len(self)):
            added_vector.append(self[i]+vector[i])
        return make_vector(added_vector,lambda x : (x == 0))    


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        if(len(self)!=len(vector)):
            return None
        subtracted_vector=[]
        for i in range(0,len(self)):
            subtracted_vector.append(self[i]-vector[i])
        return subtracted_vector 


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        minimum=min(len(self),len(vector))
        added_vector=[]
        for i in range (0,minimum):
            added_vector.append(self[i]+vector[i])
        return added_vector    
            


    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        minimum=min(len(self),len(vector))
        subtracted_vector=[]
        for i in range (0,minimum):
            subtracted_vector.append(self[i]-vector[i])
        return subtracted_vector 


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        return None, None
        
        
        
class FullVector(Vector):
    '''
    A subclass of Vector where all elements are kept explicitly as a list
    '''
    def __init__(self, lst, zero_test = lambda x : (x == 0)):
        '''
        Constructor for a FullVector on data given in the 'lst' argument - 'lst' is the list of elements in the vector
        Uses the base (parent) class attributes data and zero_test
        '''
        super(FullVector, self).__init__(lst, zero_test)
        self.lst = lst
        
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        a=len(self.lst)/2
        left_half=self.lst[:a]
        right_half=self.lst[a:]
        return left_half, right_half


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        for i in range(0,len(vector)):
            self.lst.append(vector[i])
        return self    


class SparseVector(Vector):
    '''
    Vector that has very few non-zero entries
    Values and corresponding indices are kept in separate lists
    '''
    def __init__(self, values, indices, length = 0, zero_test = lambda x : (x == 0)):
        '''
        'values' argument is the list of non-zero values and the corresponding indices are in the list 'indices'
        Uses the base (parent) class attributes data (this is where 'values' are kept) and zero_test
        Length is the length of the vector - the number of entries in 'values' is just the number of non-zero entries
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseVector, self).__init__(values, zero_test)
        # Your Code
        self.values=values
        self.indices=indices
        self.length=length
        self.zero_test=zero_test
        

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        # Your Code
        return self.length


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        # Your Code
        for element in self.indices:
            if element==i:
                k=self.indices.index(i)
                return self.values[k]
        return 0    
                


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        for j in range(0,len(self.indices)):
            if self.indices[j]==i:
                self.values[i]=val
            else:
                self.indices.append(i)
                self.values.append(val)        


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        if len(self.values)==0 :
            return True
        return False
            


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        left_vector, right_vector= [],[]
        left_vector_index, right_vector_index= [],[]
        for key in self.indices:
            if (key<(self.length)/2):
                left_vector.append(self.values[self.indices.index(key)])
                left_vector_index.append(key)
            if (key>=(self.length)/2):
                right_vector.append(self.values[self.indices.index(key)])
                right_vector_index.append(key)
        vector_left=SparseVector (left_vector, left_vector_index, (self.length)/2, self.zero_test)  
        vector_right=SparseVector (right_vector, right_vector_index, self.length-((self.length)/2), self.zero_test)
        return vector_left, vector_right


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        lst = []
        for i in range(0, len(self)):
            lst.append(self[i])
        for i in range(0, len(vector)):
            lst.append(vector[i])
        self = make_vector(lst,lambda x : (x == 0))
        return self
    
    
'''v1 = make_vector([0,1,2,0,0,0,0,3,0,0,0,0,0,4],lambda x : (x == 0))
v2 = make_vector([5,0,0,0,0,6,0,0,0,0,0,7,0,8],lambda x : (x == 0))
v1 = v1.merge(v2)
print v1.values , v1.indices'''
