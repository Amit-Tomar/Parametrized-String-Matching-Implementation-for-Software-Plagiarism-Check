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
    if (len(lst)>=50):
        for i in lst:
            if (i == 0):
                count = count + 1
        print count
                 
        if (count/len(lst)>=0.4):
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
    # Your Code
    variables = []
    indices = []
    if (is_long_and_sparse(data) == True):
        for i in data:
            if (i!=0):
                variables.append(i)
                indices.append(data.index(i))
        sparse_vector = SparseVector(variables,indices)
    else :
        full_vector = FullVector(data)
    
    
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
        self.new_vector = lst


    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        # Your Code
        return len(self.new_vector)

    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        # Your Code
        return self.new_vector[i-1]

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        # Your Code
        if (i < len(self)-1):
            self[i] = val
        elif(i >= len(self)-1):
            self.new_vector.append(val)
    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        # Your Code
        count = 0
        for i in self.new_vector:
            if (i == 0):
                count = count + 1
            print count
        if (count == len(self.new_vector)):
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
        for i, j in zip(self.new_vector, vector): 
            if i == j:
                return True
            else :
                return False
            


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        final_mult = []
        if (len(self) == len(vector)):
            for i in range(0,len(self)):
                final_mult.append(self.new_vector[i] * vector.new_vector[i])
            return final_mult    
        else:
            return "none"


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        final_add = []
        if (len(self) == len(vector)):
            for i in range(0,len(self)):
                final_add.append(self.new_vector[i] + vector.new_vector[i])
                
            return final_add
        else:
            return "none"


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code    
        final_sub = []
        if (len(self) == len(vector)):
            for i in range(0,len(self)):
                final_sub.append(self.new_vector[i] - vector.new_vector[i])
            return final_sub
        else:
            return "none"        


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        if(len(self.new_vector) == len(vector)):
            for i in range(0,len(self)):
                self.new_vector[i] = self.new_vector[i] + vector[i]
                
            return self.new_vector
        else:
            if (len(self) > len(vector)):
                for i in range(0,len(vector)):
                    self.new_vector[i] = self.new_vector[i] + vector[i]
            else:
                for i in range(0,len(self)):
                    self.new_vector[i] = self.new_vector[i] + vector[i]


    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        if(len(self) == len(vector)):
            for i in range(0,len(self)-1):
                self.new_vector[i] = self.new_vector[i] - vector[i]
                
            return self.new_vector
        else:
            if (len(self) > len(vector)):
                for i in range(0,len(vector)-1):
                    self.new_vector[i] = self.new_vector[i] - vector[i]
            else:
                for i in range(0,len(self)-1):
                    self.new_vector[i] = self.new_vector[i] - vector[i]



    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        left_part = []
        right_part = []
        if (len(self.lst) % 2) == 0:
            left_part = self.lst[:len(self.lst) / 2]
            right_part = self.lst[len(self.lst) / 2:]
        
        else:
            left_part = self.lst[:(len(self.lst) + 1) / 2]
            right_part = self.lst[(len(self.lst) + 1) / 2:]
        
        return left_part, right_part
        
        
        
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
        # Your Code
        left_part = []
        right_part = []
        if (len(self.lst) % 2) == 0:
            left_part = self.lst[:len(self.lst) / 2]
            right_part = self.lst[len(self.lst) / 2:]
        
        else:
            left_part = self.lst[:(len(self.lst) + 1) / 2]
            right_part = self.lst[(len(self.lst) + 1) / 2:]
        
        return FullVector(left_part), FullVector(right_part)
        

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        self.lst = self.lst + self.vector
        
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
        # Your Code
        super(SparseVector, self).__init__(values, zero_test)
        self.Values = values
        self.Zero_test = zero_test
        self.Indices = indices
        self.Length = length
        self.final_list = []
        for i in len(values):
            self.final_list.append(self.Indices[i],self.Values[i])

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        # Your Code
        return self.Length

    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        # Your Code
        return self.Values[self.Indices.index(i)]

    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        if i in self.Indices:
            self.final_list[self.final_list.index(i)][1] = val
        if i not in self.Indices:
            self.final_list.append((i,val))
            
        self.Values = [x[1] for x in self.final_list]
        self.Indices = [x[0] for x in self.final_list]


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        count = 0
        for i in self.new_vector:
            if (i == 0):
                count = count + 1
        print count
        if (count == len(self.new_vector)):
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
        right_half = []
        left_half = []
        if (len(self)%2==0):
            left_half = self.lst[:len(self.lst) / 2]
            right_half = self.lst[len(self.lst) / 2:]   
        else:
            left_half = self.lst[:(len(self.lst) + 1) / 2]
            right_half = self.lst[(len(self.lst) + 1) / 2:]
        return right_half,left_half
        

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        self.Indices = self.Indices + vector.indices
        self.Values = self.Values + vector.Values
        