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
    if(len(vector_list)==0):
        return None
    count =0
    index =[]
    vectors = []
    for i in range(0,len(vector_list)):
        if vector_list[i].is_zero() == True:
            count += 1
        else:
            index+=[i]
            vectors+=[vector_list[i]]
    if(float(count)/len(vector_list) >1 - DENSITY_THRESHOLD):
        matrix = SparseMatrix( vectors, index, len(vector_list),len(vector_list[0]))
    else:
        matrix = FullMatrix(vector_list,len(vector_list[0]))
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

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if(isinstance(key,tuple)):
            row = self.rows[key[0]]
            item = row[key[1]]
            return item
        if(isinstance(key,int)):
            return self.rows[key]
    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if len(self.rows) <= self.MIN_RECURSION_DIM:
            return True
        
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        matk=[]
        if len(mat)!=len(self):
            return None
        for i in range(0,len(self)):
            mat1 = self[i]
            mat2 = mat[i]
            matk += [mat1 + mat2]
        matrix = make_matrix(matk)
        return matrix


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        matk=[]
        if len(mat)!=len(self):
            return None
        for i in range(0,len(self)):
            mat1 = self[i]
            mat2 = mat[i]
            matk += [mat1 - mat2]
        matrix = make_matrix(matk)
        return matrix


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        matk=[]
        min_row_len = min (len(mat),len(self) )
        for i in range(0,min_row_len):
            mat1 = self[i]
            mat2 = mat[i]
            matk += [mat1+mat2]
        matrix = make_matrix(matk)
        return matrix   


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        matk=[]
        min_row_len = min (len(mat),len(self) )
        for i in range(0,min_row_len):
            mat1 = self[i]
            mat2 = mat[i]
            matk += [mat1-mat2]
        matrix = make_matrix(matk)
        return matrix

    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        left_mat = []
        right_mat = []
        for j in range(len(self)):
            i=self[j]
            left_vec, right_vec = i.split()
            left_mat  += [left_vec]
            right_mat += [right_vec]
        left = make_matrix(left_mat)
        right = make_matrix(right_mat)
        return left, right    
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left, right = self.left_right_split() 
        tr = []
        br = []
        bl = []
        tl = []
        s=len(left)/2
        for i in range(0, len(left)/2):
            tl += [left[i]]
        for i in range(len(left)/2 ,len(left)):
            bl += [left[i]]
        for i in range(0, len(right)/2):
            tr += [right[i]]
        for i in range(len(right)/2 ,len(right)):
            br += [right[i]]
        topleft, topright, bottomleft, bottomright = FullMatrix(tl,s) , FullMatrix(tr,s) ,FullMatrix(bl,s) , FullMatrix(br,s)
        return topleft, topright, bottomleft, bottomright
    
    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        for i in range(len(mat)):
            self[i].lst+=mat[i].lst
        self.vec_len+=mat.ncols


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        for i in range(len(mat)):
            self.vectors.append(mat[i])


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
            vecs += [FullVector(i,lambda x: x==0)]
        for i in vecs:
            j = i*vec
            sum.append(j)
        return FullVector(sum , lambda x:x==0)   
    
    def pad(self, add_temp):
        zero_add = [0]*(add_temp - self.ncols)
        zero_vec = make_vector(zero_add,lambda x:x==0)
        zero_mat = [0]*add_temp
        mat_vec = make_vector(zero_mat,lambda x:x==0)
        for i in range(0,len(self)):
            self[i].merge(zero_vec)
        for i in range(add_temp - self.nrows):
            self.vectors.append(mat_vec)
        self.vec_len = add_temp
        self.length = add_temp

    def unpad(self,a,b,at):
        vectors=[]
        for i in range(a):
            vec=[]
            for j in range(b):
                vec+=[self[i][j]]
            vectors+=[FullVector(vec)]
        return make_matrix(vectors)
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
            #for i in range(len(A)):
                #print A[i].lst,B[i].lst,C[i].lst,D[i].lst,E[i].lst,F[i].lst,G[i].lst,H[i].lst
            if(self.is_small()):
                matrix = []
                for pos in range(len(self)):
                    matrix.append(mat.rmul(self[pos]))
                return FullMatrix(matrix,len(self[pos])) 
            '''
            #A, B, C, D = mat.get_quarters()
            #E, F, G, H = self.get_quarters()
            l = [A,B,C,D,E,F,G,H]
            for i in l:
            ''' 
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
        if(len(mat) != len(self)):
            return None
        for i in range(0,len(mat)):
            if not (self[i] == mat[i]):
                return None
        return True


