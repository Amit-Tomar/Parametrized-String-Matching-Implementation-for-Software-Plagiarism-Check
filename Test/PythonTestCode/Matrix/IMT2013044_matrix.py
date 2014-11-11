'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD, FullVector
import math

def get_nearest_number(num):
    n = 0
    while (1):
        if num <= math.pow(2, n):
            nearest_num = math.pow(2, n)  
            break
        n = n + 1
    return nearest_num           

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
    if(len(vector_list)==0):
        return None
    vects = []
    indices = []
    count = 0
    for vector_obj in vector_list:
        if(vector_obj.is_zero()):
            count += 1
        else:
            vects.append(vector_obj)
            indices.append(vector_list.index(vector_obj))
    density = float(count)/len(vector_list)
    if(density > 1):
        matrix = SparseMatrix(vects, indices, len(vector_list), len(vector_list[0]))
        return matrix
    else:
        matrix = FullMatrix(vector_list)
        return matrix
    
class Matrix(object):
    '''
    Base Matrix Class - implements basic matrix operations
    '''
    MIN_RECURSION_DIM = 1

    def __init__(self, rows):
        '''
        'rows' is a list of vectors
        Keep this as the row list for the matrix
        '''
        # Your Code
        self.row_list = rows

    def __len__(self):
        '''
        Return the number of rows of the matrix - equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        # Your Code
        return len(self.row_list)

    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        # Your Code
        if attr == 'ncols':
            if self.row_list == []:
                return 0
            return len(self.row_list[0])
        if attr == 'nrows':
            return len(self.row_list)
        return None

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if(isinstance(key, tuple)):
            return self.row_list[key[0]][key[1]]
        else:
            return self.row_list[key]

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if len(self.row_list) <= self.MIN_RECURSION_DIM:
            return True

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        if len(self)!=len(mat):
            return None
        result = []
        for i in range(len(mat)):
            result = result + [ self.row_list[i] + mat.row_list[i] ]
        matrix = make_matrix(result)
        return matrix

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        if len(self)!=len(mat):
            return None
        result = []
        for i in range(len(mat)):
            result.append(self.row_list[i] - mat.row_list[i])
        matrix = make_matrix(result)
        return matrix

    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        for i in range(min(len(self),len(mat))):
            self.row_list[i] += mat.row_list[i]
        return self   

    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        for i in range(min(len(self),len(mat))):
            self.row_list[i] -= mat.row_list[i]
        return self

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
        for i in range(len(self)):
            left,right = self[i].split()
            left_matrix.append(left)
            right_matrix.append(right)
        vector_list1 = []
        vector_list2 = []
        for lst in left_matrix:
            vector_list1.append(make_vector(lst, lambda x : (x == 0)))
        for lst in right_matrix:
            vector_list2.append(make_vector(lst, lambda x : (x == 0)))
        return make_matrix(vector_list1), make_matrix(vector_list2)
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_matrix, right_matrix = self.left_right_split()
        topleft = make_matrix(left_matrix[:len(left_matrix)/2])
        topright = make_matrix(right_matrix[:len(right_matrix)/2])
        bottomleft = make_matrix(left_matrix[len(left_matrix)/2:])
        bottomright = make_matrix(right_matrix[len(right_matrix)/2:])
        return topleft, topright, bottomleft, bottomright

    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        for i in range(len(self)):
            for j in range(len(mat.row_list[i].data)):
                self.row_list[i].data.append(mat.row_list[i].data[j])
        return self
    
    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        for vec_obj in mat.row_list:
            self.row_list.append(vec_obj)
        return self

    def rmul(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        row_self = len(self)
        col_vec = len(vec)
        if row_self != col_vec:
            return None
        prod = []
        for j in range(len(self[0])):
            temp = 0
            for i in range(len(self)):
                temp = temp + vec[i]*self.row_list[i][j]
            prod.append(temp)
        vect = FullVector(prod, lambda x : (x == 0))
        return vect
        
    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        if ( self.ncols != mat.nrows ):
            return None
        result = []
        orig_len_self = len(self)
        orig_len_mat = len(mat[0])
        if self.is_small() or mat.is_small():
            for vec_obj in self.row_list:
                result.append(mat.rmul(vec_obj))
            return make_matrix(result)
        else:
            x1 = math.log(len(self),2)
            x2 = math.log(len(self[0]),2)
            x3 = math.log(len(mat[0]),2)
            y1 = int(x1)
            y2 = int(x2)
            y3 = int(x3)
            z1 = x1 - y1
            z2 = x2 - y2
            z3 = x3 - y3
            if z1 != 0 or z2 != 0 or z3 != 0 or len(self) != len(self[0]) or len(self) != len(mat[0]):
                '''If the matrices A, B are not of type 2^n x 2^n we fill the missing rows and columns with zeros.'''
                order = get_nearest_number(max((len(self)), len(mat[0]), len(mat)))
                temp1 = []
                if int(order) - self.ncols != 0:
                    for i in range(len(self)):
                        temp1.append(make_vector([0]*(int(order) - self.ncols), lambda x : (x == 0)))
                    mat1 = FullMatrix(temp1)
                temp2 = []
                if int(order) - len(self) != 0:
                    for i in range(int(order) - len(self)):
                        temp2.append(make_vector([0]*int(order), lambda x : (x == 0)))
                    mat2 = FullMatrix(temp2)
                if temp1 != []:
                    self = self.merge_cols(mat1)
                if temp2 != []:
                    self = self.merge_rows(mat2)
                    
                temp1 = []
                if int(order) - mat.ncols != 0:
                    for i in range(len(mat)):   
                        temp1.append(make_vector([0]*(int(order) - mat.ncols), lambda x : (x == 0)))
                    mat1 = FullMatrix(temp1)                
                temp2 = []
                if int(order) - len(mat) != 0:
                    for i in range(int(order) - len(mat)):
                        temp2.append(make_vector([0]*int(order), lambda x : (x == 0)))
                    mat2 = FullMatrix(temp2)                
                if temp1 != []:
                    mat = mat.merge_cols(mat1)
                if temp2 != []:
                    mat = mat.merge_rows(mat2) 
            A, B, C, D = self.get_quarters()
            E, F, G, H = mat.get_quarters()    
            P1 = A * ( F - H )
            P2 = ( A + B ) * H
            P3 = ( C + D ) * E
            P4 = D * ( G - E )
            P5 = ( A + D ) * ( E + H )
            P6 = ( B - D ) * ( G + H )
            P7 = ( C - A ) * ( E + F )
            C1 = P4 + P5 - P2 + P6
            C2 = P1 + P2
            C3 = P3 + P4
            C4 = P1 - P3 + P5 + P7
            C1 = C1.merge_cols(C2)
            C3 = C3.merge_cols(C4)
            semi_final_matrix = C1.merge_rows(C3)
            '''Remove the extra zeroes which were added in the end'''
            filtered_vectors = []
            filtered_list = []
            for i in range(orig_len_self):
                filtered_vectors.append(semi_final_matrix.row_list[i])
                filtered_list.append([])
            for i in range(len(filtered_vectors)):
                for j in range(orig_len_mat):
                    filtered_list[i].append(filtered_vectors[i].data[j])
            final_vector = []
            for lst in filtered_list:
                final_vector.append(make_vector(lst, lambda x : (x == 0)))
            final_matrix = make_matrix(final_vector)
            return final_matrix           
            
    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if len(self) != len(mat):
            return False
        count = 0
        for i in range(len(mat)):
            if mat[i] == self[i]:
                count = count + 1
        if count == len(mat):
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
    def __init__(self, vectors, indices, length=0, vec_length=0):
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
        self.zero_vec = make_vector([0]*vec_length, lambda x : x==0)        

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
        if isinstance(key, tuple):
            if key[0] in self.indices:
                index = self.indices.index(key[0])
                return self.vectors[index][key[1]]
            else:
                return 0
        else:
            if key in self.indices:
                index = self.indices.index(key)
                return self.vectors[index]
            else:
                return self.zero_vec
        
    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        for vectors in mat:
            self.append(vectors)
        return self

    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_matrix, right_matrix = self.left_right_split()
        topleft = make_matrix(left_matrix[:len(left_matrix)/2])
        topright = make_matrix(right_matrix[:len(right_matrix)/2])
        bottomleft = make_matrix(left_matrix[len(left_matrix)/2:])
        bottomright = make_matrix(right_matrix[len(right_matrix)/2:])
        return topleft, topright, bottomleft, bottomright

data1 = [ [1,2,1,1,3,4,1,1],
          [1,1,5,6,1,1,7,8],
          [1,2,1,2,1,2,1,2],
          [1,4,1,4,1,4,1,4] ]
data2 = [ [1,0,2,0],
          [3,0,4,0],
          [1,5,1,5],
          [2,2,2,2],
          [1,1,1,1],
          [4,4,4,4],
          [3,9,3,9],
          [21,3,13,4] ]
vector_list1 = []
vector_list2 = []
for lst in data1:
    vector_list1.append(make_vector(lst, lambda x : (x == 0)))
for lst in data2:
    vector_list2.append(make_vector(lst, lambda x : (x == 0)))
matrix1 = make_matrix(vector_list1)
matrix2 = make_matrix(vector_list2)
print matrix1
print matrix2
matrix = matrix1*matrix2
for vec_obj in matrix.row_list:
    print vec_obj.data