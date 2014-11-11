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
    non_zero = []
    indices = []
    for obj in range(len(vector_list)):
        if(vector_list[obj].is_zero() == False):
            non_zero.append(vector_list[obj])
            indices.append(obj)
    density = float(len(non_zero))/len(vector_list)
    if(density <= DENSITY_THRESHOLD):
        matrix = SparseMatrix(non_zero , indices , len(vector_list))
        return matrix
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
        if attr == 'nrows': 
            return len(self.rows)
        if attr == 'ncolumns':
            return len(self.rows[0])
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        if(isinstance(key, tuple) == True ): 
            return self.rows[key[0]][key[1]]
        else:
            return self.rows[key]        

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if ( len(self) <= self.MIN_RECURSION_DIM):
            return True
        else:
            return False
    
    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        if len(self) != len(mat):
            return None
        else:
            sum_matrix = []
            for item in range(len(self)):
                sum_matrix.append(self[item] + mat[item])
                sum_mat = make_matrix(sum_matrix)
            return sum_mat
        

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        if len(self) != len(mat):
            return None
        else:
            diff_matrix = []
            for item in range(len(self)):
                diff_matrix.append(self[item] - mat[item])
                diff_mat = make_matrix(diff_matrix)
            return diff_mat


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        mini = min(len(self), len(mat))
        for i in range(0 , mini):
            self[i] = self[i] + mat[i]
         
    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        mini = min(len(self), len(mat))
        for i in range(0 , mini):
            self[i] = self[i] - mat[i]

    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        left_list = []
        right_list = []
        for vector in len(self):
            left_list.append(vector.split()[0])
            right_list.append(vector.split()[1])
        return left_list , right_list
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        left, right = self.left_right_split()
        topleft = left[:len(self)//2]
        topright = right[:len(self)//2]
        bottomleft = left[len(self)//2:]
        bottomright = right[len(self)//2:]
            
        return make_matrix(topleft), make_matrix(topright), make_matrix(bottomleft), make_matrix(bottomright)
        
    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        matrix_merged = []
        for i in range(len(self)):
            lst = []
            for value1 in self[i]:
                lst.append(value1)
            for value2 in mat[i]:
                lst.append(value2)
        matrix_merged.append(lst)        
        return make_matrix(matrix_merged)

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        matrix = []
        
        for i in range(len(self)):
            matrix.append(self[i])
        for i in range(len(mat)):
            matrix.append(mat[i])
            
        return make_matrix(matrix)


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        rmul_vector = []
        for i in range (len(vec)):
            val = 0
            for j in range (len(self)):
                val = val + vec[i]*self[i][j]
            rmul_vector.append(val)
            
        return make_vector(rmul_vector , self.zero_test)
    

    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        matrix = []
        if (self.is_small() or mat.is_small == True):
            for i in range(len(self)):
                rows = []
                for j in range(len(mat[0])):
                    val = 0
                    for k in range(len(mat[0])):
                        val += self[i][k] * mat[k][j]
                    rows.append(val)
                matrix.append(make_vector((rows) , zero_test=lambda x : (x == 0)))
            return make_matrix(matrix)
        else:
            topleft , topright , bottomleft , bottomright = self.get_quarters()
            top_left , top_right , bottom_left , bottom_right = mat.get_quarters()
            val1 = topleft * (top_right - bottom_right)
            val2 = (topleft + topright) * bottom_right
            val3 = (bottomleft + bottomright) * top_left
            val4 = bottomright * (bottom_left - top_left)
            val5 = (topleft + bottomright) * (top_left + bottom_right)
            val6 = (topright - bottomright) * (bottom_left + bottom_right)
            val7 = (topleft - bottomleft) * ( top_left + top_right)          
            row1 = val4+val5+val6-val2
            row2 = val1+val2
            row3 = val3+val4
            row4  = val1-val3+val5-val7
            col1 = row1.merge_cols(row2)
            col2 = row3.merge_cols(row4)
            mat = col1.merge_rows(col2)
            return mat


    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        if len(self) == len(mat):
            for i in range(len(mat)):
                if not self[i] == mat[i]:
                    return False
            return True
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
        self.vectors = vectors
        self.indices = indices
        self.length = length

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        return len(self.indices)
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        if isinstance(key, tuple) == True:
            if key[0] in self.indices:
                return self.rows[self.indices.index(key[0])][key[1]]
            return 0
        if type(key) == int:
            if key in self.indices:
                return self.rows[self.indices.index(key)]
            else:
                if key < len(self):
                    mat = [0]*len(self.rows[0])
                    mat = make_vector(mat , zero_test = lambda x : (x == 0))
                    return mat
        return None

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        merge_vector = []
        merge_indices = []
        for row1 in range(len(self)):
            merge_vector.append(self[row1])
            merge_indices.append(self.indices[row1])
        for row2 in range(len(mat)):
            merge_vector.append(mat[row2])
            merge_indices.append(len(self)+mat.indices[row2])
        merge_vector = SparseMatrix( merge_vector , merge_indices , self.length + mat.length )


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        left = self[(len(self)//2):]
        right = self[:(len(self)//2)]
        topleft = []
        bottomleft = []
        topright = []
        bottomright = []

        for i in range(len(left)):
            if self.indices[i] < self.length//2:
                topleft.append(left[i])
            else:
                bottomleft.append(left[i])
        for i in range(len(right)):
            if self.indices[i] < self.length//2:
                topright.append(right[i])
            else:
                bottomright.append(right[i])
                
        top_left = make_matrix(topleft)
        bottom_left = make_matrix(bottomleft)
        top_right = make_matrix(topright)
        bottom_right = make_matrix(bottomright)
        return top_left , bottom_left , top_right , bottom_right


    if __name__ == '__main__':
        
        m1 = [make_vector([1,2,3,6] , zero_test=lambda x : (x==0)) , make_vector([3,4,5,6] , zero_test = lambda x : (x ==0)) , make_vector([5,6,7,8] , zero_test = lambda x : (x == 0)) , make_vector([7,8,9,10] , zero_test = lambda x : (x ==0))]
        m2 = [make_vector([1,2,3,6] , zero_test = lambda x : (x == 0)) , make_vector([3,4,5,6] , zero_test = lambda x : (x==0)) , make_vector([5,6,7,8] , zero_test = lambda x : (x == 0)),make_vector([7,8,9,10] , zero_test = lambda x : (x ==0))]
        m1_mat = make_matrix(m1)
        m2_mat = make_matrix(m2)
        
        mat3 = m1_mat + m2_mat
        
        for vec in mat3:
            for e in vec:
                print e,
