
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
    lst_not_zero = []
    ind_lst = []
    for a in vector_list:
        if(a.is_zero() != True):
            ind_lst.append(vector_list.index(a))
            lst_not_zero.append(a)
    dens_thrsh = float(len(lst_not_zero))/len(vector_list)
    if  (dens_thrsh < DENSITY_THRESHOLD) :
        sprs_mat = SparseMatrix(lst_not_zero,ind_lst,len(vector_list))
        return sprs_mat
    elif (dens_thrsh == DENSITY_THRESHOLD) :
        sprs_mat = SparseMatrix(lst_not_zero,ind_lst,len(vector_list))
        return sprs_mat
    else:
        full_mat = FullMatrix(vector_list)
        return full_mat

    

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
        count =0
        lst_new = []
        if(len(self) == len(mat)):
            for x in range(len(self)):
                if(len(self.rows[x]) == len(mat.rows[x])):
                    count += 1
            if(count == len(self)):
                for x in range(len(self)):
                    add_vect = self[x].add(self[x],mat[x])
                    list_new.append(add_vect)
            addtn_matrix = make_matrix(lst_new)
            return addtn_matrix
        elif(len(self)!=len(mat)):
            return None


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        count =0
        lst_new = []
        if(len(self) == len(mat)):
            for p in range(len(self)):
                if(len(self.rows[p]) == len(mat.rows[p])):
                    count += 1
            if(count == len(self)):
                for p in range(len(self)):
                    sub_vector = self[p].sub(self[p],mat[p])
                    lst_new.append(sub_vector)
            sub_matrix = make_matrix(lst_new)
            return sub_matrix
        elif(len(self)!=len(mat)):
            return None


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        minim = min(len(self), len(mat))
        for y in range(0,minim):
            self[y] = self[y] + mat[y]

    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        minim = min(len(self),len(mat))
        for item in range(0,minim):
            self[item]= self[item] - mat[item]

    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        splt_left = []
        splt_right = []
        for lst_vector in len(self):
            splt_left.append(lst_vector.splt(lst_vector))
            splt_right.append(lst_vector.splt(lst_vector))
        mat_left=make_vector(splt_left)
        mat_right=make_vector(splt_right)
        
        return mat_left,mat_right
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_splt,right_splt = self.left_right_splt()
        top_left = left_splt[:len(self)//2]
        bottom_left = left_splt[len(self)//2:]
        bottom_right = right_splt[len(self)//2:]
        top_right = right_splt[:len(self)//2]
        
        return top_left,top_right,bottom_left,bottom_right
        

    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        mat_merg=[]
        for i in range(len(self)):
            lst=[]
            for val1 in self[i]:
                lst.append(val1)
            for val2 in mat[i]:
                lst.append(val2)
        mat_merg.append(lst)

        return self.make_matrix(mat_merg)

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        mat_merg=[]
        
        for b in range(len(mat)):
            mat_merg.append(b)
        for b in range(len(self)):
            mat_merg.append(b)
        
        return self.make_matrix(mat_merg)

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        mult_vect=[]
        for a in range(len(self)):
            if(len(self)==len(vec)):
                mult_vect.append(self[a] * vec)
            else:
                return None
        return mult_vect
                

    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        mat=[]
        
        if (self.is_small() or mat.is_small == True):
            for a in range(len(self)):
                row=[]
                for b in range(len(mat[0])):
                    c=0
                    for d in range(len(mat[0])):
                        c+=self[a][d]*mat[d][b]
                    row.append(c)
                mat.append(make_vector((row),zero_test=lambda x : (x == 0)))
            return make_matrix(mat)
        else:
            A,B,C,D = self.get_quarters()
            E,F,G,H = mat.get_quarters()
            P1 = A * (F-H)
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
            for x in self.lst:
                if(self.lst[x]!=self.vector[x]):
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
        mat_merg=[]
        
        for s in range(len(mat)):
            mat_merg.append(s)
        for s in range(len(self)):
            mat_merg.append(s)
        
        return mat_merg

    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        left_splt,right_splt = self.left_right_splt()
        top_left = left_splt[:len(self)//2]
        bottom_left = left_splt[len(self)//2:]
        bottom_right = right_splt[len(self)//2:]
        top_right = right_splt[:len(self)//2]
        
        return top_left,top_right,bottom_left,bottom_right
    
    if __name__ == '__main__':
        m1 = [make_vector([1, 2,3,4],zero_test = lambda x : (x == 0)), make_vector([3, 4,5,6],zero_test = lambda x : (x == 0)),make_vector([2, 4,3,1],zero_test = lambda x : (x == 0)),make_vector([5, 4,3,1],zero_test = lambda x : (x == 0))]
    m2 = [make_vector([1,2,5, 6],zero_test =lambda x : (x == 0)), make_vector([2,3,7, 8],zero_test=lambda x : (x == 0)),make_vector([2,4,5, 4],zero_test = lambda x : (x == 0)),make_vector([2, 4,3,1],zero_test = lambda x : (x == 0))]
    m1_mat = make_matrix(m1)
    m2_mat = make_matrix(m2)
        
    mat3 = m1_mat*m2_mat
    for vect in mat3:
        for e in vect:
            print e,
    
