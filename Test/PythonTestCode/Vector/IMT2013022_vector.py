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
    num = 0
    if(len(lst) > SIZE_THRESHOLD):
        for item in range(len(lst)):
            if(item == 0):
                num += 1
        density = num/len(lst)
        if(density >= DENSITY_THRESHOLD):
            return True
    

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    if is_long_and_sparse(data, zero_test):
        index = []
        vect = []
        for item , value in enumerate(data):
            if value != 0:
                index.append(item)
                vect.append(value)
        length_vect = len(index)       
        vector = SparseVector(vect ,index ,length_vect ,zero_test)       
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
        for item in self.lst:
            if(item!=0):
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
        # Your Code
        for item in range(len(self)):
            if(self[item]!=vector[item]):
                return False
        return True
            

    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        prod = 0
        if(len(self) != len(vector)):
            return None
        for item in range(len(self)):
                prod += self[item] * vector[item]
        return prod


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        vector_addn = []
        if(len(vector)==len(self)):
            for item in range (len(self)):
                vect = 0
                vect = vect + (self[item]+vector[item])
                vector_addn.append(vect)
            return make_vector(vector_addn,self.zero_test)  
        else:
            return None
        


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        vector_subn = []
        if(len(vector)==len(self)):
            for item in range (len(self)):
                vect = self[item] - vector[item]
                vector_subn.append(vect)
            return make_vector(vector_subn,self.zero_test)  
        else:
            return None
        


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        minimum = min(len(self), len(vector))
        for item in range(minimum):
            self[item] += vector[item]

    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        minimum = min(len(self.data),vector)
        for item in range (0,minimum):
            self[item] -=vector[item]


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
        first_half = []
        second_half= []
        
        if(len(self)%2 != 0):
            for item in range((len(self)/2)+1 , len(self)):
                second_half.append(self[item])
            for item in range(0 , (len(self)/2)+1):
                first_half.append(self[item])
        else:
            for item in range(len(self)/2 , len(self)):
                second_half.append(self[item])
            for item in range(0 , len(self)/2):
                first_half.append(self[item])
        
        return first_half,second_half 

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        for item in range(0 , len(vector)):
            self.lst.append(vector[item])
            
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
        self.indices=indices
        self.zero_test=zero_test
        self.length=length


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
        if i >= self.length:
            return None
        if i in self.indices:
            return self.lst[self.indices.index(i)]
        return 0


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        if i not in self.indices:
            self.indices.append(i)
            self.lst.append(val)
        else:
            self[self.indices.index(i)] = val

    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        for item in range(len(self.values)):
            if(self.values[item] != 0):
                return False
        return True

            
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        left = []
        right = []
        if(len(self)%2 == 0):
            x = len(self)/2
        else:
            x=len(self)/2+1
        for i in range(x):
            left.append(self[i])
            left_vec = make_vector(left,self.zero_test)
        for i in range(len(right)):
            right.append(self[i])
            right_vec = make_vector(right,self.zero_test)
        return left_vec,right_vec

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        for item in range(0 , len(vector)):
            self.values.append(vector[item])

if __name__ == '__main__':
    
    m1 =[1,2,3]
    m2 =[1,2,2]
    
    m3 = make_vector(m1,zero_test = lambda x : (x == 0)) - make_vector(m2,zero_test = lambda x : (x == 0))
    
    for i in m3:
        print i,                                                                                                          
    