'''
Created on 16-Nov-2013

@author: raghavan
'''

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 50

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    count = 0
    for element in lst:
        if element == 0:
            count += 1
    
    if (len(lst) >= 50 and (count / len(lst)) > 0.4):
        return True
    else:
        return False
    # Your Code

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    
    if is_long_and_sparse(data, zero_test = None ) == False:
        return FullVector(data)
    else:
        indices = []
        values = []
        count = 0
        for element in data:
            indices.append(count)
            values.append(data[count]) 
        return SparseVector(values, indices, len(values), zero_test = 0)
    
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
        self.DATA = lst
        
        # Your Code


    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        return len(self.DATA)
        # Your Code


    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        return self.DATA[i]
        # Your Code
    

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        self.DATA[i] = val
        # Your Code

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        count = 0
        for x in self.DATA:
            if x == 0:
                count += 1
        if (count == len(self.DATA)):
            return True
        else:
            return False
         
        # Your Code


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
        if self.DATA == vector:
            return True
        else:
            return False
        # Your Code


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        final_list = [];
        if len(self.DATA) == len(vector):
            for i in range(0, len(self.DATA)):
                    final_list.append(self.DATA[i] * vector.DATA[i])
            return final_list
        else:
            return None
        
        # Your Code


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        final_list = []
        if len(self.DATA) == len(vector):
            for i in range(0, len(vector)):
                final_list.append(self.DATA[i] + vector.DATA[i])
            return final_list
        else:
            return None
        # Your Code


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        final_list = []
        if len(self.DATA) == len(vector):
            for i in range(0, len(vector)):
                final_list.append(self.DATA[i] - vector.DATA[i])
            return final_list
        else:
            return None
        # Your Code


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
            Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        for i in range(0, min(len(self.DATA), len(vector))):
            self.DATA[i] = self.DATA[i] + vector[i]
       
        return self.DATA

    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        for i in range(0, min(len(self.DATA), len(vector))):
            self.DATA[i] = self.DATA[i] - vector[i]
            
        return self.DATA
        # Your Code


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        list1, list2 = [], []
        if len(self.DATA) % 2 == 0:
            list1 = self.DATA[:len(self.DATA) / 2]
            list2 = self.DATA[len(self.DATA) / 2:]
        
        else:
            list1 = self.DATA[:(len(self.DATA) + 1) / 2]
            list2 = self.DATA[(len(self.DATA) + 1) / 2:]
        
        return Vector(list1), Vector(list2) 
    
        
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
        self.zero_test = zero_test #Check

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        list1, list2 = [], []
        if len(self.lst) % 2 == 0:
            list1 = self.lst[:len(self.lst) / 2]
            list2 = self.lst[len(self.lst) / 2:]
        
        else:
            list1 = self.lst[:(len(self.lst) + 1) / 2]
            list2 = self.lst[(len(self.lst) + 1) / 2:]
        
        return FullVector(list1), FullVector(list2)
        
        # Your Code


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        self.lst = self.lst + vector.lst
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
        self.VALUES = values
        self.INDICES = indices
        self.LENGTH = length
        self.ZERO_TEST = zero_test
        self.final_list = []
        for value in range(0, len(values)):
            self.final_list.append((self.INDICES[value], self.VALUES[value]))

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        return self.LENGTH
        # Your Code


    
    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        return self.VALUES[self.INDICES.index(i)]
        # Your Code


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        if i in self.INDICES:
            self.final_list[self.final_list.index(i)][1] = val
        if i not in self.INDICES:
            self.final_list.append((i, val))
        
        self.VALUES = [x[1] for x in self.final_list]
        self.INDICES = [x[0] for x in self.final_list]
            
        # Your Code


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        count = 0
        for y in self.final_list:
            if y[1] == 0:
                count += 1
        
        if count == len(self.final_list):
            return True
        else:
            return False
        # Your Code


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        list1, list2 = [], []
        ind_list1, ind_list2 = [], []
        if len(self.VALUES) % 2 == 0:
            list1 = self.VALUES[:len(self.VALUES) / 2]
            list2 = self.VALUES[len(self.VALUES) / 2:]
            ind_list1 = self.INDICES[:len(self.INDICES) / 2]
            ind_list2 = self.INDICES[len(self.INDICES) / 2:]
        
        else:
            list1 = self.VALUES[:(len(self.VALUES) + 1) / 2]
            list2 = self.VALUES[(len(self.VALUES) + 1) / 2:]
            ind_list1 = self.INDICES[:(len(self.INDICES) + 1) / 2]
            ind_list2 = self.INDICES[(len(self.INDICES) + 1) / 2:]
        
        return SparseVector(list1, ind_list1, self.LENGTH, zero_test = None), SparseVector(list2, ind_list2, self.LENGTH, zero_test = None)
        # Your Code


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        self.INDICES = self.INDICES + vector.INDICES
        self.VALUES = self.VALUES + vector.VALUES
        # Your Code
        
'''a = SparseVector([1,2,3,4,5,6], [10,11,12,13,14,15], 20, zero_test = None)
b = SparseVector([7,8,9,0],[16,17,18,19], 20, zero_test =  None)

a.merge(b)
print (a.INDICES, a.VALUES)'''
    