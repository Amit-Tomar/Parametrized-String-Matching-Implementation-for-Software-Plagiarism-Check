'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 50
zero_test=lambda x :(x==0)

def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    # Your Code
    count_total=0
    count_zero=0
    for a in lst:
        if(zero_test(a)==True):
            count_total+=1
            count_zero+=1
        else:
            count_total+=1
    ratio = float(count_zero)/float(count_total)
    if(count_total>=SIZE_THRESHOLD and ratio>=DENSITY_THRESHOLD):
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
    lst_vector=[[],[]]
    
    for a in data:
        if(zero_test(a)==False):
            lst_vector[0].append(a)
            lst_vector[1].append(data.index(a))
    if(is_long_and_sparse(data,zero_test)==True):
        vector=SparseVector(lst_vector[0],lst_vector[1],0, zero_test)
    else:
        vector=FullVector(data,zero_test)
      
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
        self.data=lst
        self.test=zero_test

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
        count_zero=0
        total=0
        for a in self.data:
            if(self.test(a)==True):
                count_zero+=1
                total+=1
            else:
                total+=1
        if(total==count_zero):
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
        if(self.data==vector):
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
        dot_pro=[]
        ref=0
        temp=0
        sum_elem=0
        sum=0
        if(len(self.data)!=len(vector)):
            return None
        else:
            while(ref<len(vector)):
                sum+=(self.data[ref]*vector[ref])
                ref=ref+1
        l=len(dot_pro)
        while(temp<l):
            sum_elem+=dot_pro[temp]
            temp+=1
        return sum

    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        add=[]
        ref=0
        if(len(self.data)!=len(vector)):
            return None
        else:
            while(ref<len(self.data)):
                add.append(self.data[ref]+vector[ref])
                ref=ref+1
        return make_vector(add,zero_test)

    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        # Your Code
        sub=[]
        ref=0
        if(len(self.data)!=len(vector)):
            return None
        else:
            while(ref<len(self.data)):
                sub.append(self.data[ref]+vector[ref])
                ref=ref+1
        return make_vector(sub,zero_test)



    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        min_len=min(len(self.data),len(vector))
        iadd=[]
        ref=0
        while(ref<min_len):
                iadd.append(self.data[ref]+vector[ref])
                ref=ref+1
        return iadd
        
      
    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        # Your Code
        min_len=min(len(self.data),len(vector))
        isub=[]
        ref=0
        while(ref<min_len):
                isub.append(self.data[ref]-vector[ref])
                ref=ref+1
        return isub
        

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two vectors separately
        '''
        left=[]
        right=[]
        count=len(self.data)
        ref=0
        temp=count/2
        while(ref<temp):
            left.append(self.data[ref])
            ref=ref+1
        while(ref>=temp and ref<count):
            right.append(self.data[ref])
            ref=ref+1
        
        return left,right
        


class FullVector(Vector):
    '''
    A subclass of Vector where all elements are kept explicitly as a list
    '''
    def __init__(self, lst, zero_test = lambda x : (x == 0)):
        '''
        Constructor for a FullVector on data given in the 'lst' argument - 'lst' is the list of elements in the vector
        Uses the base (parent) class attributes data and zero_test
        '''
        self.full_lt=lst
        super(FullVector, self).__init__(lst, zero_test)

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        # Your Code
        obj=Vector(self.full,zero_test)
        split=obj.split()
        return split
        

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        app=[]
        ref=0
        temp=0
        while(ref<len(vector)):
            app.append(vector[ref])
            ref=ref+1
        while(temp<len(self.full_lt)):
            app.append(self.full_lt[temp])
            temp=temp+1
        return app
        
        


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
        self.value=values
        self.indice=indices
        self.len=length
        
        # Your Code

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        # Your Code
        return self.len


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        # Your Code
        if i in self.indice:
            return self.value[self.indice.index(i)]
        
        


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        # Your Code
        if i in self.indice:
            self.value[self.indice.index(i)]=val
        
        else:
            self.indice.append(i)
            self.value.append(val)
            


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        # Your Code
        count=0
        ref=len(self.value)
        for a in self.value:
            if a==0:
                count+=1
        if (count==ref):
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
        obj=Vector(self.values,zero_test)
        split=obj.split()
        return split

    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        # Your Code
        app=[]
        ref=0
        temp=0
        while(ref<len(vector)):
            app.append(vector[ref])
            ref=ref+1
        while(temp<len(self.value)):
            app.append(self.value[temp])
            temp=temp+1
