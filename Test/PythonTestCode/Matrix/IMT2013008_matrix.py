'''
Created on 16-Nov-2013

@author: raghavan
'''
ROWS = []
COLUMNS = []
A_ROWS = []
A_COLUMNS = []
flag = 0

from bisect import bisect_left
from vector import FullVector, SIZE_THRESHOLD, DENSITY_THRESHOLD
from vector import make_vector
import vector

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code

    if len(ROWS) < 2:
        ROWS.append(len(vector_list))
        COLUMNS.append(len(vector_list[0]))       
        i = 0
        while(1):
            if 2**i >= COLUMNS[-1]:
                break
            i = i + 1
        A_COLUMNS.append(2**i)
        zero = [0]*(2**i - COLUMNS[-1])
        for k in range(len(vector_list)):
            vec = vector_list[k].merge(FullVector(zero))
            vector_list[k] = vec
   
        i = 0
        while(1):
            if 2**i >= ROWS[-1]:
                break
            i = i + 1
        A_ROWS.append(2**i)
        zero = [0]*(len(vector_list[0]))
        for k in range(2**i - ROWS[-1]):
            vector_list.append(FullVector(zero))
            
    '''if len(A_ROWS) == 2 and len(A_COLUMNS) == 2:
        print "LLLLLLLLLLLLLL",A_COLUMNS[1],len(vector_list[0])
        if A_ROWS[0] == len(vector_list) or A_COLUMNS[1] == len(vector_list[0]):
            print "kkkkkkkkkkkkkkkkkkk"
            down = A_ROWS[0] - ROWS[0]
            side = A_COLUMNS[1] - COLUMNS[1]
            vector_list = vector_list[:len(vector_list)-down]

            for i in range(len(vector_list)):
                if vector_list[i].is_zero():
                    vector_list[i] = FullVector([0]*(len(vector_list[i])-side))
                else:
                    vector_list[i] = vector_list[i].Slicing(side)'''
        
                 
    count = 0
    indices = []
    vectors = []
    print vector_list
    for i in range(len(vector_list)):
        
        if vector_list[i].is_zero():
            count += 1
            indices.append(i)
            vectors.append(vector_list[i])
                
    if (count / (len(vector_list)) > DENSITY_THRESHOLD and len(vector_list[0]) > SIZE_THRESHOLD):
        matrix = SparseMatrix(vectors, indices, count)
    else:
        matrix = FullMatrix(vector_list) 
    '''for vec in matrix:
        for elem in vec.components():
            print elem,
        print
    print'''
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

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if isinstance(key, tuple):
            return self.rows[key[0]][key[1]]
        else:
            return self.rows[key] 

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if len(self.rows) <= 5:
            return True
        else:
            return False

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        sum_mat = []
        if len(mat) != len(self):
            return None
        for i in range(len(self.rows)):
            sum_mat.append([])
            for j in range(len(self.rows[0])):
                sum_mat[-1].append(mat[i][j] + self[i][j])
            sum_mat[-1] = make_vector(sum_mat[-1])
        return make_matrix(sum_mat)

    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        sub_mat = []
        if len(mat) != len(self):
            return None
        for i in range(len(self.rows)):
            sub_mat.append([])
            for j in range(len(self.rows[0])):
                sub_mat[-1].append(self[i][j] - mat[i][j])
            sub_mat[-1] = make_vector(sub_mat[-1])
        return make_matrix(sub_mat)

    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code

        if len(mat) > len(self):
            min_len = len(self)
        elif len(mat) < len(self):
            min_len = len(mat)
            
        for i in range(min_len):
            for j in range(len(self.rows[0])):
                self[i][j] += mat[i][j]
        return self

    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        if len(mat) > len(self):
            min_len = len(self)
        elif len(mat) < len(self):
            min_len = len(mat)
            
        for i in range(min_len):
            for j in range(len(self.rows[0])):
                self[i][j] -= mat[i][j]
        return self

    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        vec_left = []
        vec_right = []
        for vec in self.rows:
            left, right = vec.split()
            vec_left.append(left);
            vec_right.append(right)
        
        return make_matrix(vec_left), make_matrix(vec_right)
            
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        mat_left, mat_right = self.left_right_split()
        top_left = mat_left[:len(mat_left)//2]
        bottom_left = mat_left[len(mat_left)//2:]
        top_right = mat_right[:len(mat_right)//2]
        bottom_right = mat_right[len(mat_right)//2:]
        return make_matrix(top_left),make_matrix(top_right),make_matrix(bottom_left),make_matrix(bottom_right), 

    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        merged = []
        for vec in self.rows:
            merged.append(vec)
        for vec in mat.rows:
            merged.append(vec)
        return make_matrix(merged)

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        merged = []
        i=0
        for vec in mat.rows:
            merged.append(self[i].merge(vec))
            i += 1
        return make_matrix(merged)     

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        rmul=[]
        c=0
        excess = len(self.rows) - len(vec)
        excessVec = make_vector([0]*excess)
        vec = vec.merge(excessVec)
        if len(self.rows)!=len(vec):
            return None
        else:
            for i in range(len(vec)):
                c=0
                for j in range(len(vec)):
                    c+=vec[j]*self[j][i] 
                rmul.append(c)
        rmul = rmul[:len(rmul)-excess]
        return make_vector(rmul)
    

    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        prod=[]
        if self.is_small() or mat.is_small():
            for vec in self.rows:
                prod.append(vec * mat)
            return make_matrix(prod)
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

            top_left=p4+p5+p6-p2
            top_right=p1+p2
            bottom_left=p3+p4
            bottom_right=p1-p3+p5-p7
            
            merged_up=top_left.merge_rows(top_right)
            merged_down=bottom_left.merge_rows(bottom_right)
            final=merged_up.merge_cols(merged_down)
 
        if len(final)==A_ROWS[0] or len(final[0])==A_COLUMNS[0] :
            down = A_ROWS[0] - ROWS[0]
            side = A_COLUMNS[1] - COLUMNS[1]
            final = final[:len(final)-down]
            
            temp = []
            product = []
            count = COLUMNS[1]
            print side
            print count

            for i in range(len(final)):
                temp = []
                count = COLUMNS[1]
                for elem in final[i].components():
                    temp.append(elem)
                    count -= 1
                    if count == 0:
                        break
                product.append(make_vector(temp))
            mat_prod = make_matrix(product)
                        
            return mat_prod
        return final

    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if (len(self.rows)!=len(mat)):
            return False
        else:
            for i in range(len(mat)):
                if self.rows[i]!=mat[i]:
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
        return len(self.indices)

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        # Your Code
        
        if isinstance(key, tuple) and key in self.indices:
            return self.rows[key[0],key[1]]
        elif isinstance(key, tuple) and key not in self.indices:
            return 0
        elif key in self.indices:
            return self.rows[key]
        else:
            return make_vector([0]*len(self.rows[0])) 
    
    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        mergedi=[]
        mergedv=[]
        for i in range(self.length):
            if i in self.indices and i in mat.indices:
                mergedv.append(self[i].merge(mat[i]))
                mergedi.append(i)
            elif i in self.indices and i not in mat.indices:
                mergedv.append(self[i].merge(make_vector([0]*len(mat[0]))))
                mergedi.append(i)
            elif i not in self.indices and i in mat.indices:
                mergedv.append(mat[i].merge(make_vector([0]*len(self[0]))))
                mergedi.append(i) 
            
            
        return make_matrix(mergedv,mergedi,self.length)


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left,right=self.left_right_split()
        mid_point = int(self.length//2) 
        for i in range(len(self.indices)):
            if self.indices[i] >= mid_point:
                top_left = make_matrix(left.vectors[:i+1],left.indices[:i+1], mid_point)
                top_right = make_matrix(left.vectors[i+1:],left.indices[i+1:], self.length-mid_point)
                bottom_left = make_matrix(right.vectors[:i+1],right.indices[:i+1], mid_point)
                bottom_right = make_matrix(right.vectors[i+1:],right.indices[i+1:], self.length-mid_point)
        return top_left,top_right,bottom_left,bottom_right
    
    
m1 = [[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[2,2,2,2,2,2,2,2,2,2],[0,0,0,0,0,0,0,0,0,0]]
m2 = [[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0]]

M1 = []
M2 = []
for i in range(len(m1)):
    M1.append(make_vector(m1[i]))
for i in range(len(m2)):
    M2.append(make_vector(m2[i]))
    
mat1 = make_matrix(M1)
mat2 = make_matrix(M2)

mat = mat1*mat2

for vec in mat:
    for elem in vec.components():
        print elem,
    print


    
    