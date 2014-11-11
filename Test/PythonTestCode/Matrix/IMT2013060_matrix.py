'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD, Vector
import vector

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    values = []
    indices = []
    count = 0
    ncount = 0 
    for obj in vector_list:
        values.append(obj)
        indices.append(ncount)
        if obj.is_zero():
            count += 1
        ncount += 1
    if (len(vector_list) >= 50 and (count / len(vector_list)) > 0.4):
        
        return SparseMatrix(values, indices, length = len(vector_list))
    else:
        return FullMatrix(vector_list)

    # Your Code
    

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
        self.ROWS = rows
        # Your Code


    def __len__(self):
        '''
        Return the number of rows of the matrix - equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        return len(self.ROWS)
        # Your Code


    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        if attr == len(self.ROWS):
            return len(self.ROWS)
        # Your Code
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        if isinstance(key, tuple):
            return self.rows[key[0]-1][key[1]-1]
        else:
            return self.rows[key-1]
        # Your Code
        

    def is_small(self): #Doubt
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if len(self.rows) < 50:
            return True
        else: 
            return False
        # Your Code
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        final_matrix = Matrix([])
        if len(self.ROWS) == len(mat.ROWS):
            for i in range(0, len(mat)):
                final_matrix.ROWS.append(self.ROWS[i] + mat.ROWS[i])
            return final_matrix.ROWS
        else:
            return None
        # Your Code


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        final_matrix = Matrix([])
        if len(self.ROWS) == len(mat.ROWS):
            for i in range(0, len(mat)):
                final_matrix.ROWS.append(self.ROWS[i] - mat.ROWS[i])
            return final_matrix.ROWS
        else:
            return None
        # Your Code


    def __iadd__(self, mat): #This function is wrong
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        count = 0
        if len(self.ROWS) > len(mat.ROWS):
            count = len(self.ROWS)
        else:
            count = len(vector)
            
        if len(vector) == len(self.ROWS):
            final_list = self.ROWS + mat.ROWS
            return final_list
        
        else:
            final_list = []
            for x in range(0, count):
                final_list.append(self.ROWS[x] + mat.ROWS[x])
            return final_list
        # Your Code


    def __isub__(self, mat): #Doubt
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        list1, list2 = [], []
        if len(self.ROWS) % 2 == 0:
            list1 = self.ROWS[:len(self.ROWS) / 2]
            for obj in list1:
                obj.split()
            list2 = self.ROWS[len(self.ROWS) / 2 :]
            for obj in list2:
                obj.split()
            
        return 
        # Your Code

        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        
        # Your Code


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


    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code


    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code


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
    The vectors (non-zero) and their 
    corresponding indices are kept in separate lists
    '''
    def __init__(self, vectors, indices, length=0):
        '''
        'length' is the number of rows of the matrix - the number of entries in 'vectors' is just the number of
        non-zero rows
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseMatrix, self).__init__(vectors)
        # Your Code


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        # Your Code
    

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
        
list1 = [Vector([1,2,3]), Vector([20,30,40]),Vector([2,4,6])]  
list2 = [Vector([10,20,30]), Vector([2,5,7]), Vector([10,20,30])]      
matrix1 = Matrix(list1)
matrix2 = Matrix(list2)

a = Vector([1,2,3])
b = Vector([2,3,4])

print a + b