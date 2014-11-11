'''
Created on 16-Nov-2013

@author: raghavan
'''
#from bisect import bisect_left
from vector import make_vector, DENSITY_THRESHOLD # SIZE_THRESHOLD,
ZERO_TEST = lambda x : (x == 0)
def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
    count = 0
    for vector in vector_list:
        if vector.is_zero() == True:
            count += 1
    if count >= len(vector_list)*DENSITY_THRESHOLD:
        vects , ind = [], []
        for vector in vector_list:
            if vector.is_zero() != True:
                vects.append(vector)
                ind.append(vector_list.index(vector))
        if(len(vects) == 0):
            vects.append(make_vector([0] * len(vector_list[0]), ZERO_TEST))
        return SparseMatrix(vects, ind, len(vector_list))
    else:
        return FullMatrix(vector_list)
        
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
        self.p_rows = 0
        self.p_cols = 0
    
    def pad(self, mat):
        '''This function does padding'''
        prow1, prow2, pcol1, pcol2, count, flag = self.nrows,  mat.nrows, \
         self.ncols, mat.ncols, 0,0
        while prow1 > 1:
            if prow1 % 2 == 0:
                flag = 1
            prow1 /= 2
            count += 1
        prow1 = (2 ** (count + 1))
        if flag == 1:
            prow1 = (2 ** count)
        count, flag = 0, 0
        while prow2 > 1:
            if 2 % 2 == 0:
                flag = 1
            prow2 /= 2
            count += 1
        prow2 = (2 ** (count + 1))
        if flag == 1:
            prow2 = (2 ** count)
        count, flag = 0, 0    
        while pcol1 > 1:
            if pcol1 % 2 == 0:
                flag = 1
            pcol1 /= 2
            count += 1
        pcol1 = (2 ** (count + 1))
        if flag == 1:
            pcol1 = (2 ** count)  
        count, flag = 0, 0
        while pcol2 > 1:
            if 2 % 2 == 0:
                flag = 1
            pcol2 /= 2
            count += 1
        pcol2 = (2 ** (count + 1)) 
        if flag == 1:
            pcol2 = (2 ** count)
        rows, cols = max(prow1, prow2), max(pcol1, pcol2)
        val = max(rows, cols)
        self.p_rows, self.p_cols, mat.p_rows, \
         mat.p_cols = 2**val - self.nrows, \
         val - self.ncols, val - mat.nrows, val - mat.ncols
        if flag == 1:
            temp = 0
            while temp < val - self.nrows:
                self.rows.append(make_vector([0] * self.nrows, ZERO_TEST))
                temp += 1          
            temp = 0
            while temp < val - mat.nrows:
                mat.rows.append(make_vector([0] * self.nrows, ZERO_TEST))
                temp += 1                
            for i in range(0, len(self[0])):
                temp = 0
                while temp < val - self.ncols:
                    self[i].add_elem(0)
                    temp += 1                  
            for i in range(0, len(mat[0])):
                temp = 0
                while temp < val - mat.ncols:
                    mat[i].add_elem(0)
                    temp += 1 
                       
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
        if attr == 'ncols':
            return len(self.rows[0])
        elif attr == 'nrows':
            return len(self)
        
    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if isinstance(key, tuple):
            return self.rows[key[0]][key[1]]
        else:
            return self.rows[key]

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if len(self) <= self.MIN_RECURSION_DIM: #SIZE_THRESHOLD
            return True
    
    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        matrix = []
        if self.nrows != mat.nrows or self.ncols != mat.ncols:
            return None
        for i in range(0, len(self)):
            matrix.append(self[i] + mat[i])
        return make_matrix(matrix)
            
    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        matrix = []
        if self.nrows != mat.nrows or self.ncols != mat.ncols:
            return None
        for i in range(0, len(self)):
            matrix.append(self[i] - mat[i])
        return make_matrix(matrix)
    
    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        matrix = []
        for i in range(0, min(len(self), len(mat))):
            matrix.append(self.rows[i] + mat[i])
        return make_matrix(matrix)


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        matrix = []
        for i in range(0, min(len(self), len(mat))):
            matrix.append(self.rows[i] - mat[i])
        return make_matrix(matrix)

    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        lst1, lst2 = [], []
        for i in self:
            if len(i) != 0:
                temp1, temp2 = i.split()
                lst1.append(temp1)
                lst2.append(temp2)
        return make_matrix(lst1), make_matrix(lst2)
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        mat1, mat2 = self.left_right_split()
        mat3 = mat1[len(mat1)/2:]
        mat1 = mat1[:len(mat1)/2]
        mat4 = mat2[len(mat2)/2:]
        mat2 = mat2[:len(mat2)/2]
        return make_matrix(mat1), make_matrix(mat2), \
             make_matrix(mat3), make_matrix(mat4)

    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        merged_cols = []
        for i in range(0, len(self)):
            merged_cols.append(self[i])
        for i in range(0, len(mat)):
            merged_cols.append(mat[i])
        return make_matrix(merged_cols)

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        merged = []
        for i in range(0, len(self)):
            self[i].merge(mat[i])
            merged.append(self[i])
        return make_matrix(merged)

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
        if self.ncols != mat.nrows:
            return None
        self.pad(mat)
        rows, cols = self.p_rows, mat.p_cols 
        if self.is_small() or mat.is_small():
            matrix, column, k = [], [], 0
            for i in range(0, len(self)):
                matrix.append([])
                for col in range(0, mat.ncols):
                    column = []
                    for row in range(0, mat.nrows):
                        column.append(mat[row][col])
                    matrix[k].append(self[i] * make_vector(column, ZERO_TEST))
                matrix[k] = make_vector(matrix[k], ZERO_TEST)
                k += 1
            return make_matrix(matrix)       
        a_1, a_2, a_3, a_4 = self.get_quarters()
        b_1, b_2, b_3, b_4 = mat.get_quarters()
        p_1, p_2, p_3, p_4, p_5, p_6, p_7 = a_1 * (b_2 - b_4), \
        (a_1 + a_2) * b_4, \
        (a_3 + a_4) * b_1, a_4 * (b_3 - b_1), (a_1 + a_4) * (b_1 + b_4), \
         (a_2 - a_4) * (b_3 + b_4), (a_1 - a_3) * (b_1 + b_2)
        final_mat = (((p_4 + p_5 + p_6 - p_2).merge_cols(p_3 + p_4)).\
                merge_rows((p_1 + p_2).merge_cols(p_1 - p_3 + p_5 - p_7)))
        if isinstance(final_mat, SparseMatrix):
            i = 0
            while i < cols:
                final_mat[0].pop()
        else:
            i = 0
            while i < rows:
                final_mat.rows.pop()
            i = 0
            while i < cols:
                for j in range(0, len(final_mat)):
                    final_mat[j].pop()
        return final_mat
             
    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if len(self) != len(mat):
            return False
        for i in range(0, len(self)):
            if self.rows[i] != mat.rows[i]:
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

