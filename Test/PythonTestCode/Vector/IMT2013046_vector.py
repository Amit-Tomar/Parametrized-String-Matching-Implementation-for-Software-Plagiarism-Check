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
    counter = 0
    for i in lst:
        if zero_test(i) == True:
            counter = counter + 1
    density = (counter*0.1) / len(lst)      
    if ( density > 1-DENSITY_THRESHOLD and len(lst) >= SIZE_THRESHOLD ) :
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
        for i in range (len(self)):
            if(self[i] != vector[i]):
                return False
          
            return True
    

    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        dot_product = []
        if(len(self) == len(vector)):
            for i in range (len(self)):
                dot_product.append(self[i] * vector[i])
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
        sums = []
        if(len(self)==len(vector)):
            for i in range (len(self)):
                add = 0
                add = add + self[i]+vector[i]
                sums.append(add)
            sum_vector = make_vector(sums , self.zero_test)
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
        sub = []
        if(len(self)==len(vector)):
            for i in range (len(self)):
                sub =0 
                sub = sub + self[i]-vector[i]
                sub.append(sub)
            sub_vector = make_vector(sub , self.zero_test)
            return sub_vector 
        else:
            return None

    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        minimum = min(len(self) , len(vector))
        for i in range (0 , minimum):
            self[i] = self[i] + vector[i]
      

    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        minimum = min(len(self) , len(vector))
        for i in range (0 , minimum):
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
        left_list = []
        right_list = []
        if(len(self)%2 == 0):
            for i in range(0 , len(self)/2):
                left_list.append(self[i])
            for i in range(len(self)/2 , len(self)):
                right_list.append(self[i])
        else:
            for i in range(0 , (len(self)/2)+1):
                left_list.append(self[i])
            for i in range((len(self)/2)+1 , len(self)):
                right_list.append(self[i])
        return make_vector(left_list , self.zero_test) , make_vector(right_list , self.zero_test)
              
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
        leftvec = []
        rightvec = []
        leftindex = []
        rightindex = []
        for i in range(len(self)):
            if self.indices[i] < self.length//2:
                leftvec.append(self[i])
                leftindex.append(self.indices[i])
            else:
                rightvec.append(self[i])
                rightindex.append(self.indices[i])

        left_vector = SparseVector(leftvec , leftindex , self.length//2 , self.zero_test )
        right_vector = SparseVector(rightvec , rightindex , self.length //2 , self.zero_test )
        return left_vector, right_vector

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        mergeval = []
        mergeind = []
        for i in range(len(vector)):
            mergeval.append(vector.values[i])
            mergeind.append(self.indices[i])
        for i in range(len(self)):
            mergeval.append(self.values[i])
            mergeind.append(self.indices[i])
        return SparseVector(mergeval , mergeind , self.length+vector.length , self.zero_test)
    
    
    
     
    if __name__ == '__main__':
        '''m1 = [make_vector([1,2,3,4] , zero_test=lambda x : (x==0)) , make_vector([3,4,5,6] , zero_test = lambda x : (x ==0)) , make_vector([5,6,7,8] , zero_test = lambda x : (x == 0)) , make_vector([7,8,9,10] , zero_test = lambda x : (x ==0))]
        m2 = [make_vector([1,2,3,4] , zero_test = lambda x : (x == 0)) , make_vector([3,4,5,6] , zero_test = lambda x : (x==0)) , make_vector([5,6,7,8] , zero_test = lambda x : (x == 0)),make_vector([7,8,9,10] , zero_test = lambda x : (x ==0))]
        m1_mat = make_matrix(m1)
        m2_mat = make_matrix(m2)'''
        m1_mat=[1,2,3]
        m2_mat=[4,5,6]
        
        mat3 = make_vector(m1_mat , zero_test=lambda x : (x==0))+ make_vector(m2_mat , zero_test=lambda x : (x==0))
        
        for e in mat3:
            #for e in vec:
            print e,
