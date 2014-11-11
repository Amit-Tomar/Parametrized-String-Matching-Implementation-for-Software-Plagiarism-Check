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
    if len(lst) >= SIZE_THRESHOLD:
        count = 0
        for element in lst:
            if not zero_test(element):
                count += 1
        if count <= DENSITY_THRESHOLD * len(lst):
            return True


def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    if is_long_and_sparse(data, zero_test):
        value = []
        indices = []
        for index in range (0, len(data)):
            if not zero_test(data[index]):
                value.append(data[index])
                indices.append(index)
        vector = SparseVector(value, indices, len(data))
    else :
        vector = FullVector(data)
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
        self.zero = zero_test
        

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

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        # Your Code
        flag = 0 
        for element in self.data:
            if not self.zero(element):
                flag = 1
                break
        if flag == 0:
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
        flag = 0 
        if len(self) == len(vector):
            for i in range (0, len(self)):
                if self[i] != vector[i]:
                    flag = 1
        if flag == 0:
            return True
            

    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        if len(self) == len(vector):
            dot_product = 0
            for i in range(0, len(self)):
                dot_product += self[i] * vector[i]
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
        data = []
        if len(self) == len(vector):
            add = 0
            for i in range(0, len(self)):
                add = self[i] + vector[i]
                data.append(add)
            return make_vector(data, self.zero)
        else :
            return None
            
           
    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        data = []
        if len(self) == len(vector):
            diff = 0
            for i in range(0, len(self)):
                diff = self[i] - vector[i]
                data.append(diff)
            return make_vector(data, self.zero)
        else :
            return None


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        length = min(len(self), len(vector))
        for i in range(0, length):
            self[i] += vector[i]
        return self


    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        length = min(len(self), len(self))
        for i in range(0, length):
            self[i] -= vector[i]
        return self
            
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        lst1 = self.data[0: len(self)/2]
        lst2 = self.data[len(self)/2: len(self)]
        return make_vector(lst1, self.zero), make_vector(lst2, self.zero) 
        
        
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
        

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        lst1 = self.data[0: len(self)/2]
        lst2 = self.data[len(self)/2: len(self)]
        return FullVector(lst1, self.zero), FullVector(lst2, self.zero)


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        for element in vector.components():
            self.data.append(element)
        self = make_vector(self.data, self.zero)
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
        # Your Code
        super(SparseVector, self).__init__(values, zero_test)
        self.indices = indices
        self.length = length
        

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
        if i in self.indices:
            return self.data[self.indices.index(i)]
        else: 
            return 0


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        if i in self.indices:
            self.data[self.indices.index(i)] = val
        else :
            temp = [i, val]
            border = 0
            for index in self.indices :
                if i > index:
                    border = self.indices.index(index) + 1
                else:
                    break
            self.indices = self.indices[0:border] + temp[0:1] + self.indices[border:]
            self.data = self.data[0:border] + temp[1:] + self.data[border:]
            
    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        if len(self.data) == 0:
            return True


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        limit = 0
        for index in self.indices:
            if index < self.length/2:
                limit = self.indices.index(index) + 1
            else :
                break
        values1 = self.data[0:limit]
        values2 = self.data[limit:]
        indices1 = self.indices[0:limit]
        indices2 = self.indices[limit:]
        return SparseVector(values1, indices1, self.length/2, self.zero), SparseVector(values2, indices2, self.length - self.length/2 , self.zero)

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        vec = []
        for index in range(0, len(self)):
            vec.append(self[index])
        for index in range(0, len(vector)):
            vec.append(vector[index])
        return make_vector(vec, lambda x : (x == 0))
    

