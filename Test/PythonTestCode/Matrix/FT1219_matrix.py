'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import SparseVector, make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD, ZERO_TEST

def is_large_and_sparse(vector_list):
    '''
    Checks if it is worth using a sparse representation for a matrix (rows given in the argument 'lst' of vectors)
    '''
    nonzero_count = len([v for v in vector_list if (not v.is_zero())])
    # True if the vector is long enough and there are enough number of non zero entries
    return (len(vector_list) > SIZE_THRESHOLD and nonzero_count < (len(vector_list) * DENSITY_THRESHOLD))

def make_matrix(data):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    matrix = None
    if (is_large_and_sparse(data)):
        indices = []
        rows = []
        for idx, row in enumerate(data):
            if not row.is_zero():
                indices.append(idx)
                rows.append(row)
        matrix = SparseMatrix(rows, indices, len(data))
    else:
        matrix = FullMatrix(data)
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
        return None


    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        return len(self.rows[0]) if (attr == 'ncols') else (len(self) if (attr == 'nrows') else None)
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        if isinstance(key, tuple):
            return self[key[0]][key[1]]
        elif isinstance(key, int):
            return self.rows[key]
        else:
            return None


    def __setitem__(self, key, val):
        '''
        Set the key-th element (row if key is an int and is a elementary type otherwise)
        of the vector to 'val' using the indexing operator [] on a Matrix object
        '''
        if isinstance(key, tuple):
            self[key[0]][key[1]] = val
        elif isinstance(key, int):
            self.rows[key] = val


    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        return (self.nrows < self.MIN_RECURSION_DIM and self.ncols < self.MIN_RECURSION_DIM)
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        if (self.nrows != mat.nrows):
            return None
    
        return make_matrix([(self[i] + mat[i]) for i in range(self.nrows)])


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        if (self.nrows != mat.nrows):
            return None
    
        return make_matrix([(self[i] - mat[i]) for i in range(self.nrows)])


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        for row in range(min(self.nrows, mat.nrows)):
            self[row] +=  mat[row]
        return self


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        for row in range(min(self.nrows, mat.nrows)):
            self[row] -=  mat[row]
        return self


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        matleft = []
        matright = []
        for row in range(self.nrows):
            left, right = self[row].split()
            matleft.append(left)
            matright.append(right)
        return make_matrix(matleft), make_matrix(matright)
        
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        matleft, matright = self.left_right_split()
        rowsby2 = self.nrows/2
        topleft = make_matrix(matleft.rows[:rowsby2])
        bottomleft = make_matrix(matleft.rows[rowsby2:])
        topright = make_matrix(matright.rows[:rowsby2])
        bottomright = make_matrix(matright.rows[rowsby2:])
        return topleft, topright, bottomleft, bottomright


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        return make_matrix([self[i].merge(mat[i]) for i in range(self.nrows)]) if (self.nrows == mat.nrows) else None


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        return (make_matrix(self.rows + mat.rows) if (self.ncols == mat.ncols) else None)


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        if (len(vec) == self.nrows):
            return make_vector([sum([(vec[r]*self[r, c]) for r in range(len(vec))]) for c in range(self.ncols)],
                               vec.zero_test)
        else:
            return None


    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        if (self.ncols == mat.nrows):
            if (self.is_small() or mat.is_small()):
                return make_matrix([(self[r]*mat) for r in range(self.nrows)])
            else:
                matA, matB, matC, matD = self.get_quarters()
                matE, matF, matG, matH = mat.get_quarters()
                matp1 = matA * (matF - matH)
                matp2 = (matA + matB) * matH
                matp3 = (matC + matD) * matE
                matp4 = matD * (matG - matE)
                matp5 = (matA + matD) * (matE + matH)
                matp6 = (matB - matD) * (matG + matH)
                matp7 = (matA - matC) * (matE + matF)
                
                matP = matp5 + matp4 - matp2 + matp6
                matQ = matp1 + matp2
                matR = matp3 + matp4
                matS = matp1 + matp5 - matp3 - matp7
                
                topmat = matP.merge_cols(matQ)
                bottommat = matR.merge_cols(matS)
                return topmat.merge_rows(bottommat)
        else:
            return None


    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        if (self.nrows != mat.nrows):
            return False
        else:
            for i in range(self.nrows):
                if not (self[i] == mat[i]):
                    return False
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

    def __len__(self):
        '''
        Return the number of rows of the matrix - equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        return len(self.rows)

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
        self.size = max(indices[-1], length) if (len(indices) > 0) else length


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        return self.size


    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        if isinstance(key, tuple):
            return self[key[0]][key[1]]
        elif isinstance(key, int):
            idx = bisect_left(self.indices, key)
            return (self.rows[idx] if (idx < len(self.indices) and self.indices[idx] == key) else
                    SparseVector([], [], self.ncols, ZERO_TEST))
        else:
            return None


    def __setitem__(self, key, val):
        '''
        Set the key-th element (row if key is an int and is a elementary type otherwise)
        of the vector to 'val' using the indexing operator [] on a Matrix object
        '''
        if isinstance(key, tuple):
            self[key[0]][key[1]] = val
        elif isinstance(key, int):
            idx = bisect_left(self.indices, key)
            if (idx < len(self.indices) and self.indices[idx] == key):
                self.rows[idx] = val
            else:
                self.rows.insert(idx, val)
                self.indices.insert(idx, key)


    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        shift_indices = [(mat.indices[i] + len(self)) for i in range(len(mat.indices))]
        return SparseMatrix((self.rows + mat.rows), (self.indices + shift_indices), (len(self) + len(mat)))


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        matleft, matright = self.left_right_split()
        rowsby2 = self.nrows/2
        idx = bisect_left(self.indices, rowsby2)
        bottom_indices = [(index - rowsby2) for index in self.indices[idx:]]
        topleft = SparseMatrix(matleft.rows[:idx], matleft.indices[:idx], rowsby2)
        bottomleft = SparseMatrix(matleft.rows[idx:], bottom_indices, (len(matleft) - rowsby2))
        topright = SparseMatrix(matright.rows[:idx], matright.indices[:idx], rowsby2)
        bottomright = SparseMatrix(matright.rows[idx:], bottom_indices, (len(matright) - rowsby2))
        return topleft, topright, bottomleft, bottomright