'''
Created on 16-Nov-2013

@author: raghavan

Modified on 12-Dec-2013

@modifier: Nigel Steven Fernandez (IMT2013027)
'''

from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD
import itertools
import math

def is_long_and_sparse_matrix(vector_list):
    '''
    Checks if it is worth using a sparse representation for a matrix (vectors given in the argument 'vector_list')
    '''
    is_long = len(vector_list) >= SIZE_THRESHOLD
    is_sparse = ((len([vector for vector in vector_list if vector.is_zero()]) / float(len(vector_list)))
                 >= DENSITY_THRESHOLD)
    
    return is_long and is_sparse


def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    if(is_long_and_sparse_matrix(vector_list)):
        if(len([vector for vector in vector_list if (not vector.is_zero())]) != 0):
            #creating 2 lists simultaneously
            indices, values = zip(*[(index, vector) for index, vector in enumerate(vector_list) 
                                    if (not vector.is_zero())])
        else:
            #(all vector are zero vectors)
            #storing first zero vector for calculating the number of columns of matrix = length of the zero vector
            #else the matrix will be empty and the number of columns will be lost
            indices, values = [0], [vector_list[0]]
        matrix = SparseMatrix(list(values), list(indices), len(vector_list))
    else:
        matrix = FullMatrix(vector_list)
    
    return matrix
    

