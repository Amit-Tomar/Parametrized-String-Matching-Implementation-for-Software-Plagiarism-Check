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
    if(len(lst)>=SIZE_THRESHOLD):
        count=0
        for k in lst:
            if(zero_test(k)):
                count=count+1
        density=count/len(lst)
        if(density>(1-DENSITY_THRESHOLD)):
            return True
        
def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    # Your Code
    if(is_long_and_sparse(data, zero_test)):
        values=[]
        indices=[]
        for k in data:
            if(zero_test(k)==False):
                values.append(k)
                indices.append(data.index(k))
                               
        vector=SparseVector(values,indices,len(data),zero_test)
        return vector
    else:
        vector= FullVector(data,zero_test)
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
        # Your Code vector
        self.data=lst
        self.zero_test=zero_test
        

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
        self.data[i]=val
    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        # Your Code
        for k in self.data:
            if(k!=0):
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
        
        for i in xrange(len(self)):
            if(self[i] != vector[i]):
                return False
        return True

    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        prod=0
        if(len(self)!=len(vector)):
            return None
        else:
            for i in xrange(len(self)):
                prod=prod+(self[i]*vector[i])
            return prod

    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        if(len(self)!=len(vector)):
            return None
        else:
            DATA=[]
            for k in range(len(self)):
                DATA.append(self[k]+vector[k])
            
        return make_vector(DATA,self.zero_test)
        

    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        if(len(self)!=len(vector)):
            return None
        else:
            DATA=[]
            for k in xrange(len(self)):
                DATA.append(self[k]-vector[k])
        return make_vector(DATA,self.zero_test)

    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        if(len(self)!=len(vector)):
            return None
        else:
            for k in range(len(self)):                
                self.__setitem__(k,self[k]+vector[k])
            
                
        

    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        if(len(self)!=len(vector)):
            return None
        else:
            for k in range(len(self)):                
                self.__setitem__(k,self[k]-vector[k])
        

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
        x=self.__len__()/2
        vector1=make_vector(self.data[0:x],self.zero_test)
        vector2=make_vector(self.data[x:-1]+[self.data[-1]],self.zero_test)
        return vector1,vector2 

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        lst=self.data+vector.data
        self.data=lst

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
        self.data=[]
        x=0
        while(x<length):
            self.data[x]=0
            x+=1
        for i in xrange(len(self.values)):
            self.data[self.indices[i]]=self.values[i]

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
            return self.values[i]
        else:
            return 0

    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        if i in self.indices:
            self.value[i]=val
        else:
            self.data[i]=val


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        if(len(self.value)==0):
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
        x=self.length/2
        i=0
        lst1=[]
        lst2=[]
        while(i<self.length):
            lst1[i]=0
            lst2[i]=0
            i+=1
        for i in self.indices:
            if(i<x):
                lst1[i]=self.values[i]
            else:
                lst2[i]=self.values[i]
        vector1=make_vector(lst1,self.zero_test)
        vector2=make_vector(lst2,self.zero_test)
        return vector1,vector2

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        
if __name__ == '__main__':
    data=[1,0,0,0,0,0,0,0,0,0]
    vector1=make_vector(data,None)
    vector2=make_vector(data,None)
    print vector1.__eq__(vector2)
    print vector1.data
    vector1.merge(vector2)
    print vector1.data
    