'''
Created on 16-Nov-2013

@author: raghavan
'''
zero_append=[]
from math import ceil, log
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD

def printmatrix(mat):
    for vec in mat:
        for i in vec:
            print i, 
        print
        
def remove_pad(matrix):
    rm_row = zero_append[0]
    rm_col = zero_append[3]

    new_list = [[0]*rm_col]*rm_row
    for i in range(rm_row):
        for j in range(rm_col):
            new_list[i][j] = matrix[i][j]
    return new_list


def pad_matrix(vector_list):
    '''
    To pad the matrix
    '''
    nrow_pad = int(pow(2, ceil(log(len(vector_list), 2))))
    ncol_pad = int(pow(2, ceil(log(len(vector_list[0]), 2))))
    zero_append.append(len(vector_list)) 
    zero_append.append(len(vector_list[0])) 
    if nrow_pad == len(vector_list) and ncol_pad == len(vector_list[0]):
        return vector_list
    new_list = [[0]*ncol_pad]*len(vector_list)
    
    for i in range(len(vector_list)):
        for j in range(len(vector_list[0])):
            new_list[i][j] = vector_list[i][j]
    
    i = 0
    while( i < nrow_pad-len(vector_list)):
        new_list.append([0]*len(new_list[0]))
        i += 1
    
    vect_list = []
    for i in new_list:
        vect_list.append(make_vector(i, zero_test = lambda x : (x == 0)))
           
    return vect_list

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    matrix = []
    #vect_matrix = []

    if len(vector_list) > 5:
        vector_list = pad_matrix(vector_list)
    
    '''for vect in vector_list:
        vect_matrix.append(make_vector(vect, zero_test = lambda x : (x == 0)))'''
    count = 0
    
    if len(vector_list) > SIZE_THRESHOLD:
        for vect in vector_list:
            if vect.is_zero():
                count += 1

        if count/len(vector_list) > DENSITY_THRESHOLD:
            vect_list = []
            indices = []
            for ind in range(len(vector_list)):
                if vector_list[ind].is_zero() == False:
                    print "TGDRG"
                    vect_list.append(vector_list[ind])
                    indices.append(ind)
                    
            matrix = SparseMatrix(vect_list, indices, len(vector_list))
            return matrix
    
    matrix = FullMatrix(vector_list)

    return matrix
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
        self.rows = rows
        #self.rows_m = make_matrix(self.rows)
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
            return len(self.rows)
        if attr == 'ncolumns':
            return len(self.rows[0])
        # Your Code
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        if type(key) == int:
            return self.rows[key]
        elif isinstance(key, tuple) == True:
            return self.rows[key[0]][key[1]]
        # Your Code
        

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if len(self) <= self.MIN_RECURSION_DIM:
            return True
        return False
        # Your Code
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        if len(self) != len(mat):
            return None
        sum_matrix = []
        for i in range(len(self)):
            sum_matrix.append(make_vector(self[i], zero_test = lambda x : (x == 0))+make_vector(mat[i],zero_test = lambda x : (x == 0) ))
        
        sum_mat = make_matrix(sum_matrix)

        return sum_mat
        # Your Code


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        if len(self) != len(mat):
            return None
        sub_mat = []
        
        
        for i in range(len(self)):
            sub_mat.append(make_vector(self[i],zero_test = lambda x : (x == 0)) - make_vector(mat[i], zero_test = lambda x : (x == 0)))
        sub_matrix = make_matrix(sub_mat)
        return sub_matrix
        # Your Code


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        min_len = min(len(self), len(mat))
        
        for i in range(min_len):
            self[i] = self[i] + mat[i]
        # Your Code


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        min_len = min(len(self), len(mat))
        
        for i in range(min_len):
            self[i] = self[i] - mat[i]
        # Your Code


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        left = []
        right = []
        for vector in range(len(self)):
            left.append(self[vector].split()[0])
            right.append(self[vector].split()[1])
        '''left_mat = make_matrix(left)
        right_mat = make_matrix(right)
 
        return left_mat, right_mat'''
        return left, right
        # Your Code
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        left, right = self.left_right_split()
        #print left[0][0]
        topleft = left[:len(self)//2]
        topright = right[:len(self)//2]
        bottomleft = left[len(self)//2:]
        bottomright = right[len(self)//2:]

        '''for vect in range(len(topleft)):
            for i in vect.components():
                print i'''
        
        return make_matrix(topleft), make_matrix(topright), make_matrix(bottomleft), make_matrix(bottomright)
        # Your Code

    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        merge_mat = []
        
        for i in range(len(self)):
            lst = []
            for val1 in self[i]:
                lst.append(val1)
            for val2 in mat[i]:
                lst.append(val2)
            merge_mat.append(lst)
        merge_matrix = make_matrix(merge_mat)
        return merge_matrix 
        # Your Code


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        merge_mat = []
        
        for i in range(len(self)):
            merge_mat.append(self[i])
        for i in range(len(mat)):
            merge_mat.append(mat[i])
        merge_matrix = make_matrix(merge_mat)
        return merge_matrix
        # Your Code


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        mult_vect = []
        for i in range(len(self)):
            if len(self[i]) == len(vec):
                mult_vect.append(self[i] * vec)
            else:
                return None
        return mult_vect
        # Your Code


    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        if self.is_small() == True:
            matrix = []

            for i in range(len(self)):
                row = []
                for j in range(len(mat[0])):
                    val = 0
                    for k in range(len(mat)):
                        val += self[i][k]*mat[k][j]
                    row.append(val)
                matrix.append(row)
            act_mat = make_matrix(matrix)
            return act_mat
        else:

            top_left1, top_right1, bottom_left1, bottom_right1 = self.get_quarters()
            top_left2, top_right2, bottom_left2, bottom_right2 = mat.get_quarters()
            part1 = top_left1 * (top_right2 - bottom_right2)
            part2 = (top_left1 + top_right1) * bottom_right2
            part3 = (bottom_left1 + bottom_right1) * top_left2
            part4 = bottom_right1 * (bottom_left2 - top_left2)
            part5 = (top_left1 + bottom_right1)*(top_left2 + bottom_right2)
            part6 = (top_right1 - bottom_right1)*(bottom_left2 + bottom_right2)
            part7 = (top_left1 - bottom_left1)*(top_left2 + top_right2)

            top_left = part4 +  part5 + (part6 - part2) 
            top_right = part1 + part2
            bottom_left = part3 + part4
            bottom_right = part1 - part3 + part5 - part7
            top = top_left.merge_cols(top_right)
            bottom = bottom_left.merge_cols(bottom_right)
            mat = top.merge_rows(bottom)
            return remove_pad(mat)
        # Your Code


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
        return len(self.indices)
        # Your Code
    

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
                    lst = [0]*len(self.rows[0])
                    lst_mat = make_vector(lst, zero_test = lambda x : (x == 0))
                    return lst_mat
        return None
        # Your Code

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        merge_vect = []
        merge_ind = []
        for row in range(len(self)):
            merge_vect.append(self[row])
            merge_ind.append(self.indices[row])
    
        for row in range(len(mat)):
            merge_vect.append(mat[row])
            merge_ind.append(len(self)+mat.indices[row])
        merge_vect = SparseMatrix(merge_vect, merge_ind , self.length + mat.length )
        # Your Code


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        left = self[(len(self)//2):]
        right = self[:(len(self)//2)]
        topleft_vect = []
        bottomleft_vect = []
        topright_vect = []
        bottomright_vect = []

        for i in range(len(left)):
            if self.indices[i] < self.length//2:
                topleft_vect.append(left[i])
            else:
                bottomleft_vect.append(left[i])
        for i in range(len(right)):
            if self.indices[i] < self.length//2:
                topright_vect.append(right[i])
            else:
                bottomright_vect.append(right[i])
                
        top_left = make_matrix(topleft_vect)
        bottom_left = make_matrix(bottomleft_vect)
        top_right = make_matrix(topright_vect)
        bottom_right = make_matrix(bottomright_vect)
        return top_left, bottom_left, top_right, bottom_right
        
        
        # Your Code

