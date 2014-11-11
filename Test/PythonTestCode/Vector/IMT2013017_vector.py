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
    for i in lst:
        if (i == 0) :
            count = count + 1
    if ((len(lst) >= SIZE_THRESHOLD) and ((count/len(lst)) >= DENSITY_THRESHOLD)) :
        return True
    

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    if is_long_and_sparse(data, zero_test):
        values = []
        indices = []
        for i, value in enumerate(data):
            if value != 0:
                values.append(value)
                indices.append(i)       
        vector = SparseVector(values ,indices ,len(indices) ,zero_test)       
    else:
        vector = FullVector(data ,zero_test)
       
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
        self.lst=lst
        self.zero_test=zero_test


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
            if i == 0:
                count = count + 1
        if (count == len(self.lst)):
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
        if len(vector) == len(self.lst):
            for i in range(len(self.lst)):
                if (self.lst[i] != vector[i]):
                    return False
                else:
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
        if len(vector) != len(self.lst):
            return None
        else:
            for i in range(len(self.lst)):
                dot_product = dot_product + (self.lst[i] * vector[i])
            return dot_product


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        add_vector = []
        if len(vector) != len(self.lst):
            return None
        else:
            for i in range(len(self)):
                x = 0
                x = x + (self.lst[i] + vector[i])
                add_vector.append(x)
            return make_vector(add_vector, self.zero_test)
        
    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        subst_vector = []
        if len(vector) != len(self.lst):
            return None
        else:
            for i in range(len(self.lst)):
                subst_vector.append(self.lst[i] - vector[i])
            return make_vector(subst_vector, self.zero_test)


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        iadd_vector = []
        for i in range(min(len(self.lst),len(vector))):
            iadd_vector.append(self.lst[i] + vector[i])
        if len(vector) < len(self.lst):
            for i in range(len(vector)+1,len(self.lst)):
                iadd_vector.append(self.lst[i])
        elif len(self.lst) < len(vector):
            for i in range(len(self.lst)+1,len(vector)):
                iadd_vector.append(vector[i])
        return make_vector(iadd_vector, self.zero_test)

    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        isub_vector = []
        for i in range(min(len(self.lst),len(vector))):
            isub_vector.append(self.lst[i] - vector[i])
        if len(vector) < len(self.lst):
            for i in range(len(vector)+1,len(self.lst)):
                isub_vector.append(self.lst[i])
        elif len(self.lst) < len(vector):
            for i in range(len(self.lst)+1,len(vector)):
                isub_vector.append(vector[i])
        return make_vector(isub_vector, self.zero_test)


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
        left_half = []
        right_half= []
        
        if((len(self) % 2) != 0):
            for i in range((len(self.lst)/2) + 1 , len(self.lst)):
                right_half.append(self.lst[i])
            for i in range( 0 , (len(self.lst)/2) + 1):
                left_half.append(self.lst[i])
        else:
            for i in range(len(self.lst)/2 , len(self.lst)):
                right_half.append(self.lst[i])
            for i in range( 0 , len(self.lst)/2 ):
                left_half.append(self.lst[i])
        
        return left_half,right_half 

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        for i in range( 0 , len(vector) ):
            self.lst.append(vector[i])
            
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
        self.zero_test = zero_test
        self.length = length


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        # Your Code
        return len(self.lst)


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        # Your Code
        return self.lst[i]


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        self.lst[i] = val

    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        count = 0
        for i in self.lst:
            if (i == 0):
                count = count + 1
        if (count == len(self.lst)):
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
        left_half = []
        right_half = []
        if((len(self.lst) % 2) == 0):
            l = len(self.lst)/2
        else:
            l = len(self.lst)/2 + 1
        for i in range(l):
            left_half.append(self.lst[i])
            left_vector = make_vector(left_half,self.zero_test)
        for i in range(len(right_half)):
            right_half.append(self.lst[i])
            right_vector = make_vector(right_half,self.zero_test)
        return left_vector,right_vector

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        for i in range( 0 , len(vector) ):
            self.lst.append(vector[i])
        