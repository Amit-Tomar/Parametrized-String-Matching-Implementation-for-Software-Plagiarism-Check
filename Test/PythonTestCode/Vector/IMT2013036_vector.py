'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 5

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    # Your Code
    zero = 0
    ele = len(lst)
    for num in lst:
        if zero_test(num):
            zero = zero+1
    if ele > SIZE_THRESHOLD:
        if float(zero)/ele > (1-DENSITY_THRESHOLD):
            return True
        else:
            return False
    
def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    if (is_long_and_sparse(data,zero_test)):
        values = []
        indices = []
        for i in range(len(data)):
            if zero_test(data[i]) == False:
                values.append(data[i])
                indices.append(i)
        length = len(data)
        sparse = SparseVector(values, indices, length)
        return sparse
    else:
        full = FullVector(data)
        return full
    
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
        self.lst = lst
        self.zero_test = zero_test

    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        # Your Code
        length = len(self.lst)
        return length

    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        # Your Code
        item = self.lst[i]
        return item
    
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
        for i in self:
            if self.zero_test(i):
                return True
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
        check = 0
        if len(self) == len(vector):
           
            for i in range(len(vector)):
                if self[i] != vector[i]:
                    check = 1
                    break
        if check == 0:
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
        mult = []
        if len(self) != len(vector):
            return None
        else:
            for i in range(len(self)):
                mult += self[i]*vector[i]
            return mult

    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        add = []
        new_vector = make_vector(self.lst,self.zero_test)
        
        if len(vector) != len(new_vector):
            return None
        else:
            for i in range(len(vector)):
                add.append(vector[i]+new_vector[i])
            return add
        
    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        sub=[]
        new_vector = make_vector(self.lst,self.zero_test)
        
        if len(vector) != len(new_vector):
            return None
        else:
            for i in range(len(vector)):
                sub.append(vector[i]-new_vector[i])
            return sub

    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        mini=min(len(self),len(vector))
        iadd=[]
        for i in range(mini):
            iadd.append(self[i]+vector[i])
        return iadd
            

    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        mini=min(len(self),len(vector))
        isub=[]
        for i in range(mini):
            isub.append(self[i]-vector[i])
        return isub

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
        if len(self)%2==0:
            half=len(self)/2
        else:
            half=(len(self)/2)+1
        left=self[half:]
        right=self[:half]
            
        return left,right

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        merge_vector=[]
        for i in range(len(self)):
            merge_vector.append(self[i])
            merge_vector.append(vector[i])
        return merge_vector

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
        # Your Code
        self.values=values
        self.indices=indices
        self.length=length

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        # Your Code
        return len(self.values)

    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        # Your Code
        if i in self.indices:
            return self.values[i]
        else:
            return None

    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        if i not in self.indices:
            self.indices.append(i)
            self.values[i]=val
        else:
            self.values[i]=val
            
    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        count=0
        for i in range(len(self)):
            if self[i] == 0:
                count += 1
        if count == len(self):
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
        
        if len(self)%2 == 0:
            half = len(self)/2
        else:
            half = (len(self)/2)+1
            left = self[half:]
            right = self[:half]
            
        return left,right

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        merge_vector=[]
        for i in range(len(self)):
            merge_vector.append(self[i])
            merge_vector.append(vector[i])
        return merge_vector

'''if __name__ == '__main__':
    lst = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    zero_test = lambda x : (x == 0)
    print is_zero()'''