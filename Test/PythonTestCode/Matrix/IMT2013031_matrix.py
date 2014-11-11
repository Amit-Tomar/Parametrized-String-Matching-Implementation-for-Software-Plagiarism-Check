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
    count = 0
    for vector1 in vector_list:
        vector_obj = Vector(vector1, zero_test = lambda x : (x == 0))
        if(vector_obj.is_zero()==True):
            count = count+1 
    if((count/len(vector_list))>DENSITY_THRESHOLD and len(vector_list)>SIZE_THRESHOLD):
        i = 0
        matrix_elmts = []
        matrix_indices = []
        while(i<len(vector_list)):
            vector_obj1 = Vector(vector_list[i] , zero_test = lambda x : (x == 0))
            if(vector_obj1.is_zero()==True):
                matrix_elmts.append(vector_list[i])
                matrix_indices.append(i)
                i = i+1
    else:
        i = 0
        matrix_elmts = []
        while(i<len(vector_list)):
            matrix_elmts.append(vector_list[i])
            i = i+1
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
        if(attr=="nrows"):
            return len(self.rows)
        if(attr=="ncols"):
            return len(self.rows[0])
    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        if(isinstance(key , tuple)==True):
            return self.rows[key[0]][key[1]]
        if(isinstance(key , int)==True):  
            return self.rows[key-1]

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if(len(self.rows)<=self.MIN_RECURSION_DIM):
            return True
        else:
            return False
    
    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        if(self.__len__()==len(mat)):
            i = 0
            j = 0
            sum_matrix = []
            row_matrix = []
            while(i<self.__len__()):
                while(j<len(self.rows[0])):
                    k = mat[i][j]+self.rows[i][j]
                    row_matrix.append(k)
                    j = j+1
                sum_matrix.append(row_matrix)
                i = i+1
                j = 0
                row_matrix = []
            return sum_matrix
        else:
            return None
            
    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        if(self.__len__()==len(mat)):
            i = 0
            j = 0
            diff_matrix = []
            row_matrix = []
            while(i<self.__len__()):
                while(j<len(self.rows[0])):
                    k = self.rows[i][j]-mat[i][j]
                    row_matrix.append(k)
                    j = j+1
                diff_matrix.append(row_matrix)
                i = i+1
                j = 0
                row_matrix = []
            return diff_matrix
        else:
            return None


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        if(self.__len__()==len(mat)):
            i = 0
            j = 0
            sum_matrix = []
            row_matrix = []
            while(i<min(self.__len__() , len(mat))):
                while(j<len(self.rows[0])):
                    k = self.rows[i][j]+mat[i][j]
                    row_matrix.append(k)
                    j = j+1
                sum_matrix.append(row_matrix)
                i = i+1
                j = 0
                row_matrix = []
            return sum_matrix
        else:
            return None
        


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        if(self.__len__()==len(mat)):
            i = 0
            j = 0
            diff_matrix = []
            row_matrix = []
            while(i<min(self.__len__() , len(mat))):
                while(j<len(self.rows[0])):
                    k = self.rows[i][j]-mat[i][j]
                    row_matrix.append(k)
                    j = j+1
                diff_matrix.append(row_matrix)
                i = i+1
                j = 0
                row_matrix = []
            return diff_matrix
        else:
            return None


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        first_half_mat = []
        second_half_mat = []
        for vector in self.rows:
            vector_obj = Vector(vector, zero_test = lambda x : (x == 0))
            (first , last) = vector_obj.split()
            first_half_mat.append(first)
            second_half_mat.append(last)
        make_matrix(first_half_mat)
        make_matrix(second_half_mat)
            
            
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        first_half_mat = []
        second_half_mat = []
        for vector in self.rows:
            vector_obj3 = Vector(vector, zero_test = lambda x : (x == 0))
            (first , last) = vector_obj3.split()
            first_half_mat.append(first)
            second_half_mat.append(last)
        vector_obj4 = Vector(first_half_mat , zero_test = lambda x : (x == 0))
        (topleft , topright) = vector_obj4.split()
        vector_obj5 = Vector(first_half_mat , zero_test = lambda x : (x == 0))
        (bottomleft , bottomright) = vector_obj5.split()    
        return topleft , topright , bottomleft , bottomright 
        
    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        merge_col = self.rows+mat
        return merge_col


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        merge_row = []
        i = 0
        while(i<len(self.rows)):
            merge_row.append(self.rows[i]+mat[i])
            i = i+1
        return merge_row
            


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        if(self.__len__()==len(vec)):
            rmul_vector = []
            sum_elmts = 0
            i = 0
            j = 0
            while(i<len(self.rows[0])):
                while(j<len(vec)):
                    sum_elmts = sum_elmts+(vec[j]*self.rows[j][i])
                    j = j+1
                rmul_vector.append(sum_elmts)
                sum_elmts = 0
                j = 0
                i = i+1
            return rmul_vector
        else: 
            return None
            
    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        mul_matrix = []
        if(len(mat)<self.MIN_RECURSION_DIM and len(self.rows)<self.MIN_RECURSION_DIM):
            for vector in mat:
                first_row = self.__rmul__(vector)
                mul_matrix.append(first_row)
            
            
        
        
    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        if(self.rows==mat):
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
    def __init__(self, vectors, indices, length):
        '''
        'length' is the number of rows of the matrix - the number of entries in 'vectors' is just the number of
        non-zero rows
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseMatrix, self).__init__(vectors)
        self.mat_values = vectors
        self.mat_indices = indices 
        self.length = length
    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        return len(self.mat_indices) 
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        zero_matrix = []
        i = 0
        while(i<self.__len__()):
            zero_matrix.append(0)
            i = i+1
            if(isinstance(key , tuple)==True):
            if key[0] in self.mat_indices:
            return self.mat_values[key[0]][key[1]]
            else:
            return 0
        if(isinstance(key , int)==True):
            if key in self.mat_indices:
                return self.mat_values[key]
            else:
            return zero_matrix 
            

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        marge_values = []
        merge_indices = []
        merge_sparese_indices = []    
        i = 0
        while(i<len(self.mat_values)):
            merge_values.append(self.mat_values[i]+mat[i])
            i = i+1
        j = 0
        while(i<len(mat)):
            merge_indices[j] = self.__len__()-1+j
            j = j+1
        merge_sparse_indies = self.mat_indices+merge_indices 
        return merge_values , merge_sparse_indices
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        first_half_mat = []
        second_half_mat = []
        for vector in self.mat_values:
            vector_obj6 = Vector(vector , zero_test = lambda x : (x == 0))
            (first , last) = vector_obj6.split()
            first_half_mat.append(first)
            second_half_mat.append(last)
        vector_obj7 = Vector(first_half_mat , zero_test = lambda x : (x == 0))
        (topleft , topright) = vector_obj7.split()
        vector_obj8 = Vector(first_half_mat , zero_test = lambda x : (x == 0))
        (bottomleft , bottomright) = vector_obj8.split()    
        return topleft , topright , bottomleft , bottomright     