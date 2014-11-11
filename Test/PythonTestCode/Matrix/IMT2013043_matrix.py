'''s
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD,Vector

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Cod
    non_zero = []
    indices = []
    print vector_list
    for obj in vector_list:
        print obj
        if obj.is_zero() == False:
            non_zero.append(obj)
            indices.append(vector_list.index(obj))
    
    fraction = float(len(non_zero)) / len(vector_list)
    if fraction <= DENSITY_THRESHOLD:
        return SparseMatrix(non_zero,indices,len(vector_list))
    else:
        return FullMatrix(non_zero)
        
            
    
    

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
        self.rows = rows
        
        


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
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if isinstance(key,tuple):
            return self.rows[key[0]][key[1]]
        else:
            return self.rows[key]
        

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if len(self.rows) <= self.MIN_RECURSION_DIM:
            return True
        else:
            return False
            
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        temp = []
        if len(self) == len(mat):
            if len(self[0]) == len(mat[0]):
                for i in range(len(self)):
                    temp.append(self[i] + mat[i])
            return make_matrix(temp)
        
        else:
            return None
        
         

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        temp = []
        if len(self) == len(mat):
            if len(self[0]) == len(mat[0]):
                for i in range(len(self)):
                    temp.append(self[i] - mat[i])
            return make_matrix(temp)
        
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
        i = 0
        while i < min(len(self),len(mat)):
            self[i] += mat[i]
            i += 1



    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        i = 0
        while i < min(len(self),len(mat)):
            self[i] -= mat[i]
            i += 1



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
        for i in self:
            temp1,temp2 = i.split(i)
            left.append(temp1)
            right.append(temp2)
        leftMatrix =  make_matrix(left)
        rightMatrix = make_matrix(right)
        
        return leftMatrix,rightMatrix            
        
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        leftMatrix , rightMatrix = self.left_right_split()
        tLeft = []
        tRight = []
        bLeft = []
        bRight = []
        i = 0
        mid = len(leftMatrix)/2
        
        while(i<mid):
            tLeft.append(leftMatrix[i])
            i+=1
        
        while(i<len(leftMatrix)):
            bLeft.append(leftMatrix[i])
            i+=1
        
        i = 0
        mid = len(rightMatrix)/2
        
        while(i<mid):
            tRight.append(rightMatrix[i])
            i+=1
        
        while(i<len(rightMatrix[i])):
            bRight.append(rightMatrix[i])
            i+=1
        topleft = make_vector(tLeft)
        topright = make_vector(tRight)
        bottomleft = make_vector(bLeft)
        bottomright = make_vector(bRight)
        
        return topleft, topright, bottomleft, bottomright
            
                


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        final = []
        for i in range(len(self)):
            final.append(self[i] + mat[i])
        merged = make_matrix(final)
        return merged
            
            

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        final = []
        for i in range(len(self)):
            final.append(self[i])
        for i in range(len(mat)):
            final.append(mat[i])
        merged = make_matrix(final)
        return merged


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        if len(self[0] != len(vec)):
            return None
        vectors = []
        for i in range(len(self[0])):
            temp = []
            for j in range(len(self)):
                temp.append(self[i][j])
            vectors .append(temp)
        Vectors = []
        for i in vectors:
            Vectors += [make_vector(i,lambda x : x == 0)]
        return vec*Vectors
            
            
        
        

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
                    matrix.append(mat.rmul(self[pos]))
                return make_matrix(matrix) 
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
        
        else:
            return None



    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if len(self)!=len(mat):
            return False
        else:
            count = 0
            for i in range(len(self)):
                if self[i] == mat[i]:
                    count += 1
                if count == len(self):
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
        self.length = length
        self.vectors = vectors
        self.indices = indices
        
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
        if isinstance(key,tuple):
            i = key[0]
            j = key[1]
            if i in self.indices:
                index = self.indices.index(i)
                return self.vectors[index][j]
        # needs review       
        else:
            return self.vectors[key[0]]
    
    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        temp = []
        for i in range(len(self)):
            temp.append(self[i])
        for i in range(len(mat)):
            temp.append(mat[i])
        mergeMatrix  = make_matrix(temp)
        return mergeMatrix

    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        # Your Code
        left, right = self.left_right_split() 
        tRight = []
        bRight = []
        bLeft = []
        tLeft = []
        mid = len(left)/2
        for i in range(0, mid):
            tLeft.append(left[i])
        for i in range(mid ,len(left)):
            bLeft.append(left[i])
        mid = len(right)/2
        for i in range(0, mid):
            tRight.append(right[i])
        for i in range(mid ,len(right)):
            bRight.append(right[i])
        topLeft = make_matrix(tLeft)
        topRight = make_matrix(tRight)
        bottomLeft = make_matrix(bLeft)
        bottomRight = make_matrix(bRight)
        return topLeft , topRight , bottomLeft , bottomRight

def temp(a,b):
    x = max(len(a),len(b))
    k = int(x**0.5)
    return 2**(k+1)
    
if __name__ == "__main__":
    
