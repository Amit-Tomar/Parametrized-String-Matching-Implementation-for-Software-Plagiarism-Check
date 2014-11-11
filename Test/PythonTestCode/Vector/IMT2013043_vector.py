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
        if zero_test(i) == True:
            count += 1
    if len(lst)> SIZE_THRESHOLD and (count/len(lst)>DENSITY_THRESHOLD):
        return True
    else :
        return False
    

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    if is_long_and_sparse(data, zero_test) == False:
        vector = FullVector(data, zero_test)
    else:
        index = []
        elements = []
        for i in range(0, len(data)):
            if zero_test(data[i]) == False:
                elements += [data[i]]
                index += [i]
                
        vector = SparseVector(elements, index, len(data), zero_test)
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
        self.zero_test = lambda x : (x == 0)

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
        count = 0
        for i in self:
            if i == 0:
                count += 1
        if count == (len(self)-1):
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
        i = 0
        count = 0
        while i < len(self):
            if self[i] == vector[i]:
                count += 1
        if count == len(self) :
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
        resul = 0
        i = 0
        while(i<len(self)):
            resul += (self[i]*vector[i])
        return resul


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        temp = []
        i = 0
        vec1 = make_vector(vector.data , self.zero_test)
        vec2 = make_vector(self.data , self.zero_test)
        while i < len(vec1):
            temp.append(vec1[i] + vec2[i])
        return temp
          
        
    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        temp = []
        i = 0
        vec1 = make_vector(vector.data , self.zero_test)
        vec2 = make_vector(self.data , self.zero_test)
        while i < len(vec1):
            temp.append(vec1[i] - vec2[i])
        return temp


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        i = 0
        while i < min(len(vector),len(self)):
            self[i] += vector[i]
        return self
    
    
    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        i = 0
        while i < min(len(vector),len(self)):
            self[i] -= vector[i]
        return self
        

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
        length = len(self.lst)
        lst1, lst2 = make_vector(self.lst[:length/2], self.zero_test), \
         make_vector(self.lst[length/2:], self.zero_test)
        return lst1, lst2

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        i = 0;
        while(i<len(vector)):
            self.append(vector[i])
            i += 1


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
        self.length  = length
        self.values = values
        self.indices = indices
    
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
        j = 0
        if i in self.indices:
            while j < len(self.indices):
                if self.indices[j] == i:
                    return self.values[j]
        else:
            return 0    
        
            

    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        index = 0
        if i in self.indices:
            index = self.indices.index(i)
            self.values[index] = val
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
        
        

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        val1, val2, ind1, ind2 = [], [], [], []
        for i in range(0, self.length):
            if i < self.length/2:
                ind1.append(i)
            else:
                val2.append(self.values[self.indices.index(i)])
                ind2.append(i)
        for i in range(0, self.length):    
            if i < self.length/2 and i not in ind1:
                val1.append(0)
            elif i < self.length/2 and i in ind1:
                val1.append(self.values[self.indices.index(i)])
            elif i > self.length/2 and i not in ind2:
                val2.append(0)
            elif i > self.length/2 and i in ind2:
                val2.append(self.values[self.indices.index(i)])   
        vect1, vect2 = make_vector(val1, self.zero_test), \
         make_vector(val2, self.zero_test)
        return vect1, vect2
            



    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        for i in vector.lst:
            self.lst.append(i)
            self.length+=1
            self.indices.append(self.length)
            
                   