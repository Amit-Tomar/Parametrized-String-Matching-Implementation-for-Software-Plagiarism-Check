'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 5
#lst=[1,2,3,4,5,6,7,8,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    count1 = 0
    total = len(lst)
    if total > SIZE_THRESHOLD:
        for i in lst:
        #print i
            if zero_test(i):
            #print "kahfsk"
                count1 = count1+1
            #print count1
    #total = len(lst)
    count = float(count1)/total
    d = DENSITY_THRESHOLD
    
    if count <= d:
        return True
    else:
        return False

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    #sparse_vector=[]
    #full_vector=[]
    values = []
    indices = []
    #length = 0
    #lst=[]
    if(is_long_and_sparse(data, zero_test) == True):
        for i in range(len(data)):
            if not zero_test(data[i]):
                values.append(data[i])
                indices.append(i)
            vec = SparseVector(values, indices, zero_test)
            #print vec
    else:
        vec = FullVector(data, zero_test)
        #print vec
    
    return vec
                
    
class Vector(object):
    '''
    Base Vector class - implements a number of the common methods required for a Vector
    '''
    def __init__(self, lst, zero_test = lambda x : (x == 0)):
        '''
        Have a data attribute that is initialized to the list of elements given in the argument 'lst'
        zero_test is a function that tests if a given element is zero (remember you could potentially
        have a vector of complex numbers, even a vector of functions, ... not just numbers) 
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
        return val

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        count = 0
        for i in self:
            if self[i] == 0:
                count = count+1
        if(count == len(self)):
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
        '''if self == vector:
            return True
        else:
            return False'''
        count = 0
        if(len(self) == len(vector)):
            for i in self:
                if self[i] == vector[i]:
                    count = count+1
        if(count == len(self)):
            return True
        else:
            return False


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        mul_vec = []
        #print self
        if len(self) == len(vector):
            for i in range(len(self)):
                #print self[i]
                #print vector[i]
                #print self[i],vector.lst[i]
                mul_vec.append(self[i] * vector.lst[i])
                return mul_vec
        else:
            return None


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        add_vec=[]
        new_vec=make_vector(self.data, self.zero_test)
        if len(self) == len(new_vec):
            for i in len(self):
                add_vec.append(self[i] + new_vec[i])
                return add_vec
        else:
            return None


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        sub_vec=[]
        new_vec=make_vector(self.data, self.zero_test)
        if len(self) == len(new_vec):
            for i in len(self):
                sub_vec.append(self[i] - new_vec[i])
                return sub_vec
        else:
            return None

    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        iadd_vec = []
        min_len = min(len(self),len(vector))
        for i in range(min_len):
            iadd_vec.append(self[i] + vector[i])
            return iadd_vec


    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        isub_vec = []
        min_len = min(len(self),len(vector))
        for i in range(min_len):
            isub_vec.append(self[i] - vector[i])
            return isub_vec



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
        Uses the base (parent) class attributes data and zero_test3,4,5,2,1
        '''
        super(FullVector, self).__init__(lst, zero_test)

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        bisect_left()
        if(len(self) % 2 == 0):
            half=len(self)/2
            vec1=self[:half]
            vec2=self[half:]
            return vec1,vec2
        else:
            half=len((self)/2)+1
            vec1=self[:half]
            vec2=self[half:]
            return vec1,vec2


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        merged_vec=[]
        for i in range(len(self)):
            merged_vec.append(self[i])
            merged_vec.append(vector[i])
        return merged_vec
            
                        
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
        self.len = length
        self.zero_test = zero_test


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        return len(self.values)


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        for i in self.indices:
            return self.values[i]
        

                 
    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        if i in self.indices:
            self.values[i] = val
        else:
            self.indices[i].append(i)
            self.values[i] = val
        
            

    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        count = 0
        for i in range(len(self)):
            if self[i] == 0:
                count = count+1
        if(count == len(self)):
            return True
        else:
            return False


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        if(len(self % 2 == 0)):
            half=len(self)/2
            s_vec1=self[:half]
            s_vec2=self[half:]
            return s_vec1,s_vec2
        else:
            half = (len(self)/2)+1
            s_vec1=self[:half]
            s_vec2=self[half:]
            return s_vec1,s_vec2
            

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        merged_vec=[]
        for i in range(len(self)):
            merged_vec.append(self[i])
            merged_vec.append(vector[i])
        return merged_vec
if __name__ == '__main__':
    pass #lst=[1,2,3,4,5,6,7,8,9,10]#,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #zero_test = lambda x : (x == 0)
    #print is_long_and_sparse(lst, zero_test)
    #print make_vector(lst, zero_test)