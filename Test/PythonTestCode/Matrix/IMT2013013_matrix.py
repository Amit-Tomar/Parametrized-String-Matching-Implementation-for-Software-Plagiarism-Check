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
    lst=[]
    indices=[]
    for elem in vector_list:
        for i in range(len(elem)):
            if(elem[i] != 0):
                lst.append(elem)
                indices.append(vector_list.index(elem))

    d = float(len(lst))/len(vector_list)

    if(d <= DENSITY_THRESHOLD):
        matrix = SparseMatrix(lst,indices,len(vector_list))
        
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
#         matrix_row=[]
#         for i in range(len(rows)):
#             matrix_row.append(rows[i])
#         return matrix_row


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
        This allows accessing the elements of a matri.zero_test(elem)x using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        if( isinstance(key, tuple) == True ): 
            return self.rows[key[0]][key[1]]
        elif type(key) == int:
            return self.rows[key]

        

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if len(self) <= self.MIN_RECURSION_DIM:
            return True
        else:
            return False
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (.zero_test(elem)allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        
        cnt = 0
        vector_sum = []
        if(len(self) == len(mat)):
            for i in range(len(self)):
                if(len(self.rows[i]) == len(mat.rows[i])):
                    cnt += 1
            if(cnt == len(self)):
                for i in range(len(self)):
                    vector_sum.append(self[i] + mat[i])
                matrix_sum = make_matrix(vector_sum)
            return matrix_sum
        else:
            return None
        
        '''if len(self) != len(mat):
            return None
        else:
            add_mat = []
            for i in range(len(self)):
                add_mat.append(self[i]+mat[i])
            matrix_add = make_matrix(add_mat)
            return matrix_add'''


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        vector_diff = []
        cnt = 0
        if(len(self) == len(mat)):
            for i in range(len(self)):
                if(len(self.rows[i]) == len(mat.rows[i])):
                    cnt += 1
            if(cnt == len(self)):
                for i in range(len(self)):
                    vector_diff.append(self[i] - mat[i])
                matrix_sub = make_matrix(vector_diff)
            return matrix_sub
        else:
            return None
        
        
        '''if len(self) != len(mat):
            return None
        sub_mat = []
        for i in range(len(self)):
            sub_mat.append(self[i] - mat[i])
        matrix_sub = make_matrix(sub_mat)
        return matrix_sub'''


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        count = 0
        iadd_vec = []
        min_len = min(len(self),len(mat))
        for i in range(min_len):
            if(len(self.rows[i] == len(mat.rows[i]))):
                count = count+1
        if(count == len(self)):
            iadd_vec.append(self[i] + mat[i])
            return iadd_vec



    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        count = 0
        isub_vec = []
        min_len = min(len(self),len(mat))
        for i in range(min_len):
            if(len(self.rows[i] == len(mat.rows[i]))):
                count = count+1
        if(count == len(self)):
            isub_vec.append(self[i] - mat[i])
            return isub_vec



    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        for i in range(len(self)):
            left_half, right_half = self.split(self[i])
        left_mat = make_matrix(left_half)
        right_mat = make_matrix(right_half)
        return left_mat, right_mat     
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        half = len(self)//2
        left_half, right_half = self.left_right_split()
        top_left = left_half[half:]
        top_right = right_half[half:]
        bottom_left = left_half[:half]
        bottom_right = right_half[:half]
        return make_matrix(top_left), make_matrix(top_right), make_matrix(bottom_left), make_matrix(bottom_right)


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''  
        merge_col_mat = []
        for i in range(len(self)):
            lst = []
            for elem1 in self[i]:
                lst.append(elem1)
            for elem2 in mat[i]:
                lst.append(elem2)
            merge_col_mat.append(lst)
        merge_matrix = make_matrix(merge_col_mat)
        return merge_matrix 


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        merged_row_matrix=[]
        for elem1 in self:
            merged_row_matrix.append(elem1)
        for elem2 in mat:
            merged_row_matrix.append(elem2)
        merged_row_matrix = make_matrix(merged_row_matrix)
        return merged_row_matrix


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        mult_vector = []
        for i in range(len(self)):
            if(len(vec) == len(self[i])):
                #vector = self[i] * vec
                mult_vector.append(self[i] * vec)
                return mult_vector
            else:
                return None
            
        '''mult_vect = []
        for i in range(len(self)):
            if len(self[i]) == len(vec):
                mult_vect.append(self[i] * vec)
            else:
                return None
        return mult_vect'''


    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        new_vector = []
        if(len(mat) == len(self)):
            if(self.is_small() == True or mat.is_small() == True):
                for i in range(len(self)):
                    vector = self[i] * mat
                    new_vector.append(vector)
                return vector
            else:  
                a, b, c, d = self.get_quarters()
                e, f, g, h = mat.get_quarters()
                
                p1 = a*(f-h)
                p2 = (a+b)*h
                p3 = (c+d)*e
                p4 = d*(g-e)
                p5 = (a+d)*(e+h)
                p6 = (b-d)*(g+h)
                p7 = (a-c)*(e+f)
                
                top_left = p4+p5+p6-p2
                top_right = p1+p2
                bottom_left = p3+p4
                bottom_right = p1-p3+p5-p7
                
                top = top_left.merge_cols(top_right)
                bottom = bottom_left.merge_cols(bottom_right)
                new_matrix = top.merge_rows(bottom)
                return new_matrix
        

    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        if(len(self) == len(mat)):
            for i in range(len(self)):
                for j in range(len(self[i])):
                    if(mat[i][j] == self[i][j]):
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
                    lst = [0]*len(self.rows[0])
                    lst_mat = make_vector(lst, zero_test = lambda x : (x == 0))
                    return lst_mat
        return None

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        merged_row_matrix=[]
        merged_indices_mat = []
        for elem1 in self:
            merged_row_matrix.append(self(elem1))
            merged_indices_mat.append(self.indices(elem1))
        for elem2 in mat:
            merged_row_matrix.append(mat(elem2))
            merged_indices_mat.append(len(self) + mat.indices(elem2))
        merged_row_matrix = SparseMatrix(merged_row_matrix, merged_indices_mat, self.length + mat.length )



    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        tl_vector = []
        bl_vector = []
        tr_vector = []
        br_vector = []

        left_half = self[(len(self)//2):]
        right_half = self[:(len(self)//2)]

        for i in range(len(left_half)):
            if self.indices[i] < self.length//2:
                tl_vector.append(left_half[i])
            else:
                bl_vector.append(left_half[i])
        for i in range(len(right_half)):
            if self.indices[i] < self.length//2:
                tr_vector.append(right_half[i])
            else:
                br_vector.append(right_half[i])
                
        top_left = make_matrix(tl_vector)
        bottom_left = make_matrix(bl_vector)
        top_right = make_matrix(tr_vector)
        bottom_right = make_matrix(br_vector)
        return top_left, bottom_left, top_right, bottom_right

                  

if __name__ == '__main__':
    v1 = make_vector([1,1], lambda x : (x == 0))
    mat1 = make_matrix([v1, v1])#, [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]])#, [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]])
    mat2 = make_matrix([v1, v1])#, [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]])#, [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]])
    '''mat1 = make_matrix([[1, 1, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    mat2 = make_matrix([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]])
    '''
    #print mat1 
    #print mat2
    mat3 = mat1 * mat2
    for vec in mat3:
        for e in vec:
            print e,
