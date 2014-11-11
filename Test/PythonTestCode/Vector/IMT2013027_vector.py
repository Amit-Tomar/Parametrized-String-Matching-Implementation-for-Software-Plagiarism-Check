'''
Created on 16-Nov-2013

@author: raghavan

Modified on 12-Dec-2013

@modifier: Nigel Steven Fernandez (IMT2013027)
'''

from bisect import bisect_left
import itertools

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 50


def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    is_long = len(lst) >= SIZE_THRESHOLD
    is_sparse = (len([elem for elem in lst if zero_test(elem)]) / float(len(lst))) >= DENSITY_THRESHOLD
    
    return is_long and is_sparse


def make_vector(data, zero_test = lambda x : (x == 0)):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    if(is_long_and_sparse(data, zero_test)):
        if(sum(data) != 0):
            #creating 2 lists simultaneously
            indices, values = zip(*[(index, element) for index, element in enumerate(data) if (not zero_test(element))])
        else:
            indices, values = [], []
        vector = SparseVector(list(values), list(indices), len(data), zero_test)
    else:
        vector = FullVector(data, zero_test)
    
    return vector

    
class Vector(object):
    '''
    Base Vector class - implements a number of the common methods required for a Vector
    '''    
    def __init__(self, lst, zero_test):
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
        
        return None

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        return len([elem for elem in self.data if (not self.zero_test(elem))]) == 0


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
        if(type(vector) == FullVector):
            return list(self.components()) == list(vector.components())
        else:
            return False


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if(not isinstance(vector, Vector)):
            return NotImplemented
        elif(len(self) == len(vector)):
            return sum([(elem1 * elem2) for elem1, elem2 in itertools.izip(self.components(), vector.components())])
        else:
            return None


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if(len(self) == len(vector)):
            return make_vector([(elem1 + elem2) 
                                for elem1, elem2 in itertools.izip(self.components(), vector.components())], 
                                self.zero_test)
        else:
            return None


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if(len(self) == len(vector)):
            return make_vector([(elem1 - elem2) for elem1, elem2 in 
                                itertools.izip(self.components(), vector.components())],
                                self.zero_test)
        else:
            return None
        

    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        if(len(self) <= len(vector)):
            self = make_vector([(elem1 + elem2) for elem1, elem2 in 
                                itertools.izip(self.components(), vector.components())],
                                self.zero_test)
        else:
            self = make_vector([(elem1 + elem2) for elem1, elem2 in 
                                itertools.izip_longest(self.components(), vector.components(), fillvalue = 0)],
                                self.zero_test)
            
        return self


    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        
        if(len(self) <= len(vector)):
            self = make_vector([(elem1 - elem2) for elem1, elem2 in 
                                itertools.izip(self.components(), vector.components())],
                                self.zero_test)
        else:
            self = make_vector([(elem1 - elem2) for elem1, elem2 in 
                                itertools.izip_longest(self.components(), vector.components(), fillvalue = 0)],
                                self.zero_test)
            
        return self


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''      
        #The vector passed will already be padded to the nearest power of 2  
        data = list(self.components())
        left_vector = make_vector(data[0 : (len(data) / 2)], self.zero_test)
        right_vector = make_vector(data[(len(data) / 2) : len(data)], self.zero_test)
        
        return left_vector, right_vector
    
    
    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        self = make_vector(list(self.components()) + list(vector.components()), self.zero_test)
        
        return self
        
                
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
        return super(FullVector, self).split()


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        return super(FullVector, self).merge(vector)


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
        self.indices = indices
        #If no length is passed, the length is assumed to be =  (highest index + 1)
        if(length == 0):
            self.length = indices[-1] + 1
        else:
            self.length = length
        

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        return self.length


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        #taking care of negative index
        if(i < 0):
            i = len(self) + i
        #using bisection algorithm in sorted list - 'indices'
        index_of_i = bisect_left(self.indices, i)
        
        if(index_of_i != len(self.indices) and self.indices[index_of_i] == i):
            return self.data[index_of_i]
        else:
            return 0


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        #taking care of negative index
        if(i < 0):
            i = len(self) + i
        #using bisection algorithm in sorted list - 'indices'        
        index_of_i = bisect_left(self.indices, i)
        
        #if i is in indices list
        if(index_of_i != len(self.indices) and self.indices[index_of_i] == i):
            if(val != 0):
                self.data[index_of_i] = val
            else:
                del self.indices[index_of_i]
                del self.data[index_of_i]
        else:
            if(val != 0):
                index_to_insert = bisect_left(self.indices, i)
                self.indices.insert(index_to_insert, i)
                self.data.insert(index_to_insert, val)
        
        return None


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        return len(self.data) == 0


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        #Calling split method of Vector class because
        #splitting a sparse vector may produce a full vector as one half. 
        #Therefore expanding a sparse vector into its components.
        return super(SparseVector, self).split()
        

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        if(type(vector) == FullVector):
            return super(SparseVector, self).merge(vector)
        else:
            #Sparse vector merged with another sparse vector = sparse vector
            self.data = self.data + vector.data
            self.indices = self.indices + [len(self) + index for index in vector.indices]
            self.length += vector.length
    
        return self
    
    
    def __eq__(self, vector):
        '''
        Check if this vector is identical to another 'vector' (allows use of operator == to compare vectors)
        Overrides default implementation of this method in Vector class
        '''
        if(type(vector) == SparseVector):
            return [self.data, self.indices, self.length] == [vector.data, vector.indices, vector.length]
        else:
            return False