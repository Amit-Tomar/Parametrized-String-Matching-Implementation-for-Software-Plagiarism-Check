'''
Created on 16-Nov-2013

@author: raghavan
'''
#from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 50

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    # Your Code
    count = 0
    for i in lst:
        if (zero_test(i)):
            count += 1
    if count >= len(lst)*DENSITY_THRESHOLD:
        return True
            
def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    #print data,
    values , indices = [] , []
    if is_long_and_sparse(data , zero_test):
        #print 'Sparse'
        for i in range(0, len(data)):
            if data[i] != 0 :
                values += [data[i]]
                indices += [i]
        return SparseVector(values, indices, len(data) , zero_test)
    else:
        #print 'Full'
        return FullVector(data, zero_test)
 
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
    
    def add_elem(self, element):
        '''Add the element'''
        self.lst.append(element)

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
        
    def pop(self):
        '''popping the last element'''
        self.lst.pop()
 
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        # Your Code
        for i in range(0, len(self)):
            if self[i] != 0:
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
        for i in range(0, len(self)):
            if (self.zero_test(self[i]-vector[i]) != True):
                return False
        return True
            
    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        if len(self) != len(vector):
            return None
        val = 0
        for i in range(0, len(self)):
            val += (self[i] * vector[i])
        return val
            
    def __add__(self, vector):
        '''
        Return the sum of this columnvector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        if len(self) != len(vector):
            return None
        summed_vect = []
        for i in range(0, len(self)):
            summed_vect.append(self[i] + vector[i])
        return make_vector(summed_vect, self.zero_test)

    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code     
        if len(self) != len(vector):
            return None
        subbed_vect = []
        for i in range(0, len(self)):
            subbed_vect.append(self[i] - vector[i])
        return make_vector(subbed_vect, self.zero_test)

    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        for i in range(0, min(len(self), len(vector))):
            self.lst[i] += vector[i]
              
    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        for i in range(0, min(len(self), len(vector))):
            self.lst[i] -= vector[i]

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        length = len(self)
        lst1, lst2 = self.lst[:length/2], self.lst[length/2:]
        return make_vector(lst1, self.zero_test), \
             make_vector(lst2, self.zero_test)
            
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
        length = len(self)
        lst1, lst2 = make_vector(self.lst[:length/2], self.zero_test), \
         make_vector(self.lst[length/2:], self.zero_test)
        return lst1, lst2

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        for i in range(0, len(self.lst)):
            self.lst.append(vector[i])

class SparseVector(Vector):
    '''
    Vector that has very few non-zero entries
    Values and corresponding indices are kept in separate lists
    '''
    def __init__(self, values, indices, length = 0, \
                  zero_test = lambda x : (x == 0)):
        '''
        'values' argument is the list of non-zero values and the corresponding indices are in the list 'indices'
        Uses the base (parent) class attributes data (this is where 'values' are kept) and zero_test
        Length is the length of the vector - the number of entries in 'values' is just the number of non-zero entries
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseVector, self).__init__(values, zero_test)
        # Your Code
        self.indices = indices
        self.length = length
        
    def add_elem(self, element):
        '''Add an element'''
        if element != 0:
            self.lst.append(element)
            self.indices.append(self.length)
        self.length += 1
        
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
        if i not in self.indices and i < len(self):
            return 0
        elif len(self) == 0:
            return 0
        return self.lst[self.indices.index(i)]

    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate lst into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        if i in self.indices:
            self.lst[self.indices.index(i)] = val
        else:
            self.indices.append(i)
            self.lst.append(val)
    def pop(self):
        self.length -= 1 
            
    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        if len(self.lst) == 0:
            return True
    
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        if len(self.lst) == 0:
            return make_vector([0]*(self.length/2), self.zero_test), \
                 make_vector([0]*(self.length - self.length/2), self.zero_test)
        val1, val2 = [], []
        for i in range(0, self.length):
            if i < self.length/2 and i not in self.indices:
                val1.append(0)
            if i < self.length/2 and i in self.indices:
                val1.append(self[i])
            if i >= self.length/2 and i not in self.indices:
                val2.append(0)
            if i >= self.length/2 and i in self.indices:
                val2.append(self[i])
        return make_vector(val1, self.zero_test), \
         make_vector(val2, self.zero_test)

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        if isinstance(vector, SparseVector):
            for i in range(0, len(vector)):
                self.lst.append(vector[i])
                if i in vector.indices:
                    self.indices.append(vector.indices[i] + len(self) -1)
        else:
            for i in range(0, self.length):
                self.lst.append(vector[i])
                self.indices.append(i + self.length -1)
        self.length += vector.length