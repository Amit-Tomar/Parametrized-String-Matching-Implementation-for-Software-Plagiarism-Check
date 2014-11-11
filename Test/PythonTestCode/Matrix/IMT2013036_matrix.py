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
    matrix = []
    vect_matrix = []
    
    for vect in vector_list:
        vect_matrix.append(make_vector(vect, zero_test = lambda x : (x == 0)))
    count = 0
    if len(vect_matrix) > SIZE_THRESHOLD:
        for vect in vect_matrix:
            
            if vect.is_zero():
                count += 1
        if count/len(vect_matrix) >= DENSITY_THRESHOLD:
            vect_list = []
            indices = []
            for ind in range(len(vect_matrix)):
                if vect_matrix[ind].is_zero() == False:
                    vect_list.append(vect_matrix[ind])
                    indices.append(ind)
            matrix = SparseMatrix(vect_list, indices, len(vect_matrix))
            return matrix
    
    matrix = FullMatrix(vect_matrix)
    return matrix
    '''not_zero=[]
    indices=[]
    for i in vector_list:
        if i.is_zero(i) != True:
            not_zero.append(i)
            indices.append(vector_list.index(i))
    
    density = float(len(not_zero))/len(vector_list)
    
    if(density <= DENSITY_THRESHOLD):
        sparse = SparseMatrix(not_zero,indices,len(vector_list))
        return sparse
    
    else:
        full = FullMatrix(vector_list)
        return full'''
            

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
        self.rows=rows

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
        if attr == 'nrows':
            return len(self.rows)
        if attr == 'ncols':
            return len(self.rows[0])
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if isinstance(key,tuple) == True:
            return self.rows[key[0]][key[1]]
        elif type(key) == int:
            return self.rows[key]

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if len(self) <= self.MIN_RECURSION_DIM:
            return True
        else:
            return False

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        c = 0
        new=[]
        if len(self) == len(mat):
            for i in range(len(self)):
                if len(self.rows[i]) == len(mat.rows[i]):
                    c+=1
            if(c == len(self)):
                for i in range(len(self)):
                    sum_vector = self[i] + mat[i]
                    new.append(sum_vector)
            sum_matrix = make_matrix(new)
            return sum_matrix
        else:
            return None
                    

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        c = 0
        new=[]
        if len(self) == len(mat):
            for i in range(len(self)):
                if len(self.rows[i]) == len(mat.rows[i]):
                    c+=1
            if(c == len(self)):
                for i in range(len(self)):
                    diff_vector = self[i] - mat[i]
                    new.append(diff_vector)
            diff_matrix = make_matrix(new)
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
        # Your Code
        c = 0
        new=[]
        if len(self) == len(mat):
            for i in range(len(self)):
                if len(self.rows[i]) == len(mat.rows[i]):
                    c+=1
            if(c == len(self)):
                for i in range(len(self)):
                    sum_vector = self[i] + mat[i]
                    new.append(sum_vector)
            sum_matrix = make_matrix(new)
            return sum_matrix
        else:
            for i in range(min(len(self),len(mat))):
                if len(self.rows[i]) == len(mat.rows[i]):
                    c+=1
            if(c == len(self)):
                for i in range(min(len(self),len(mat))):
                    sum_vector = self[i] + mat[i]
                    new.append(sum_vector)
            sum_matrix = make_matrix(new)
            return sum_matrix

    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        c = 0
        new=[]
        if len(self) == len(mat):
            for i in range(len(self)):
                if len(self.rows[i]) == len(mat.rows[i]):
                    c+=1
            if(c == len(self)):
                for i in range(len(self)):
                    diff_vector = self[i] - mat[i]
                    new.append(diff_vector)
            diff_matrix = make_matrix(new)
            return diff_matrix
        else:
            for i in range(min(len(self),len(mat))):
                if len(self.rows[i]) == len(mat.rows[i]):
                    c+=1
            if(c == len(self)):
                for i in range(min(len(self),len(mat))):
                    diff_vector = self[i] - mat[i]
                    new.append(diff_vector)
            diff_matrix = make_matrix(new)
            return diff_matrix


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        left = []
        right = []
        for vector in range(len(self)):
            left.append(self[vector].split()[0])
            right.append(self[vector].split()[1])
        return left, right
    
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
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
        # Your Code
        matrix = []
        
        for i in range(len(mat)):
            matrix.append(self[i]+mat[i])
        
        matrix = make_matrix(matrix)
        return matrix
        
    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        matrix = []
        for i in range(len(self)):
            matrix.append(self[i])
        for j in range(len(mat)):
            matrix.append(mat[j])
        return matrix
        


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        mult = []
        for i in range(len(self)):
            if len(self[i]) == len(vec):
                mult.append(self[i] * vec)
            else:
                return None
        return mult

    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        matrix = []
        row1 = []
        row2 = []
        
        a , b , c , d = self.get_quarters()
        e , f , g , h = mat.get_quarters()
        if len(self.rows[0]) != len(mat.rows):
            return None
        
        else:
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
                part1 = a*(f-h)
                part2 = (a+b)*h
                part3 = (c+d)*e
                part4 = d*(g-e)
                part5 = (a+d)*(e+h)
                part6 = (b-d)*(g+h)
                part7 = (a-c)*(e+f)
                    
                top_left = part4 + part5 + part6 - part2
                top_right = part1 + part2
                bottom_left = part3 + part4
                bottom_right = part1 - part3 + part5 -part7
                row1 = top_left.merge_cols(top_right)
                row2 = bottom_left.merge_cols(bottom_right)
                matrix = row1.merge_rows(row2)
                return matrix
             


    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if len(self) != len(mat):
            return None
        else:
            for i in range(len(self)):      
                if self[i] == mat[i]:
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
        return len(self.indices)
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        # Your Code
        if isinstance(key,tuple) == True:
            return self.rows[key[0]][key[1]]
        else:
            return self.rows[key]
        
    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        matrix = []
        for i in range(len(self)):
            matrix += self[i]
        for j in range(len(mat)):
            matrix += mat[j]
        return matrix
        

    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        nrow = 0
        for rows in self:
            nrow += 1
        if nrow%2 == 0:
            half = nrow/2
        else:
            half = (nrow/2)+1
        for i in range(len(self)):
            left,right = self.split(self[i])
        
        topleft = left[half:]
        bottomleft = left[:half]
        topright = right[half:]
        bottomright = right[:half]
        
        return topleft, topright, bottomleft, bottomright
   
'''if __name__ == '__main__':
    mat1 = make_matrix([[1, 2, 3], [4, 5, 6]])#, [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]])
    mat2 = make_matrix([[1, 2], [3, 4], [5, 6]])#, [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]])
    
    mat1 = make_matrix([[1, 1, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    mat2 = make_matrix([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]])
    
    print mat1
    mat3 = mat1*mat2
    for vec in mat3:
        for e in vec:
            print e,
        print'''