class Matrix(object):
    '''
    Base Matrix Class - implements basic matrix operations
    '''
    
    MIN_RECURSION_DIM = 5
            
    def __init__(self, rows):
        '''
        'rows' is a list of vectors
        Keep this is the row list for the matrix
        '''
        self.rows = rows


    def __len__(self):
        '''
        Return the number of rows of the matrix - equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        return len(self.rows)


    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        if(attr == "nrows"):
            return len(self)
        elif(attr == "ncols"):
            return len(self[0])
        elif(attr == 'zero_vec'):
            #Returns a zero vector of length = no of columns in 'self' matrix
            return make_vector([0] * len(self.rows[0]), self.rows[0].zero_test)
        else:
            raise AttributeError("{} object has no attribute {}".format(self.__class__.__name__, attr))
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        if(isinstance(key, tuple)):
            return self.rows[key[0]][key[1]]
        else:
            return self.rows[key]
        

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if(self.nrows < self.MIN_RECURSION_DIM):
            return True
        else:
            return False
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        if(self.nrows == mat.nrows):
            return make_matrix([(row1 + row2) for row1, row2 in itertools.izip(self.components(), mat.components())])
        else:
            return None


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        if(self.nrows == mat.nrows):
            return make_matrix([(row1 - row2) for row1, row2 in itertools.izip(self.components(), mat.components())])
        else:
            return None


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        #izip creates a list of tuples of corresponding list elements upto the min length of the 2 lists
        #while izip_longest creates a list of tuples of corresponding list elements upto the max length of the 2 lists
        #the 'fillvalue' here will be a zero vector
        if(self.nrows <= mat.nrows):
            self = make_matrix([(row1 + row2) for row1, row2 in itertools.izip(self.components(), mat.components())])
        else:
            self = make_matrix([(row1 + row2) for row1, row2 in 
                                itertools.izip_longest(self.components(), mat.components(), fillvalue = self.zero_vec)])
            
        return self


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        if(self.nrows <= mat.nrows):
            self = make_matrix([(row1 - row2) for row1, row2 in itertools.izip(self.components(), mat.components())])
        else:
            self = make_matrix([(row1 - row2) for row1, row2 in 
                                itertools.izip_longest(self.components(), mat.components(), fillvalue = self.zero_vec)])
            
        return self


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''        
        left_rows, right_rows = zip(*[(row.split()) for row in self.components()])
        
        return make_matrix(left_rows), make_matrix(right_rows)
    
        
    def top_bottom_split(self):
        '''
        Matrix is divided into two halves - top and botton
        The two halves are returned after a call to make_matrix
        '''
        rows = list(self.components())
        top = make_matrix(rows[0 : (len(rows) / 2)])
        bottom = make_matrix(rows[(len(rows) / 2) : len(rows)])
        
        return top, bottom
    
    
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''        
        left, right = self.left_right_split()
        top_left, bottom_left = left.top_bottom_split()
        top_right, bottom_right = right.top_bottom_split()

        return top_left, top_right, bottom_left, bottom_right


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        return make_matrix([row1.merge(row2) for row1, row2 in itertools.izip(self.components(), mat.components())])


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        return make_matrix(list(self.components()) + list(mat.components()))


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        if(len(vec) == self.nrows):
            transposed_matrix = make_matrix([make_vector(list(column), vec.zero_test) 
                                 for column in itertools.izip(*self.components())])
            return make_vector([(vec * row) for row in transposed_matrix.components()], vec.zero_test)
        else:
            return None
        

    def __mul__(self, mat):
        '''
        Wrapper function. Actual implementation in method - multiply.
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''  
        if(self.ncols == mat.nrows):
            #if the starting matrices are small then directly do a multiplication
            if(self.is_small() or mat.is_small()):
                return self.multiply(mat)
            self, mat, pad_info = self.pad(mat)
            mat_m = self.multiply(mat)
            return mat_m.unpad(pad_info)
            #unpadding of self and mat is not required as __mul__ only uses copies of the 2 matrices
            #and the padding change will not get reflected in the calling function
        else:
            return None


    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        if(type(mat) == FullMatrix):
            return list(self.components()) == list(mat.components())
        else:
            return False


    def components(self):
        '''
        Allows one to iterate through the elements of the matrix as shown below
        for vector in matrix.components(): (matrix is an object of type Matrix or any of its derived classes)
        '''
        for i in xrange(self.nrows):
            yield self[i]
            
    #function added by @modifier

    def multiply(self, mat):
        '''
        Actual implementation of multiplication of two matrices.
        '''       
        if(self.is_small() or mat.is_small()):
            #Regular multiplication
            return make_matrix([row * mat for row in self.components()]) 
                   
        else:
            #Strassen's algorithm
            #self_quarters = A, B, C, D
            self_quarters = self.get_quarters()
            #mat_quarters = E, F, G, H
            mat_quarters = mat.get_quarters()
                
            p_1 = self_quarters[0].multiply(mat_quarters[1] - mat_quarters[3])
            p_2 = (self_quarters[0] + self_quarters[1]).multiply(mat_quarters[3])
            p_3 = (self_quarters[2] + self_quarters[3]).multiply(mat_quarters[0])
            p_4 = self_quarters[3].multiply(mat_quarters[2] - mat_quarters[0])
            p_5 = (self_quarters[0] + self_quarters[3]).multiply(mat_quarters[0] + mat_quarters[3])
            p_6 = (self_quarters[1] - self_quarters[3]).multiply(mat_quarters[2] + mat_quarters[3])
            p_7 = (self_quarters[0] - self_quarters[2]).multiply(mat_quarters[0] + mat_quarters[1] )
                
            top_left = p_5 + p_4 - p_2 + p_6
            top_right = p_1 + p_2
            bottom_left = p_3 + p_4
            bottom_right = p_1 + p_5 - p_3 - p_7
                
            top = top_left.merge_cols(top_right)
            bottom = bottom_left.merge_cols(bottom_right)
            return top.merge_rows(bottom)

    
    def print_matrix(self):
        '''
        Prints a matrix.
        '''
        for row in self.components():
            print list(row.components())

    
    def get_pow_2(self, mat):
        '''
        Returns the nearest upper power of 2 to the maximum dimension of the 2 matrices.
        '''        
        max_dim = max(self.nrows, self.ncols, mat.nrows, mat.ncols)
        
        return int(pow(2, math.ceil(math.log(max_dim, 2))))


    def pad(self, mat):
        '''
        Pad two matrices with zero_vectors as rows and columns to nearest multiple of 2.
        '''
        pow_2 = self.get_pow_2(mat)
        pad_info = [(pow_2 - dim) for dim in [self.nrows, self.ncols, mat.nrows, mat.ncols]]
        
        self = (self.merge_rows(make_matrix([make_vector([0] * self.ncols, self[0].zero_test) 
                for _ in xrange(pad_info[0])])) if(pad_info[0] != 0) else self)
        self = (self.merge_cols(make_matrix([make_vector([0] * pad_info[1]) for _ in xrange(self.nrows)]))
                if(pad_info[1] != 0) else self)

        mat = (mat.merge_rows(make_matrix([make_vector([0] * mat.ncols, mat[0].zero_test) 
                for _ in xrange(pad_info[2])])) if(pad_info[2] != 0) else mat)
        mat = (mat.merge_cols(make_matrix([make_vector([0] * pad_info[3]) for _ in xrange(mat.nrows)]))
               if(pad_info[3] != 0) else mat)

        return self, mat, pad_info


    def unpad(self, pad_info):
        '''
        Unpads a matrix (removes excess zero vectors) using padding information passed.
        '''  
        unrows = pad_info[0]
        uncols = pad_info[3]
             
        self = make_matrix(list(self.components())[ : -unrows]) if(unrows != 0) else self  
        self = (make_matrix([make_vector(list(row.components())[ : -uncols]) for row in self.components()]) 
                if(uncols != 0) else self)
        
        return self
 
    
