
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
    non_zero_list = []
    list_indices = []
    for item in vector_list:
        if(item.is_zero() != True):
            list_indices.append(vector_list.index(item))
            non_zero_list.append(item)
    den_thresh= float(len(non_zero_list))/len(vector_list)
    if  (den_thresh < DENSITY_THRESHOLD) :
        sparse_mat = SparseMatrix(non_zero_list,list_indices,len(vector_list))
        return sparse_mat
    elif (den_thresh == DENSITY_THRESHOLD) :
        sparse_mat = SparseMatrix(non_zero_list,list_indices,len(vector_list))
        return sparse_mat
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
        if( isinstance(key, tuple) == False ):
            return self.rows[key] 
        else:
            return self.rows[key[0],key[1]]

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if ( len(self) > self.MIN_RECURSION_DIM):
            return False
        else:
            return True

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        number=0
        new_list = []
        if(len(self)!=len(mat)):
            return None
        elif(len(self) == len(mat)):
            for i in range(len(self)):
                if(len(self.rows[i]) == len(mat.rows[i])):
                    number += 1
            if(number == len(self)):
                for j in range(len(self)):
                    add_vector = self[j].add(self[j],mat[j])
                    new_list.append(add_vector)
            matrix_add = make_matrix(new_list)
            return matrix_add
        


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        number =0
        new_list= []
        if(len(self)!=len(mat)):
            return None
        elif(len(self) == len(mat)):
            for i in range(len(self)):
                if(len(self.rows[i]) == len(mat.rows[i])):
                    number += 1
            if(number == len(self)):
                for j in range(len(self)):
                    sub_vector = self[j].sub(self[j],mat[j])
                    new_list.append(sub_vector)
            matrix_diff = make_matrix(new_list)
            return matrix_diff
        


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        min_add = []
        for i in range(min(len(self),len(mat))):
            min_add.append(self[i] + mat[i])
        if len(mat) < len(self):
            for i in range(len(mat)+1,len(self)):
                min_add.append(self[i])
        elif len(self) < len(mat):
            for i in range(len(self)+1,len(mat)):
                min_add.append(mat[i])
        return make_vector(min_add, self.zero_test)

    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        min_sub = []
        for i in range(min(len(self),len(mat))):
            min_sub.append(self[i] - mat[i])
        if len(mat) < len(self):
            for i in range(len(mat)+1,len(self)):
                min_sub.append(self.data[i])
        elif len(self) < len(mat):
            for i in range(len(self)+1,len(mat)):
                min_sub.append(mat[i])
        return make_vector(min_sub, self.zero_test)


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        split_left = []
        split_right = []
        for lst_vector in len(self):
            split_left.append(lst_vector.split(lst_vector))
            split_right.append(lst_vector.split(lst_vector))
        matrix_left=make_vector(split_left)
        matrix_right=make_vector(split_right)
        
        return matrix_left,matrix_right
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        l_spl,r_spl = self.l_r_spl()
        
        t_l_spl = l_spl[:len(self)//2]
        t_r_spl = r_spl[:len(self)//2]
        b_l_spl = l_spl[len(self)//2:]
        b_r_spl = r_spl[len(self)//2:]
        
        return t_l_spl,t_r_spl,b_l_spl,b_r_spl
        

    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        m_mer=[]
        for i in range(len(self)):
            bracket=[]
            for val1 in mat[i]:
                bracket.append(val1)
            for val2 in self[i]:
                bracket.append(val2)
            
        m_mer.append(bracket)

        return self.make_matrix(m_mer)

    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        m_mer=[]
        
        for i in range(len(self)):
            m_mer.append(i)
        for j in range(len(mat)):
            m_mer.append(j)
        
        return self.make_matrix(m_mer)

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        mul_vec=[]
        for i in range(len(self)):
            if(len(self)!=len(vec)):
                return None
            else:
                mul_vec.append(self[i] * vec)
            
        return mul_vec
                

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
            top_left,top_right,top_up,top_bottom = self.get_quarters()
            tip_left,tip_right,tip_up,tip_bottom = mat.get_quarters()
            element1 = top_left * (tip_right-tip_bottom)
            element2 = (top_left+top_right) * tip_bottom
            element3 = (top_up+top_bottom) * tip_left
            element4 = top_bottom * (tip_up-tip_left)
            element5 = (top_left+top_bottom) * (tip_left+tip_bottom)
            element6 = (top_right-top_bottom) * (tip_up+tip_bottom)
            element7 = (top_left-top_up) * (tip_left+tip_right)          
            
            token1 = element4+element5+element6-element2
            token2 = element1+element2
            token3 = element3+element4
            token4  = element1-element3+element5-element7
                
            count1 = token1.merge_cols(token2)
            count2 = token3.merge_cols(token4)
            matrix = count1.merge_rows(count2)
            return matrix
                        
            
            
            
    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if(len(self)==len(mat)):
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
        mat_mer=[]
        
        for i in range(len(mat)):
            mat_mer.append(i)
        for j in range(len(self)):
            mat_mer.append(j)
        
        return mat_mer

    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        l_spl,r_spl = self.l_r_spl()
        
        t_l_spl = l_spl[:len(self)//2]
        t_r_spl = r_spl[:len(self)//2]
        b_l_spl = l_spl[len(self)//2:]
        b_r_spl = r_spl[len(self)//2:]
        
        return t_l_spl,t_r_spl,b_l_spl,b_r_spl
        
    
    if __name__ == '__main__':
        matrix1 = [make_vector([1,2,3,4],zero_test = lambda x : (x == 0)), make_vector([5,2,6,7],zero_test = lambda x : (x == 0)),make_vector([9, 7,3,8],zero_test = lambda x : (x == 0)),make_vector([6, 5,3,1],zero_test = lambda x : (x == 0))]
    matrix2 = [make_vector([7,5,9,6],zero_test =lambda x : (x == 0)), make_vector([2,8,7,9],zero_test=lambda x : (x == 0)),make_vector([1,3,5,6],zero_test = lambda x : (x == 0)),make_vector([2,5,3,9],zero_test = lambda x : (x == 0))]
    matrix1_mat = make_matrix(matrix1)
    matrix2_mat = make_matrix(matrix2)
        
    matrix3 = matrix1_mat*matrix2_mat
    for vector in matrix3:
        for k in vector:
            print k,
   