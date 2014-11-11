'''
Created on 16-Nov-2013

@author: raghavan
'''
# from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
#     print type(vector_list)
    nonzero_list , vec_indices = [] , []
#     print type(vector_list[0])
#     for object1 in vector_list:
#         print object1
#         if(object1.is_zero()!=True):
#             nonzero_list.append(object1)
#             vec_indices.append(vector_list.index(object1))
    for i in range(0,len(vector_list)):
        if(vector_list[i].is_zero()!=True):
#             print vector_list[i]
            nonzero_list.append(vector_list[i])
            vec_indices.append(i)
#             vec_indices.append(vector_list.index(vector_list[i]))
#     print vec_indices,nonzero_list
    density = float(len(nonzero_list))/len(vector_list)    
    if(density<=DENSITY_THRESHOLD and len(vector_list)>=SIZE_THRESHOLD):
        return SparseMatrix(nonzero_list , vec_indices , len(vector_list))
    else:
        return FullMatrix(vector_list)
    

class Matrix(object):
    '''
    Base Matrix Class - implements basic matrix operations
    '''
    MIN_RECURSION_DIM = 3

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
        if (isinstance(key , tuple)==True):
            return self.rows[key[0]][key[1]]
            
        else:
            return self.rows[key]
        
        
    def __getsublist__(self,key):
        return self.rows[:key]
            

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if (len(self.rows)<=self.MIN_RECURSION_DIM):
            if(len(self[0])<=self.MIN_RECURSION_DIM):
                return True
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        
        
        final_add = []
        if(len(self)==len(mat)):
            for i in range(len(self)):
                addition = []
                for j in range(len(self[0])):
                    addition.append(self[i, j]+mat[i, j])
                final_add.append(make_vector(addition,zero_test = lambda x : (x == 0)))
            return make_matrix(final_add)
        else:
            return None


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        
        
        final_sub = []
        if(len(self)==len(mat)):
            for i in range(len(self)):
                subtraction = []
                for j in range(len(self[0])):
                    subtraction.append(self[i, j] - mat[i, j])
                final_sub.append(make_vector(subtraction,zero_test = lambda x : (x == 0)))
            return make_matrix(final_sub)
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
        min_row = min(len(self) , len(mat))
        for i in range(min_row):
            for j in range(len(self[0])):
                self[i , j] = self[i , j] + mat[i , j]


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        min_row = min(len(self) , len(mat))
        for i in range(min_row):
            for j in range(len(self[0])):
                self[i , j] = self[i , j] - mat[i , j]


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        left_matrix , right_matrix = [] , [] 
        for row in self.rows:
            left , right = row.split()
            left_matrix.append(left)
            right_matrix.append(right)
        return make_matrix(left_matrix) , make_matrix(right_matrix)
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_matrix , right_matrix = self.left_right_split()
        topleft_matrix, topright_matrix, bottomleft_matrix, bottomright_matrix = [] , [] , [] , []
        topleft_matrix = left_matrix.rows[:int(len(left_matrix)/2)]
        bottomleft_matrix = left_matrix.rows[int(len(left_matrix)/2):]
        topright_matrix = right_matrix.rows[:int(len(right_matrix)/2)]
        bottomright_matrix = right_matrix.rows[int(len(right_matrix)/2):]
        return make_matrix(topleft_matrix), make_matrix(topright_matrix), make_matrix(bottomleft_matrix), make_matrix(bottomright_matrix)
    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        matrix = []
        final_matrix = []
        if(len(self)==len(mat)):
            for i in range(len(self)):
                matrix = []
                for j in range(len(self[0])):
                    matrix.append(self[i,j])
                for j in range(len(mat[0])):
                    matrix.append(mat[i,j])
                final_matrix.append(make_vector(matrix,zero_test = lambda x : (x == 0)))
        return make_matrix(final_matrix)


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        for i in range(len(mat)):
            self.rows.append(mat[i])
        return self

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        


    def __mul__(self, mat, row = [0], col = [0] , flag = [0]):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        if(len(self[0])==len(mat)):
            if flag[0] == 0 :
             
                row[0] = len(self)
                col[0] = len(mat[0])
                flag[0] = 1
            
            if(len(self)%2!=0 or len(self[0])%2!=0 or len(mat)%2!=0 or len(mat[0])%2!=0): 
                n = 1
                maximum = max(len(self), len(self[0]), len(mat), len(mat[0]))
                while(1):
                    if(maximum>2**(n-1) and maximum<2**n):
                        break
                    n += 1
                global number
                number = n
                count, lst = len(self)+1, [0]*len(self[0])
                while(count<=2**n):
                    self.rows.append(make_vector((lst),zero_test = lambda x : (x == 0)))
                    count += 1
                count, lst = len(mat), [0]*len(mat[0])
                while(count<2**n):
                    mat.rows.append(make_vector((lst),zero_test = lambda x : (x == 0)))
                    count += 1
                count = len(self[0])
                i = 0
                while(i<2**n):
                    self.rows[i] = self.rows[i].merge(make_vector(([0]*(2**n- count)), zero_test = lambda x : (x == 0)))
                    i += 1
                count, i = len(mat[0]), 0
                while(i<2**n):
                    
                    mat.rows[i] = mat.rows[i].merge(make_vector(([0]*(2**n - count)), zero_test = lambda x : (x == 0)))
                    i += 1
            
            if(self.is_small()==True or mat.is_small()==True):
                sum ,i ,j ,k = 0 ,0 ,0 ,0
                matrix ,final = [] ,[]
                while(i<len(self)):
                    j = 0
                    matrix = []
                    while(j<len(self[0])):
                        k = 0
                        sum = 0
                        while(k<len(self[0])):
                            sum = sum + self[i , k]*mat[k , j]
                            k += 1
                        matrix.append(sum)
                        j += 1
                    matrix = make_vector(matrix, zero_test = lambda x : (x == 0))
                    final.append(matrix)
                    i += 1
                final = make_matrix(final)
                return final
             
            else:
                   
                
                A,B,C,D=self.get_quarters()
                E,F,G,H=mat.get_quarters()
                p1=A*(F-H)
                p2=(A+B)*H
                p3=(C+D)*E
                p4=D*(G-E)
                p5=(A+D)*(E+H)
                p6=(B-D)*(G+H)
                p7=(A-C)*(E+F)
                solution = [p4+p5+p6-p2,p1+p2,p3+p4,p1-p3+p5-p7]
                final1 = solution[0].merge_cols(solution[1])
                final2 = solution[2].merge_cols(solution[3])
                final = final1.merge_rows(final2)
                unpad , final_unpad = [] ,[]
                
                if(len(final)==2**number and len(final[0])==2**number):
                    for i in range(row[0]):
                             
                        unpad = []
                        for j in range(col[0]):
                            unpad.append(final[i][j])
                        final_unpad.append(make_vector(unpad,zero_test = lambda x : (x == 0)))
                    final = make_matrix(final_unpad)
                    return final
                return final 
                  
        else:
            print "not possible"
           
            
            
            

         

    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if(len(self)==len(mat) and len(self[0])==len(mat[0])):
            for i in len(self):
                for j in len(self[0]):
                    if (self[i,j]!=mat[i,j]):
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
        return len(self.values)
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        # Your Code
        if (isinstance(key,tuple)==True):
            return self.values[key[0]][key[1]]
        else:
            return None

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        if(len(self)==len(mat)):
            for i in range(len(self)):
                self.values.append(mat[i])


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_matrix , right_matrix = [] , [] 
        for row in self.values:
            left , right = row.split()
            left_matrix.append(left)
            right_matrix.append(right)
        left_matrix1 , right_matrix1 = make_matrix(left_matrix) , make_matrix(right_matrix)
        topleft_matrix, topright_matrix, bottomleft_matrix, bottomright_matrix = [] , [] , [] , []
        topleft_matrix = left_matrix[:int(len(left_matrix)/2)]
        bottomleft_matrix = left_matrix[int(len(left_matrix)/2):]
        topright_matrix = right_matrix[:int(len(right_matrix)/2)]
        bottomright_matrix = right_matrix[int(len(right_matrix)/2):]
        return make_matrix(topleft_matrix), make_matrix(topright_matrix), make_matrix(bottomleft_matrix), make_matrix(bottomright_matrix)
if __name__ == '__main__':
    pass