class FullMatrix(Matrix):
    '''
    A subclass of Matrix where all rows (vectors) are kept explicitly as a list
    '''
    def __init__(self, vectors):
        '''
        Constructor for a FullVector on data given in the 'vectors' argument - 'vectors' is the list of elements in the matrix
        Uses the base (parent) class attributes rows
        '''
        super(FullMatrix, self).__init__(vectors)


class SparseMatrix(Matrix):
    '''
    A subclass of Matrix where most rows (vectors) are zero vectors
    The vectors (non-zero) and their corresponding indices are kept in separate lists
    '''
    def __init__(self, vectors, indices, length=0):
        '''
        'length' is the number of rows of the matrix - the number of entries in 'vectors' is just the number of
        non-zero rows
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseMatrix, self).__init__(vectors)
        self.indices = indices
        #If no length is passed, the length is assumed to be =  (highest index + 1)
        if(length == 0):
            self.length = indices[-1] + 1
        else:
            self.length = length


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        return self.length
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        i = key[0] if isinstance(key, tuple) else key
        
        #using bisection algorithm in sorted list - 'indices'
        index_of_row = bisect_left(self.indices, i)
        
        if(index_of_row != len(self.indices) and self.indices[index_of_row] == i):
            if(isinstance(key, tuple)):
                return self.rows[index_of_row][key[1]]
            else:
                return self.rows[index_of_row]
        else:
            return self.zero_vec


    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''        
        if(type(mat) == FullMatrix):
            return super(SparseMatrix, self).merge_rows(mat)
        else:
            #Sparse vector merged with another sparse vector = sparse vector
            if(mat[0].is_zero()):
                mat.rows = []
                mat.indices = []
            self.rows = self.rows + mat.rows
            self.indices = self.indices + [len(self) + index for index in mat.indices]
            self.length += mat.length
    
        return self


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        #Calling get_quarters method of Matrix class because
        #dividing a sparse matrix into 4 may produce a full matrix as one half. 
        #Therefore expanding a sparse matrix into its components.
        return super(SparseMatrix, self).get_quarters()


    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        Overrides default implementation of this method in Matrix class        
        '''
        if(type(mat) == SparseMatrix):
            return [self.rows, self.indices, self.length] == [mat.rows, mat.indices, mat.length]
        else:
            return False