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
    global list_len
    list_len = len(lst)
    if(list_len > SIZE_THRESHOLD):
        count_zero = 0
        for x in range(0, list_len-1):
            if(lst(x) == "0"):
                count_zero += 1
        part_zero = (count_zero/list_len)
        if(part_zero > DENSITY_THRESHOLD):
            return True
        else:
            return False
    else:
        return False
        
        
def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    length = len(data)
    if(is_long_and_sparse(data,None) == True):
        values = []
        indices = []
        for i in data:
            if(i != 0):
                values.append[i]
                indices.append[data.index(i)]
        sparse_vector = SparseVector(values,indices,length)
        
        return sparse_vector
    
    else:
        full_vector = FullVector(data)
    
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
        self.given_vector = lst
        


    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        return len(self.given_vector)


    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        if(i<=len(self)):
            return self.given_vector[i]
        else:
            return None

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        self.given_vector[i] = val

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        
        for i in self.given_vector:
            if(i != 0):
                return False
        return True
            
    def components(self):
        '''
        DENSITY_THRESHOLD Allows one to iterate through the elements of the vector as shown below
        for elem in vector.components(): (vector is an object of type Vector or any of its derived classes)
        '''
        for i in xrange(len(self)):
            yield self[i]


    def __eq__(self, vector):
        '''
        Check if this vector is identical to another 'vector' (allows use of operator == to compare vectors)
        '''
        if(len(self) != len(vector)):
         return False
        else:
            for i in range(0, len(self)-1):
                if(self.given_vector(i) != vector(i)):
                    return False
            return True 


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        vector_mult = []
        if(len(self) != len(vector)):
            return False
        else:
            for i in range(0, len(self)):
                vector_mult.append(self.given_vector[i] * vector[i])
            
            final = 0
            for i in vector_mult:
                final = final+ i
        
        return final

    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        vector_add = []
        if(len(self) != len(vector)):
            return None
        else:
            for i in range(0, len(self)):
                vector_add.append(self.given_vector[i] + vector[i])
        
        vector_sum = make_vector(vector_add,None)
        return vector_add


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        vector_sub = []
        if(len(self) != len(vector)):
            return False
        else:
            for i in range(0, len(self)):
                vector_sub.append(self.given_vector[i] - vector[i])
        
        vector_diff = make_vector(vector_sub,None)
        return vector_diff


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        if(len(self) == len(vector)):
            for i in range(0, len(self)):
                self.given_vector[i] = self.given_vector[i]+vector[i]
            return self.given_vector
        
        else:
            len_self = len(self)
            len_vector = len(vector)
            if(len_self > len_vector):
                for i in range(0, len_vector):
                    self.given_vector[i] = self.given_vector[i] + vector[i]
                return self.given_vector
            else:
                for i in range(0, len_self):
                    self.given_vector[i] = self.given_vector[i] + vector[i]
                return self.given_vector
                



    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        if(len(self) == len(vector)):
            for i in range(0, len(self)-1):
                self.given_vector[i] = self.given_vector[i]-vector[i]
            return self.given_vector
        else:
            len_self = len(self)
            len_var = len(vector)
            if(len_self > len_var):
                for i in range(0, len_var):
                    self.given_vector[i] = self.given_vector[i] - vector[i]
                return self.given_vector
            else:
                for i in range(0, len_self):
                    self.given_vector[i] = self.given_vector[i] - vector[i]
                return self.given_vector
                

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        return self.given_vector[0:len(self)/2],self.given_vector[len(self)/2 :]
            
        
        
        
        
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
        self.intial_vector = lst
        
        
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        
        left_vector = self.given_vector[0:len(self)/2]
        right_vector = self.given_vector[len(self)/2:]
        return left_vector,right_vector
        



    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        for i in vector:
            self.initial_vector.append[i]
        


class SparseVector(Vector):
    '''
    Vector that has very few non-zero entries
    Values and corresponding indices are kept in separate lists
    '''
    def __init__(self, values, indices, length , zero_test = lambda x : (x == 0)):
        '''
        'values' argument is the list of non-zero values and the corresponding indices are in the list 'indices'
        Uses the base (parent) class attributes data (this is where 'values' are kept) and zero_test
        Length is the length of the vector - the number of entries in 'values' is just the number of non-zero entries
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseVector, self).__init__(values, zero_test)
        # Your Code
        self.length = length
        self.values_vector = values
        self.indices_vector = indices

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        return len(self.indices_vector)
        

    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        if(i> self.length):
            return None
        
        for val in indices:
            if(val == i):
                index_val = self.indices_vector.index[i]
                return self.values_vector[index_val]
            else:
                return 0

    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        for x in self.indices_vector:
            if(x == i):
                self.values_vector[self.indices_vector.index(x)] == val
            else:
                self.indices_vector.append[x]
                self.values_vector.append[val]
                
        
    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        if(len(self.values_vector) == 0): 
            return True
        else:
            return False

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        x = list_len
        for element in vector:
            if(element != 0):
                self.values_vector.append[element]
                self.indices_vector.append[x]
            else:
                x += 1



vec = make_vector([1,2,3,4],None) * make_vector([1,2,3,5],None)
print vec
