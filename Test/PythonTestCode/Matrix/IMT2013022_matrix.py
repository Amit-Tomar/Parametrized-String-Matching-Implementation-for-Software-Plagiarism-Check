
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
    count = 0
    matrix = []
    vect_matrix = []
    for vect in vector_list:
        vect_matrix.append(make_vector(vect, zero_test = lambda x : (x == 0)))
    count = 0
    if len(vect_matrix) > 2:
        for vect in vect_matrix:
            
            if vect.is_zero():
                count += 1
        if count/len(vect_matrix) <= DENSITY_THRESHOLD:
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
        if (attr=="nrows"):
            return len(self.rows)
        # Your Code
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if( isinstance(key, tuple) == True ): 
            return self.rows[key[0],key[1]]
        else:
            return self.rows[key]

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if ( len(self) <= self.MIN_RECURSION_DIM):
            return True
        else:
            return False

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        '''count =0
        
        list_new = []
        if(len(self) == len(mat)):
            for item in range(len(self)):
                if(len(self.rows[item]) == len(mat.rows[item])):
                    count += 1
                if(count == len(self)):
                    for item in range (len(self)):
                        vect = 0
                        vect = vect + (self[item]+mat[item])
                        list_new.append(vect)
                    return make_vector(list_new,self.zero_test)
        elif(len(self)!=len(mat)):
            return None'''
        
        if len(self) == len(mat):
            sum_matrix = []
            for item in range(len(self)):
                sum_matrix.append(self[item]+mat[item])
                sum_mat = make_matrix(sum_matrix)
            return sum_mat
        else:
            return None


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        '''count =0
        list_new = []
        if(len(self) == len(mat)):
            for item in range(len(self)):
                if(len(self.rows[item]) == len(mat.rows[item])):
                    count += 1
            if(count == len(self)):
                for item in range(len(self)):
                    sub_vector = self[item].sub(self[item],mat[item])
                    list_new.append(sub_vector)
            sub_matrix = make_matrix(list_new)
            return sub_matrix
        elif(len(self)!=len(mat)):
            return None'''
        if len(self) != len(mat):
            return None
        else:
            sum_matrix = []
            for i in range(len(self)):
                sum_matrix.append(self[i]-mat[i])
                sum_mat = make_matrix(sum_matrix)
            return sum_mat


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        minimum = min(len(self), len(mat))
        for item in range(0,minimum):
            self[item] = self[item] + mat[item]

    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        minimum = min(len(self),len(mat))
        for item in range(0,minimum):
            self[item]= self[item] - mat[item]

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
        
        return make_matrix(left), make_matrix(right)
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_split,right_split = self.left_right_split()
        top_left = left_split[:len(self)//2]
        bottom_left = left_split[len(self)//2:]
        bottom_right = right_split[len(self)//2:]
        top_right = right_split[:len(self)//2]
        
        return make_matrix(top_left),make_matrix(top_right),make_matrix(bottom_left),make_matrix(bottom_right)
        

    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        matrix_merged=[]
        for i in range(len(self)):
            lst=[]
            for val1 in self[i]:
                lst.append(val1)
            for val2 in mat[i]:
                lst.append(val2)
        matrix_merged.append(lst)

        return self.make_matrix(matrix_merged)

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        matrix_merged=[]
        
        for item in range(len(mat)):
            matrix_merged.append(item)
        for item in range(len(self)):
            matrix_merged.append(item)
        
        return self.make_matrix(matrix_merged)

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        mult_vector=[]
        for item in range(len(self)):
            if(len(self)==len(vec)):
                mult_vector.append(self[item] * vec)
            else:
                return None
        return mult_vector
                

    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        matrix=[]
        
        if (self.is_small() or mat.is_small == True):
            for i in range(len(self)):
                row=[]
                for j in range(len(mat[0])):
                    c=0
                    for k in range(len(mat[0])):
                        c+=self[i][k]*mat[k][j]
                    row.append(c)
                matrix.append(make_vector((row),zero_test=lambda x : (x == 0)))
            return make_matrix(matrix)
        else:
            A,B,C,D = self.get_quarters()
            E,F,G,H = mat.get_quarters()
            
            
            P1 = A * self.sub(F,H)
            P2 = (A+B) * H
            P3 = (C+D) * E
            P4 = D * (G-E)
            P5 = (A+D) * (E+H)
            P6 = (B-D) * (G+H)
            P7 = (A-C) * (E+F)          
            
            R1 = P4+P5+P6-P2
            R2 = P1+P2
            R3 = P3+P4
            R4  = P1-P3+P5-P7
                
            Q1 = R1.merge_cols(R2)
            Q2 = R3.merge_cols(R4)
            mat = Q1.merge_rows(Q2)
            return mat
                        
            
            
            
    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if(len(self)==len(mat)):
            for item in self.lst:
                if(self.lst[item]!=self.vector[item]):
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
        # Your Code
        self.indices=indices
        self.length=self.length

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
        # Your Code
    
        vect_merged = []
        index_merged = []
        
        for item in range(len(mat)):
            vect_merged.append(mat[item])
            index_merged.append(len(self)+mat.indices[item])
            
        for item in range(len(self)):
            vect_merged.append(self[item])
            index_merged.append(self.indices[item])
    
        
        merge_vect = SparseMatrix(vect_merged, index_merged , self.length + mat.length )

    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_split,right_split = self.left_right_split()
        top_left = left_split[:len(self)//2]
        bottom_left = left_split[len(self)//2:]
        bottom_right = right_split[len(self)//2:]
        top_right = right_split[:len(self)//2]
        
        return top_left,top_right,bottom_left,bottom_right
        
    
if __name__ == '__main__':
    
    m1 = [make_vector([1,2,1,2,1,3,1,1],zero_test = lambda x : (x == 0)), make_vector([1,1,3,1,4,1,5,1],zero_test = lambda x : (x == 0)),make_vector([1,1,5,1,0,1,2,1],zero_test = lambda x : (x == 0)),make_vector([1,4,1,3,1,1,1,2],zero_test = lambda x : (x == 0)), make_vector([1,3,1,1,8,1,1,7],zero_test = lambda x : (x == 0)),make_vector([ 1,3,1,6,1,2,1,1],zero_test = lambda x : (x == 0))]
    m2 = [make_vector([1,7,1,2,1,3,1,1],zero_test = lambda x : (x == 0)), make_vector([1,1,9,1,4,1,8,1],zero_test = lambda x : (x == 0)),make_vector([8,1,5,1,0,1,2,1],zero_test = lambda x : (x == 0)),make_vector([1,9,1,3,1,1,7,2],zero_test = lambda x : (x == 0)), make_vector([1,3,1,1,9,1,1,7],zero_test = lambda x : (x == 0)),make_vector([ 1,3,1,6,1,3,1,1],zero_test = lambda x : (x == 0))]
    #m1 = [[1,2],[3,4]]
    #m2 = [[5,6],[7,8]]
    m1_mat = make_matrix(m1)
    m2_mat = make_matrix(m2)
        
    mat3 = m1_mat * m2_mat
    for vec in mat3:
        for e in vec:
            print e,
    