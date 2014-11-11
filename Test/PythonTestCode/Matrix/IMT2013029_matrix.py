'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD
from vector import Vector

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    values = []
    indices = []
    count_zero = 0
    count_total = len(vectors_list)
    for list in vector_list:
        vector = Vector(list)
        if(self.is_zero == True):
            count_zero += 1
        else:
            values.append[list]
            indices.append[vectors_list.index[list]]
            
    percent = count_zero/count_total
    if(percent > 0.4):
        SparseMatrix(values,indices,count_total)
        
    else:
        FullMatrix(vectors_list)
         
        
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
        if(attr == len(self)):
            return len(self.rows)
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        if(type(key) is tuple == True):
            return self.rows[keys[0]][keys[1]]
        else:
            return self.rows[key]
        

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if(len(self) >= 5):
            return True
        else:
            return False
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        rows_length = len(self)
        list = []
        matrix_add = []
        if(len(self) != len(mat)):
            return None
        else:
            for i in range (0,rows_length):
                list.append[self.rows[i] + mat[i]]
            matrix_add.append[list]
            


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        rows_length = len(self)
        col_length = len(self.rows[0])
        list = []
        matrix_diff = []
        if(len(self) != len(mat)):
            return None
        else:
            for i in range (0,rows_length):
                list.append[self.rows[i] - mat[i]]
            matrix_diff.append[list]


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        length_row = len(self)
        length_col = len(self.rows(0))
        mat_row = len(mat)
        mat_col = len(mat(0))
        if(len(self) == len(mat)):
            for i in range(0,length_row):
                    self.rows[i] + mat[i] 
            return self.rows
        
        else:
            if(length_row > len(mat)):
                for i in range(0, len_mat):
                    for i in range(0, length_col):
                        self.rows[i][j] += mat[i][j]
                
                return self.rows
            
            if(length_row > len(mat)):
                for i in range(0, length_row):
                    for i in range(0, length_col):
                        self.rows[i][j] += mat[i][j]            
            
                return self.rows
            

    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        length_row = len(self)
        length_col = len(self.rows(0))
        mat_row = len(mat)
        mat_col = len(mat(0))
        if(len(self) == len(mat) and len(self.rows(0)) == len(mat(0))):
            for i in range(0,length_row):
                self.rows[i]-=mat[i]
                    
            return self.rows
        
        else:
            if(length_row > len(mat)):
                for i in range(0, len_mat):
                    self.rows[i] -= mat[i]
                
                return self.rows
            
            if(length_row > len(mat)):
                for i in range(0, length_row):
                    for j in range(0, length_col):
                        self.rows[i][j] = self.rows[i][j] - mat[i][j]            
            
                return self.rows


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        left_mat = []
        riht_mat = []
        for i in range(0, len(self)):
            newvector = make_vector(self.rows[i])
            left_part,right_part = newvector.split(self)
            left_mat.append(left_part)
            right_mat.append(right_part)
        
        return left_mat,right_mat
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        right_mat = []
        left_mat = []
        left_part,right_part = self.left_right_spit(self)
        left_mat.append(left_part)
        right_mat.append(right_part)
        self.half1 = []
        self.half2 = []
        self.half3 = []
        self.half4 = []
        if (len(left_mat) % 2 == 0):
            for i in range(0 , (len(self.data)/2)):
                self.half1.append(self.data[i])
            for j in range((len(self.data)/2) , len(self.data)):
                self. half2.append(self.data[j])
        else:
            for i in range(0 , (len(self.data)/2)+1):
                self.half1.append(self.data[i])
            for j in range((len(self.data)/2)+1 , len(self.data)):
                self.half2.append(self.data[j])
           
        return self.half1 , self.half2

        if (len(right_mat) % 2 == 0):
            for i in range(0 , (len(self.data)/2)):
                self.half3.append(self.data[i])
            for j in range((len(self.data)/2) , len(self.data)):
                self. half4.append(self.data[j])
        else:
            for i in range(0 , (len(self.data)/2)+1):
                self.half3.append(self.data[i])
            for j in range((len(self.data)/2)+1 , len(self.data)):
                self.half4.append(self.data[j])
           
        return self.half3 , self.half4


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        if(len(self) == len(mat)):
            for i in range(0, len(self)):
                vector_taken = self.rows[i]
                vector_taken.merge(mat[i])

        else:
            if(len(self) < len(mat)):
                for i in range(0, len(self)):
                    vector_taken = self.rows[i]
                    vector_taken.merge(mat[i])
            if(len(self) > len(mat)):
               for i in range(0, len(mat)):
                   vector_taken = make_vector(self.rows[i])
                   vector_taken.merge(mat[i])
            

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        for i in range(0, len(mat)):
            self.rows.append(mat[i])
        return self.rows

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        mul_vector = []
        for i in  range(0,len(self)):
            if(len(self.rows[i]) == len(vector)):
                mul_vector.append[self.rows[i]*vec]
            else:
                return None
            
    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        if self.is_small() == True:
            new_matrix = []
            for i in range(len(self)):
                new_row = []
                for j in range(len(mat[0])):
                    val = 0
                    for k in range(len(mat)):
                        val += self[i][k]*mat[k][j]
                    new_row.append(val)
                matrix.append(new_row)
            mod_matrix = make_matrix(matrix)
            return mod_matrix
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
            top_left = part4 + part5 + part6 -part2
            top_right = part1 + part2
            bottom_left = part3 + part4
            bottom_right = part1 - part3 + part5 - part7
            top = top_left.merge_cols(top_right)
            bottom = bottom_left.merge_cols(bottom_right)
            mat = top.merge_rows(bottom)
            return mat
        # Your Code


        
        


    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        if(len(mat) != len(self.rows)):
            return False
        
        for i in range(0,len(self.rows)):
            if(self.rows[i] != mat[i]):
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
    def __init__(self, vectors, indices, length):
        '''
        'length' is the number of rows of the matrix - the number of entries in 'vectors' is just the number of
        non-zero rows
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseMatrix, self).__init__(vectors)
        # Your Code
        self.values = vectors
        self.indices = indices
        self.length = length

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        return self.length  
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        if(type(key) is tuple == True):
            for i in self.indices:
                if(i ==  key(0)):
                    return self.values[i][key(1)]
        else:            
            for i in self.indices:
                if(i ==  key(0)):
                    return self.values[i]
            
            
    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        x = self.length
        for i in range(0,len(mat)):
            vector = Vector(mat[i])
            if (vector.is_zero != True):
                self.values.append[mat[i]]
                self.indices.append[x]
            else:
                x+=1
                


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''




      
