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
    non_zero_list =[]
    indices =[]
    for obj in vector_list:
        if not obj.is_zero(obj):
            non_zero_list.append(obj)
            indices.append(vector_list.index[obj])
    
    non_zero_percentage = float(len(non_zero_list) / len(vector_list))
    if density <= DENSITY_THRESHOLD:
        matrix = SparseMatrix(non_zero_list,indices,len(vector_list))
        
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
    
        
    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if isinstance(key,tuple) == True:
            return self.rows[key[0]][key[1]]
        else:
            return self.rows[key]
                                 
    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if len(self.rows) <= self.MIN_RECURSION_DIM:
            return True
        else:
            return False    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        if len(mat) == len(self):
            if len(mat[0]) == len(self[0]):
                temp =[]
                i = 0
                while i < len(self):
                    temp.append(self[i] + mat[i])
                    i+=1
                matrix = make_matrix(temp)
                return matrix
            else:
                return None

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        if len(mat) == len(self):
            if len(mat[0]) == len(self[0]):
                temp =[]
                i = 0
                while i < len(self):
                    temp.append(self[i] - mat[i])
                    i+=1
                return temp
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
        minimum = min(len(mat),len(self))
        i = 0
        while i < minimum:
            self[i] += mat[i]
            i+=1
    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        i = 0
        minimum = min(len(mat),len(self))
        while i < minimum:
            self[i] -= mat[i]

    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        left_list = []
        right_list =[]
        for i in self.rows:
            left_vector,right_vector = i.split(i)
            left_list.append(left_vector)
            right_list.append(right_vector)
            
        left_matrix = make_matrix(left_list)
        right_matrix = make_matrix(right_list)
        
        return left_matrix, right_matrix
            
            
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        top_left_list = []
        top_right_list = []
        bottom_left_list =[]
        bottom_right_list = []
        left_matrix,right_matrix = self.left_right_split()
        length1 = len(left_matrix) / 2
        length2 = len(left_matrix) - length1
        i = 0
        while i < length1:
            top_left_list.append(left_matrix[i])
            i += 1
            
        j = 0
        while j < length2:
            bottom_left_list.append(left_matrix(length1 + j))
            j += 1
            
        length1 = len(right_matrix) / 2
        length2 = len(right_matrix) - length1
        i = 0
        while i < length1:
            top_right_list.append(right_matrix[i])
            i += 1
            
        j = 0
        while j < length2:
            bottom_right_list.append(right_matrix(length1 + j))
            j += 1
            
        top_left_matrix = make_matrix(top_left_list)
        top_right_matrix = make_matrix(top_right_list)
        bottom_left_matrix = make_matrix(bottom_left_list)
        bottom_right_matrix = make_matrix(bottom_right_list)
            
        return top_left_matrix, top_right_matrix, bottom_left_matrix, bottom_right_matrix
    
    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        if len(mat[0]) == len(self[0]):
            j,i=0
            for list in mat:
                while i < len(list):
                    self[j].append(list[i])
                    i+=1
                j+=1
        else:
            return None
    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        if len(self) == len(mat):
            for i in mat:
                self.append(i)
        else:
            return None

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        i = 0
        j = 0
        list = []
        if len(vec) == len(self):
            while i < len(self[0]):
                sum = 0
                while j < len(self):
                    sum = sum + (vec[j] * self[j][i])
                    j += 1
                list.append[sum]
                i += 1
            return make_vector(list,zero_test)
        
        else:
            return None
    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        if is_small(self) or is_small(mat):
            if len(self[0]) == len(mat):
                while i < len(self):
                    __rmul__(self[i],mat)
                    
    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        i,j = 0
        if len(self) == len(mat) and len(self[0]) == len(mat[0]):
            while i <len(self):
                while j < len(self[i]):
                    if self[i][j] == mat[i][j]:
                        return True
                    else:
                        return False
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
        self.vectors = vectors
        self.indices =indices
        self.length = length


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        # Your Code
        return len(self.values)
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        # Your Code
        return self.values[i]
    
    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        if len(self.values) == len(mat):
            for i in mat:
                if i in indices:
                    self.append(i)
        else:
            return None

    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        top_left_list = []
        top_right_list = []
        bottom_left_list =[]
        bottom_right_list = []
        left_matrix,right_matrix = self.values.left_right_split()
        length1 = len(left_matrix) / 2
        length2 = len(left_matrix) - length1
        i = 0
        while i < length1:
            if i in indices:
                top_left_list.append(left_matrix[i])
                i += 1
            
        j = 0
        while j < length2:
            if i in indices:
                bottom_left_list.append(left_matrix(length1 + j))
                j += 1
            
        length1 = len(right_matrix) / 2
        length2 = len(right_matrix) - length1
        i = 0
        while i < length1:
            if i in indices:
                top_right_list.append(right_matrix[i])
                i += 1
            
        j = 0
        while j < length2:
            if i in indices:
                bottom_right_list.append(right_matrix(length1 + j))
                j += 1
            
        top_left_matrix = make_matrix(top_left_list)
        top_right_matrix = make_matrix(top_right_list)
        bottom_left_matrix = make_matrix(bottom_left_list)
        bottom_right_matrix = make_matrix(bottom_right_list)
            
        return top_left_matrix, top_right_matrix, bottom_left_matrix, bottom_right_matrix

        