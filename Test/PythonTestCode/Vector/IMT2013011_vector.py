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
    counter = 0
    if len(lst) > SIZE_THRESHOLD:
        for i in lst:
            if zero_test(i):
                counter  += 1
                
        dens = counter/len(lst)
        
        if dens >= DENSITY_THRESHOLD:
            return True
    return False 


def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''

    if not is_long_and_sparse(data, zero_test):
        n_vect = FullVector(data)
    else:
        values = []
        indices = []
        for i in range(len(data)):
            if not zero_test(data[i]):
                values.append(data[i])
                indices.append(i)
        n_vect = SparseVector(values, indices, len(data))
    return n_vect

    
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
        self.lst = lst
        self.zero_test = zero_test        


    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        return len(self.lst)


    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        return self.lst[i]
    

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        self.lst[i] = val

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        for i in self:
            if not self.zero_test(i):
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
        if len(self) == len(vector):
            for i in range(len(vector)):
                if self[i] != vector[i]:
                    return False
            return True
        return False


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if len(self) != len(vector):
            return None
        mul_vect = 0
        for i in range(len(vector)):
            mul_vect += self[i]*vector[i]

        return mul_vect


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if len(self) != len(vector):
            return None
        add_vector = []
        for i in range(len(vector)):
            add_vector.append(self[i] + vector[i])
        vect = make_vector(add_vector, self.zero_test)
        return vect


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if len(self) != len(vector):
            return None
        sub_vector = []
        for i in range(len(vector)):
            sub_vector.append(self[i] - vector[i])
        vect = make_vector(sub_vector, self.zero_test)
        return vect


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        minimum = min(len(self), len(vector))
        for i in range(minimum):
            self[i] = self[i] + vector[i]


    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        minimum = min(len(self), len(vector))
        for i in range(minimum):
            self[i] = self[i] - vector[i]


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
        left = self[:len(self)//2]
        right = self[len(self)//2:]
        return make_vector(left, self.zero_test), make_vector(right, self.zero_test)


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        merge_vector = []
        for i in range(len(self)):
            merge_vector.append(self[i])
        for i in range(len(vector)):
            merge_vector.append(vector[i])
        return merge_vector


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
        self.length = length
        self.indices = indices


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        return len(self.lst)


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        if i >= self.length:
            return None
        if i in self.indices:
            return self.lst[self.indices.index(i)]
        return 0


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        if i not in self.indices:
            self.indices.append(i)
            self.lst.append(val)
        else:
            self[self.indices.index(i)] = val


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        for i in range(len(self)):
            if self.zero_test(self[i]) == False:
                return False
        return True


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''

        lval = []
        rval = []
        lind = []
        rind = []
        for i in range(len(self)):
            if self.indices[i] < self.length//2:
                lval.append(self[i])
                lind.append(self.indices[i])
            else:
                rval.append(self[i])
                rind.append(self.indices[i])

        left = SparseVector(lval, lind , self.length//2, self.zero_test)
        right = SparseVector(rval, rind , self.length - self.length//2)
        return left, right


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        merge_value = []
        merge_indice = []
        for i in range(len(self)):
            merge_value.append(self[i])
            merge_indice.append(self.indices[i])
        for i in range(len(vector)):
            merge_value.append(vector[i])
            merge_indice.append(self.indices[i])
        merge_vect = SparseVector(merge_value, merge_indice, self.length, vector.length)
        return merge_vect