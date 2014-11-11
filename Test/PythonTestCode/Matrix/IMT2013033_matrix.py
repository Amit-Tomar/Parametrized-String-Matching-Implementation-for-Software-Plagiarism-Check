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
    count =0
    for vector in vector_list:
        if vector.is_zero():
            count += 1
    if(len(vector_list) > SIZE_THRESHOLD and count/len(vector_list) > DENSITY_THRESHOLD):
        matrix = SparseMatrix()
    else:   matrix = FullMatrix()
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
        if attr == "nrows":
            return len(self.rows)

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if (isinstance (key , tuple)==True):
            return [self[key][0] , self[key][1]]
        else:
            return self[key]
    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if(len(self) < self.MIN_RECURSION_DIM):
            return True
        else:
            return False

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        add_vector = []
        if len(self)==len(mat):
            for i in range(0 , len(mat)):
                for j in range(0 , len(mat)):
                    add_vector.append(self[i][j] + mat[i][j])
            return add_vector
        else:
            return None

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        sub_vector = []
        if len(self)==len(mat):
            for i in range(0 , len(mat)):
                for j in range(0 , len(mat)):
                    sub_vector.append(self[i][j] - mat[i][j])
            return sub_vector
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
        if len(self)==len(mat):
            for i in range(0 , len(mat)):
                for j in range(0 , len(mat)):
                    self[i][j] = self[i][j] + mat[i][j]
            return 
        else:
            if len(self)>len(mat):
                for i in range(0 , len(mat)):
                    for j in range(0 , len(mat)):
                        self[i][j] = self[i][j] + mat[i][j]
            elif len(self)<len(mat):
                for i in range(0 , len(self)):
                    for j in range(0 , len(self)):
                        self[i][j] = self[i][j] + mat[i][j]

    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        if len(self)==len(mat):
            for i in range(0 , len(mat)):
                for j in range(0 , len(mat)):
                    self[i][j] = self[i][j] - mat[i][j]
            return 
        else:
            if len(self)>len(mat):
                for i in range(0 , len(mat)):
                    for j in range(0 , len(mat)):
                        self[i][j] = self[i][j] - mat[i][j]
            elif len(self)<len(mat):
                for i in range(0 , len(self)):
                    for j in range(0 , len(self)):
                        self[i][j] = self[i][j] - mat[i][j]

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
        for  i in range(0 , len(self)):
            mat = make_vector(self[i] , lambda x : (x == 0))
            left_vec , right_vec = mat.split()
            left_matrix.append(left_vec) 
            right_matrix.append(right_vec)
        return self.makematrix(left_matrix) , self.makematrix(right_matrix)
    
    def top_bottom_split(self):
        matrix = len(self)
        length = matrix/2
        if(matrix%2==0):
            a = [self[i:i+(matrix)/2] for i in range(0, matrix, matrix/2)]
            return a[0], a[1]
        else:
            d = [self[i:i+(matrix)/2+1] for i in range(0, matrix, (matrix/2)+1)]
            return d[0] , d[1]
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        top = []
        bottom = []
        top , bottom = self.top_bottom_split()[0] , self.top_bottom_split()[1]
        topleft , bottomleft = top.left_right_split()[0] , top.left_right_split()[1]
        topright , bottomright = bottom.left_right_split()[0] , bottom.left_right_split()[1]
        return topleft , topright , bottomleft , bottomright

    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        a = []
        for i in range(len(self)):
                a += self[i]
        for i in range(len(mat)):
                a += mat[i]
        return self.make_matrix(a)

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        a = []
        for i in range(len(self)):
            a.append([self[i] + mat[i]])
        return self.make_matrix(a)

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        if(len(vec)==len(self)):
            res_vector = []
            for i in range(len(vec)):
                sum_row = 0
                for j in range(0 , len(vec)):
                    sum_row += vec[j]*self[i][j]
                res_vector = res_vector.append(sum_row)
                return self.makevector(res_vector , lambda x : (x == 0))
        else:
            return None
            
    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        if ((mat.is_small()==True) or (self.is_small()==True)):
            if(len(self[0])==len(mat)):
                new_matrix = [[0] * len(mat[0])] * len(self)
                for i in range(0 , len(self)):
                    for j in range(0 , len(mat[0])):
                        for k in range(0 , len(mat)):
                            new_matrix[i][j] += self[i][k]*mat[k][j]
                    return new_matrix
        else:
            A = self
            B = mat
            A11,A12,A21,A22 = self.get_quarters()
            B11,B12,B21,B22 = mat.get_quarters()
            M1 = (A11 + A22) * B22
            M2 = (A21 + A22) * B11
            M3 = A11 * (B12 - B22)
            M4 = A22 * (B21 - B11)
            M5 = (A11 + A12) * B22
            M6 = (A21 - A11) * (B11 + B12)
            M7 = (A12 - A22) * (B21 + B22)
            
            C11 = M1+M4-M5+M7
            C12 = M3+M5
            C21 = M2+M4
            C22 = M1-M2+M3+M6
            c11 = Matrix(C11)
            c12 = Matrix(C12)
            c21 = Matrix(C21)
            c22 = Matrix(C22)
            C1 = c11.merge_rows(c12)
            C2 = c21.merge_rows(c22)
            c1 = Matrix(C1)
            c2 = Matrix(C2)
            C = c1.merge_cols(c2)
            return C

    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        for i in range(len(self)):
            for j in range(len(self)):
                if self[i][j]==mat[i][j]:
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
        

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        # Your Code
        return len(self.vectors)

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        ''' 
        # Your Code
        if (isinstance (key , tuple)==True):
            if(self[key][1]!=0):
                return [self[key][0] , self[key][1]]
        else:
            if(self[key][1]!=0):
                return self[key]
        
    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        a = []
        for i in range(len(self)):
            a.append([self[i] + mat[i]])
        return self.make_matrix(a)

    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        
    if __name__ == '__main__':
        pass
    m1 = [make_vector([1,2,1,2],zero_test = lambda x : (x == 0)), make_vector([3,1,4,1],zero_test = lambda x : (x == 0)),make_vector([5,1,0,1],zero_test = lambda x : (x == 0)),make_vector([1,4,1,3],zero_test = lambda x : (x == 0))]
    m2 = [make_vector([1,1,4,1],zero_test = lambda x : (x == 0)), make_vector([2,1,7,1],zero_test = lambda x : (x == 0)),make_vector([3,1,1,9],zero_test = lambda x : (x == 0)),make_vector([1,7,1,5],zero_test = lambda x : (x == 0))]
    m1_mat = make_matrix(m1)
    m2_mat = make_matrix(m2)  
    mat3 = m1_mat*m2_mat
    for vec in mat3:
        for e in vec:
            print e