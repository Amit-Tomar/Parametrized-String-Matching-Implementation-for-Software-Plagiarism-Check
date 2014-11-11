'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 50

def is_long_and_sparse(lst, zero_test=(lambda x:x==0)):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    # Your Code
    no_of_zeros  = 0
    no_of_element = len(lst)
    for element in lst:
        if zero_test(element):
            no_of_zeros += 1
    density = float(no_of_zeros) / no_of_element
    if no_of_element > SIZE_THRESHOLD:
        if density > DENSITY_THRESHOLD:
            return True
    return False

def make_vector(data, zero_test=(lambda x:x==0)):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    if is_long_and_sparse(data, zero_test) == False:
        vector = FullVector(data, zero_test)
    else:
        index_list = []
        ele_list = []
        for i in range(0, len(data)):
            if zero_test(data[i]) == False:
                ele_list += [data[i]]
                index_list += [i]
                
        vector = SparseVector(ele_list, index_list, len(data), zero_test)
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
        value = self.lst[i]
        return value
        
    

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
        len_lst = len(self)
        for i in range(0, len_lst):
            if self.zero_test(self[i]) == False:
                return False
        return True

    def components(self):
        '''
        Allows one to iterate through the elements of the vector as shown below
        for elem in vector.components(): (vector is an object of type Vector or any of its derived classes)
        '''
        for i in xrange(len(self)):
            yield i, self[i]


    def __eq__(self, vector):
        '''
        Check if this vector is identical to another 'vector' (allows use of operator == to compare vectors)
        '''
        # Your Code
        for idx, elem in self.components():
            if(elem != vector[idx]):
                return False
        return True
        

    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        product = 0
        if(len(vector) != len(self)):
            return None
        for idx, elem in self.components():
            product += elem*vector[idx]
        return product

    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        sum = []
        if(len(vector) != len(self)):
            return None
        for idx, elem in self.components():
            sum += [elem+vector[idx]]
        sum_vec = make_vector(sum, lambda x : (x == 0))
        return sum_vec       


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        sum = []
        if(len(vector) != len(self)):
            return None
        for idx, elem in self.components():
            sum += [elem-vector[idx]]
        sum_vec = make_vector(sum, lambda x : (x == 0))
        return sum_vec 


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        iadd =[]
        min_length = min(len(self),len(vector))
        for i in range(0,min_length):
            iadd += [self[i] + vector[i]]
        add_vec = make_vector(iadd, lambda x : (x == 0))
        return add_vec


    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        iadd =[]
        min_length = min(len(self),len(vector))
        for i in range(0,min_length):
            iadd += [self[i] - vector[i]]
        add_vec = make_vector(iadd, lambda x : (x == 0))
        return add_vec   

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        return None,None
        
        
        
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
        left_list = []
        left_ind = []
        right_ind = []
        right_list = []
        split_index = len(self)/2
        for i in range(0,split_index):
            left_list += [self[i]]
        for i in range(split_index,len(self)):
            right_list += [self[i]]
        left_vec = FullVector(left_list, zero_test = lambda x : (x == 0))
        right_vec = FullVector(right_list, zero_test = lambda x : (x == 0))
        return left_vec, right_vec
        


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        for ele in vector.lst:
            self.lst.append(ele)
        


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
        self.values = values
        self.indices = indices
        self.length = length
        self.zero_test = zero_test


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
        if i in self.indices:
            index = self.indices.index(i)
            return self.values[index]
        return 0


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        self.lst[i] = val


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
        left_list = []
        left_ind = []
        right_ind = []
        right_list = []
        split_index = self.length/2
        for i in range(0,split_index):
            if i in self.indices:
                left_list += [self.values[self.indices.index(i)]]
                left_ind += [i]
            else:
                left_list += [0]
        for i in range(split_index,self.length):
            if i in self.indices:
                right_list += [self.values[self.indices.index(i)]]
                right_ind += [i]
            else:
                right_list += [0]
        left_vec = make_vector(left_list, lambda x : (x == 0))
        right_vec = make_vector(right_list, lambda x : (x == 0))
        return left_vec, right_vec

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        for ele in vector.lst:
            if(ele!=0):
                self.lst.append([ele])
                self.indices.append(self.length)
            self.length+=1
