'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD
import math

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    count = 0
    total_count = 0
    vec_list = []
    indices_list = []
    row = 0

    for i in vector_list:
        flag = 0
        for j in i:
            total_count += 1
            if j!= 0:
                flag = 1
        if flag==0:
            count += 1
    if float(count)/ float(total_count) < DENSITY_THRESHOLD and total_count > SIZE_THRESHOLD:
        for i in vector_list:
            flag = 0
            for j in i:
                total_count += 1
                if j!= 0:
                    flag = 1
            row += 1
            if flag == 1:
                vec_list.append(i)
                indices_list.append(row)
        matrix = SparseMatrix(vec_list, indices_list, len(vector_list))
    else:
        matrix = FullMatrix(vector_list)        

    return matrix
                
            
    
class Matrix(object):
    '''
    Base Matrix Class - implements basic matrix operations
    '''
    MIN_RECURSION_DIM = 0

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
        
        if attr == 'nrows':
            return len(self.rows)

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
    
        if isinstance(key, int):
            return self.rows[key]
        else:
            return self.rows[key[0]][key[1]]
            
    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if len(self) < self.MIN_RECURSION_DIM or len(self[0]) < self.MIN_RECURSION_DIM:
            return True
        else: 
            return False

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        sum_mat = []
        if len(self) == len(mat):
            for i in range(len(self)):
                if self[i]!= None and mat[i]!= None:
                    vector1 = make_vector(self[i], None)
                    vector2 = make_vector(mat[i], None)
                    vector = (vector1 + vector2) 
                    sum_mat.append(vector.data)
            mat = make_matrix(sum_mat)
            return mat
        
        return None       

    def __sub__(self,  mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
       
        sub_mat = []
        if len(self) == len(mat):
            for i in range(len(self)):
                if self[i]!=None and mat[i]!=None:
                    vector1 = make_vector(self[i], None)
                    vector2 = make_vector(mat[i], None)
                    vector = (vector2 - vector1) 
                    sub_mat.append(vector.data)
            mat = make_matrix(sub_mat)
            return mat
        
        return None  
        

    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''

        rows = min (len(self), len(mat))
        cols = min(len(self[0]), len(mat[0]))
        
        for i in range(0, rows):
            for j in range(0, cols):
                self[i][j] = self[i][j] + mat[i][j]
                
        mat = self.make_matrix(self)
        return mat


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        rows = min (len(self), len(mat))
        cols = min(len(self[0]), len(mat[0]))
        
        for i in range(0, rows):
            for j in range(0, cols):
                self[i][j] = self[i][j] - mat[i][j]
                
        mat = self.make_matrix(self)
        return mat


    def left_right_split(self, mat):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        left_mat = []
        right_mat = []
        for i in mat.rows:
            obj = make_vector(i, None)
            left, right = obj.split()
            left_mat.append(left.data)
            right_mat.append(right.data)
            
        matrix_left = make_matrix(left_mat)
        matrix_right = make_matrix(right_mat)
        return matrix_left, matrix_right
        
        
    def get_quarters(self, mat):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
  
        mat_left = self.left_right_split(mat)[0]
        mat_right = self.left_right_split(mat)[1]
        top_left = mat_left.rows[:(len(mat_left) / 2)]
        top_right = mat_right.rows[:(len(mat_right) / 2)]
        bottom_left = mat_left.rows[(len(mat_left) / 2):]
        bottom_right = mat_right.rows[(len(mat_right) / 2):]  
        mat_top_left = make_matrix(top_left)
        mat_top_right = make_matrix(top_right)
        mat_bottom_left = make_matrix(bottom_left)
        mat_bottom_right = make_matrix(bottom_right)
        
        return (mat_top_left, mat_top_right, mat_bottom_left, mat_bottom_right)
            


    def merge_cols(self, mat1, mat2):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        new = []
        
        minimum = min (len(mat1), len(mat2))
        for j in range(0, minimum):
            sublist = []
            for i in range(len(mat1[0])):
                sublist.append(mat1[j][i])
            for i in range(len(mat2[0])):
                sublist.append(mat2[j][i])          
            new.append (sublist)
            
        mat_object = FullMatrix(new)
        return mat_object
    
    
    def merge_rows(self, mat1, mat2):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        new = []
        
        for i in mat1:
            new.append(i)
            
        for j in mat2:
            new.append(j)
        
        return FullMatrix(new)

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
   
        transposed = []
        final_m = []
        for i in range(0, len(self)):
            sublist = []
            for j in range(0, len(self[0])):
                sublist.append(self[j][i])
            transposed.append(sublist)
            
        for i in range(0, len(vec)):
            vec_tr = make_vector(transposed[i], None)
            final_m.append(vec * vec_tr)
        final_obj = make_vector(final_m)
        return final_obj
    

    def strassen(self, mat1, mat2, n):
        '''
        Returns the product matrix with the padded eroes to the mul function. The two matrices mat1 and mat2 are modified versions
        of the original matrices that are to be multiplied. mat1 and mat2 are square matrices of the same order such that the strassen
        algorithm can be conveniently applied on them in this function.
        '''
        if n == 1:    
            ele = [[0]]
            ele[0][0] = mat1[0][0] * mat2[0][0]
            return ele
            
        else:
            a = self.get_quarters(mat1)[0]
            b = self.get_quarters(mat1)[1]
            c = self.get_quarters(mat1)[2]
            d = self.get_quarters(mat1)[3]
                
            e = self.get_quarters(mat2)[0]
            f = self.get_quarters(mat2)[1]
            g = self.get_quarters(mat2)[2]
            h = self.get_quarters(mat2)[3]
                
            p1 = self.strassen(a + d, e + h, n/2)
            p2 = self.strassen(c + d, e, n/2)
            p3 = self.strassen(a, f - h, n/2)
            p4 = self.strassen(d, g - e, n/2)
            p5 = self.strassen(a + b, h, n/2)
            p6 = self.strassen(c - a , e + f, n/2)
            p7 = self.strassen(b - d, g + h, n/2)

            p1_obj = make_matrix(p1)
            p2_obj = make_matrix(p2)
            p3_obj = make_matrix(p3)
            p4_obj = make_matrix(p4)
            p5_obj = make_matrix(p5)
            p6_obj = make_matrix(p6)
            p7_obj = make_matrix(p7)
                
            c11 = ((p1_obj+ p4_obj) - p5_obj )+ p7_obj 
            c12 = p3_obj + p5_obj
            c21 = p2_obj + p4_obj
            c22 = (p1_obj + p3_obj) - p2_obj + p6_obj

            c = []
            for row in range(len(c11) * 2):
                sublist = []
                for col in range(len(c11) * 2):
                    sublist.append(0)
                c.append(sublist)
   
            length = len(c11) 
            
        
            for i in range(length):
                for j in range(length):
                    c[i][j] = c11[i][j]
                    c[i][j + length] = c12[i][j]
                    c[i + length][j] = c21[i][j]
                    c[i + length][j + length] = c22[i][j]
 
     
            c_obj = FullMatrix(c)
            return c_obj
           
    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        
        if len(self[0]) != len(mat):
            print "cannot multiply"
            return None
        
        if(self.is_small() == True):
            transposed = []
            for i in range(0, len(mat)):
                sublist1 = []
                for j in range(0, len(mat[0])):
                    sublist1.append(mat[j][i])
                transposed.append(sublist1)
                
            product_list = []   
                 
            for i in self:
                vector1 = make_vector(i, None)
                sublist = []
                for j in transposed:
                    vector2 = make_vector(j, None)
                    sublist.append(vector1 * vector2)
                product_list.append(sublist)
            prod_list_obj = make_matrix(product_list)
            
            return prod_list_obj
            
        else:
    
            lengths = []
            rows1 = len(self)
            same = len(self[0])
            cols2 = len(mat[0])
            lengths.append(rows1)
            lengths.append(same)
            lengths.append(cols2)
            ref_length = max(lengths)
            difference_r = int((2 ** math.ceil(math.log(ref_length, 2))) - rows1)
            difference = int ((2 ** math.ceil(math.log(ref_length,2))) - same)
            diff_col = int ((2 ** math.ceil(math.log(ref_length, 2))) - cols2) 
                       
            mat_row = []
            mat_col = []
             
            if difference_r == 0 and difference == 0:
                mat1_self = make_matrix(self.rows)
               
            elif difference_r == 0:
                new = []
                for i in range(len(self)):
                    sublist = []
                    for j in range(difference):
                        sublist.append(0)
                    new.append(sublist)
                mat1_self = self.merge_cols(self.rows, new)
                
            elif difference == 0:
                new = []
                for i in range(difference_r):
                    sublist = []
                    for j in range(len(self[0])):
                        sublist.append(0)
                    new.append(sublist)
                mat1_self = self.merge_rows(self.rows, new)

            else:            
                for i in range(0, difference_r):
                    sublist = []
                    for j in range(0, same):
                        sublist.append(0)
                    mat_row.append(sublist)
                mat_row_obj = FullMatrix(mat_row)
                self_obj = make_matrix(self.rows)
                final_obj_self = self.merge_rows(self_obj, mat_row_obj)
                for i in range(0, len(final_obj_self)):
                    sublist = []   
                    for j in range(0, difference):
                        sublist.append(0)
                    mat_col.append(sublist)
                mat_col_obj = FullMatrix(mat_col)                    
                mat1_self = self.merge_cols(final_obj_self, mat_col_obj)
        
            mat_row = []
            mat_col = []          
                
            if difference == 0 and diff_col == 0:
                final = make_matrix(mat.rows)
                                
            elif difference == 0:
                new = []
                for i in range(len(mat)):
                    sublist = []
                    for j in range(diff_col):
                        sublist.append(0)
                    new.append(sublist)
                final = self.merge_cols(mat.rows, new)
                
            elif diff_col == 0:
                new = []
                for i in range(difference):
                    sublist = []
                    for j in range(len(self[0])):
                        sublist.append(0)
                    new.append(sublist)
                final = self.merge_rows(mat.rows, new)

            else:      
                      
                for i in range(0, difference):
                    sublist1 = []
                    for j in range(0, cols2):
                        sublist1.append(0)
                    mat_row.append(sublist1)
                mat_row_obj_m = make_matrix(mat_row)
                self_obj_m = make_matrix(mat.rows)
                final_obj_self_m = self.merge_rows(self_obj_m, mat_row_obj_m)
                
                for i in range(0, len(final_obj_self_m)):
                    sublist = []   
                    for j in range(0, diff_col):
                        sublist.append(0)
                    mat_col.append(sublist)
                mat_col_obj_m = make_matrix(mat_col)
                final = self.merge_cols(final_obj_self_m, mat_col_obj_m)                   
            prod = self.strassen(mat1_self, final, len(mat1_self))        
            non_zero_list = []
            
            for i in range (0, len(self)):
                sublist1 = []
                for j in range(0, len(mat[0])):
                    sublist1.append(prod[i, j])
                non_zero_list.append(sublist)
            non_zero_list_obj = make_matrix(non_zero_list)   
             
            return non_zero_list_obj
                
           
            
    def __eq__(self, mat):
        
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        
        if len(self) != len(mat):
            return False
        
        if len(self[0]) != len(mat[0]):
            return False
        
        for i in range(0, len(self)):
            for j in range(0, len(self[0])):
                if self[i][j] != mat[i][j]:
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
        vectors = self.vectors



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
        return len(self.vectors)
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''

        
        if isinstance(key, int):
            if key in self.indices:
                return self.vectors[key]
            else:
                return None
        else:
            if key[0] in self.indices:
                return self.vectors[key[0]][key[1]]
            else:
                return None        
   

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        final_matrix_values = []
        final_matrix_indices = []
    
        for i in range(0, len(self)):
            final_matrix_values.append(self[i])
            final_matrix_indices.append(self.indices[i])
            
        for i in range(0, len(mat)):
            final_matrix_values.append(mat[i])
            final_matrix_indices.append(mat.indices[i])
        merged_obj = SparseMatrix(final_matrix_values, final_matrix_indices, self.length)
        return merged_obj


    def get_quarters(self, mat):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        mat_left, mat_right = mat.left_right_split()
        
        top_left_vector = mat_left.vectors[:(len(mat_left) / 2)]
        top_left_indices = mat_left.indices[:(len(mat_left) / 2)]
        top_right_vector = mat_right.vectors[:(len(mat_right) / 2)]
        top_right_indices = mat_right.indices[:(len(mat_right) / 2)]
        
        bottom_left_vector = mat_left.vectors[(len(mat_left) / 2):]
        bottom_left_indices = mat_left.indices[(len(mat_left) / 2):]
        bottom_right_vector = mat_right.vectors[(len(mat_right) / 2):]        
        bottom_right_indices = mat_right.indices[(len(mat_right) / 2):]  
        
        mat_top_left_obj = SparseMatrix(top_left_vector, top_left_indices, self.length )
        mat_top_right_obj = SparseMatrix(top_right_vector, top_right_indices, self.length )
        mat_bottom_left_obj = SparseMatrix(bottom_left_vector, bottom_left_indices, self.length )
        mat_bottom_right_obj = SparseMatrix(bottom_right_vector, bottom_right_indices, self.length )
        
        return mat_top_left_obj, mat_top_right_obj, mat_bottom_left_obj, mat_bottom_right_obj
            
            
if __name__ == '__main__':
    pass

    a = [[1,11,2,1],[2,0,45,2],[3,0,8,3],[9,4,6,4]]
    b = [[5,1,5,5],[2,6,6,6],[3,5,7,5],[12,9,8,1]]
   # a = [[1,9,1,0,7,6,0],[1,0,3,0,5,6,0],[8,8,3,0,5,0,0],[1,2,0,4,0,6,12],[0,2,3,9,5,0,0]]
    #b = [[1,0],[2,0],[1,0],[4,0],[1,0],[7,0],[0,0]]

    a_obj = make_matrix(a)
    b_obj = make_matrix(b)
    final = a_obj * b_obj
    print "The final product matrix is: ", final.rows
