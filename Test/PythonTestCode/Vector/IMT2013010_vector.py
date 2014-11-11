'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left

DENSITY_THRESHOLD = 0.4
SIZE_THRESHOLD = 50
def zero_test(element):
    if(element==0):
        return True
    else:
        return False
def is_long_and_sparse(lst, zero_test):
    '''
    Checks if it is worth using a sparse representation for a vector (elements given in the argument 'lst')
    '''
    count_zero=0
    for x in lst:
        if(zero_test(x)==True):
            count_zero+=1
    if(len(lst)>=SIZE_THRESHOLD and (count_zero/len(lst))>=DENSITY_THRESHOLD):
        return True
    else:
        return False


def make_vector(data, zero_test):
    '''
    Make a vector out of the list of data values in 'data'
    Depending on whether this list passes the 'is_long_and_sparse' test, either instantiate the FullVector class
    or the SparseVector class
    '''
    if(is_long_and_sparse(data,zero_test)==True):
        value_list=[]
        indices_list=[]
        length=len(data)
        for x in data:
            if(zero_test(x)==True):
                continue
            else:
                value_list.append(x)
                indices_list.append(data.index(x))
        sparse_vector_object=SparseVector(value_list,indices_list,length)
        return sparse_vector_object
    else:
        full_vector_object=FullVector(data)
    return full_vector_object


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
        self.list=lst


    def __len__(self):
        '''
        Returns the length of the vector (this method allows you to use the built-in function len()
        on any object of type Vector.
        '''
        return len(self.list)


    def __getitem__(self, i):
        '''
        Return the i-th element of the vector (allows you to use the indexing operator [] on a Vector object)
        '''
        return self.list[i]
    

    def __setitem__(self, i, val):
        '''
        Set the i-th element of the vector to 'val' using the indexing operator [] on a Vector object
        '''
        self.list[i]=val

    
    def is_zero(self):
        '''
        Check if the vector object is identically zero (all elements are zero)
        '''
        count=0
        for x in self.list:
            if(x==0):
                count+=1
        if(count==len(self.list)):
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
        i=0
        if(len(self.list)==len(vector.list)):
            while(i<len(self.list)):
                if(self.list[i]==vector.list[i]):
                    continue
                else:
                    break
                i+=1
            if(i==len(self.list)-1):
                return True
            else:
                return False
        else:
            return False


    def __mul__(self, vector):
        '''
        Return the inner(dot)-product of this vector with another 'vector' (allows use of * operator between vectors)
        Assumes that the elements of the vectors have a * operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        i=0
        dot_product_value=0
        if(len(self.list)==len(vector.list)):
            while(i<len(self.list)):
                dot_product_value+=self.list[i]*vector.list[i]
                i+=1
            return dot_product_value
        else:
            return None


    def __add__(self, vector):
        '''
        Return the sum of this vector with another 'vector' (allows use of + operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        i=0
        sum_list=[]
        if(len(self.list)==len(vector.list)):
            while(i<len(self.list)):
                sum_list.append(self.list[i]+vector.list[i])
                i+=1
            sum_object=make_vector(sum_list,zero_test)
            return sum_object
        else:
            return None


    def __sub__(self, vector):
        '''
        Return the difference of this vector with another 'vector' (allows use of - operator between vectors)
        Use the make_vector function to instantiate the appropriate subclass of Vector
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        If the lengths of this and 'vector' are not the same, then return None
        '''
        i=0
        diff_list=[]
        if(len(self.list)==len(vector.list)):
            while(i<len(self.list)):
                diff_list.append(self.list[i]-vector.list[i])
                i+=1
            diff_object=make_vector(diff_list,zero_test)
            return diff_object
        else:
            return None


    def __iadd__(self, vector):
        '''
        Implements the += operator with another 'vector'
        Assumes that the elements of the vectors have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        i=0
        sum_list1=[]
        sum_list=[]
        if(len(self.list)==len(vector.list)):
            while(i<len(self.list)):
                sum_list.append(self.list[i]+vector.list[i])
                i+=1
            return make_vector(sum_list,zero_test)
        else:
            j=0
            smaller_value=min(len(self.list),len(vector.list))
            larger_value=max(len(self.list),len(vector.list))
            while(j<smaller_value):
                sum_list1.append(self.list[j]+vector.list[j])
                j+=1
            while(j<larger_value):
                if(larger_value==len(self.list)):
                    sum_list1.append(self.list[j])
                elif(larger_value==len(vector.list)):
                    sum_list1.append(vector.list[j])
                j+=1
            return make_vector(sum_list1,zero_test)


    def __isub__(self, vector):
        '''
        Implements the -= operator with another 'vector'
        Assumes that the elements of the vectors have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the two lengths (in case the vectors are of different lengths)
        '''
        i=0
        diff_list1=[]
        diff_list=[]
        if(len(self.list)==len(vector.list)):
            while(i<len(self.list)):
                diff_list.append(self.list[i]-vector.list[i])
                i+=1
            return make_vector(diff_list,zero_test)
        else:
            j=0
            smaller_value=min(len(self.list),len(vector.list))
            larger_value=max(len(self.list),len(vector.list))
            while(j<smaller_value):
                diff_list1.append(self.list[j]-vector.list[j])
                j+=1
            while(j<larger_value):
                if(larger_value==len(self.list)):
                    diff_list1.append(self.list[j])
                elif(larger_value==len(vector.list)):
                    diff_list1.append(vector.list[j])
                j+=1
            return make_vector(diff_list1,zero_test)


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
        self.list=lst

    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (full) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        lsthalf1=[]
        lsthalf2=[]
        if(len(self)%2==0):
            lsthalf1=self.list[:(len(self.list)/2)]
            lsthalf2=self.list[(len(self.list)/2):]
            return lsthalf1,lsthalf2
        else:
            lsthalf1=self.list[:(len(self.list)+1)/2]
            lsthalf2=self.list[(len(self.list)+1)/2:]
            return (lsthalf1,lsthalf2)


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        for i in range(len(vector.list)):
            self.list.append(vector.list[i])


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
        self.values=values
        self.indices=indices
        self.length=length


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse vectors
        '''
        return self.length
        


    def __getitem__(self, i):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse vectors
        '''
        if i in self.indices:
            return self.values[self.indices.index(i)]
        else:
            return 0


    def __setitem__(self, i, val):
        '''
        Overriding the default __setitem__ method with behavior specific to sparse vectors
        Locate the index i and if it is not already there insert appropriate values into data and indices
        If the index i is there then update the corresponding value to 'val'
        '''
        if i in self.indices:
            self.values[self.indices.index(i)]=val
        else:
            self.indices.append(i)
            self.values.append(val)


    def is_zero(self):
        '''
        Overriding the default is_zero method specific to sparse vectors
        '''
        if(len(self.indices)==0 or len(self.values)==0):
            return True
        else:
            return False


    def split(self):
        '''
        Split the vector into two halves - left and right
        Return two (sparse) vectors separately
        This overrides the default implementation of this method in the Vector Class
        '''
        lstvalue1=[]
        lstindex1=[]
        lstvalue2=[]
        lstindex2=[]
        index=0
        if(self.length%2==0):
            while(index<=(self.length/2)):
                lstvalue1.append(self.values[index])
                lstindex1.append(self.indices[index])
                index+=1
            while(index<=len(self.length)):
                lstvalue2.append(self.values[index])
                lstindex2.append(self.indices[index])
                index+=1
        else:
            while(index<=(self.length+1/2)):
                lstvalue1.append(self.values[index])
                lstindex1.append(self.indices[index])
                index+=1
            while(index<=len(self.length)):
                lstvalue2.append(self.values[index])
                lstindex2.append(self.indices[index])
                index+=1
        return ((lstvalue1,lstindex1),(lstvalue2,lstindex2))


    def merge(self, vector):
        '''
        Merge this vector with 'vector' - append the elements together (this followed by 'vector')
        '''
        i=0
        while(i<len(vector.list)):
            if(vector.list[i]==0):
                continue
            else:
                self.indices.append(i)
                self.values.append(vector.list[i])




vector_obj2=FullVector([1,2,3,4,5,6,7,8,9],zero_test)
vector_obj=FullVector([1,2,3,4,5,6,7,8],zero_test)
vector_obj.merge(vector_obj2)
print vector_obj.list
