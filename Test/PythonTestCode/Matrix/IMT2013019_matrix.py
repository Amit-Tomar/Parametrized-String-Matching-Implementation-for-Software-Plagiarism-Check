'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD,FullVector

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
    count=0
    value_list=[]
    index_list=[]
    length=len(vector_list)
    for i in range(0,len(vector_list)):
        if(vector_list[i].is_zero()==False):
            value_list.append(vector_list[i])
            index_list.append(vector_list.index(vector_list[i]))
            count+=1
    
    if(length>SIZE_THRESHOLD and float(count)/float(length)>1-DENSITY_THRESHOLD):
        sparsematrix=SparseMatrix(value_list,index_list,len(vector_list))
        return sparsematrix
    else:
        fullmatrix=FullMatrix(vector_list)
        return fullmatrix
        
    

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
        return len(self.rows)
        # Your Code


    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        # Your Code
        if(attr=='nrows'):
            return len(self.rows)
        if(attr=='ncols'):
            return len(self.rows[0])
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if(isinstance(key,int)):
            return self.vectors[key]
        else:
            row = self.vectors[key[0]]
            return row[key[1]]
        

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if(len(self.rows) < self.MIN_RECURSION_DIM):
            return True
        return False
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        matrix_sum=[]
        if(len(self) != len(mat)):
            return None
        for i in range(0,len(self)):
            matrix_sum.append(self[i] + mat[i])
        return make_matrix(matrix_sum)


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        matrix_sum=[]
        if(len(self) != len(mat)):
            return None
        for i in range(0,len(self)):
            matrix_sum.append(self[i] - mat[i])
        return make_matrix(matrix_sum)


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        for i in range(0,min(len(self),len(mat))):
            self[i] = self[i] + mat[i]


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        for i in range(0,min(len(self),len(mat))):
            self[i] = self[i] - mat[i]


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        left_matrix,right_matrix = [], []
        for i in self:
            left_vector,right_vector=i.split()
            left_matrix.append(left_vector)
            right_matrix.append(right_vector)
        return make_matrix(left_matrix),make_matrix(right_matrix)
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_matrix , right_matrix = self.left_right_split()
        
        topleft = []
        topright = []
        bottomleft = []
        bottomright = []
        
        
        mid = len(left_matrix) / 2
        for i in range(0 , mid):
            topleft.append(make_vector((left_matrix[i]) , lambda x : (x == 0)))
        for i in range(mid , len(left_matrix)):
            bottomleft.append(make_vector((left_matrix[i]) , lambda x : (x == 0)))
            
        mid = len(right_matrix) / 2
        for i in range(0 , mid):
            topright.append(make_vector((right_matrix[i]) , lambda x : (x == 0)))
        for i in range(mid , len(left_matrix)):
            bottomright.append(make_vector((right_matrix[i]) , lambda x : (x == 0)))
            
        return make_matrix(topleft) , make_matrix(topright) , make_matrix(bottomleft) , make_matrix(bottomright)
    
    
    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        a = []
        for i in range(0,len(self)):
            for j in mat[i].lst:
                self[i].lst.append(j)


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        for i in mat:
            self.vectors.append(i)
                


    def rmul(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        vectors = []
        vecs = []
        for j in range(0,len(self[0])):
            temp = []
            for i in range(len(self)):
                temp += [self[i].lst[j]]
            vectors += [temp]
        sum = []
        for i in vectors:
            vecs.append( FullVector(i,lambda x: x==0))
        for i in vecs:
            j = i*vec
            sum.append(j)
        return FullVector(sum , lambda x:x==0)   


    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        if(self.ncols == mat.nrows):
            A, B, C, D = self.get_quarters()
            E, F, G, H = mat.get_quarters()
            if(self.is_small()):
                matrix = []
                for pos in range(len(self)):
                    print len(self[pos])
                    matrix.append(mat.rmul(self[pos]))
                return make_matrix(matrix) 
            else:
                a = (A+D)*(E+H)
                b = (C+D)*E
                c = A*(F-H)
                d = (D)*(G-E)
                e = (A+B)*H
                f = (C-A)*(E+F)
                g = (B-D)*(G+H)
                tl = a+d-e+g
                tr = c+e
                bl = b+d
                br = a-b+c+f

                tl=tl.merge_cols(tr)
                bl=bl.merge_cols(br)
                rix=tl.merge_rows(bl)
                return rix
        return None


    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        count=1
        for i in range(0,len(self)):
            if(self[i]==mat[i]):
                continue
            else:
                count=0
        if(count==0):
            return False
        else:
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
        self.vectors=vectors



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
        self.vectors=vectors
        self.indices=indices
        self.length=length


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        # Your Code
        highest=max(self.indices)
        return max(self.length,highest)
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        # Your Code
        if(isinstance(key,int)):
            if(self[key].is_zero()==False):
                index=self.indices.index(key)
                return self.vectors[index]
            else:
                return 0
        else:
            if(self[key[0]].is_zero()==False):
                return self[key[0]].getitem[key[1]]
            else:
                return 0
                

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        a = []
        for i in range(len(self)):
            a.append(self[i])
        for i in range(len(mat)):
            a.append(mat[i])
        merge_mat  = make_matrix(a)
        return merge_mat


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_matrix , right_matrix = self.left_right_split()
        topleft = []
        topright = []
        bottomleft = []
        bottomright = []      
        mid = len(left_matrix) / 2
        for i in range(0 , mid):
            topleft.append(make_vector((left_matrix[i]) , lambda x : (x == 0)))
        for i in range(mid , len(left_matrix)):
            bottomleft.append(make_vector((left_matrix[i]) , lambda x : (x == 0)))
            
        mid = len(right_matrix) / 2
        for i in range(0 , mid):
            topright.append(make_vector((right_matrix[i]) , lambda x : (x == 0)))
        for i in range(mid , len(left_matrix)):
            bottomright.append(make_vector((right_matrix[i]) , lambda x : (x == 0)))
            
        return make_matrix(topleft) , make_matrix(topright) , make_matrix(bottomleft) , make_matrix(bottomright)

