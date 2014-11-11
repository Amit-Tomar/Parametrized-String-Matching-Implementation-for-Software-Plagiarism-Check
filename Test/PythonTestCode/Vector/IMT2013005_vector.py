from __future__ import division
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
    count = 0
    for ele in lst:
        if(zero_test(ele)==0):
            count += 1
    if (count/len(lst)>=DENSITY_THRESHOLD and len(lst)>=SIZE_THRESHOLD):
        return True
                

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    values = []
    indices = []
    for i in range(len(data)):
        if(data[i]!=0):
            values.append(data[i])
            indices.append(i)
    if(is_long_and_sparse(data , zero_test)==True):
        vector = SparseVector(values , indices , len(data) , zero_test)
        return vector 
    else:
        vector = FullVector(data , zero_test)
        return vector

    
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
        self.data = lst
        self.Zero_test = zero_test


    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        # Your Code
        return len(self.data)


    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        # Your Code
        return self.data[i]

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        # Your Code
        self.data[i] = val
        return val
    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        # Your Code
        for ele in self.data:
            if(ele!=0):
                return False
        return True

    def components(self):
        '''
        Allows one to iterate through the elements of the vector as shown below
        for elem in vector.components(): (vector is an object of type Vector or any of its derived classes)
        '''
        for i in range(len(self)):
            yield self[i]


    def __eq__(self, vector):
        '''
        Check if this vector is identical to another 'vector' (allows use of operator == to compare vectors)
        '''
        # Your Code
        for i in range(len(self)):
            if (self[i]!=vector[i]):
                return False
        return True


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        dot_product = []
        if(len(self)==len(vector)):
            for i in range(len(self)):
                dot_product.append(self[i]*vector[i])
            return dot_product
        else:
            return None


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        add = []
        if(len(self)==len(vector)):
            for i in range(len(self)):
                add.append(self[i]+vector[i])
            return make_vector(add , self.Zero_test)
        else:
            return None


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        sub = []
        if(len(self)==len(vector)):
            for i in range(len(self)):
                sub.append(self[i]+vector[i])
            return make_vector(sub , self.Zero_test)
        else:
            return None


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        min_sum = min(len(self) , len(vector))
        for i in range(min_sum):
            self[i] = self[i] + vector[i]

    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        min_sum = min(len(self) , len(vector))
        for i in range(min_sum):
            self[i] = self[i] - vector[i]


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        vec1 = self.data[:int(len(self)/2)]
        vec2 = self.data[int(len(self)/2):]
        return make_vector(vec1 , self.Zero_test) , make_vector(vec2 , self.Zero_test)      
        
        
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
        self.data = lst

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        vec1 = self[:int(len(self)/2)]
        vec2 = self[int(len(self)/2):]
        return FullVector(vec1 , self.Zero_test) , FullVector(vec2 , self.Zero_test) 


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        merge = []
        for i in range(len(self)):
            merge.append(self[i])
        for i in range(len(vector)):
            merge.append(vector[i])  
        return make_vector(merge,zero_test = lambda x : (x == 0))
        '''for j in vector:
            merge.append(vector[j])'''

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
        self.Values = values
        self.Indices = indices
        self.Length = length
        self.Zero_test = zero_test


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        # Your Code
        return self.Length


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        # Your Code
        if i not in self.Indices:
            return 0
        if i in self.Indices:
            return self.data[self.Indices.index(i)]


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        if i not in self.Indices:
            self.data.append(val)
            self.Indices.append(i)
        if i in self.Indices:
            self.data[self.Indices.index(i)]=val


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        for elem in self.data:
            if(elem!=0):
                return False
        return True


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        data =[]
        for i in range(len(self)):
            if i in self.Indices:
                
                data.append(self.Values[self.Indices.index(i)])
            else:
                data.append(0)
        indices1 , indices2 = [], []
        vec1 = data[:int(len(self)/2)]
        vec2 = data[int(len(self)/2):]
        i = 0
        while(i<len(self)):
            if(i<len(vec1)):
                indices1.append(i)
            else:
                indices2.append(i)
            i += 1
        return SparseVector(vec1, indices1, len(vec1) , self.Zero_test) , SparseVector(vec2 ,indices2,len(vec2), self.Zero_test) 


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        merge = []
        for i in self:
            if(self[i]!=0):
                merge.append(self[i])
        for j in vector:
            if(vector[i]!=0):
                merge.append(vector[j])
if __name__ == '__main__':
    pass
# a=[1,2,0,3,5,0,8,0,0,0]
# c=[1,2,0,3,5,0,8,0,0,0]
# obj=make_vector(a,zero_test = lambda x : (x == 0))
# obj1=make_vector(c,zero_test = lambda x : (x == 0))
# # d,e=obj.split()
# # print d.Indices,e.Indices
# # obj1=make_vector(c,zero_test = lambda x : (x == 0))
# # b=FullVector(a,zero_test = lambda x : (x == 0))
# # b.merge(obj1)
# b=obj.merge(obj1)
# print b.data