
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
    non_zero_vector = []
    indices = []
    for ele in range(len(vector_list)):
        if(vector_list[ele].is_zero() != True):
            non_zero_vector.append(vector_list[ele])
            indices.append(ele)
    density = float(len(non_zero_vector))/len(vector_list)
    if(density > DENSITY_THRESHOLD):
        matrix = FullMatrix(vector_list)
        return matrix
    else:
        matrix = SparseMatrix(non_zero_vector , indices , len(vector_list))
        return matrix

class Matrix(object):
    '''
    Base Matrix Class - implements basic matrix operations
    '''
    MIN_RECURSION_DIM = 5

    def __init__(self, rows):
        '''
        'rows' is a list of vectors
        Keep this in the row list for the matrix
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
        if attr == 'nrows' :
            return len(self.rows)
        if attr == 'ncolumns' :
            return len(self.rows[0])
        

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        if( isinstance(key, tuple) == False ): 
            return self.rows[key]
        else:
            return self.rows[key[0]][key[1]]

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if ( len(self) > self.MIN_RECURSION_DIM):
            return False
        else:
            return True
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        '''add_vec = []
        if(len(self) == len(mat)):
            if(len(self[0]) == len(mat[0])):
                for i in range(len(self)):
                    add_vec.append(self[i].add(self[i] , mat[i]))
                add_matrix = make_matrix(add_vec)
                return add_matrix
            else:
                return None'''
        if len(self) != len(mat):
            return None
        else:
            sum_matrix = []
            for item in range(len(self)):
                sum_matrix.append(self[item]+mat[item])
                sum_mat = make_matrix(sum_matrix)
            return sum_mat
        

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        if len(self) != len(mat):
            return None
        else:
            sub_matrix = []
            for item in range(len(self)):
                sub_matrix.append(self[item]-mat[item])
                sub_mat = make_matrix(sub_matrix)
            return sub_mat
        
       


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        minimum_value = min(len(self), len(mat))
        
        for i in range(0 , minimum_value):
            self[i] = self[i] + mat[i]
      
        

        


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        minimum_value = min(len(self), len(mat))
        
        for i in range(0 , minimum_value):
            self[i] = self[i] - mat[i]


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        left_mat = []
        right_mat = []
        for vector in len(self):
            right_mat.append(vector.split(vector))
            left_mat.append(vector.split(vector))
        return left_mat, right_mat
       
        
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        left, right = self.left_right_split()
        topleft = left[:len(self)//2]
        topright = right[:len(self)//2]
        bottomleft = left[len(self)//2:]
        bottomright = right[len(self)//2:]
        
        return make_matrix(topleft) , make_matrix(topright) , make_matrix(bottomleft) , make_matrix(bottomright)
        


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        merge_mat = []
       
        for i in range(len(self)):
            lists = []
            for val1 in self[i]:
                lists.append(val1)
            for val2 in mat[i]:
                lists.append(val2)
            merge_mat.append(lists)
        merge_matrix = make_matrix(merge_mat)
        return merge_matrix


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        merge_mat = []
        
        for i in range(len(self)):
            merge_mat.append(self[i])
        for i in range(len(mat)):
            merge_mat.append(mat[i])
        return make_matrix(merge_mat)


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        rmul = []
        for item in range (len(vec)):
            val = 0
            for var in range (len(self)):
                val = val + vec[item]*self[item][var]
            rmul.append(val)
            
        return make_vector(rmul , self.zero_test)


    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        mul_matrix = []
        
        if (mat.is_small == True or self.is_small() == True ):
            for item in range(len(self)):
                rows = []
                for var in range(len(mat[0])):
                    count = 0
                    for item1 in range(len(mat[0])):
                        count += self[item][item1]*mat[item1][var]
                    rows.append(count)
                mul_matrix.append(make_vector((rows) , zero_test=lambda x : (x == 0)))
            return make_matrix(mul_matrix)
        else:
            qu1 , qu2 , qu3 , qu4 = self.get_quarters()
            mqu1 , mqu2 , mqu3 , mqu4 = mat.get_quarters()
            mul1 = qu1 * (mqu2-mqu4)
            mul2 = ( qu1+qu2) * mqu4
            mul3 = (qu3+qu4) *  mqu1
            mul4 = qu4 * (mqu3- mqu1)
            mul5 = ( qu1+qu4) * ( mqu1+mqu4)
            mul6 = (qu2-qu4) * (mqu3+mqu4)
            mul7 = ( qu1-qu3) * ( mqu1+mqu2)          
            
            row1 = mul4+mul5+mul6-mul2
            row2 = mul1+mul2
            row3 = mul3+mul4
            row4  = mul1-mul3+mul5-mul7
                
            col1 = row1.merge_cols(row2)
            col2 = row3.merge_cols(row4)
            mat = col1.merge_rows(col2)
            return mat


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
                    item = [0]*len(self.rows[0])
                    item = make_vector(item , zero_test = lambda x : (x == 0))
                    return item
        return None

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
        merge_vect = SparseMatrix( merge_vect , merge_ind , self.length + mat.length )
        


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
        return top_left , bottom_left , top_right , bottom_right
    
    if __name__ == '__main__':
        m1 = [make_vector([1,2,3,6] , zero_test=lambda x : (x==0)) , make_vector([3,4,5,6] , zero_test = lambda x : (x ==0)) , make_vector([5,6,7,8] , zero_test = lambda x : (x == 0)) , make_vector([7,8,9,10] , zero_test = lambda x : (x ==0))]
        m2 = [make_vector([1,2,3,6] , zero_test = lambda x : (x == 0)) , make_vector([3,4,5,6] , zero_test = lambda x : (x==0)) , make_vector([5,6,7,8] , zero_test = lambda x : (x == 0)),make_vector([7,8,9,10] , zero_test = lambda x : (x ==0))]
        m1_mat = make_matrix(m1)
        m2_mat = make_matrix(m2)
        
        mat3 = m1_mat + m2_mat
        
        for vec in mat3:
            for e in vec:
                print e,
