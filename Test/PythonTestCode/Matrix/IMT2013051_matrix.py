'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
    count=0
    vectors=[]
    indices=[]
    for i in xrange(len(vector_list)):
        if vector_list[i].is_zero() is False:
            count=count+1
            vectors.append(vector_list[i])
            indices.append(i)
    density=count/len(vector_list)
    if(density<DENSITY_THRESHOLD and (len(vector_list)>SIZE_THRESHOLD)):
        matrix=SparseMatrix(vectors,indices,len(vector_list))
        return matrix
    else:
        matrix=FullMatrix(vector_list)
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
        # Your Code
        self.rows=rows
        
    def __len__(self):
        '''
        Return the number of rows of the matrix - equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        # Your Code
        return len(self.rows)

    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        # Your Code
        if(attr=='nrows'):
            return len(self.rows)
        else:
            return len(self.rows[0])
              

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if(isinstance(key,int)):
            return self.rows[key-1]
        else:
            return self.rows[key[0]-1][key[1]-1]

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if len(self) <= self.MIN_RECURSION_DIM:
            return True
        return False

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        if(len(self.rows)!=len(mat.rows)):
            return None
        else:
            sum_matrix = []
            
            for i in range(len(self.rows)):
                sum_matrix.append(self[i]+mat[i])
            sum_mat = make_matrix(sum_matrix)
            return sum_mat
        
        
        
    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        if(len(self.rows)!=len(mat.rows)):
            return None
        else:
            difference_matrix = []
            for i in range(len(self.rows)):
                difference_matrix.append(self[i]-mat[i])
            difference_mat = make_matrix(difference_matrix)
            return difference_mat

    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        min_len = min(len(self.rows), len(mat))
        for i in range(min_len):
            self.rows[i] = self.rows[i] + mat[i]

    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        min_len = min(len(self.rows), len(mat))
        for i in range(min_len):
            self.rows[i] = self.rows[i] - mat[i]

    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        left = []
        right = []
        for i in range(len(self)):
            left.append(self[i].split()[0])
            right.append(self[i].split()[1])
        left_mat = make_matrix(left)
        right_mat = make_matrix(right)
 
        return left_mat, right_mat
        
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        lf, rt = self.left_right_split()
        x=len(self.rows)/2
        top_left = lf[:x]
        top_right = rt[:x]
        bottom_left = lf[x:]
        bottom_right = rt[x:]
        return make_matrix(top_left), make_matrix(top_right), make_matrix(bottom_left), make_matrix(bottom_right)

    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        if(len(vec)==len(self)):
            lst = []
            sum_element=0
            for j in range(len(self[0])):
                for i in range(len(vec)):
                    sum_element=sum_element+(self[i][j]*vec[i])
                lst.append(sum_element)
                sum_element=0
            vector=make_vector(lst,None)
            return vector
        else:
            return None
    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        product=[]
        

    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if(len(self)==len(mat)):
            for i in xrange(len(self)):
                if (self[i]==mat[i]) is False:
                    return False
            return True
        else:
            return False        
class FullMatrix(Matrix):
    '''
    A subclass of Matrix where all rows (vectors) are kept explicitly as a list
    '''
    def __init__(self, vectors):
        '''
        Constructor for a FullVector on data given in the 'lst' argument - 'lst' is the list of elements in the vector
        Uses the base (parent) class attributes data and zero_test
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
        # Your Code
        self.length=length
        self.vectors=vectors
        self.indices=indices

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        # Your Code
        return self.length

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        # Your Code
        
    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
if __name__ == '__main__':
    data=[1,0,0,0,0,0,0,0,0,0]
    data1= [1, 1, 1, 1, 1, 1, 1,1,1,1]
    vector1=make_vector(data,None)
    vector2=make_vector(data1,None)
    mat1 = make_matrix([vector1,vector1,vector1,vector1,vector1,vector1,vector1,vector1,vector1,vector1,])
    mat2 = make_matrix([vector1,vector1,vector1,vector1,vector1,vector1,vector1,vector1,vector1,vector1,])
    if (mat1==mat2) is True:
        print 123
    
    vector3=mat1.__rmul__(vector2)
    print vector3.data