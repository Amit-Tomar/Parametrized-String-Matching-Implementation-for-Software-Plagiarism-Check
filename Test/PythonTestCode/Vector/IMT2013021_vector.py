'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 3

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    # Your Code
    
    if len(lst) < SIZE_THRESHOLD:
        return False
    
    else:    
        zeros = [lst[i] for i in range(len(lst))
                 if zero_test(lst[i])]                
        return len(zeros) >= DENSITY_THRESHOLD * len(lst)
        
    

def make_vector(data, zero_test = lambda x: x==0):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    
    if not is_long_and_sparse(data, zero_test):
        vector = FullVector(data, zero_test)
        
    else:
        indices = [key for key, elem in enumerate(data) if not zero_test(elem)]
        values = [elem for key, elem in enumerate(data) if not zero_test(elem)]
        vector = SparseVector(values, indices, len(data), zero_test)
        
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
        
        self.zero_test = zero_test
        self.vector_list = lst


    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        # Your Code
        
        return len(self.vector_list)


    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        # Your Code
        
        return self.vector_list[i]
    

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        # Your Code
        
        self.vector_list[i] = val

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        # Your Code
        
        zero = True
        
        for i in range(len(self)):
            if self[i] != 0:
                zero = False
                break
            
        return zero


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
        
        if len(self) != len(vector):
            return False
        
        check = True
        
        for i in range(len(self)):
            if self[i] != vector[i]:
                check = False
                break
        
        return check                


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        
        if len(vector) != len(self):
            return None
        
        return sum([self[i] * vector[i] for i in range(len(self))])


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        
        if len(vector) != len(self):
            return None
        
        sum_lst = ([self[key] + vector[key]
                     for key in range(len(vector))])
        
        return make_vector(sum_lst, self.zero_test)

    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        
        if len(vector) != len(self):
            return None
        
        sub_lst = ([self[key] - vector[key]
                     for key in range(len(vector))])
        
        return make_vector(sub_lst, self.zero_test)


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        
        rng = min(len(self) , len(vector))
        
        sum_lst = [self[count] + vector[count]
                            for count in range(rng)]
        
        return make_vector(sum_lst, self.zero_test)
    
    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code

        rng = min(len(self) , len(vector))
        
        sub_lst = [self[count] - vector[count]
                            for count in range(rng)]
        
        return make_vector(sub_lst, self.zero_test)
    
    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        
        count = len(self)
        
        lt_list = [self[i] for i in range(count / 2)]
        rt_list = [self[i] for i in range(count / 2, count)]
               
        return (make_vector(lt_list, self.zero_test),
                make_vector(rt_list, self.zero_test))
        
    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code

        t_list = [self[i] for i in range(len(self))]
        
        for i in range(len(vector)):
            t_list.append(vector[i])
            
        return make_vector(t_list, self.zero_test)       
        
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
            

class SparseVector(Vector):
    '''
    Vector that has very few non-zero entries
    Values and corresponding indices are kept in separate lists
    '''
    def __init__(self, values, indices, length = 0,
                 zero_test = lambda x : (x == 0)):
        '''
        'values' argument is the list of non-zero values and the corresponding indices are in the list 'indices'
        Uses the base (parent) class attributes data (this is where 'values' are kept) and zero_test
        Length is the length of the vector - the number of entries in 'values' is just the number of non-zero entries
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseVector, self).__init__(values, zero_test)
        # Your Code
        
        self.values = values
        self.indices = indices
        self.length = length


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
        
        if i >= len(self):
            return None
            
        idx = bisect_left(self.indices, i)
        
        return (0 if idx == len(self.values) else
                (0 if self.indices[idx] != i else self.values[idx]))    


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        
        idx = bisect_left(self.indices, i)
    
        if self.indices[idx] == i:
            self.values[idx] = val
        else:    
            self.indices.insert(idx, i)
            self.values.insert(idx, val)

if __name__ == '__main__':
    pass
    