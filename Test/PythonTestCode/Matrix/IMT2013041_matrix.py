'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD, FullVector, SparseVector

ROW_NO = 0
COL_NO = 0
UPPER = 0

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
    value_list = []
    index_list = []
    if (len(vector_list) < SIZE_THRESHOLD):
        return FullMatrix(vector_list)
    else:
        count = 0
        for vector in vector_list:
            if vector.is_zero():
                count += 1
        if count <= (SIZE_THRESHOLD * DENSITY_THRESHOLD):        
            return FullMatrix(vector_list)
        else:
            length = len(vector_list)
            for index, vector in enumerate(vector_list):
                if vector.is_zero() == False:
                    value_list.append(vector)
                    index_list.append(index)
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
        self.vector_matrix = rows


    def __len__(self):
        '''
        Return the number of rows of the matrix - equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        # Your Code
        return len(self.vector_matrix)


    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        # Your Code
        if attr == 'nrows':
            return len(self.vector_matrix)
        if attr == 'ncols':
            if self.vector_matrix == []:
                return 0
            return len(self.vector_matrix[0])
        return None
        

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if isinstance(key, int):
            return self.vector_matrix[key]
        else:
            return self.vector_matrix[key[0]][key[1]]
        

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
        if len(mat) != len(self):
            return None
        sum_list = []
        for i in range(len(self)):
            sum_list.append(self[i] + mat[i])
        return make_matrix(sum_list)
                       
                
    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        if len(mat) != len(self):
            return None
        diff_list = []
        for i in range(len(self)):
            diff_list.append(self[i] - mat[i])
        return make_matrix(diff_list)

    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        sum_list = []
        min_len = min(len(self), len(mat))
        for i in range(0, min_len):
            sum_list.append(self[i] + mat[i]) 
        return make_matrix(sum_list)


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        diff_list = []
        min_len = min(len(self), len(mat))
        for i in range(0, min_len):
            diff_list.append(self[i] + mat[i]) 
        return make_matrix(diff_list)


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        left_matrix_list = []
        right_matrix_list = []
        for vector in self:
            left_vector, right_vector = vector.split()
            left_matrix_list.append(left_vector)
            right_matrix_list.append(right_vector)
        return make_matrix(left_matrix_list), make_matrix(right_matrix_list)


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
        left_matrix, right_matrix = self.left_right_split()
        for i in range(len(left_matrix) / 2):
            topleft.append(left_matrix[i])
            topright.append(right_matrix[i])
        for i in range(len(left_matrix) / 2, len(left_matrix)):
            bottomleft.append(left_matrix[i])
            bottomright.append(right_matrix[i])
        return make_matrix(topleft), make_matrix(topright), make_matrix(bottomleft), make_matrix(bottomright)
    
    
    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        if (len(self) != len(mat) ):
            return None     
        for i in range(len(self)):
            self[i].merge(mat[i])
        return self


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        merged_list = []
        if (len(self.vector_matrix[0]) != len(mat.vector_matrix[0])) :
            return None
        for i in range(len(self)):
            merged_list.append(self[i])
        for  i in range(len(mat)):
            merged_list.append(mat[i])
        return make_matrix(merged_list)
            

    def upper_initalize(self, mat):
        '''Initializes the global variable UPPER
        '''
        global ROW_NO, COL_NO, UPPER
        ROW_NO = len(self)
        COL_NO = len(mat[0])
        max1 = max(self.ncols, len(self))
        max2 = max(mat.ncols, len(mat))
        max_no = max(max1, max2)
        
        i = 1
        temp = 0
        while(1):
            if((2**i) > max_no > (2**(i-1))):
                temp = 2**i
                break
            if(2**i == max_no):
                temp = 2**i
                break
            i += 1
            
        UPPER = temp
        
    def pad(self, mat):
        '''
        Pads a given matrix with 0s to the nearest exponent of 2
        '''
        max1 = max(self.ncols, len(self))
        max2 = max(mat.ncols, len(mat))
        max_no = max(max1, max2)
        
        i = 1
        temp = 0
        while(1):
            if((2**i) > max_no > (2**(i-1))):
                temp = 2**i
                break
            if(2**i == max_no):
                temp = 2**i
                break
            i += 1
            
        col_list = [0]*(temp - self.ncols)
        zero_vec = FullVector(col_list, lambda x:x==0)
        row_list = [0]*temp
        mat_vec = FullVector(row_list,lambda x:x==0)
        temp_matrix = [elem for elem in self]
        for elem in temp_matrix:
            elem.merge(zero_vec)
            
        for i in range(temp - self.nrows):
            self.vectors.append(mat_vec)
            
        col_list1 = [0]*(temp - mat.ncols)
        zero_vec1 = FullVector(col_list1, lambda x:x==0)
        row_list1 = [0]*temp
        mat_vec1 = FullVector(row_list1,lambda x:x==0)
        temp_matrix = [elem for elem in mat]
        for elem in temp_matrix:
            elem.merge(zero_vec1)
            
        for i in range(temp - mat.nrows):
            mat.vectors.append(mat_vec1)
    
        
    def unpad(self, row, col):
        '''
        Unpads a given matrix
        ''' 
        vectors = []
        for i in range(row):
            vec = []
            for j in range(col):
                vec += [self[i][j]]
            vectors += [FullVector(vec)]
        return make_matrix(vectors)
    
    
    def rmul(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        vector_list = []
        if len(vec) != len (self) :
            return None    
        for i in range(len(self)):
            sum_mult = 0
            for j in range(len(vec)) :
                sum_mult += (self[j][i] * vec[j])    
            vector_list.append(sum_mult)
        return make_vector(vector_list, lambda x : x==0)    
         

    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        global ROW_NO, COL_NO, UPPER
        if (len(self[0]) == len(mat)):
            self.pad(mat)
            product = []
            if (self.is_small() or mat.is_small()):
                for i in range(len(self)):
                    temp = mat.rmul(self[i])
                    product.append(temp)
                return make_matrix(product)
                    
            else:          
                a, b, c, d = self.get_quarters()
                e, f, g, h = mat.get_quarters() 
                p1 = a * ( f - g )
                p2 = ( a + b ) * h
                p3 = ( c + d ) * e
                p4 = d * ( g - e )
                p5 = ( a + d ) * ( e + h )
                p6 = ( b - d ) * ( g + h )
                p7 = ( a - c ) * ( e + f )
                                      
                matrix1  = p4 + p5 + p6 - p2
                matrix2  = p1 + p2
                matrix3  = p3 + p4 
                matrix4  = p1 + p5 - ( p3 + p7 )  
                
                matrix1 = matrix1.merge_cols(matrix2)
                matrix3 = matrix3.merge_cols(matrix4)
                            
                matrix1 = matrix1.merge_rows(matrix3)
                if len(matrix1) == UPPER:
                    matrix1 = matrix1.unpad(ROW_NO, COL_NO)
                return matrix1
            return None
        

    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        for i in range(len(mat)):
            if mat[i] != self.vector_matrix[i]:
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
        self.vectors = vectors

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
        return self.length
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        # Your Code
        if(isinstance(key,tuple)):
            if key[0] > self.length:
                return None
            if(key[0] in self.indices):
                index = self.indices.index(key[0])
                return self.vectors[index][key[1]]
            else:
                return 0
        if(isinstance(key,int)):
            if(key in self.indices):
                index = self.indices.index(key)
                return self.vectors[index]
            else:
                return make_vector([0]*self.length,lambda x : x==0)
                

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        merged_list = []
        if (len(self[0]) != len(mat.vector_matrix[0])) :
            return None
        for i in range(len(self)):
            merged_list.append(self[i])
        for  i in range(len(mat)):
            merged_list.append(mat[i])
        return make_matrix(merged_list)

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
        left_matrix, right_matrix = self.left_right_split()
        for i in range(len(left_matrix) / 2):
            topleft.append(left_matrix[i])
            topright.append(right_matrix[i])
        for i in range(len(left_matrix) / 2, len(left_matrix)):
            bottomleft.append(left_matrix[i])
            bottomright.append(right_matrix[i])
        return make_matrix(topleft), make_matrix(topright), make_matrix(bottomleft), make_matrix(bottomleft)
        
                    
if __name__ == '__main__':
    temp = []
    a1 = make_vector([1,1,1,1,1,1,1], lambda x : (x == 0))
    a2 = make_vector([1,1,1,1,1,1,1], lambda x : (x == 0))
    a3 = make_vector([1,1,1,1,1,1,1], lambda x : (x == 0))
    a4 = make_vector([1,1,1,1,1,1,1], lambda x : (x == 0))
    a5 = make_vector([1,1,1,1,1,1,1], lambda x : (x == 0))
    m1 = make_matrix([a1, a2, a3,a4, a5])
     
    v1 = make_vector([1,1,1,1,1],  lambda x : (x == 0))
    v2 = make_vector([1,1,1,1,1],  lambda x : (x == 0))
    v3 = make_vector([1,1,1,1,1],  lambda x : (x == 0))
    v4 = make_vector([1,1,1,1,1],  lambda x : (x == 0))
    v5 = make_vector([1,1,1,1,1],  lambda x : (x == 0))
    m2 = make_matrix([v1, v2, v3, v4, v5]) 
    m2.upper_initalize(m1) 
    print "m1"
    for elem in m1:
        print elem.data
    print "m2"
    for elem in m2:
        print elem.data
    print "m"
    m = m2 * m1
    for elem in m:
        print elem.data

    