'''
Created on 16-Nov-2013

@author: raghavan
'''
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD, FullVector

def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
    count=0
    indices, vectors=[],[]
    for vector in vector_list:
        if vector.is_zero()==True:
            count+=1
    if float(count)/len(vector_list)>=DENSITY_THRESHOLD and len(vector_list)>SIZE_THRESHOLD:
        for i in vector_list:
            indices.append(vector_list.index(i))
            vectors.append(i)
        return SparseMatrix(vectors, indices, len(vector_list))
    else:
        return FullMatrix(vector_list)
    

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
        # Your Code
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        # Your Code
        if(isinstance(key,tuple)):
            return self.rows[key[0]][key[1]]
        else:
            return self.rows[key]
            

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if len(self)<=self.MIN_RECURSION_DIM:
            return True
        else:
            return False
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        final_list=[]
        if(len(self)!=len(mat)):
            return None
        else:
            for i in range(0,len(self)):
                final_list.append(self[i]+mat[i])
            return final_list    


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        final_list=[]
        if(len(self)!=len(mat)):
            return None
        else:
            for i in range(0,len(self)):
                final_list.append(self[i]-mat[i])
            return final_list


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        final_list=[]
        length=min(len(self),len(mat))
        for i in range(0,length):
            final_list.append(self[i]+mat[i])
        return final_list



    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        final_list=[]
        length=min(len(self),len(mat))
        for i in range(0,length):
            final_list.append(self[i]-mat[i])
        return final_list


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        a,b,left,right=[],[],[],[]
        for vector_list in self:
            a,b=vector_list.split()
            left.append(a)
            right.append(b)
        return make_matrix(left), make_matrix(right)
        
        
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left, right=self.left_right_split()
        length=len(left)/2
        topleft=left[:length+1]
        topright=right[:length+1]
        bottomleft=left[length+1:]
        bottomright=right[length+1:]
        return topleft, topright, bottomleft, bottomright


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        merged_list=[]
        length=min(len(self),len(mat))
        for i in range (0,length):
            temp=self[i].merge(mat[i])
            merged_list.append(temp)
        matrix=make_matrix(merged_list)
        return matrix    

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        for i in mat:
            self.append(i)
        return self    


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        rmultiplied=[]
        if len(self)!=len(vec):
            return None
        else:
            for i in range (0,len(self)):
                temp=self[i]*vec[i]
                rmultiplied.append(temp)
            for i in rmultiplied:
                rmultiplied += [FullVector(i,lambda x: x==0)]
            for i in rmultiplied:
                j= i*rmultiplied
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
            if(self.is_small()):
                matrix = []
                for pos in range(len(self)):
                    matrix.append(mat.rmul(self[pos]))
                return make_matrix(matrix) 
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
        if len(self)!=len(mat):
            return False
        else:
            for i in range(0,len(self)):
                if(self[i]!=mat[i]):
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
        self.vectors=vectors
        self.indices=indices
        self.length=length


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
        if key in self.indices:
            a=self.indices.index[key]
            return self.vectors[a]
        else:
            return 0

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        merged_vector, merged_indices, lst = self.vectors, self.indices, []
        for i in mat.vectors:
            merged_vector.append(i)
            merged_indices.append(mat.indices[mat.vectors.index(i)])
        for i in range(0, len(self)):
            if i in merged_indices:
                lst.append(merged_vector[merged_indices.index(i)])
            else:
                lst.append(0)
        return make_vector(lst)
        


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        lst1, lst2 = [], []
        for i in range(0, len(self)):
            temp1, temp2 = self.rows[i].split()
            lst1.append(temp1)
            lst2.append(temp2)
        mat1 = make_matrix(lst1[:len(lst1)/2])
        mat2 = make_matrix(lst2[:len(lst2)/2])
        mat3 = make_matrix(lst1[len(lst1)/2:])
        mat4 = make_matrix(lst2[len(lst2)/2:])
        return mat1, mat2, mat3, mat4
    
        
data1 = [ [1,2,3,4],
          [5,6,7,8],
          [9,10,11,12],
          [1,1,1,1] ]
data2 = [ [1,2,3,4],
          [11,21,13,14],
          [1,8,7,6],
          [2,2,2,2] ]
vector_list1 = []
vector_list2 = []
for lst in data1:
    vector_list1.append(make_vector(lst, lambda x : (x == 0)))
for lst in data2:
    vector_list2.append(make_vector(lst, lambda x : (x == 0)))
matrix1 = make_matrix(vector_list1)
matrix2 = make_matrix(vector_list2)
print len(matrix2)
matrixa, matrixb=matrix1.left_right_split()
print matrixa, matrixb
#for i in matrix.vectors:
 #   print i.data