'''
Created on 16-Nov-2013

@author: raghavan
'''

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 50

from bisect import bisect_left
#from matrix import A_COLUMNS, COLUMNS

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    # Your Code
    count = 0
    for elem in lst:
        if zero_test(elem):
            count += 1
    if len(lst) > 5 and count/(len(lst)*1.0) > DENSITY_THRESHOLD:
        return True
    return False

def make_vector(data, zero_test = lambda x : (x == 0)):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    '''if len(A_COLUMNS)==2 :
        if len(data)==A_COLUMNS[1]:
            side = A_COLUMNS[1] - COLUMNS[1]
            data = data[:len(data)-side]'''
    if not is_long_and_sparse(data, zero_test):
        vector = FullVector(data, zero_test)
    else:
        values = []
        indices = []
        for i in range(len(data)):
            if zero_test(data[i]) == False:
                values.append(data[i])
                indices.append(i)
        vector = SparseVector(values, indices, len(data), zero_test)
        
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
        self.zero_test = zero_test


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
        if i < len(self.data):
            return self.data[i]
        else:
            return 0
    

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
        for i in range(len(self.data)):
            if self.zero_test(self.data[i]) == False:
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
        for i in range(len(vector)):
            if vector[i] != self.data[i]:
                return False
        return True

    '''def __mul__(self, vector):
        '''
    ''' Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None'''
    '''
        # Your Code
        if len(vector) != len(self.data):
            return None
        i = 0
        dot_prod = 0
        for elem in vector.components():
            dot_prod += elem * self.data[i]
            i += 1
        return dot_prod
    '''
    
    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        if len(vector) != len(self.data):
            return None
        i = 0
        sum_vectors = []
        for elem in self.components():
            sum_vectors.append(elem + vector[i])
            i += 1
        return make_vector(sum_vectors, self.zero_test)
        

    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        if len(vector) != len(self.data):
            return None
        i = 0
        sub_vector = []
        for elem in vector.components():
            sub_vector.append(self.data[i] - elem)
            i += 1
        return make_vector(sub_vector, self.zero_test)


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        if len(vector) < len(self.data):
            min_len = len(vector)
        else:
            min_len = len(self.data)
        i = 0
        for elem in vector.components():
            self.data[i] = (elem + self.data[i])
            i += 1
            if i >= min_len:
                break
        return self
        
    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        if len(vector) < len(self.data):
            min_len = len(vector)
        else:
            min_len = len(self.data)
        
        i = 0
        for elem in vector.components():
            self.data[i] = (self.data[i] - elem)
            i += 1
            if i >= min_len:
                break
        return self   
            
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        return None, None
    
    def Slicing(self, side):
        self = self[:len(self)-side]
        return make_vector(self)
        
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
        return make_vector(self.data[:int((len(self.data)+1)//2)], self.zero_test), make_vector(self.data[int((len(self.data)+1)//2):], self.zero_test)

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        merged = []
        for elem in self.components():
            merged.append(elem)
        for elem in vector.components():
            merged.append(elem)
            
        return make_vector(merged)


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
        self.length = length
        self.zero_test = zero_test


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
            return self.values[self.indices.index(i)]
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
            self.values[i] = val
        else:
            self.indices.append(i)
            self.values.append(val)
            
    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        if len(self.values) == 0:
            return True
        return False

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        lst = []
        mid_point = int(self.length//2) 
        for i in range(self.length):
            if i in self.indices:
                lst.append(self.values[self.indices.index(i)])
            else:
                lst.append(0)
            
        return make_vector(lst[:mid_point]),  make_vector(lst[mid_point:])

        
    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        count = len(self)
        for i in range(len(vector)):
            self[count] = vector[i]
            #print count
            #print self[count]
            count += 1
        return self
    
    def Slicing(self, side):
        self = self[:len(self)-side]
        return make_vector(self)
