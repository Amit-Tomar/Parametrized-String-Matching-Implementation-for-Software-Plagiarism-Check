'''Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 50

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    count = 0 
    for i in lst:
        if zero_test(i) == True:
            count = count + 1
    length = (count* 0.1) / len(lst)        
    if (len(lst) >=  SIZE_THRESHOLD and length > 1-DENSITY_THRESHOLD):
        return True
    return False
          
def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    if is_long_and_sparse(data, zero_test):
        values = []
        indices = []
        for i , val in enumerate(data):
            if val != 0:
                values.append(values)
                indices.append(i)
        vector = SparseVector(values , indices , len(data) , zero_test)        
    else:
        vector = FullVector(data , zero_test)
        
    return vector

class Vector(object):
    '''
    Base Vector class - implements a number of the common methods required for a Vector
    '''
    def __init__(self, lst, zero_test = lambda x : (x == 0)):
        '''
        Have a data attribute that is initialized to the list of elements given in the argument 'lst'
        zero_test is a function that tests if a given element is zero (remember you 
        could potentially
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
        return self.data[i]
    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        for i in range(len(self)):
            if(self[i] != 0):
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
        if(len(self) == len(vector)):
            for i in range (len(self)):
                if(self[i] != vector[i]):
                    return False
            
            return True
        else:
            return None

    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        dot_pro = []
        if(len(self) == len(vector)):
            for i in range (len(self)):
                dot_pro.append(self[i] * vector[i])
            return dot_pro   
        else:
            return None

    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        add_vector = []
        if(len(self)==len(vector)):
            for i in range (len(self)):
                add = 0
                add = add + self[i]+vector[i]
                add_vector.append(add)
            sum_vector =  make_vector(add_vector , self.zero_test)
            return sum_vector
        else:
            return None

    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        sub_vector = []
        if(len(self)==len(vector)):
            for i in range (len(self)):
		sub = 0
                sub = sub + self[i]-vector[i]
                sub_vector.append(sub)
            diff_vector = make_vector(sub_vector , self.zero_test)
            return diff_vector   
        else:
            return None

    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        mini = min(len(self) , len(vector))
        for i in range (0 , mini):
            self[i] = self[i] + vector[i]
        

    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        mini = min(len(self) , len(vector))
        for i in range (0 , mini):
            self[i] = self[i] - vector[i]
        
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
        length1 = []
        length2 = []
        if(len(self)%2 == 0):
            for i in range(0 , len(self)/2):
                length1.append(self[i])
            for i in range(len(self)/2 , len(self)):
                length2.append(self[i])
        else:
            for i in range(0 , (len(self)/2)+1):
                length1.append(self[i])
            for i in range((len(self)/2)+1 , len(self)):
                length2.append(self[i])
        return make_vector(length1 , self.zero_test) , make_vector(length2 , self.zero_test)
                     
    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        merged = []
        for ele in self.components():
            merged.append(ele)
        for ele in vector.components():
            merged.append(ele)
        
        return make_vector(merged , self.zero_test)
            
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
        self.length = length
        
    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        return len(self.data)        


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        if i >= self.length:
            return None
        if i in self.indices:
            return self.data[self.indices.index(i)]
        return 0


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        
        if i not in self.indices:
            self.indices.append(i)
            self.data.append(val)
        else:
            self[self.indices.index(i)] = val
        
    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        for i in range(len(self)):
            if self.zero_test(self[i]) == False:
                return False
        return True
        

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        leftvalue = []
        rightvalue = []
        leftindex = []
        rightindex = []
        for i in range(len(self)):
            if self.indices[i] < self.length//2:
                leftvalue.append(self[i])
                leftindex.append(self.indices[i])
            else:
                rightvalue.append(self[i])
                rightindex.append(self.indices[i])

        return SparseVector(leftvalue , leftindex , self.length//2 , self.zero_test) , SparseVector(rightvalue , rightindex , self.length//2 , self.zero_test)
    

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        merge_value = []
        merge_indices = []
        for i in range(len(self)):
            merge_value.append(self.values[i])
            merge_indices.append(self.indices[i])
        for i in range(len(vector)):
            merge_value.append(vector.values[i])
            merge_indices.append(self.indices[i])
        return SparseVector(merge_value , merge_indices , self.length+vector.length , self.zero_test)
    
    if __name__ == '__main__':
        
        m1_mat=[1,2,3]
        m2_mat=[4,5,6]
        
        mat3 = make_vector(m1_mat , zero_test=lambda x : (x==0))+ make_vector(m2_mat , zero_test=lambda x : (x==0))
        
        for e in mat3:
            print e,
