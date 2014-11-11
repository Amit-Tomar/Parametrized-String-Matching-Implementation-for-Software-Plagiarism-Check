'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 50

ZERO_TEST = lambda x : (x == 0)

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    nonzero_count = len([elem for elem in lst if not zero_test(elem)])
    # True if the vector is long enough and there are enough number of non zero entries
    return (len(lst) > SIZE_THRESHOLD and nonzero_count < (len(lst) * DENSITY_THRESHOLD))

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    vector = None
    if (is_long_and_sparse(data, zero_test)):
        indices = []
        elems = []
        for idx, elem in enumerate(data):
            if not zero_test(elem):
                indices.append(idx)
                elems.append(elem)
        vector = SparseVector(elems, indices, len(data))
    else:
        vector = FullVector(data)
    return vector

    
class Vector(object):
    '''
    Base Vector class - implements a number of the common methods required for a Vector
    '''
    def __init__(self, lst, zero_test = ZERO_TEST):
        '''
        Have a data attribute that is initialized to the list of elements given in the argument 'lst'
        zero_test is a function that tests if a given element is zero (remember you could potentially
        have a vector of complex numbers, even a vector of functions, ... not just numbers 
        '''
        self.data = lst
        self.zero_test = zero_test


    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        return len(self.data)


    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        return self.data[i]
    

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        self.data[i] = val

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        return (len([x for x in self.data if not self.zero_test(x)]) == 0)


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
        if (len(self) != len(vector)):
            return False
        else:
            for i in range(len(self)):
                if (self[i] != vector[i]):
                    return False
            return True


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        return sum([(self[i]*vector[i]) for i in range(len(self))]) if (len(vector) == len(self)) else None


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if (len(vector) != len(self)):
            return None
    
        return make_vector([(self[i] + vector[i]) for i in range(len(self))], self.zero_test)


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if (len(vector) != len(self)):
            return None
    
        return make_vector([(self[i] - vector[i]) for i in range(len(self))], self.zero_test)


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        for i in range(min(len(self), len(vector))):
            self[i] += vector[i]
        return self


    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        for i in range(min(len(self), len(vector))):
            self[i] -= vector[i]
        return self

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        return None, None
        
        
    def __str__(self):
        lststr = '['
        for i in range(len(self)):
            lststr += str(self[i]) + ', '
        lststr = lststr[:-2] + ']'
        return lststr
            
        
class FullVector(Vector):
    '''
    A subclass of Vector where all elements are kept explicitly as a list
    '''
    def __init__(self, lst, zero_test = ZERO_TEST):
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
        lenby2 = len(self)/2
        left = FullVector(self.data[:lenby2])
        right = FullVector(self.data[lenby2:])
        return left, right


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        return FullVector((self.data + vector.data), self.zero_test)


class SparseVector(Vector):
    '''
    Vector that has very few non-zero entries
    Values and corresponding indices are kept in separate lists
    '''
    def __init__(self, values, indices, length = 0, zero_test = ZERO_TEST):
        '''
        'values' argument is the list of non-zero values and the corresponding indices are in the list 'indices'
        Uses the base (parent) class attributes data (this is where 'values' are kept) and zero_test
        Length is the length of the vector - the number of entries in 'values' is just the number of non-zero entries
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseVector, self).__init__(values, zero_test)
        self.indices = indices
        self.size = max(indices[-1], length) if (len(indices) > 0) else length


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        return self.size


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        idx = bisect_left(self.indices, i)
        return self.data[idx] if (idx < len(self.indices) and self.indices[idx] == i) else 0


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        idx = bisect_left(self.indices, i)
        if (idx < len(self.indices) and self.indices[idx] == i):
            self.data[idx] = val
        else:
            self.data.insert(idx, val)
            self.indices.insert(idx, i)


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        return (len(self.data) == 0)


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        lenby2 = len(self)/2
        idx = bisect_left(self.indices, lenby2)
        all_zeros = SparseVector([], [], lenby2)
        left = all_zeros if (idx == 0) else SparseVector(self.data[:idx], self.indices[:idx], lenby2)
        right_indices = [(index - lenby2) for index in self.indices[idx:]]
        right =(all_zeros   if (idx == len(self.indices)) 
                            else SparseVector(self.data[idx:], right_indices, (len(self) - lenby2)))
        return left, right


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        shift_indices = [(vector.indices[i] + len(self)) for i in range(len(vector.indices))]
        return SparseVector((self.data + vector.data), (self.indices + shift_indices), (len(self) + len(vector)),
                            self.zero_test)