class SparseMatrix(Matrix):
    '''
    A subclass of Matrix where most rows (vectors) are zero vectors
    The vectors (non-zero) and their corresponding indices are kept in separate lists
    '''
    def __init__(self, vectors, indices, length = 0):
        '''
        'length' is the number of rows of the matrix - the number of entries in 'vectors' is just the number of
        non-zero rows
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseMatrix, self).__init__(vectors)
        # Your Code
        self.indices = indices
        self.length = length
        self.p_rows = 0
        self.p_cols = 0

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
        if isinstance(key, tuple):
            if key[0] in self.indices:
                return self.rows[key[0]][key[1]]
            else:
                return 0
        elif key not in self.indices:
            return make_vector([0] * self.ncols, ZERO_TEST)
        else:
            return self.rows[key]

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        merged_vect = []
        for i in range(0, len(self)):
            self[i].merge(mat[i])
            merged_vect.append(self[i])
        return make_matrix(merged_vect)
            
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        lst1, lst2 = [], []
        for i in range(0, len(self)):
            temp1, temp2 = self[i].split()
            lst1.append(temp1)
            lst2.append(temp2)
        mat1 = make_matrix(lst1[:len(lst1)/2])
        mat2 = make_matrix(lst2[:len(lst2)/2])
        mat3 = make_matrix(lst1[len(lst1)/2:])
        mat4 = make_matrix(lst2[len(lst2)/2:])
        return mat1, mat2, mat3, mat4