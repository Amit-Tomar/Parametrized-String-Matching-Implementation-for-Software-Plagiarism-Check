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
    zero_count = 0
    length = len(lst)
    for elem in lst:
        if elem != 0:
            zero_count += 1
        else:
            continue
    if length >= SIZE_THRESHOLD and DENSITY_THRESHOLD * length <= zero_count:
        return True
    else:
        return False
        
        

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    indices = []
    values = []
    if (is_long_and_sparse(data, zero_test)==True):
        for i in range(0 , len(data)):
            if data[i] != 0:
                values.append(data[i])
                indices.append(i)
                return SparseVector(values , indices)
            else:
                continue
    else:
        return FullVector(data)
    
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
        self.lst = lst
        self.zero_test = zero_test


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
        self.lst[i] = val

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        # Your Code
        count = 0
        for i in self.lst:
            if self.lst[i] != 0:
                count += 1
            else:
                continue
        if count == 0:
            return True
        else:
            return False
            

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
        for i in range(0 , len(vector)):
            if self[i] == vector[i]:
                return True
            else:
                return False

    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        dot_product = 0
        if(len(self.lst)==len(vector)):
            for i in range(0 , len(vector)):
                dot_product = dot_product + (self.lst[i]*vector[i])
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
        add_vector = []
        if(len(self.lst)==len(vector)):
            for i in range(0 , len(vector)):
                add_vector.append(self.lst[i]+vector[i])
            return make_vector(add_vector , self.zero_test)
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
        sub_vector = []
        if(len(self.lst)==len(vector)):
            for i in range(0 , len(vector)):
                sub_vector.append(self.lst[i]-vector[i])
            return make_vector(sub_vector , self.zero_test)
        else:
            return None

    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        if(len(self.lst)==len(vector)):
            for i in range(0 , len(vector)):
                self.lst[i] = self.lst[i] + vector[i]
            return make_vector(self.lst , self.zero_test)
        else:
            if(len(self.lst) > len(vector)):
                for i in range(0 , len(vector)):
                    self.lst[i] = self.lst[i] + vector[i]
                return make_vector(self.lst , self.zero_test)
            else:
                for i in range(0 , len(self.lst)):
                    self.lst[i] = self.lst[i] + vector[i]
                return make_vector(self.lst , self.zero_test)
        

    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        if(len(self.lst)==len(vector)):
            for i in range(0 , len(vector)):
                self.lst[i] = self.lst[i] - vector[i]
            return make_vector(self.lst , self.zero_test)
        else:
            if(len(self.lst) > len(vector)):
                for i in range(0 , len(vector)):
                    self.lst[i] = self.lst[i] - vector[i]
                return make_vector(self.lst , self.zero_test)
            else:
                for i in range(0 , len(self.lst)):
                    self.lst[i] = self.lst[i] - vector[i]
                return make_vector(self.lst , self.zero_test)

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

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        matrix = len(self.lst)
        length = matrix/2
        if(matrix%2==0):
            even = [self.lst[i:i+length] for i in range(0, matrix, length)]
            return even[0] , even[1]
        else:
            odd = [self.lst[i:i+length+1] for i in range(0, matrix, length+1)]
            return odd[0] , odd[1]

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        self.lst = self.lst + vector


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
        self.values = values
        self.indices = indices


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        # Your Code
        return len(self.values)


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        # Your Code
        return self.values[i]


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        for i in range(0 , len(self.indices)):
            if i in self.indices:
                self.values[i] = val
            else:
                self.indices.append(i)
                self.values[i] = val
                
    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        count = 0
        for i in self.indices:
            if self.values[i] != 0:
                count += 1
            else:
                continue
        if count == 0:
            return True
        else:
            return False


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        
        matrix = len(self.indices)
        length = matrix/2
        if(matrix%2==0):
            even_val = [self.values[i:i+length] for i in range(0, matrix, length)]
            even_ind = [self.indices[i:i+length] for i in range(0, matrix, length)]
            return even_val[0] , even_ind[0], even_val[1] , even_ind[1]
        else:
            odd_val = [self.values[i:i+length+1] for i in range(0, matrix, length+1)]
            odd_ind = [self.indices[i:i+length+1] for i in range(0, matrix, length+1)]
            return odd_val[0] , odd_ind[0], odd_val[1] , odd_ind[1]
        self.even_val = even_val
        self.even_ind = even_ind
        self.odd_val = odd_val
        self.odd_ind = odd_ind

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        length = len(vector)
        if(length%2==0):
            self.split(vector)
            self.indices = self.indices + self.even_ind
            self.values = self.values + self.even_val
        else:
            self.split(vector)
            self.indices = self.indices + self.odd_ind
            self.values = self.values + self.odd_val