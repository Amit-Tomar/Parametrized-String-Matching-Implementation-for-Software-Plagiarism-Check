'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD
import var_globals

def reset_globals():
    '''
    Reset the values of the global variables from var_globals.py
    '''
    
    var_globals.COL_LENGTH = 0
    var_globals.ROW_LENGTH = 0
    var_globals.COL_PAD    = 0
    var_globals.ROW_PAD    = 0
    var_globals.FLAG_COL   = 0
    var_globals.FLAG_ROW   = 0

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
    
    if len(vector_list) < SIZE_THRESHOLD:
        return FullMatrix(vector_list, len(vector_list), len(vector_list[0]))
    
    else:    
        count = [vector_list[i] for i in range(len(vector_list))
                 if vector_list[i].is_zero()]
                
        if len(count) > DENSITY_THRESHOLD * len(vector_list):
            
            indices = [key for key, elem in enumerate(vector_list)
                      if not elem.is_zero()]
            values = [elem for key, elem in enumerate(vector_list)
                      if not elem.is_zero()]
            
            return SparseMatrix(values, indices,
                                len(vector_list), len(vector_list[0]))
            
        else:
            return FullMatrix(vector_list, len(vector_list),
                              len(vector_list[0]))
        

class Matrix(object):
    '''
    Base Matrix Class - implements basic matrix operations
    '''
    MIN_RECURSION_DIM = 5
    
    def __init__(self, rows, length, ncols):
        '''
        'rows' is a list of vectors
        Keep this is the row list for the matrix
        '''
        # Your Code

        self.row_list = rows
        self.length = length
        self.ncols = ncols

    def __len__(self):
        '''
        Return the number of rows of the matrix
        Equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        # Your Code
        
        return self.length

    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        # Your Code
    
        if attr == 'nrows':
            return len(self)

        elif attr == 'ncols':
            return self.ncols


    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        
        if isinstance(key, int):
            return self.row_list[key]
        
        else:
            return self.row_list[key[0]][key[1]]

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
    
        return (len(self) < 5)

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        
        if len(self) != len(mat):
            return None
        
        sum_mat = [self[i] + mat[i] for i in range(len(self))]
        
        return make_matrix(sum_mat)
            


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        
        if len(self) != len(mat):
            return None
        
        sum_mat = [self[i] - mat[i] for i in range(len(self))]
        
        return make_matrix(sum_mat)


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code

        rng = min(len(self) , len(mat))
        
        rlist = [self[count] + mat[count]
                            for count in range(rng)]
        
        return make_matrix(rlist)


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code

        rng = min(len(self) , len(mat))
        
        rlist = [self[count] - mat[count]
                            for count in range(rng)]
        
        return make_matrix(rlist)


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code

        lmat = [self[i].split()[0] for i in range(len(self))]
        rmat = [self[i].split()[1] for i in range(len(self))]
        
        return make_matrix(lmat), make_matrix(rmat)
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code

        lmat, rmat = self.left_right_split()
        
        count = len(lmat)       
        
        tl_list = [lmat[i] for i in range(count / 2)]
        bl_list = [lmat[i] for i in range(count / 2, count)]        
            
        count = len(rmat)        
        
        tr_list = [rmat[i] for i in range(count / 2)]
        br_list = [rmat[i] for i in range(count / 2, count)]                
            
        return (make_matrix(tl_list),
                make_matrix(tr_list),
                make_matrix(bl_list),
                make_matrix(br_list))


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
                  
        t_list = [self[i].merge(mat[i]) for i in range(len(mat))]
        
        return make_matrix(t_list)

    
    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        
        t_list = [self[i] for i in range (len(self))]
        
        for i in range(len(mat)):
            t_list.append(mat[i])
            
        return make_matrix(t_list)

    
    def pad_row(self):
        '''
        Pad the rows of this matrix to the nearest power of 2 
        '''
        
        pad = 2             
        
        while pad < self.nrows:
            pad = pad << 1
               
        pad -= self.nrows
        
        if var_globals.FLAG_ROW == 0:
            var_globals.FLAG_ROW += 1
            var_globals.ROW_LENGTH = self.nrows
       
        if pad != 0:
            if var_globals.ROW_PAD == 0:
                var_globals.ROW_PAD = pad
            
            pad_vector = [make_vector([0] * self.ncols)
                        for _ in range(pad)]                
            
            new_mat = self.merge_rows(make_matrix(pad_vector))
            t_list = [new_mat[i] for i in range(len(new_mat))]
            
            return make_matrix(t_list)
        
        else:
            return self        
            
    
    def pad_col(self):
        '''
        Pad the columns of this matrix to the nearest power of 2
        '''
                
        pad = 2               
        
        while pad < self.ncols:
            pad = pad << 1
             
        pad -= self.ncols
        
        if var_globals.FLAG_COL == 1:
            var_globals.COL_LENGTH = self.ncols
        
        var_globals.FLAG_COL += 1
       
        if pad != 0:
            var_globals.COL_PAD = pad
                      
            pad_vector = [make_vector([0] * pad)
                        for _ in range(self.nrows)]
            
            new_mat = self.merge_cols(make_matrix(pad_vector))
            
            t_list = [new_mat[i] for i in range(len(new_mat))]
            
            return make_matrix(t_list)
        
        else:
            return self
    
    
    def rmul(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code

        if len(self) != len(vec):
            return None
    
        mul = []

        for i in range(self.ncols):            
            col = [self[count][i] for count in range(len(self))]            
            mul.append(vec * col)  
    
        return make_vector(mul, vec.zero_test)
    
    
    def unpad(self):
        ''' Return this matrix to original dimensions ''' 
        
        m_list = []
        
        for i in range(var_globals.ROW_LENGTH):
            v_list = [self[i][j] for j in range(var_globals.COL_LENGTH)]
            
            print v_list
            
            m_list.append(make_vector(v_list))
        
        reset_globals()
        
        return make_matrix(m_list)

    
    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        
        if self.ncols != len(mat):
            
            print 'Incompatible matrices:',
            print 'Columns of matrix 1 not equal to rows of matrix 2'
            return None
            
        else:
            
            mat_1 = self.pad_col()
            mat_1 = mat_1.pad_row()
            
            mat_2 = mat.pad_col()
            mat_2 = mat_2.pad_row()
            
            if not mat_1.is_small():                
                p_1 = [mat_1.get_quarters(), mat_2.get_quarters()]
                pr1 = p_1[0][0] * (p_1[1][1] - p_1[1][3])
                pr2 = (p_1[0][0] + p_1[0][1]) * p_1[1][3]
                pr3 = (p_1[0][2] + p_1[0][3]) * p_1[1][0]
                pr4 = p_1[0][3] * (p_1[1][2] - p_1[1][0])
                pr5 = (p_1[0][0] + p_1[0][3]) * (p_1[1][0] + p_1[1][3])
                pr6 = (p_1[0][1] - p_1[0][3]) * (p_1[1][2] + p_1[1][3])
                pr7 = (p_1[0][0] - p_1[0][2]) * (p_1[1][0] + p_1[1][1])
                
                soln = [[(pr4 + pr5 + pr6 - pr2), (pr1 + pr2)],
                        [(pr3 + pr4), (pr1 - pr3 + pr5 - pr7)]]
                
                soln[0][0] = soln[0][0].merge_cols(soln[0][1])
                soln[1][0] = soln[1][0].merge_cols(soln[1][1])             
                soln[0][0] = soln[0][0].merge_rows(soln[1][0])
                
                final = soln[0][0]               
                
            else:
                final = make_matrix([mat_2.rmul(mat_1[i])
                                     for i in range(len(mat_1))])
              
            return (final if len(final) < var_globals.ROW_LENGTH
                    else final.unpad())
        
    
    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code

        if len(mat) != len(self):
            return False

        check = True
    
        for i in range(len(self)):
            if self[i] != mat[i]:
                check = False
                break
    
        return check


class FullMatrix(Matrix):
    '''
    A subclass of Matrix where all rows (vectors) are kept explicitly as a list
    '''
    def __init__(self, vectors, length, ncols):
        '''
        Constructor for a FullVector on data given in the 'lst' argument - 'lst' is the list of elements in the vector
        Uses the base (parent) class attributes data and zero_test
        '''
        super(FullMatrix, self).__init__(vectors, length, ncols)



class SparseMatrix(Matrix):
    '''
    A subclass of Matrix where most rows (vectors) are zero vectors
    The vectors (non-zero) and their corresponding indices are kept in separate lists
    '''
    def __init__(self, vectors, indices, length=0, ncols=0):
        '''
        'length' is the number of rows of the matrix - the number of entries in 'vectors' is just the number of
        non-zero rows
        You can assume that the number of entries in values and indices is the same.
        '''
        super(SparseMatrix, self).__init__(vectors, length, ncols)
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
        
        if isinstance(key, int):
            if key >= len(self):
                return None
            
            if len(self.indices) == 0 or len(self.vectors) == 0:                
                return make_vector([0] * self.ncols, lambda x: x == 0)
            
            idx = bisect_left(self.indices, key)
            
            return (make_vector([0] * self.ncols)               
                    if (idx == len(self.indices) or self.indices[idx] != key)
                        else self.vectors[idx])
            
        else:
            if key[0] >= len(self):
                return None
            
            idx = bisect_left(self.indices, key[0])
            
            return (0 if (idx == len(self.vectors)
                          or self.indices[idx] != key[0])
                    else self.vectors[idx][key[1]]) 
    
if __name__ == '__main__':    
    pass