class FullMatrix(Matrix):
    '''
    A subclass of Matrix where all rows (vectors) are kept explicitly as a list
    '''
    def __init__(self, vectors,vec_len ):
        '''
        Constructor for a FullVector on data given in the 'lst' argument - 'lst' is the list of elements in the vector
        Uses the base (parent) class attributes data and zero_test
        '''
        super(FullMatrix, self).__init__(vectors)
        self.vectors = vectors
        self.vec_len=vec_len
    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        # Your Code
        if attr == 'nrows':
            return len(self.vectors)
        if attr == 'ncols':
            if self.rows==[]:
                return 0
            return len(self.vectors[0])
        return None
        
class SparseMatrix(Matrix):
    '''
    A subclass of Matrix where most rows (vectors) are zero vectors
    The vectors (non-zero) and their corresponding indices are kept in separate lists
    '''
    def __init__(self, vectors, indices, length=0,vec_len=0):
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
        self.vec_len = vec_len
        
    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        # Your Code
        if attr == 'nrows':
            return self.length
        if attr == 'ncols':
            if self.rows==[]:
                return 0
            return self.vec_len
        return None   
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
        if(isinstance(key,tuple)):
            if(key[0] in self.indices):
                index = self.indices.index(key[0])
                return self.vectors[index][key[1]]
        if(isinstance(key,int)):
            if(key in self.indices):
                index = self.indices.index(key)
                return self.vectors[index]
            else:
                return make_vector([0]*self.vec_len,lambda x : x==0)

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        j=len(mat)
        for i in range(j):
            if(mat[i].is_zero() == False):
                self.vectors.append(mat[i])
                self.indices+=[self.length]
            self.length+=1
    
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left, right = self.left_right_split() 
        tr = []
        br = []
        bl = []
        tl = []
        s=len(left)/2
        for i in range(0, len(left)/2):
            tl += [left[i]]
        for i in range(len(left)/2 ,len(left)):
            bl += [left[i]]
        for i in range(0, len(right)/2):
            tr += [right[i]]
        for i in range(len(right)/2 ,len(right)):
            br += [right[i]]
        return FullMatrix(tl,s) , FullMatrix(tr,s) ,FullMatrix(bl,s) , FullMatrix(br,s)
    
def temp(a,b):
    x = max(a.nrows,a.ncols,b.nrows,b.ncols)
    k=2
    while k<=x:
        k*=2
    return k

zero_test = lambda x : x==0 
data1 = [ [1,2,1,1,3,4,1,1],
          [1,2,1,1,3,4,1,1],
          [1,2,1,1,3,4,1,1],
          [1,2,1,1,3,4,1,1] ]
data2 = [ [1,1,2,1],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0] ]
vector_list3 = []
vector_list1 = []
vector_list2 = []
for lst in data1:
    vector_list1.append(make_vector(lst, lambda x : (x == 0)))
for lst in data2:
    vector_list2.append(make_vector(lst, lambda x : (x == 0)))
matrix2 = make_matrix(vector_list2)
matrix1 = make_matrix(vector_list1)
print matrix1,matrix2
t= temp(matrix1,matrix2)
m= matrix2*matrix1
print m
for i in range(len(m)):
    print m[i].lst
