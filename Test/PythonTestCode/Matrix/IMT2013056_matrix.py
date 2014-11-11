'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD
import math
def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
    if(len(vector_list)==0):
        return None
    count = 0
    index = []
    vectors = []
    for i in range(0, len(vector_list)):
        if vector_list[i].is_zero() == True:
            count += 1
        else:
            index += [i]
            vectors += [vector_list[i]]
    if(float(count)/len(vector_list) > 1-DENSITY_THRESHOLD):
        matrix = SparseMatrix( vectors, index, len(vector_list), \
                               len(vector_list[0]))
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
        # Your Code
        self.rows = rows

        


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
        if(attr == 'rows'):
            return len(self.rows[0])
        
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        value = 0
        result = []
        if(len(self) == len(mat)):
            for i in len(mat):
                value = self[i] + mat[i]
                result.append(value)
        else:
            return None

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        value = 0
        result = []
        if(len(self) == len(mat)):
            for i in len(mat):
                value = self[i] - mat[i]
                result.append(value)
        else:
            return None

    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        result = []
        if(len(self) != len(mat)):
            length = min(len(self), len(mat))
            for i in range(0, length):
                value = self[i] + mat[i]
                result.append(value)
            return value
        else:
            for i in range(0, len(self)):
                value = self[i] + mat[i]
                result.append(value)
            return value
        


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        result = []
        if(len(self) != len(mat)):
            length = min(len(self), len(mat))
            for i in range(0, length):
                value = self[i] - mat[i]
                result.append(value)
            return value
        else:
            for i in range(0, len(self)):
                value = self[i] - mat[i]
                result.append(value)
            return value
        


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        left_matrix = []
        right_matrix = []
        count = 0
        for i in range(0, len(self) / 2):
            left_matrix.append(self[i])
            count += 1
        for i in range(count, len(self)):
            right_matrix.append(self[i])
        return self.make_matrix(left_matrix), self.make_matrix(right_matrix)
        
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_matrix, right_matrix = self.left_right_split()
        top_left_matrix = []
        top_right_matrix = []
        bottom_left_matrix = []
        bottom_right_matrix = []
        
        top_left_matrix = math.floor(len(left_matrix/2))
        bottom_left_matrix = math.ceil(len(left_matrix/2))
        for i in range(top_left_matrix):
            top_left_matrix.append(left_matrix[i])
        for i in range(top_right_matrix):
            bottom_left_matrix.append(left_matrix[i])
        
        top_right_matrix = math.floor(len(right_matrix/2))
        bottom_right_matrix = math.ceil(len(right_matrix/2))
        for i in range(top_right_matrix):
            top_right_matrix.append(right_matrix[i])
        for i in range(bottom_right_matrix):
            bottom_right_matrix.append(right_matrix[i])
            
        

    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        for cols in mat:
            self.append(cols)
        return self


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        for rows in mat:
            self.append(rows)
        return self
        


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        self_transpose = []
        vector = []
        for i in range(0, len(self)):
            var = []
            for j in range(0, len(self[i])):
                value = self[j][i]
                var.append(value)
            self_transpose.append(var)
        for i in range (len(vec)):
            final_value = 0
            for j in range(len(self_transpose)):
                value = vec[j] * self_transpose[i][j]
                final_value = value + final_value
            vector.append(final_value)
        return vector
        
        
        


    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        if(self.ncols == mat.nrows):
            A, B, C, D = self.get_quarters()
            E, F, G, H = mat.get_quarters()
            if(self.is_small()):
                matrix = []
                for pos in range(len(self)):
                    matrix.append(mat.rmul(self[pos]))
                return make_matrix(matrix) 
            
            '''
            #A, B, C, D = mat.get_quarters()
            #E, F, G, H = self.get_quarters()
            l = [A,B,C,D,E,F,G,H]
            for i in l:
            ''' 
            a = (A + D) * (E + H)
            b = (C + D) * E
            c = A * (F - H)
            d = (D) * (G - E)
            e = (A + B) * H
            f = (C - A) * (E + F)
            g = (B - D) * (G + H)
            tl = a + d - e + g
            tr = c + e
            bl = b + d
            br = a - b + c + f

            tl = tl.merge_cols(tr)
            bl = bl.merge_cols(br)
            rix = tl.merge_rows(bl)
            return rix
        return None


    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        for i in len(self):
            for j in len(mat):
                if(self[i] == mat[i]):
                    return True
                


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
        self.vectors = vectors
        self.indices = indices
        self.length = length
      


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        # Your Code
        return len(self.length)
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        # Your Code
        return self[key]

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        for i in self:
            for j in mat:
                mat[j].extend(self[i])
                i+=1
        
        
        


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_matrix, right_matrix = self.left_right_split()
        
        top_left_matrix = []
        top_right_matrix = []
        bottom_left_matrix = []
        bottom_right_matrix = []
        
        top_left_matrix = math.floor(len(left_matrix/2))
        bottom_left_matrix = math.ceil(len(left_matrix/2))
        for i in range(top_left_matrix):
            top_left_matrix.append(left_matrix[i])
        for i in range(top_right_matrix):
            bottom_left_matrix.append(left_matrix[i])
        
        top_right_matrix = math.floor(len(right_matrix/2))
        bottom_right_matrix = math.ceil(len(right_matrix/2))
        for i in range(top_right_matrix):
            top_right_matrix.append(right_matrix[i])
        for i in range(bottom_right_matrix):
            bottom_right_matrix.append(right_matrix[i])
            
        
        
if __name__ == '__main__':
    pass
    