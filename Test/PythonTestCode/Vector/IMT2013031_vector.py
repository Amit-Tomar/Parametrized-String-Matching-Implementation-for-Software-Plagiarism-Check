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
    if(len(lst)>SIZE_THRESHOLD):
        count = 0
        for elmt in lst:
            if(zero_test(elmt)==0):
                count = count+1
        if((count/len(lst))>DENSITY_THRESHOLD):
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
    if(is_long_and_sparse(data , zero_test)==False):
        i = 0
        vector_elmts = []
        while(i<len(data)):
            vector_elmts[i] = data[i]
            i = i+1
    if(is_long_and_sparse(data , zero_test)==True):
        i = 0
        vector_elmts = []
        vector_indices = []
        while(i<len(data)):
            if(data[i]!=0):
                vector_elmts[i] = data[i]
                vector_indices[i] = i
            i = i+1
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
        return self.data[i-1] 
    

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        self.data[i-1] = val 

    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        i = 0
        for elmt in self.data:
            if(elmt==0):
                i = i+1
            else:
                return False
        if(i==self.__len__()-1):
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
        if(vector==self.data):
            return True
        else:
            return False
    
    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        dot_product = 0
        if(len(self.data)==vector):
            for elmt1 , elmt2 in self.data , vector:
                dot_product = dot_product+(elmt1*elmt2)
            return dot_product
        else:
            return None

    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if(self.__len__()==len(vector)):
            i = 0
            sum_vector = []
            while(i<self.__len__()):
                sum_vector[i] = vector[i]+self.data[i]
                i = i+1
            return make_vector(sum_vector , self.zero_test)
        else:
            return None
    
        
    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        if(self.__len__()==len(vector)):
            i = 0
            difference_vector = []
            while(i<self.__len__()):
                difference_vector[i] = self.data[i]-vector[i]
                i = i+1
            return make_vector(difference_vector , self.zero_test)
        else:
            return None


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        if(len(vector)==self.__len__()):
            self.__add__(vector)
        else:
            i = 0
            sum_vector = []
            while(i<min(self.__len__() , len(vector))):
                sum_vector[i] = self.data[i]+vector[i]
                i = i+1
            return sum_vector
    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        if(len(vector)==self.__len__()):
            self.__sub__(vector)
        else:
            i = 0
            difference_vector = []
            while(i<min(self.__len__() , len(vector))):
                difference_vector[i] = self.data[i]-vector[i]
                i = i+1
            return difference_vector
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        if((self.__len__())%2==0):
            first_half_vector = self.data[:(self.__len__()/2)]
            second_half_vector = self.data[(self.__len__()/2):]
            return first_half_vector , second_half_vector
        else:
            first_half_vector = self.data[:(self.__len__()/2)]
            second_half_vector = self.data[((self.__len__()/2)+1):]
            return first_half_vector , second_half_vector        
        
        
        
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
        self.data = lst
        self.zero_test = zero_test

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        if((self.__len__())%2==0):
            first_half_vector = self.data[:(self.__len__()/2)]
            second_half_vector = self.data[(self.__len__()/2):]
            return first_half_vector , second_half_vector
        else:
            first_half_vector = self.data[:(self.__len__()/2)]
            second_half_vector = self.data[((self.__len__()/2)+1):]
            return first_half_vector , second_half_vector  


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        merrge_vector = self.data+vector


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
        self.values = values
        self.indices = indices
        self.length = len(values)
        self.zero_test = zero_test


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        return self.length


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        return self.values[i-1]


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        if i in self.indices:
            self.values[i] = val 
        else:
            self.values.append(val)
            self.indices.append(i)

    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        if(self.length==0):
            return True
        else:
            return False
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        if(self.length%2==0):
            first_half_values = self.values[:(self.length/2)]
            first_half_indices = self.indices[:(self.length/2)]
            second_half_values = self.values[(self.length/2):]
            second_half_indices = self.indices[(self.length/2):]
            return first_half_values , first_half_indices , second_half_values , second_half_indices 
        else:
            first_half_values = self.values[:(self.length/2)]
            first_half_indices = self.indices[:(self.length/2)]
            second_half_values = self.values[((self.length/2)+1):]
            second_half_indices = self.indices[((self.length/2)+1):]
            return first_half_values , first_half_indices, second_half_values , second_half_indices


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        merge_sparse_values = self.values+vector
        i = 0
        vector_indices = []
        while(i<len(vector)):
            vector_indices[i] = self.length-1+i
        merge_sparse_indies = self.indices+vector_indices 