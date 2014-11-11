
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
    list = []
    list_indices = []
    for i in vector_list:
        if(i.is_zero() != True):
            list_indices.append(vector_list.index(i))
            list.append(i)
    density_limit = float(len(list))/len(vector_list)
    if  (density_limit < DENSITY_THRESHOLD) :
        sparse = SparseMatrix(list,list_indices,len(vector_list))
        return sparse
    elif (density_limit == DENSITY_THRESHOLD) :
        sparse = SparseMatrix(list,list_indices,len(vector_list))
        return sparse
    else:
        full = FullMatrix(vector_list)
        return full

    

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
        #Your Code
        if (attr=="nrows"):
            return len(self.rows)
    

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
        if ( len(self.rows) <= self.MIN_RECURSION_DIM):
            return True
        else:
            return False

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        count = 0
        new_list = []
        if(len(self.rows) == len(mat)):
            for item in range(len(self.rows)):
                if(len(self.rows[item]) == len(mat.rows[item])):
                    count = count + 1
            if(count == len(self.rows)):
                for i in range(len(self.rows)):
                    add_vector = self.rows[i].add(self.rows[i],mat[i])
                    new_list.append(add_vector)
            add_matrix = make_matrix(new_list)
            return add_matrix
        elif(len(self.rows)!=len(mat)):
            return None


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        count =0
        new_list = []
        if(len(self.rows) == len(mat)):
            for i in range(len(self.rows)):
                if(len(self.rows[i]) == len(mat.rows[i])):
                    count = count + 1
            if(count == len(self.rows)):
                for i in range(len(self.rows)):
                    sub_vector = self.rows[i].sub(self.rows[i],mat[i])
                    new_list.append(sub_vector)
            sub_matrix = make_matrix(new_list)
            return sub_matrix
        elif(len(self.rows) != len(mat)):
            return None


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        minimum = min(len(self.rows), len(mat))
        for i in range(0,minimum):
            self.rows[i] = self.rows[i] + mat[i]

    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        minimum = min(len(self.rows),len(mat))
        for i in range( 0, minimum ):
            self.rows[i]= self.rows[i] - mat[i]

    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        split_left_matrix = []
        split_right_matrix = []
        for lst_vector in len(self.rows):
            split_left_matrix.append(lst_vector.split(lst_vector)[0])
            split_right_matrix.append(lst_vector.split(lst_vector)[1])
        matrix_left = make_matrix(split_left_matrix)
        matrix_right = make_matrix(split_right_matrix)
        
        return matrix_left,matrix_right
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_splited_part,right_splited_part = self.left_right_split()
        top_left = left_splited_part[:len(self.rows)//2]
        bottom_left = left_splited_part[len(self.rows)//2:]
        bottom_right = right_splited_part[len(self.rows)//2:]
        top_right = right_splited_part[:len(self.rows)//2]
        
        return top_left,top_right,bottom_left,bottom_right
        

    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        merge_matrix = []
        for i in range(len(self.rows)):
            part = []
            for val1 in self.rows[i]:
                part.append(val1)
            for val2 in mat[i]:
                part.append(val2)
        merge_matrix.append(part)

        return self.make_matrix(merge_matrix)

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        merge_matrix = []
        
        for i in range(len(mat)):
            merge_matrix.append(i)
        for i in range(len(self.rows)):
            merge_matrix.append(i)
        
        return self.make_matrix(merge_matrix)

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        multiplied_vector = []
        for i in range(len(self.rows)):
            if(len(self.rows) == len(vec)):
                multiplied_vector.append(self.rows[i] * vec)
            else:
                return None
        return multiplied_vector
                

    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        matrix = []
        
        if (mat.is_small() or self.is_small == True):
            for i in range(len(self.rows)):
                row = []
                for j in range(len(mat[0])):
                    value = 0
                    for k in range(len(mat[0])):
                        value = value + self.rows[i][k]*mat[k][j]
                    row.append(value)
                matrix.append(make_vector((row),zero_test=lambda x : (x == 0)))
            return make_matrix(matrix)
        else:
            A,B,C,D = self.get_quarters()
            E,F,G,H = mat.get_quarters()
            P1 = A * ( F - H )
            P2 = ( A + B ) * H
            P3 = ( C + D ) * E
            P4 = D * ( G - E )
            P5 = ( A + D ) * ( E + H )
            P6 = ( B - D ) * ( G + H )
            P7 = ( A - C ) * ( E + F )          
            
            R1 = P4 + P5 + P6 - P2
            R2 = P1 + P2
            R3 = P3 + P4
            R4  = P1 - P3 + P5 - P7
                
            Q1 = R1.merge_cols(R2)
            Q2 = R3.merge_cols(R4)
            mat = Q1.merge_rows(Q2)
            return mat
                        
            
            
            
    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if(len(self.rows) == len(mat)):
            for i in self.lst:
                if(self.lst[i]!=self.vector[i]):
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
        self.vectors=vectors
        self.indices=indices
        self.length=self.length

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        # Your Code
        return len(self.vectors)
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        # Your Code
        if( isinstance(key, tuple) == True ): 
            return self.vectors[key[0],key[1]]
        else:
            return self.vectors[key]
    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        merge_matrix = []
        for i in range(len(mat)):
            merge_matrix.append(i)
        for i in range(len(self)):
            merge_matrix.append(i)
        
        return merge_matrix

    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_splited_matrix,right_splited_matrix = self.left_right_split()
        top_left = left_splited_matrix[:len(self)//2]
        bottom_left = left_splited_matrix[len(self)//2:]
        bottom_right = right_splited_matrix[len(self)//2:]
        top_right = right_splited_matrix[:len(self)//2]
        
        return top_left,top_right,bottom_left,bottom_right
    