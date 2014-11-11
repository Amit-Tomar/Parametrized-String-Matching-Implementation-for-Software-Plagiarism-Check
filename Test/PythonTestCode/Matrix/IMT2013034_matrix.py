'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD, FullVector

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
    flag = 0
    if len(vector_list) >= SIZE_THRESHOLD:
        count = 0
        for vector in vector_list:
            if not vector.is_zero():
                count += 1
        if count <= DENSITY_THRESHOLD * len(vector_list):
            flag = 1
    cols = len(vector_list[0])       
    if flag == 1:
        length = len(vector_list)
        vectors = []
        indices = []
        for row in range(0, length):
            if not vector_list[row].is_zero():
                vectors.append(vector_list[row])
                indices.append(row)
        return SparseMatrix(vectors, indices, length, cols)
    else:
        return FullMatrix(vector_list, cols)
    
class Matrix(object):
    '''
    Base Matrix Class - implements basic matrix operations
    '''
    
    MIN_RECURSION_DIM = 5

    def __init__(self, rows, cols):
        '''
        'rows' is a list of vectors
        Keep this is the row list for the matrix
        '''
        # Your Code
        self.rows = rows
        self.cols = cols
        self.min = self.MIN_RECURSION_DIM

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
        if (attr == 'ncols'): 
            return self.cols
        if (attr == 'nrows'):
            return len(self)

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if isinstance(key, int):
            return self.rows[key]
        else:
            return self.rows[key[0]][key[1]]
        

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if len(self) <= self.min:
            return True
        else:
            return False

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        if len(self) == len(mat):
            add = []
            for row in range (0, len(self)):
                add.append(self[row] + mat[row])
            return make_matrix(add)
        else:
            return None
            

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        if len(self) == len(mat):
            sub = []
            for row in range (0, len(self)):
                sub.append(self[row] - mat[row])
            return make_matrix(sub)
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
        length = min(len(self), len(mat))
        for row in range (0, length):
            self[row] += mat[row]
        return self


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        length = min(len(self), len(mat))
        for row in range (0, length):
            self[row] -= mat[row]
        return self

    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        lrows = []
        rrows = []
        for row in range(0, len(self)):
            lrow, rrow = self[row].split()
            lrows.append(lrow)
            rrows.append(rrow)
        return make_matrix(lrows), make_matrix(rrows)
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        topleft = []
        topright = []
        bottomleft = []
        bottomright = []
        left, right = self.left_right_split()
        for rowno in range(0, len(self)/2):
            topleft.append(left[rowno])
            topright.append(right[rowno])
        for rowno in range(len(self)/2, len(self)):
            bottomleft.append(left[rowno])
            bottomright.append(right[rowno])
        return make_matrix(topleft), make_matrix(topright), make_matrix(bottomleft), make_matrix(bottomright)
            
    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        for nrow in range(0, len(self)):
            self[nrow].merge(mat[nrow])
        return self       

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        mat_list = []
        for nrow in range(0, len(self)):
            mat_list.append(self[nrow])
        for nrow in range(0, len(mat)):
            mat_list.append(mat[nrow])
        return make_matrix(mat_list) 

    def rmul(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        if len(vec) == len(self):
            vec_list = []
            for cols in range(0, self.ncols):
                vec_element = []
                for rows in range(0, len(self)):
                    vec_element.append(self[rows][cols])
                vector = make_vector(vec_element, lambda x : (x == 0))
                vec_list.append(vec * vector)
            return make_vector(vec_list, lambda x : (x == 0))
        else :
            return None
        
    def padding(self, mat):
        '''
        To convert a matrix in a form 2^n x 2^n
        '''
        length = max(len(mat), mat.ncols)
        final = 1
        while length > final:
            final *= 2
        mat_vec = FullVector([0]* final, lambda x:x==0)
        vec_list = []
        for row in range(0, len(mat)):
            element = []
            for col in range(0, mat.ncols):
                element.append(mat[row][col])
            for col in range(mat.ncols, final):
                element.append(0)
            vect = make_vector(element, lambda x:x==0)
            vec_list.append(vect)
        for row in range(len(mat), final):
            vec_list.append(mat_vec)
        mat1 = make_matrix(vec_list)
        return mat1
            

    def remove_padding(self, mat, rows, cols):
        '''
        To remove padding from matrix
        '''
        vectors = []
        for row in range(0, rows):
            vector = []
            for col in range(0, cols):
                vector.append(mat[row][col])
            vectors.append(make_vector(vector, lambda x:x==0))
        return make_matrix(vectors)

        
    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        if(self.ncols == len(mat)):
            if(self.is_small()):
                srow, mcol = len(self), mat.ncols
                matrix = []
                for pos in range(0, len(self)):
                    matrix.append(mat.rmul(self[pos]))
                return make_matrix(matrix)
            else :
                srow, mcol = len(self), mat.ncols
                self, mat = self.padding(self), self.padding(mat)
                mat1 = self.get_quarters()
                mat2 = mat.get_quarters()
                temp_mat = []
                temp_mat.append((mat1[0]+mat1[3])*(mat2[0]+mat2[3]))
                temp_mat.append((mat1[2]+mat1[3])*mat2[0])
                temp_mat.append(mat1[0]*(mat2[1]-mat2[3]))
                temp_mat.append((mat1[3])*(mat2[2]-mat2[0]))
                temp_mat.append((mat1[0]+mat1[1])*mat2[3])
                temp_mat.append((mat1[2]-mat1[0])*(mat2[0]+mat2[1]))
                temp_mat.append((mat1[1]-mat1[3])*(mat2[2]+mat2[3]))
                topleft = temp_mat[0] + temp_mat[3] - temp_mat[4] + temp_mat[6]
                topright = temp_mat[2] + temp_mat[4]
                bottomleft = temp_mat[1] + temp_mat[3]
                bottomright = temp_mat[0] - temp_mat[1] + temp_mat[2] + temp_mat[5]
                topleft = topleft.merge_cols(topright)
                bottomleft = bottomleft.merge_cols(bottomright)
                finalmat = topleft.merge_rows(bottomleft)
                finalmat = self.remove_padding(finalmat, srow, mcol)
                return finalmat
        else:
            return None
                
    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if len(self) == len(mat):
            for rowno in range (0, len(self)):
                if not self[rowno] == mat[rowno]:
                    return False
            return True
        return False
                    

class FullMatrix(Matrix):
    '''
    A subclass of Matrix where all rows (vectors) are kept explicitly as a list
    '''
    def __init__(self, vectors, cols):
        '''
        Constructor for a FullVector on data given in the 'lst' argument - 'lst' is the list of elements in the vector
        Uses the base (parent) class attributes data and zero_test
        '''
        super(FullMatrix, self).__init__(vectors, cols)



class SparseMatrix(Matrix):
    '''
    A subclass of Matrix where most rows (vectors) are zero vectors
    The vectors (non-zero) and their corresponding indices are kept in separate lists
    '''
    def __init__(self, vectors, indices, length, cols):
        '''
        'length' is the number of rows of the matrix - the number of entries in 'vectors' is just the number of
        non-zero rows
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseMatrix, self).__init__(vectors, cols)
        # Your Code
        self.indices = indices
        self.length = length
        
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
        if isinstance(key, int):
            if key in self.indices:
                return self.rows[self.indices.index(key)]
            else :
                return make_vector([0]*self.ncols, lambda x : (x == 0))
        else:
            if key[0] in self.indices:
                return self.rows[self.indices.index(key[0]), key[1]]
            else:
                return 0
        
    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        mat_list = []
        for nrow in range(0, len(self)):
            if nrow in self.indices:
                mat_list.append(self[nrow])
            else:
                mat_list.append(make_vector([0]*self.ncols, lambda x : (x == 0)))
        for nrow in range(0, len(mat)):
            if nrow in mat.indices:
                mat_list.append(mat[nrow])
            else:
                mat_list.append(make_vector([0]*self.ncols, lambda x : (x == 0)))
        return make_matrix(mat_list) 


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottommake_vector
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        topleft = []
        topright = []
        bottomleft = []
        bottomright = []
        left, right = self.left_right_split()
        for rowno in range(0, len(self)/2):
            if rowno in left.indices:
                topleft.append(left[rowno])
            else:
                topleft.append(make_vector([0]*(self.ncols/2) , lambda x : (x == 0)))
            if rowno in right.indices:
                topright.append(right[rowno])
            else:
                topright.append(make_vector([0]*(self.ncols - self.ncols/2), lambda x : (x == 0)))
        for rowno in range(len(self)/2, len(self)):
            if rowno in left.indices:
                bottomleft.append(left[rowno])
            else:
                bottomleft.append(make_vector([0]* (self.ncols/2), lambda x : (x == 0)))
            if rowno in right.indices:
                bottomright.append(right[rowno])
            else:
                bottomright.append(make_vector([0]*(self.ncols - self.ncols/2), lambda x : (x == 0)))
        return make_matrix(topleft), make_matrix(topright), make_matrix(bottomleft), make_matrix(bottomright)
        
    

