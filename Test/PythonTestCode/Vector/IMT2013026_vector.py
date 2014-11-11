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
    count = 0
    total_count = 0
    
    for i in lst:
        total_count += 1
        if i != 0:
            count += 1
    if  float(count) / float(total_count) < DENSITY_THRESHOLD and total_count > SIZE_THRESHOLD:
        return True
    else:
        return False


def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    element = []
    indices = []
    
    if is_long_and_sparse(data, zero_test) == True:
        for i in data:
            if i != 0:
                element.append(i)
                indices.append(data.index(i))   
        sparse_vector = SparseVector(element, indices, len(data), zero_test)
        return sparse_vector
        
    else:
        full_vector = FullVector(data, zero_test)
        return full_vector

    
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
        self[i] = val

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        
        for i in self.data:
            if i != 0:
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
        i = 0
        if len(self) <> len(vector):
            return False
        
        for i in range(0, len(vector)):
            if self[i] != vector[i]:
                return False
        return True



    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        
        sum1 = 0
        if len(self) != len(vector):
            return None
        
        for i in range (len(vector)):
                sum1 += vector[i] * self[i] 
    
        return sum1
        
            


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''

        final_vector = []

        if(len(self) != len(vector)):
            return None
                
        for i in range (0, len(vector)):
            if vector[i] != None and self[i] != None:
                    final_vector.append(vector[i] + self[i])
                    
         
        final_vector_obj = make_vector (final_vector, self.zero_test)   
        
        return final_vector_obj


    def __sub__(self, vector):
        
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        final_vector = []
        
        if (len(self) != len(vector)):
            return None

        for i in range (0, len(vector)):
                if vector[i] != None and self[i] != None:
                    final_vector.append(vector[i] - self[i])
                    
        final_vector_obj = make_vector (final_vector, self.zero_test)
        return final_vector_obj


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        
        
        if len(self) == len(vector):
            self = self + vector
        else:
            minimum = min(len(self), len(vector))
            
            for i in range (0, minimum):
                if vector[i] != None and self[i] != None:
                    self[i] += vector[i]
                    
        return self



    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        
                
        if len(self) == len(vector):
            self = self - vector
        else:
            minimum = min(len(self), len(vector))
            
            for i in range (0, minimum):
                if vector[i] != None and self[i] != None:
                    self[i] -= vector[i]
                    
        return self
    

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        if len(self) < 2:
            return None, None
        else:
            left_vector =  make_vector(self[:len(self)/2], None)
            right_vector = make_vector(self[(len(self)/2):], None)
            return left_vector, right_vector

        
        
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
        self.zero_test = zero_test
        
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        
        if len(self) < 2:
            return None, None
        
        else:
            left_vector =  make_vector(self[:len(self)/2], None)
            right_vector = make_vector(self[(len(self)/2):], None)
            return left_vector, right_vector

    def merge(self, vector):
        
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        final_vector = []
        
        for i in range(0, len(self)):
            final_vector.append(self[i])
            
        for j in range(0, len(vector)):
            final_vector.append(vector[j])
            
        return final_vector

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
        self. values = values
        self.indices = indices
        self.length = length
        self.zero_test = zero_test


    def __len__(self):
        '''
        Overriding the defuault __len__ method with behavior specific to sparse vectors
        '''
        
        return len(self.values)
        


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        if i in self.indices:
            return self.values[i]
        return None


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        if i not in self.indices:
            self.indices.insert( bisect_left(self.indices, i), i )
            self.values.insert( bisect_left(self.values, val), val )
        else:
            self.values.insert( bisect_left(self.values, val), val)

    def is_zero(self):
        
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        
        for i in self.data:
            if i == 0:
                return False
        return True
                

    def split(self):
        
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        
        if len(self) < 2:
            return None, None
        
        else:
            left_vector_values =  self[:len(self)/2]
            left_vector_indices = self.indices[:len(self)/2]
            right_vector_values =  self[len(self)/2:]
            right_vector_indices = self.indices[len(self)/2:]
            left_vector_obj = SparseVector(left_vector_values, left_vector_indices, self.count)
            right_vector_obj = SparseVector(right_vector_values, right_vector_indices, self.count)
        return left_vector_obj, right_vector_obj

    def merge(self, vector):
        
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        
        final_vector_values = []
        final_vector_indices = []
    
        for i in range(0, len(self)):
            final_vector_values.append(self[i])
            final_vector_indices.append(self.indices[i])
            
        for i in range(0, len(vector)):
            final_vector_values.append(vector[i])
            final_vector_indices.append(vector.indices[i])
        merged_obj = SparseVector(final_vector_values, final_vector_indices, self.length)
        return merged_obj