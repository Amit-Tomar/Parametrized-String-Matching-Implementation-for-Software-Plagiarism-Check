'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, is_long_and_sparse, SIZE_THRESHOLD, DENSITY_THRESHOLD

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
    matrix2 = []
    count = 0
    for i in range(len(vector_list)):
        ls = []
        for j in range(len(vector_list[i])):
            ls.append( vector_list[i][j] )
        if (isinstance(ls, list)):
               ls = make_vector(ls)
        if(ls.is_zero()):
            count += 1
        matrix2.append(ls) 
    
    if float(count) / float(len(vector_list)) >= DENSITY_THRESHOLD:
        indices = []
        val_vectors = []
        for i in range(len(matrix2)):
            if(matrix2[i].is_zero() == False):
                val_vectors.append(matrix2[i])
                indices.append(i)
        mat = SparseMatrix(val_vectors, indices, len(matrix2))
    else:
        mat = FullMatrix(matrix2)
    
    return mat
    

class Matrix(object):
    '''
    Base Matrix Class - implements basic matrix operations
    '''
    MIN_RECURSION_DIM = 5
    matrix = []
    def __init__(self, rows):
        '''
        'rows' is a list of vectors
        Keep this is the row list for the matrix
        '''
        # Your Code
        self.matrix = rows


    def __len__(self):
        '''
        Return the number of rows of the matrix - equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        # Your Code
        count = 0
        for i in self:
            count += 1
        return count


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
        return self.matrix[key]


    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if(len(self) < self.MIN_RECURSION_DIM):
            return True
        return False


    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        new = []
        if(len(mat) != len(self)):
            return None
        for i in range(len(self)):
            ans = (self[i] + mat[i])
            temp2 = []
            for j in range(len(ans)):
                temp2.append(ans[j])
            new.append(make_vector(temp2))
        return Matrix(new)

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        new = []
        if(len(mat) != len(self)):
            return None
        for i in range(len(self)):
            ans = (self[i] - mat[i])
            temp2 = []
            for j in range(len(ans)):
                temp2.append(ans[j])
            new.append(make_vector(temp2))
        return Matrix(new)


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        small = mat
        big = self
        if(len(self) < len(mat)):
            small = self
            big = mat
        for i in range(len(small)):
            for j in range(len(i)):
                self[i][j] += mat[i][j]
        #self =( self[:len(mat)] + mat ) + self[len(mat):]
                    


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        small = mat
        big = self
        if(len(self) < len(mat)):
            small = self
            big = mat
        for i in range(len(small)):
            for j in range(len(i)):
                self[i][j] += mat[i][j]


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        ele = [[],[],[],[]]
        for i in range(len(self)/2):
            ls = []
            for j in range(0, int(float(len(self))/2.0 + 0.5)):
                ls.append(self[i][j])
            ele[0].append( make_vector(ls) )
            ls = []
            for j in range(int(len(self)/2), len(self[i])):
                ls.append(self[i][j])
            ele[1].append( make_vector(ls) )
            ls = []
            for j in range(0, int(float(len(self))/2.0 + 0.5)):
                ls.append(self[len(self)/2 + i][j])
            ele[2].append( make_vector(ls) )
            ls = []
            for j in range(int(len(self)/2), len(self[i])):
                ls.append(self[len(self)/2 + i][j])
            ele[3].append( make_vector(ls) )
            ls = []
            
        #return make_matrix(ele[0]), make_matrix(ele[1]), make_matrix(ele[2]), make_matrix(ele[3])
        return Matrix(ele[0]), Matrix(ele[1]), Matrix(ele[2]), Matrix(ele[3])


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        for i in range(len(self)):
            self[i].merge(mat[i])


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        ls = []
        for i in range(len(self)):
            ls.append(self[i])
        
        for i in range(len(mat)):
            ls.append(mat[i])
        
        return make_matrix(ls)

        
    def form_pad(self):
        org_row_length = len(self[0])
        org_col_length = len(self)
        
        num_row = self.is_valid(len(self[0]))
        num_col = self.is_valid(len(self))
        num = num_row if (num_row > num_col) else num_col
        
        if(num != 0):
            for i in range(len(self)):
                temp_list = []
                for j in range(len(self[i])):
                    temp_list.append(self[i][j])
                
                if not is_long_and_sparse(temp_list):
                    self[i].merge(make_vector([0] * (num - org_row_length)))
                else:
                    self[i].length = self[i].length + (num - org_row_length)
                    
        temp = num - org_col_length
        ls = []
        while(temp > 0):
            ls.append(make_vector([0]*(len(self[0]))))
            temp -= 1
                
        self = self.merge_rows(ls)
        
        return self, num - org_row_length, num - org_col_length
    
    def is_valid(self, number): 
        max = 0
        for i in range(number + 1)[1:]:
            if( 2 ** i ) >= number:
                max = 2 ** i
                break
        return max       

    def un_pad(self, ans, pad2, pad1):
        ans = ans[:-pad2]
        for i in range(len(ans)):
            ls = []
            for j in range(len(ans[i]))[:-pad1]:
                ls.append(ans[i][j])
            ans[i] = ls[:]
        return ans

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code


    def __mul__(self, tmatrix2):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        
        self, pads1_r, pads1_c = self.form_pad()
        tmatrix2, pads2_r, pads2_c = tmatrix2.form_pad()        
        
        if(pads2_c != pads1_r):
            print "ERROR"
            return
        
        ans = self.matrix_mult(self, tmatrix2)    
        
        final = self.un_pad(ans, pads1_c, pads2_r)
        
        final = make_matrix(final)
        
        return  final

    def matrix_mult(self, matrix1, matrix2, count = 0):
        if len(matrix1) <= 2:
            return Matrix( [make_vector([(matrix1[0][0] * matrix2[0][0]) + (matrix1[0][1] * matrix2[1][0]), (matrix1[0][0] * matrix2[0][1]) + (matrix1[0][1] * matrix2[1][1])]), make_vector([(matrix1[1][0] * matrix2[0][0]) + (matrix1[1][1] * matrix2[1][0]), (matrix1[1][0] * matrix2[0][1]) + (matrix1[1][1] * matrix2[1][1])])])
        else: 
            ele = [[],[],[],[],[],[],[],[]]
            
            ele[0], ele[1], ele[2], ele[3] = matrix1.get_quarters()
            
            ele[4], ele[5], ele[6], ele[7] = matrix2.get_quarters()
                
            copy_ele = [0,0,0,0,0,0,0]
            
            copy_ele[1] = make_matrix( self.matrix_mult( (ele[0] + ele[1]), (ele[7]) ) )
            copy_ele[0] = make_matrix( self.matrix_mult( ele[0], (ele[5] - ele[7]) ) )
            
            copy_ele[2] = make_matrix( self.matrix_mult( (ele[2] + ele[3]), (ele[4]) ) )
            copy_ele[3] = make_matrix( self.matrix_mult( (ele[3]), (ele[6] - ele[4]) ) )
            copy_ele[4] = make_matrix( self.matrix_mult( (ele[0] + ele[3]), (ele[7] + ele[4]) ) )
            copy_ele[5] = make_matrix( self.matrix_mult( (ele[1] - ele[3]), (ele[6] + ele[7]) ) )
            copy_ele[6] = make_matrix( self.matrix_mult( (ele[0] - ele[2]), (ele[4] + ele[5]) ) )
            '''
            
            copy_ele[0] = (ele[0]) * (ele[5] - ele[7]) 
            copy_ele[1] = (ele[0] + ele[1]) * (ele[7])
            copy_ele[2] = (ele[2] + ele[3]) * (ele[4]) 
            copy_ele[3] = (ele[3]) * (ele[6] - ele[4]) 
            copy_ele[4] = (ele[0] + ele[3]) * (ele[7] + ele[4])
            copy_ele[5] = (ele[1] - ele[3]) * (ele[6] + ele[7])
            copy_ele[6] = (ele[0] - ele[2]) * (ele[4] + ele[5])'''
            
            c1 = ( ( ( copy_ele[4] + copy_ele[3]) - copy_ele[1] ) + copy_ele[5] )
            c2 = (copy_ele[0] + copy_ele[1])
            c3 = (copy_ele[2] + copy_ele[3])
            c4 = ( ( ( copy_ele[0] + copy_ele[4] ) - copy_ele[2] ) - copy_ele[6])
            
            for i in range(len(c1)):
                c1[i].merge(c2[i])
            for j in range(len(c3)):
                c3[j].merge(c4[j])
            ans = []
            for i in c1:
                ans.append(i)
            
            for i in c3:
                ans.append(i)
            return ans


    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        for i in range(len(self)):
            if( i != mat[i] ):
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
        '''count = 0
        for i in self:
            count += 1'''
        return self.length
    

    def __getitem__(self, key, ):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        # Your Code
        if key in self.indices:
            return self.vectors[self.indices.index(key)]
        elif self.vectors != []:
            return make_vector([0]*len(self.vectors[0]))
        else:
            return make_vector([0]*len(self))
            

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        ls = []
        for i in range(len(self)):
            temp = []
            for j in range(len(self[i])):
                temp.append(self[i][j])
            ls.append(temp)
        
        for i in range(len(mat)):
            temp = []
            for j in range(len(mat[i])):
                temp.append(mat[i][j])
            ls.append(temp)
            
        self.length = len(ls)
        return make_matrix(ls)


    #def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code

if __name__  ==  '__main__':
    pass

    input2 = [[1,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,1,0,0,0,0,0], [0,0,0,0,1,0,0,0,0], [0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,1]]
    
    matrix1 = make_matrix(input2)
    matrix2 = make_matrix(input2)
    
    mat = matrix1 * matrix2
    print mat
    print "\n\nPRINTING MATRIX"
    for i in mat:
        print i
       
    input4 = [[1,0,0,0,0,0,0,0,0], [1,2,3,4,5,6,7,8,9], [0,0,1,0,0,0,0,0,0], [0,0,0,1,0,0,0,0,0], [0,0,0,0,1,0,0,0,0], [0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,1]]
    
    matrix1 = make_matrix(input4)
    matrix2 = make_matrix(input4)
    
    mat = matrix1 * matrix2
    
    print "\nPRINTING MATRIX"
    for i in mat:
        print i.lst

