
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
    # Your Code
    non_zero_list = []
    indices = []
    for obj in vector_list:
        if not obj.is_zero() :
            non_zero_list.append(obj)
            indices.append(vector_list.index(obj))
    density = float(len(non_zero_list))/len(vector_list)
    if(density <= DENSITY_THRESHOLD):
        matrix = SparseMatrix(non_zero_list,indices,len(vector_list))
        return matrix
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
        Keep this in the row list for the matrix
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
        if attr == 'nrows':
            return len(self.rows)
        if attr == 'ncols':
            if self.rows==[]:
                return 0
            return len(self.rows[0])
        return None
        

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if( isinstance(key, tuple) == True ): 
            return self.rowss[key[0]][key[1]]
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
        new_vector_list = []
        if(len(self) == len(mat)):
            if(len(mat[0]) == len(self[0])):
                for i in range(len(self)):
                    sum_vector = self[i]+mat[i]
                    new_vector_list.append(sum_vector)
                sum_matrix = make_matrix(new_vector_list)
                return sum_matrix
        else:
            return None
        

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        new_vector_list = []
        if(len(self) == len(mat)):
            if(len(mat[0])== len(self[0])):
                for i in range(len(self)):
                    sub_vector = self[i]-mat[i]
                    new_vector_list.append(sub_vector)
                sub_matrix = make_matrix(new_vector_list)
                return sub_matrix
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
        minlen = min(len(self),len(mat))
        for x in range(minlen):
            self[x] += mat[x]

    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        minlen = min(len(self),len(mat))
        for x in range(minlen):
            self[x] -= mat[x] 


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        left_vector_list = []
        right_vector_list = []
        for x in self.rows:
            left_vector, right_vector = x.split()
            left_vector_list.append(left_vector)
            right_vector_list.append(right_vector)
        left_matrix = make_matrix(left_vector_list)
        right_matrix = make_matrix(right_vector_list)
        return left_matrix, right_matrix
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        j = 0
        left_matrix, right_matrix  = self.left_right_split()
        top_left_vector = []
        bottom_left_vector = []
        top_right_vector = []
        bottom_right_vector = []
        left_top_part = int(math.floor(len(left_matrix)/2.0))
        left_bottom_part = int(math.ceil(len(left_matrix)/2.0))
        for i in range(left_top_part):
            top_left_vector.append(left_matrix[i])
        while(left_bottom_part <> len(left_matrix)):
            bottom_left_vector.append(left_matrix[left_bottom_part])
            left_bottom_part += 1
        topleft = make_matrix(top_left_vector)
        bottomleft = make_matrix(bottom_left_vector)
        
        right_top_part = int(math.floor(len(right_matrix)/2.0))
        right_bottom_part = int(math.ceil(len(right_matrix)/2.0))
        for i in range(right_top_part):
            top_right_vector.append(right_matrix[i])
        while(right_bottom_part <> len(right_matrix)):
            bottom_right_vector.append(right_matrix[right_bottom_part])
            right_bottom_part += 1
        topright = make_matrix(top_right_vector)
        bottomright = make_matrix(bottom_right_vector)
        return topleft, topright, bottomleft, bottomright
    
    
    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        new_list = []
        for i in range(len(self)):
            self[i].merge(mat[i])
            new_list.append(self[i])
        new_matrix = make_matrix(new_list)
        return new_matrix

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        new_list = []
        for i in range(len(self)):
            new_list.append(self[i])
        for i in range(len(mat)):
            new_list.append(mat[i])
        new_matrix = make_matrix(new_list)
        return new_matrix
        '''for vec in mat:
            self.append(vec)
        return self'''

    def rmul(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        new_list = []
        list_of_vectors = []
        prod = []
        if(len(self) <> len(vec)):
            return None
        else:
            lst = []
            for i in range(len(self)):
                for j in range(len(self[0])):
                    lst.append(self[j][i])
                new_list.append(lst)
                lst = []
            for lists in new_list:
                vect = make_vector(lists ,zero_test = lambda x : (x == 0))
                list_of_vectors.append(vect)
            new_matrix = make_matrix(list_of_vectors)
            for i in range(len(new_matrix)):
                prod.append(new_matrix[i]*vec)
            final_vector = make_vector(prod , zero_test = lambda x : (x == 0))
            return final_vector

    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        vec_list = []
        if self.is_small():
            if mat.is_small():
                for i in range(len(self)):
                    vec_list.append(mat.rmul(self[i]))
                new_mat = make_matrix(vec_list)
                return new_mat
        else:
            a, b, c, d = self.get_quarters()
            e, f, g, h = mat.get_quarters()
            part1 = a * (f - h)
            part2  = (a + b) * h
            part3 = (c + d) * e
            part4 = d * (g - e)
            part5 = (a+d)*(e+h)
            part6 = (b-d)*(g+h)
            part7 = (a-c)*(e+f)
            A = part4 + part5 + part6 - part2
            B = part1 + part2
            C = part3 + part4
            D = part1 - part3 + part5 - part7
            mat1 = A.merge_cols(B)
            mat2 = C.merge_cols(D)
            final_matrix = mat1.merge_rows(mat2)
            return final_matrix
            
    
    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        count = 0
        if (len(self) <> len(mat)):
            return False
        else:
            for i in range(len(self)):
                if(self[i] == mat[i]):
                    count += 1
            if( count == len(self) ):
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
        self.vectors = vectors

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
        self.vector_list = vectors
        self.indices = indices
        self.length = length
        new_list = []
        new_list += [0]*len(self.vector_list[0])
        self.zero_vector = make_vector(new_list, zero_test = lambda x : (x == 0))

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
        if ( isinstance(key,tuple) == True):
            if self.key[0] in self.vector_list:
                return self.vector_list[key[0]][key[1]]
            else:
                return 0
        else:
            if key in self.indices:
                return self.vector_list[key]
            else:
                return self.zero_vector
            
    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        new_list =[]
        for i in range(self.length):
            if i in self.indices and  i in mat.indices:
                new_list.append(self[i])
                new_list.append(mat[i])
            elif i in self.indices and i not in mat.indices:
                new_list.append(self[i])
                new_list.append(self.zero_list)
            elif i not in self.indices and i in mat.indices:
                new_list.append(self.zero_list)
                new_list.append(mat[i])
            else:
                new_list.append(self.zero_list)
                new_list.append(self.zero_list)
        new_vector = make_vector(new_list, zero_test = lambda x : (x == 0))
        new_matrix  = make_matrix(new_vector)
        return new_matrix
    
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_matrix, right_matrix  = self.left_right_matrix(self)
        top_left_vector = []
        bottom_left_vector = []
        top_right_vector = []
        bottom_right_vector = []
        left_top_part = int(math.floor(len(left_matrix)/2))
        left_bottom_part = int(math.ceil(len(left_matrix)/2))
        for i in range(left_top_part):
            top_left_vector.append(left_matrix[i])
        for i in range(left_bottom_part):
            bottom_left_vector.append(left_matrix[i])
        topleft = make_matrix(top_left_vector)
        bottomleft = make_matrix(bottom_left_vector)
        
        right_top_part = int(math.floor(len(right_matrix)/2))
        right_bottom_part = int(math.ceil(len(right_matrix)/2))
        for i in range(right_top_part):
            top_right_vector.append(right_matrix[i])
        for i in range(right_bottom_part):
            bottom_right_vector.append(right_matrix[i])
        topright = make_matrix(top_right_vector)
        bottomright = make_matrix(bottom_right_vector)
        
        return topleft, topright, bottomleft, bottomright
    
'''data1 = [[1,2,3,4],
         [5,6,7,8],
         [9,10,11,12],
         [13,14,15,16],
         [1,1,1,1],
         [2,2,2,2],
         [3,2,32,3],
         [7,6,7,6]] 
data2 = [ [1,2,3,4,5,6,7,8],
          [2,3,2,3,2,3,2,3],
          [2,2,2,2,2,2,2,2],
          [6,7,8,9,10,11,12,13]]'''
data1 =[[1,0,0,0],
        [0,2,0,0],
        [0,0,0,0],
        [0,0,0,0]]
data2 = [[0,0,0,1],
         [0,0,3,0],
         [0,0,0,0],
         [0,0,0,0]]
vector_list1 = []
vector_list2 = []
for lst in data1:
    vector_list1.append(make_vector(lst, lambda x : (x == 0)))
for lst in data2:
    vector_list2.append(make_vector(lst, lambda x : (x == 0)))
matrix1 = make_matrix(vector_list1)
matrix2 = make_matrix(vector_list2)
print matrix1
print matrix2

matrix = matrix1 + matrix2
for i in matrix.vectors:
    print i.data
#print matrix[0].data


        