'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
import math
DENSITY_THRESHOLD = 0.6
SIZE_THRESHOLD = 50

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    # Your Code
    i, length = 0, len(lst)
    for ele in lst:
        if not zero_test(ele):
            i += 1
    if(((i/length) <= DENSITY_THRESHOLD) and (length >= SIZE_THRESHOLD)):
        return True

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    indices = []
    values = []
    if is_long_and_sparse(data, zero_test):
        for i in len(data):
            if not zero_test(data[i]):
                values.append(data[i])
                indices.append(i)
        vector = SparseVector(values, indices, len(data), zero_test)
        return vector
    else:
        vector = FullVector(data, zero_test)        
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
        counter = 0
        for i in range(len(self)):
            if self.zero_test(self[i]):
                counter += 1
        if (counter == len(self)):
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
        counter = 0
        if ( len(self) <> len(vector) ):
            return False
        else:
            for i in range(len(self)):
                if(self[i] == vector[i]):
                    counter += 1
            if(counter == len(self)):
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
        mul_of_vector = 0
        if(len(self) <> len(vector)):
            return None
        else:
            for i in range(len(self)):
                mul_of_vector += self[i]*vector[i]
            return mul_of_vector 


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        sum_of_vectors = []
        new_vector = make_vector(vector.data, self.zero_test)
        if(len(self) <> len(new_vector)):
            return None
        else:
            for i in range(len(self)):
                sum_of_vectors.append(self[i] + new_vector[i])
            sum_vector  = make_vector(sum_of_vectors, self.zero_test)
            return sum_vector

    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        new_vector = make_vector(vector.data, self.zero_test)
        sub_of_vectors = []
        if(len(self) <> len(new_vector)):
            return None
        else:
            for i in range(len(self)):
                sub_of_vectors.append(self[i]-new_vector[i])
            sub_vector = make_vector(sub_of_vectors, self.zero_test)
            return sub_vector
        

    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        minlen = min(len(self), len(vector))
        sum_of_vectors = []
        for i in range(minlen):
            sum_of_vectors.append(self[i]+vector[i])
        sum_vector = make_vector(sum_of_vectors, self.zero_test)
        return sum_vector 
        

    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        minlen = min(len(self), len(vector))
        sub_of_vectors = []
        for i in range(minlen):
            sub_of_vectors.append(self[i]-vector[i])
        sub_vector = make_vector(sub_of_vectors, self.zero_test)
        return sub_vector

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
        l_part = math.floor(len(self)/2)
        r_part = math.ceil(len(self)/2)
        left_part = self.lst[:int(l_part)]
        right_part = self.lst[int(r_part):]
        left_vector = make_vector(left_part,self.zero_test)
        right_vector = make_vector(right_part,self.zero_test)
        return left_vector, right_vector


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        for ele in vector.lst:
            self.lst += [ele]
                

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
        self.Data = values
        self.indices = indices
        self.length = length
        self.zero_test = zero_test

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        # Your Code
        return len(self.Data)

    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        # Your Code
        if i in self.indices:
            ele_index = self.indices.index(i)
            return self.Data[ele_index]
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
            j = self.indices.index(i)
            self.Data[j] = val 
        else:
            self.indices.append(i)
            self.Data.append(val)

    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        counter = 0
        for i in range(len(self)):
            if self.zero_test(self[i]):
                counter += 1
        if (counter == len(self)):
            return True
        

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        l_part, l_ind = math.floor( len(self)/2 ), math.floor( len(self.indices)/2 )
        r_part, r_ind = math.ceil( len(self)/2 ), math.ceil( len(self.indices)/2 )
        left_part, left_ind = self.Data[:int(l_part)], self.indices[:int(l_ind)]
        right_part, right_ind = self.Data[int(r_part):], self.indices[int(r_ind):]
        left_vector = SparseVector(left_part, left_ind, self.length, self.zero_test)
        right_vector = SparseVector(right_part, right_ind, self.length ,self.zero_test)
        
        return left_vector, right_vector

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        '''merged_list= [] 
        indices_list = []
        for i in range(len(self)):
            merged_list.append(self[i])
            merged_list.append(vector[i])
            indices_list.append(i)
        merged_vector = SparseVector(merged_list, indices_list, self.length, self.zero_test)
        return merged_vector'''
        for ele in vector.Data:
            self.Data += [ele]