'''
Created on 16-Nov-2013

@author: raghavan
'''

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 5
zero_test = lambda x : (x == 0)

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    if(len(lst) >= SIZE_THRESHOLD):
        count = 0.0
        for elem in lst:
            if(elem == 0):
                count += 1
        if((count/len(lst))>=DENSITY_THRESHOLD):
            return True
    return False
    # Your Code

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    if(is_long_and_sparse(data, zero_test)):
        temp_data = [elem for elem in enumerate(data) if (elem[1] != 0)]
        values = [elem[1] for elem in temp_data]
        indices = [elem[0] for elem in temp_data]
        return SparseVector(values, indices, len(data))
    else:
        return FullVector(data, zero_test)
    # Your Code
    
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
        # Your Code

    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        return len(self.lst)
        # Your Code


    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        return self.lst[i]
        # Your Code
    

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        self.lst[i] = val
        # Your Code
    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        for elem in self.lst:
            if(elem != 0):
                return False
        return True
        # Your Code


        '''
        def components(self):
        
        Allows one to iterate through the elements of the vector as shown below
        for elem in vector.components(): (vector is an object of type Vector or any of its derived classes)
        
        for i in xrange(len(self)):
            yield self[i]
        '''


    def __eq__(self, vector):
        '''
        Check if this vector is identical to another 'vector' (allows use of operator == to compare vectors)
        '''
        if(len(self) != len(vector)):
            return False
        
        for pos in range(len(vector)):
            if(vector[pos] != self[pos]):
                return False
        return True
        # Your Code


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if (len(self) == len(vector)):
            dot_prod = []
            for pos in range(len(self)):
                dot_prod.append(self[pos]*vector[pos])
            return make_vector(dot_prod, self.zero_test)
        # Your Code


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if(len(self) == len(vector)):
            sum = []
            for pos in range(len(self)):
                sum.append(self[pos]+vector[pos])
            return make_vector(sum, self.zero_test)
        # Your Code


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if(len(self) == len(vector)):
            diff = []
            for pos in range(len(self)):
                diff.append(self[pos]-vector[pos])
            return make_vector(diff, self.zero_test)
        # Your Code


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        
        for pos in xrange(len(self)):
            if(pos<len(vector)):
                self[pos] = self[pos] + vector[pos]
        return self
        
        
        # Your Code


    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        for pos in xrange(len(self)):
            if(pos<len(vector)):
                self[pos] = self[pos] - vector[pos]
        return self
        # Your Code
    
    
    
        
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        first_half, second_half = self[:(len(self)/2)], self[(len(self)/2):]
        return make_vector(first_half, self.zero_test), \
            make_vector(second_half, self.zero_test)
    
    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        gen_vec_self = self[:]
        gen_vec_vector = vector[:]
        joint_vector = gen_vec_self + gen_vec_vector
        return make_vector(joint_vector, zero_test)
    
    
        
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

        

    
        # Your Code


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
        self.length = length
        # Your Code


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        return self.length
        
        # Your Code


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        '''temp_list = [0]*len(self)
        for pos in range(len(self.indices)):
            temp_list[self.indices[pos]] = self.lst[pos]
        return temp_list[i]'''
        if(isinstance(i, int)):
            if(i in self.indices):
                return self.lst[self.indices.index(i)]
            return 0
        else:
            temp_list = [0]*len(self)
            for pos in range(len(self.indices)):
                temp_list[self.indices[pos]] = self.lst[pos]
            return temp_list[i]
        # Your Code


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        
        if(i in self.indices):
            self.lst[self.indices.index(i)] = val
        else:
            if val != 0:
                self.lst.append(val)
                self.indices.append(i)
        # Your Code
