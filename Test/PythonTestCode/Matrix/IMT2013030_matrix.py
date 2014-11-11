'''
Created on 16-Nov-2013

@author: raghavan
'''
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD, zero_test

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    count = 0.0
    sparse = []
    indices = []
    for index, elem in enumerate(vector_list):
        if(elem.is_zero() and len(elem)>SIZE_THRESHOLD):
            count += 1
        else:
            sparse.append(elem)
            indices.append(index) 
    if(1>(count/len(vector_list)) > DENSITY_THRESHOLD):
        return SparseMatrix(sparse, indices, len(vector_list))
    else:
        return FullMatrix(vector_list)
    
    # Your Code
    

class Matrix(object):
    '''
    Base Matrix Class - implements basic matrix operations
    '''
    MIN_RECURSION_DIM = 3

    def __init__(self, rows):
        '''
        'rows' is a list of vectors
        Keep this is the row list for the matrix
        '''
        self.rows = rows
        # Your Code


    def __len__(self):
        '''
        Return the number of rows of the matrix - equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        return len(self.rows)
        # Your Code


    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        if attr == 'nrows':
            return len(self)
        if attr == 'ncols':
            return len(self[0])
        return None
        # Your Code
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        if (isinstance(key, int)):
            return self.rows[key]
        else:
            return self.rows[key[0]][key[1]]
        
        # Your Code
        
    def __setitem__(self, i, val):
        '''
        set the value of an item at position i
        '''
        self.rows[i] = val


    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if(len(self) <= self.MIN_RECURSION_DIM):
            return True
        return False
        # Your Code
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        if(len(self) == len(mat)):
            sum_matrix = []
            for pos in xrange(len(self)):
                sum_matrix.append(self[pos] + mat[pos])
            return make_matrix(sum_matrix)
        # Your Code


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        if(len(self) == len(mat)):
            diff_matrix = []
            for pos in range(len(self)):
                diff_matrix.append(self[pos] - mat[pos])
            return make_matrix(diff_matrix)
        # Your Code


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        
        for pos in xrange(len(self)):
            if(pos<len(mat)):
                self[pos] = self[pos] + mat[pos]
        return self
        # Your Code


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        for pos in xrange(len(self)):
            if(pos<len(mat)):
                self[pos] = self[pos] - mat[pos]
        return self
        # Your Code


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        left_mat, right_mat = [], []
        for pos in range(self.nrows):
            left_half, right_half = self[pos].split()
            left_mat.append(left_half)
            right_mat.append(right_half)
        return make_matrix(left_mat), make_matrix(right_mat)
        # Your Code
        
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        left, right = self.left_right_split()
        topleft = [left[pos] for pos in range(len(left)/2)]
        bottomleft = [left[pos] for pos in range(len(left)/2, len(left))]
        topright = [right[pos] for pos in range(len(right)/2)]
        bottomright = [right[pos] for pos in range(len(right)/2, len(right))]
        return make_matrix(topleft), make_matrix(topright), \
            make_matrix(bottomleft), make_matrix(bottomright)
        # Your Code


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        for pos in range(len(mat)):
            self[pos] = self[pos].merge(mat[pos])
        return self
        # Your Code


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        for pos in xrange(len(mat)):
            self.rows.append(mat[pos])
        return self
        # Your Code


    def rmul(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        
        if(len(vec) == len(self)):
            mul_vector = []
            for poscol in range(self.ncols):
                var = 0
                for posrow in range(len(vec)):
                    var += (vec[posrow]*self[posrow, poscol])
                mul_vector.append(var)
            return make_vector(mul_vector, zero_test)
        return None
        
        # Your Code

    def pad(self, add_temp):
        '''
        to add 0's to the matrices to make them 2^n x 2^n matrices
        '''
        zero_mat = []
        temp_mat = []
        for pos in range(add_temp - self.ncols):
            zero_mat.append(0)
        if(add_temp != self.ncols):
            zero_mat_obj = make_vector(zero_mat, zero_test)
            for pos in range(len(self)):
                temp_mat.append(self[pos].merge(zero_mat_obj))
            
        row = [0]*(add_temp)
        for elem in range(add_temp - self.nrows):
            temp_mat.append(make_vector(row, zero_test))
        return make_matrix(temp_mat)

    def __mul__(self, mat, flag = [0], remrow = [0], remcol = [0], temp = [0]):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        
        if(self.ncols == mat.nrows):
            if(self.is_small() or mat.is_small()):
                matrix = []
                for pos in range(0, len(self)):
                    matrix.append(mat.rmul(self[pos]))
                return make_matrix(matrix)
            else:
                if(flag[0] == 0):
                    maxtemp = max(self.nrows, mat.ncols, self.ncols, mat.nrows)
                    i = 1
                    add_temp = 0
                    while(1):
                        if( pow(2, i) > maxtemp > pow(2, i-1)):
                            add_temp = int(pow(2, i))
                            break
                        i += 1
                    remrow[0] = self.nrows
                    remcol[0] = mat.ncols
                    self = self.pad(add_temp)
                    mat = mat.pad(add_temp)
                    temp[0] = mat.ncols
                    flag[0] = 1
                a_mat, b_mat, c_mat, d_mat = self.get_quarters()
                e_mat, f_mat, g_mat, h_mat = mat.get_quarters()
                pm1 = a_mat*(f_mat-h_mat)
                pm2 = (a_mat+b_mat)*h_mat
                pm3 = (c_mat+d_mat)*e_mat
                pm4 = d_mat*(g_mat-e_mat)
                pm5 = (a_mat+d_mat)*(e_mat+h_mat)
                pm6 = (b_mat-d_mat)*(g_mat+h_mat)
                pm7 = (a_mat-c_mat)*(e_mat+f_mat)
                
                top_left =  (pm4+pm5+pm6)-pm2
                top_right = pm1+pm2
                bottom_left = pm3+pm4
                bottom_right = pm1+pm5-(pm7+pm3)
                
                top_left.merge_cols(top_right)
                bottom_left.merge_cols(bottom_right)
                
                final_mat = top_left.merge_rows(bottom_left)
                
                if(final_mat.ncols == temp[0]):
                    final_mat = final_mat.unpad(remrow[0], remcol[0])
                return final_mat
        # Your Code
        
        
    def unpad(self, row_len, col_len):
        '''
        to remove the added zero's in the final matrix
        ''' 
        mat_row = []
        for pos in range(row_len):
            mat_row.append(self[pos])
        mat_row_ob = make_matrix(mat_row)
        final_mat = []
        for pos in range(mat_row_ob.nrows):
            final_vector_ob = make_vector(mat_row_ob[pos][:col_len], zero_test)
            final_mat.append(final_vector_ob)
        
        return make_matrix(final_mat)

    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        if(len(mat) == len(self)):
            for pos in xrange(len(mat)):
                if mat[pos] != self[pos]:
                    return False
            return True
        return False
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
        self.length = length
        # Your Code


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        return self.length
        # Your Code
    
    
    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        if(isinstance(key, int) and key < self.nrows):
            if(key in self.indices):
                return self.rows[self.indices.index(key)]
            else:
                zero_vector = make_vector([0]*len(self.rows[0]), zero_test)
                return zero_vector
        # Your Code
        
        
    def __setitem__(self, i, val):
        if i in self.indices:
            self.rows[self.indices.index(i)] = val
        else:
            temp_mat = []
            for pos in range(len(self)):
                temp_mat.append(self[pos])
            temp_mat[i] = val
            self = make_matrix(temp_mat)
        

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        final_matrix = []
        for pos in range(len(self)):
            final_matrix.append(self[pos])
        for pos in range(len(mat)):
            final_matrix.append(mat[pos])
        return make_matrix(final_matrix)
        # Your Code


