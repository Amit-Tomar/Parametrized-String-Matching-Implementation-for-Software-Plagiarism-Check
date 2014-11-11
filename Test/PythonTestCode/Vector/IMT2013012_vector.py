'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 5
zero_test = lambda x : (x == 0)

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    count = 0
    if(len(lst) >= SIZE_THRESHOLD ):
        for elem in lst:
            if(zero_test(elem)):
                count += 1
        
        if((float(count)/len(lst)) >= DENSITY_THRESHOLD):
            return True
    
    return False
    # Your Code

def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    
    if( is_long_and_sparse(data, zero_test) ):
        values = []
        indices = []
        for indx, val in enumerate(data):
            if(not zero_test(val)):
                values.append(val)
                indices.append(indx)
                    
        return SparseVector(values, indices, len(data))
    else:
        return FullVector(data,zero_test)
        
    # Your Code

    
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
        
        self.data = lst
        #self.zero_test() = zero_test
        # Your Code


    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        return len(self.data)
        # Your Code


    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        return self.data[i]
        # Your Code
    

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        self.data[i] = val
        # Your Code

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        flag = 0
        for elem in self.data:
            if(elem != 0 or flag == 0):
                return False
                flag = 1
        return True
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
        if(len(self) == len(vector)):
            
            for indx, elem in enumerate(self):
                if(elem != vector[indx]):
                    return False
                
        return True
        # Your Code


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        
        if(len(self) == len(vector)):
            dot_product = []
            for i in range(len(self)):
                dot_product.append((self[i]*vector[i]))
                
            return make_vector(dot_product,zero_test)
        return None        
        
        # Your Code


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        
        if(len(self) == len(vector)):
            sum_vectors = []
            for i in range(len(self)):
                sum_vectors.append( self[i]+vector[i])
                
            return make_vector(sum_vectors, zero_test)  
        
        return None
        # Your Code


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        
        if(len(self) == len(vector)):
            sum_vectors = []
            for i in range(len(self)):
                sum_vectors.append( self[i]-vector[i])
                
            return make_vector(sum_vectors, zero_test)  
        
        return None
        
        # Your Code


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        
        for i in range(min(len(self),len(vector))):
            self[i] += vector[i]
                
        return self
            
        # Your Code


    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        
        for i in range(min(len(self),len(vector))):
                self[i] -= vector[i]
                
        return self
        # Your Code


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
        left = []
        right = []
             
        for indx, val in enumerate(self):
            if(indx < (len(self)/2)):
                left.append(val)
            else:
                right.append(val)
         
        return  make_vector(left,zero_test), make_vector(right, zero_test)
        
        # Your Code


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        
        self.data.extend(vector.data)
        
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
        self.indices = indices
        self.length = length
        # Your Code


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        return self.length
        # Your Code


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        
        if(isinstance(i, int)):
            if(i in self.indices):
                return self.data[self.indices.index(i)]    
            return 0
        else:
            temp_spar_list = [0]*len(self)
            for pos in range(len(self.indices)):
                temp_spar_list[self.indices[pos]] = self.data[pos]
            return temp_spar_list[i] 
        # Your Code


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        
        if(i in self.indices):
            self.data[self.indices.index(i)] = val
        elif(i < self.indices[len(self.indices)-1]):
            pos = bisect_left(self.data,i)
            self.indices = self.indices[:pos] + [i] + self.indices[pos:]
            self.data = self.data[:pos] + [val] + self.data[pos:]
        else:
            self.data.append(val)
            self.indices.append(i)
    # Your Code


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        """
        for elem in self.data:
            if(not zero_test(elem)):
                return False
        
        return False
        """
        if(len(self) == 0):
           return True
        
        return False
        
        # Your Code


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        left = []
        l_indices =[]
        right = []
        r_indices = []
        for indx, elem in enumerate(self.indices):
            if( elem < (self.length/2)):
                left.append(self.data[indx])
                l_indices.append(elem)
            else:
                right.append(self.data[indx])
                r_indices.append(elem-(len(self)/2))
       
        return SparseVector(left,l_indices, len(self)/2), SparseVector(right,r_indices, len(self)-(len(self)/2)  )
            
        # Your Code


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        extra_l = len(self)
        self.data.extend(vector.data)
        
        for elem in vector.indices:
            print extra_l ,elem
        
            self.indices.append(extra_l + elem)
        
        self.length = len(self) + len(vector)
        
        return self
        # Your Code

#a = make_vector([0,0,0,0,0,0,0,1,2], lambda x : (x == 0))
#print a.data,a.indices

    