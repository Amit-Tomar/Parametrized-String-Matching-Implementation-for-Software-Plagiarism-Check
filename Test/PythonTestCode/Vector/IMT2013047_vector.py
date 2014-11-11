'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.5
SIZE_THRESHOLD = 2

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    
    # Your Code
    count = 0
    values=[]
    indices=[]
    if len(lst) >= SIZE_THRESHOLD:
        for i in range(0,len(lst)):
            if zero_test(lst[i]) == True:
                count += 1
                
    '''    count = 0
    
    if (len(lst) >= SIZE_THRESHOLD):
        for element in lst:
            if(zero_test(element)):
                count +=1
    
    percent_zero = count/len(lst)
    
    if(float(percent_zero) >= (1 - DENSITY_THRESHOLD)):
        return True
    
    else:
        return False
        for elem in lst:
            if zero_test(elem) == True:
                count += 1
            else:
                values.append(elem)
                indices.append(lst.index(elem))'''
                
    if count >= (1 -DENSITY_THRESHOLD )* len(lst):
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
    values = []
    indices = []
    
    test = is_long_and_sparse(data, zero_test)
    
    if (test == True):
        for i in range(0,len(data)):
            values.append(data[i])
            indices.append(i)
        vector = SparseVector(values, indices, len(data), zero_test)
        
    elif test == False:
        vector = FullVector(data,zero_test)
        
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
        count = 0
        for elem in self.lst:
            if elem != 0:
                count += 1
        if count == 0:
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
        
        if (len(self) != len(vector)):
            return None
        count = 0
        for i in range(0,len(self)):
            if self[i] != vector[i]:
                count = count + 1
        
        if (count == 0):
            return True
        
        '''if (self.length == vector.length):
            for i in range(vector.length):
                if (self[i] != vector[i]):
                    return False
                else:
                    return True'''
        
        
        
    ''' if isinstance(self, FullVector):
            if isinstance(vector, FullVector):
                for i in range(len(self)):
                    if self[i] != vector[i]:
                        return False
                        break
                    else:
                        return True
                    
        elif isinstance(self,SparseVector):
            if isinstance(vector, SparseVector):
                if (self.length == vector.length and len(self.indices) == len(vector.indices)):
                    for i in range(0, self.length):
                                if (self[i] != vector[i]):
                                    return False
                                    break
                                else:
                                    return True 
                else:
                    return False
            else:
                return False
            
        else:
            return False'''
        
                        

    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        sum_list = 0
        if len(self) == len(vector):
            for i in range(len(self)):
                sum_list +=  self[i] * vector[i] 
            return sum_list
        else :
            return None   

    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        
        if len(self) != len(vector):
            return None
        
        add_lst = []
        for i in range(0, len(self)):
            add_lst.append( self[i] + vector[i] )
            
        vector = make_vector(add_lst, self.zero_test)
        return vector
        
        
        
        '''sumlist = []
        if isinstance(self,FullVector):
            if isinstance(vector,FullVector):
                if (len(self) != len(vector)):
                    return None
                else:
                    for i in range(len(self)):
                        sumlist.append(self[i]+vector[i])          
            elif isinstance(vector,SparseVector):
                sparse_new = []
                for i in range(0,vector.length):
                    if i in vector.indices:
                        sparse_new.append(vector[vector.indices.index(i)])
                    else:
                        sparse_new.append(0)
                if (len(self) != len(sparse_new)):
                    return None
                else:
                    for i in range(0,len(self)):
                        sumlist.append(self[i] + sparse_new[i])
        
        elif isinstance(self,SparseVector):
            sparse_new = []
            for i in range(0, self.length):
                if i in self.indices:
                        sparse_new.append(self[self.indices.index(i)])
                else:
                    sparse_new.append(0)
            if isinstance(vector,FullVector):
                if (len(sparse_new) != len(vector)):
                    return None
                else:
                    for i in range(0,len(vector)):
                        sumlist.append(sparse_new[i] + vector[i])
                        
            elif isinstance(vector, SparseVector):
                sparse_newer = []
                for i in range(0, vector.length):
                    if i in vector.indices:
                        sparse_newer.append(vector[vector.indices.index(i)])
                    else:
                        sparse_newer.append(0)
                if (len(sparse_new) != len(sparse_newer)):
                    return None
                else:
                    for i in range(0, self.length):
                        sumlist.append(sparse_new[i] + sparse_newer[i])
                        
        
        return make_vector(sumlist, self.zero_test)
                
                
        sumvector=make_vector(sumlist,self.zero_test)
        return sumvector'''
    
    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        diflist = []
        for i in range(len(self)):
            diflist.append(self[i] - vector[i])
        difvector=make_vector(diflist,self.zero_test)
        return difvector

    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        minlen = min(len(self),len(vector))
        for i in range(minlen):
            self[i] = self[i] + vector[i]
        return self
        
    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        minlen = min(len(self),len(vector))
        for i in range(minlen):
            self[i] = self[i] - vector[i]
        return self

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        vector1 = make_vector(self.lst[:len(self.lst)/2],self.zero_test)
        vector2 = make_vector(self.lst[len(self.lst)/2:],self.zero_test)
        return vector1,vector2
        
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
        return FullVector(self.lst[:len(self.lst)/2],self.zero_test),FullVector(self.lst[len(self.lst)/2:],self.zero_test)
        

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        lsttmp=self.lst
        lsttmp.extend(vector.self.lst)
        vectormerge = make_vector(lsttmp,self.zero_test)


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
        self.indices=indices
        self.length=length
        


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
            numindex=self.indices.index(i)
            return self.lst[numindex]
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
            numindex = self.indices.index(i)
            self.lst[numindex] = val
        else:
            self.indices.append(i)
            self.lst.append(val)


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        count = 0
        for i in self.lst:
            if i != 0 :
                count+=1
        if count == 0:
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
        l_list = []
        r_list = []
        l_values = []
        l_indices = []
        r_values = []
        r_indices = []
        
        for i in range(0, self.length/2):
            l_list.append(self[i])
        
        for i in range(self.length/2, self.length):
            r_list.append(self[i])
       
       
        for i in range(0, len(l_list)):
            if (self.zero_test(l_list[i]) == False):
                l_values.append(l_list[i])
                l_indices.append(i)
        l_vector = SparseVector(l_values, l_indices, self.length, self.zero_test)
        
        for i in range(0, len(r_list)):
            if (self.zero_test(r_list[i]) == False):
                r_values.append(r_list[i])
                r_indices.append(i)
        r_vector = SparseVector(r_values, r_indices, self.length, self.zero_test)
        
        
        return l_vector, r_vector        
   
        '''for element in left_vector:
            if(self.zerotest(element) == False):
                l_values.append(element)
                l_indices.append(left_vector.indexof(element))
        l_vector = SparseVector(l_values, l_indices, self.length, zero_test = lambda x : (x == 0))
            
        for element in right_vector:
            if(self.zerotest(element) == False):
                r_values.append(element)
                r_indices.append(right_vector.indexof(element))
        r_vector = SparseVector(r_values, r_indices, self.length, zero_test = lambda x : (x == 0))
            
        return l_vector, r_vector'''
    
    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        new_values = []
        new_indices = []
        
        for i in range(0, len(self)):
            if i in self.indices:
                new_values.append(self[i])
                new_indices.append(i)
                
        for i in range(0, len(vector)):
            if i in vector.indices:
                new_values.append(vector[i])
                new_indices.append(len(self) + i)
        
        return SparseVector(new_values, new_indices, self.length, self.zero_test)
        
vector1 = [1,2,3,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
vector2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
vector3 = [1,0,3,4,5,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
'''vector1=make_vector(vec,zero_test = lambda x : (x == 0))
vector2=make_vector(vect,zero_test = lambda x : (x == 0))
print len(vector1)
print vector2.is_zero()
vector3 = vector1 + vector2
print vector3
print vector3 == vector1
'''
'''print is_long_and_sparse(vector1,zero_test = lambda x : (x == 0))
print is_long_and_sparse(vector3,zero_test = lambda x : (x == 0))
v1= make_vector(vector1,zero_test = lambda x : (x == 0))
v2= make_vector(vector2,zero_test = lambda x : (x == 0))
v3= make_vector(vector3,zero_test = lambda x : (x == 0))
print v1 == v2
print v1 == v3
print v1 * v3
g , v = v1.split()
for i in range(len(g)):
    print g[i]

merge_vector = v1.merge(v3)
for i in range(0, len(merge_vector)):
    print merge_vector[i]'''