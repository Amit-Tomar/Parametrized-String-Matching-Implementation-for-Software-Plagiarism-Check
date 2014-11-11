'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD
from vector import Vector
zero_test = lambda x : (x == 0)

global l_rows
global l_cols
global pad_length_rows
global pad_length_cols

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    count = 0
    sparse = []
    indices = []
    for indx, elem in enumerate(vector_list):
                
        if( elem.is_zero() ):
            count += 1
        else:
            sparse.append(elem)
            indices.append(indx)
            
       
    if(float(count)/len(vector_list) > DENSITY_THRESHOLD ):
        matrix = SparseMatrix(sparse, indices, len(vector_list))
    else:
        matrix = FullMatrix(vector_list)
   
    return matrix
    # Your Code
    

class Matrix(object):
    '''
    Base Matrix Class - implements basic matrix operations
    '''
    MIN_RECURSION_DIM = 2

    def __init__(self, rows):
        '''
        'rows' is a list of vectors
        Keep this is the row list for the matrix
        '''
        self.rows = rows
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
        if attr == 'nrows' :
            return len(self.rows)
        elif(attr == 'ncols'):
            return len(self.rows[0])
        # Your Code
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        if(isinstance(key, int)):
            return self.rows[key]
        else:
            return self.rows[key[0]][key[1]]
            
        # Your Code
        
    def __setitem__(self, i, val):
        self.rows[i] = val
    
    
    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if(len(self) <= self.MIN_RECURSION_DIM):
            return True
        return False
        # Your Code
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        if(len(self) == len(mat)):
            sums = []
            for indx, val in enumerate(self.rows):
                sums.append(val + mat[indx])
            return make_matrix(sums)
        
        return None
        # Your Code


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        
        if(len(self) == len(mat)):
            diff = []
            for indx, val in enumerate(self):
                diff.append( val - mat[indx])
            return make_matrix(diff)
        
        return None
        # Your Code


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        for i in range(min(len(self),len(mat))):
                self.rows[i] = self.rows[i] + mat[i]
        
        return self
        # Your Code


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        for i in range(min(len(self),len(mat))):
                self.rows[i] = self.rows[i] - mat[i]
        
        return self
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
        for indx, elem in enumerate(self):
            lft, rgth = elem.split()
            left.append(lft)
            right.append(rgth)
            
            
        return make_matrix(left), make_matrix(right)
        
        # Your Code
        
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        topleft = []
        topright = []
        bottomleft = []
        bottomright = []
        
        left, right = self.left_right_split()
        
        for i in range(len(right)):
            
            if(i < len(right)/2):
                topleft.append(left[i])
            else:
                bottomleft.append(left[i])
                
            if(i < len(right)/2):
                topright.append(right[i])
            else:
                bottomright.append(right[i])
        
                          
        return make_matrix(topleft), make_matrix(topright), make_matrix(bottomleft), make_matrix(bottomright)  
        # Your Code


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        for indx, vector in enumerate(self):
            vector.merge(mat[indx])
        # Your Code


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        
        for i in range(len(mat)):
            self.rows.append(mat[i])
            
        
        # Your Code


    def rmul(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        
        if(len(vec) == len(self)):
            prod = [0]*len(vec)
            for i in range(len(vec)):
                
                for j in range(len(vec)):
                    prod[i] += vec[j]*self[j][i]
                                        
            return  make_vector(prod,zero_test)
            
        return None
        # Your Code


    def __mul__(self, mat, flag = [0], flag_first = [0]):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        global l_rows
        global l_cols
        global pad_length_rows
        global pad_length_cols
        
        if(self.ncols == mat.nrows):
            
            if(flag_first[0] == 0):
                l_rows =  len(self)
                l_cols = len(mat[0])
                flag_first[0] = 1
            
            
            if(flag[0] == 0):
                    self.pad()
                    pad_length_rows = len(self)
                    mat.pad()
                    pad_length_cols = mat.ncols
                    flag[0] = 1
            
            if(self.is_small() or mat.is_small()):
                m  = []
                for elem in self.rows:
                    m.append(mat.rmul(elem))
                return FullMatrix(m)
            
            else:
                if(flag[0] == 0):
                    self.pad()
                    mat.pad()
                    flag[0] = 1
                    
                A, B, C, D = self.get_quarters()
                E, F ,G, H = mat.get_quarters()
                P1 = A * (F - H)
                P2 = (A + B) * H
                P3 = (C + D) * E
                P4 = D  * (G - E)
                P5 = (A + D) * (E + H)
                P6 = (B - D) * (G + H)
                P7 = (A - C) * (E + F)             
                                
                PF1 = (P4 + P5 + P6) - P2 
                PF2 = P1 + P2
                PF3 = P3 + P4
                PF4 = (P1 + P5) - (P3 + P7)
                
                PF1.merge_cols(PF2)
                PF3.merge_cols(PF4)
                
                PF1.merge_rows(PF3)
                
                if(pad_length_rows == len(PF1) and pad_length_cols == PF1.ncols ):
                    PF1 = PF1.unpad()
                
                return PF1
                       
        return None       
            
        # Your Code

    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        for indx, elem in enumerate(self):
            if(self[indx] != mat[indx]):
                return False
        
        return True
        # Your Code


    def pad(self):
        '''
        padding to incomplete matrix
        '''
        
        l_rows = len(self)
        l_cols = len(self.rows[0])
        
        i = 1
        while(i<l_rows):
            i *= 2
           
        j = 1
        while(j<l_cols):
            j *= 2
                
        order = max(i,j)
        
        if((order - l_cols ) != 0):
            col = make_vector(([0] * (order - l_cols )), zero_test) 
            cols = []
            for i in range(l_rows):
                cols.append(col)
             
            colms = make_matrix(cols)
            self.merge_cols(colms)
        
        if((order - l_rows) != 0):        
            row = make_vector(([0] * order ),zero_test)
            rws = []
            for i in range((order - l_rows)):
                rws.append(row)
                
            rws1 = make_matrix(rws)
            self.merge_rows(rws1)
        
       
    
    def unpad(self):
        '''
        unpads the padded zeros 
        '''
        
        global l_rows
        global l_cols
        
        refined = []
        for i,elem in enumerate(self.rows):
            row_content = []
            for indx, val in enumerate(elem[:]):
                if(indx < l_cols):
                    row_content.append(val)
            
            if(i < l_rows):
                refined.append(make_vector(row_content,zero_test))
        
        self = FullMatrix(refined)
        
        for vector in self.rows:
            print vector[:]
        return self
                
                    

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
        self.length = length
        self.rows = vectors
        self.indices = indices
        # Your Code


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        return self.length
        # Your Code
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        
        if(isinstance(key,int)):
            if(not key in self.indices):
                return make_vector([],zero_test)
            else:
                return self.rows[key]
            
        elif(key[0] in self.indices):
            return self.vectors[self.indices.index(key[0])][key[1]]
            
        return 0
        
        # Your Code

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        flag = self.length
        for elem in mat:
            flag += 1
            if(not (elem == 0) ):
                self.vectors.append(elem)
                self.indices.append(flag)
            
        # Your Code


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        topleft = []
        topright = []
        bottomleft = []
        bottomright = []
        
        left, right = self.left_right_split()
        
        for i in range(len(left)):
            if(i < len(right)/2):
                topleft.append(right[i])
            else:
                bottomleft.append(right[i])
                
            if(i < len(right)/2):
                topright.append(right[i])
            else:
                bottomright.append(right[i])
                    
                        
        return make_matrix(topleft), make_matrix(topright), \
            make_matrix(bottomleft), make_matrix(bottomright)
                
        # Your Code
        
v1 = make_vector([1,2,3,4,0,0,0,0], zero_test)
v2 = make_vector([5,6,7,8,0,0,0,0], zero_test)
v3 = make_vector([0,0,0,0,0,0,0,0], zero_test)
v4 = make_vector([0,0,0,0,0,0,0,0], zero_test)
v5 = make_vector([0,0,0,0,0,0,0,0], zero_test)
v6 = make_vector([0,0,0,0,0,0,0,0], zero_test)
v7 = make_vector([0,0,0,0,0,0,0,0], zero_test)
v8 = make_vector([0,0,0,0,0,0,0,0], zero_test)
v9 = make_vector([0,0,0,0,0,0,0,0], zero_test)


v11 = make_vector([1,1,1,0,1], zero_test)
v22 = make_vector([1,1,1,1,1], zero_test)
v33 = make_vector([2,2,2,2,1], zero_test)
v44 = make_vector([3,3,3,3,1], zero_test)
#v55 = make_vector([0,1,2,3,1], ZERO_TEST)
mat = make_matrix([v1, v2, v3, v4, v5, v6, v7, v8, v9])
mat1 = make_matrix([v1, v2, v3, v4, v5, v6, v7, v8])
mat = mat*mat1