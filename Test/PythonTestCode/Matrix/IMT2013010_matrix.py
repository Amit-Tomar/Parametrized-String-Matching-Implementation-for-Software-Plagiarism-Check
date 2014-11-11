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
    zero_list=[]
    count_zero=0
    for x in range(vector_list):
        count_zero1=0
        for i in range(vector_list[x]):
            if(vector_list[x][i]==0):
                count_zero1+=1
        if(len(vector_list[x])==count_zero1):
            count_zero+=1
            zero_list.append(x)
    if(len(vector_list)>=SIZE_THRESHOLD and (count_zero/len(vector_list))>=DENSITY_THRESHOLD):
        full_matrix_object=FullMatrix(vector_list)
        return full_matrix_object
    else:
        vectors=[]
        indices=[]
        for k in range(vector_list):
            if k not in zero_list:
                vectors.append(vector_list[k])
                indices.append(k)
        sparse_matrix_object=SparseMatrix(vectors,indices,len(vector_list))
        return sparse_matrix_object


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
        self=rows
        self.MIN_RECURSION_DIM=5


    def __len__(self):
        '''
        Return the number of rows of the matrix - equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        return len(self)


    def __getattr__(self, attr):
        '''
        Another special method
        Example - suppose you want to treat the number of rows of the matrix as a property
        the code here would be something like 'if attr == 'nrows' return len(self.rows)'
        The value of 'attr' will be treated as a property of any matrix object
        '''
        
    

    def __getitem__(self, key):
        '''
        This allows accessing the elements of a matrix using a (x,y) tuple
        In fact one could access an (i,j) element of a matrix 'm' of the Matrix class as m[i,j]
        If key is a tuple do the above, else if it is an integer return the key-th row of the matrix
        '''
        return self[key[0]][key[1]]        

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        if(len(self)<=self.MIN_RECURSION_DIM):
            return True
        else:
            return False
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        add_list=[]
        add_index_count=0
        add_list.append([])
        if(len(self)==len(mat.matrix)):
            for x in range(len(self)):
                for y in range(len(self[x])):
                    add_list[add_index_count].append(self[x][y]+mat.matrix[x][y])
                add_index_count+=1
                add_list.append([])
            add_list.pop(-1)
            return add_list
        else:
            return None


    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        sub_list=[]
        sub_index_count=0
        sub_list.append([])
        if(len(self)==len(mat.matrix)):
            for x in range(len(self)):
                for y in range(len(self[x])):
                    sub_list[sub_index_count].append(self[x][y]-mat.matrix[x][y])
                sub_index_count+=1
                sub_list.append([])
            sub_list.pop(-1)
            return sub_list
        else:
            return None


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        i=0
        iadd_matrix=[]
        if(len(mat)==len(self)):
            iadd_matrix=self+mat
            return iadd_matrix
        else:
            larger_matrix_length=max(len(self),len(mat))
            smaller_matrix_length=min(len(self),len(mat))
            sub_list_num=0
            while(i<smaller_matrix_length):
                iadd_matrix.append([])
                for n in range(len(self[0])):
                    iadd_matrix[sub_list_num].append(self[i][n]+mat[i][n])
                sub_list_num+=1
                i+=1
            while(i<larger_matrix_length):
                if(larger_matrix_length==len(mat)):
                    iadd_matrix.append(mat[i])
                else:
                    iadd_matrix.append(self[i])
                i+=1
            return iadd_matrix


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        i=0
        isub_matrix=[]
        if(len(mat)==len(self)):
            isub_matrix=self-mat
            return isub_matrix
        else:
            larger_matrix_length=max(len(self),len(mat))
            smaller_matrix_length=min(len(self),len(mat))
            sub_list_num=0
            while(i<smaller_matrix_length):
                isub_matrix.append([])
                for n in range(len(self[0])):
                    isub_matrix[sub_list_num].append(self[i][n]-mat[i][n])
                sub_list_num+=1
                i+=1
            while(i<larger_matrix_length):
                if(larger_matrix_length==len(mat)):
                    isub_matrix.append(mat[i])
                else:
                    isub_matrix.append(self[i])
                i+=1
            return isub_matrix


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        matrixhalf1=[]
        matrixhalf2=[]
        if(len(self)%2==0):
            x=0
            while(x<(len(self)/2)):
                matrixhalf1.append(self[x])
                x+=1
            while(x<len(self)):
                matrixhalf2.append(self[x])
                x+=1
            return matrixhalf1,matrixhalf2
        else:
            x=0
            while(x<=((self+1)/2)):
                matrixhalf1.append(self[x])
                x+=1
            while(x<len(self)):
                matrixhalf2.append(self[x])
                x+=1
            return matrixhalf1,matrixhalf2


    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        topleft=[]
        topright=[]
        bottomleft=[]
        bottomright=[]
        top_matrix=self.left_right_split()[0]
        bottom_matrix=self.left_right_split()[1]
        i=j=k=m=0
        half_length_matrix=0
        if(len(top_matrix[0])%2==0):
            half_length_matrix=len(top_matrix[0])/2
        else:
            half_length_matrix=(len(top_matrix[0])+1)/2
        while(i<len(top_matrix)):
            topleft.append([])
            for n in range(half_length_matrix):
                topleft[i].append(top_matrix[i][n])
            i+=1
        while(k<len(top_matrix)):
            topright.append([])
            for n in range(len(top_matrix[0])-half_length_matrix):
                topright[k].append(top_matrix[k][n+2])
            k+=1
        while(j<len(bottom_matrix)):
            bottomleft.append([])
            for n in range(half_length_matrix):
                bottomleft[j].append(bottom_matrix[j][n])
            j+=1
            while(m<len(bottom_matrix)):
                bottomright.append([])
                for n in range(len(top_matrix[0])-half_length_matrix):
                    bottomright[m].append(bottom_matrix[m][n+2])
                m+=1
        return ((topleft,topright),(bottomleft,bottomright))


    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        return_matrix=self
        i=0
        while(i<len(self)):
            j=0
            while(j<len(mat.matrix[0])):
                return_matrix[i].append(mat.matrix[i][j])
                j+=1
            i+=1
        return return_matrix


    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        return_matrix=[]
        for n in range(len(self)):
            return_matrix.append(self[n])   
        i=0
        while(i<len(self)):
            return_matrix.append(mat.matrix[i])
            i+=1
        return return_matrix


    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        i=j=0
        return_mul_vector=[]
        while(i<len(vec)):
            return_mul_vector.append(vec[0]*self[0][i])
            i+=1
        l=0
        while(l<len(vec)):
            j=1
            while(j<len(vec)):
                return_mul_vector[l]+=vec[j]*self[j][l]
                j+=1
            l+=1
        return return_mul_vector


    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        Else use recursive Strassen's algorithm
        '''
        


    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        if(mat.list==mat.list):
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
        self.vector=vectors


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
        self.vector_values=vectors
        self.vector_indices=indices
        self.length=length


    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        return self.length
    

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        if key[0] in self.indices:
            return self.vector_values[self.vector_indices.index(key[0])][key[1]]

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        return_values=[]
        return_indices=[]
        mat_values=[]
        mat_indices=[]
        zero_list=[]
        count_zero=0
        for x in range(mat.matrix):
            count_zero1=0
            for i in range(mat.matrix[x]):
                if(mat.matrix[x][i]==0):
                    count_zero1+=1
            if(len(mat.matrix[x])==count_zero1):
                count_zero+=1
                zero_list.append(x)
        for i in range(mat.matrix):
            if i not in zero_list:
                mat_values.append(mat.matrix[i])
                mat_indices.append(x)
        count_zero_mat=0
        for x in mat_indices:
            if x not in self.vector_indices:
                return_indices.append(x)
                return_values.append([])
                for y in range(len(self.vector_values[0])):
                    return_values[count_zero_mat].append(0)
                    return_values[count_zero_mat].append(mat.vector_values[mat.vector_indices.indices(x)][y])
                count_zero_mat+=1
        count_zero_self=0
        for z in self.vector_indices:
            if z not in mat_indices:
                return_indices.append(x)
                return_values.append([])
                for y in range(len(self.vector_values[0])):
                    return_values[count_zero_self].append(self.vector_values[self.vector_indices.indices(x)][y])
                    return_values[count_zero_self].append(0)
                count_zero_self+=1
        count__zero=0
        for z in self.vector_indices:
            if z in mat.vector_indices:
                return_indices.append(x)
                return_values.append([])
                for y in range(len(self.vector_values[0])):
                    return_values[count__zero].append(self.vector_values[self.vector_indices.indices(x)][y])
                    return_values[count__zero].append(mat.vector_values[mat.vector_indices.indices(x)][y])
                count__zero+=1
        return (return_indices, return_values)

    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        top_right_values=[]
        top_right_indices=[]
        top_left_values=[]
        top_left_indices=[]
        bottom_right_values=[]
        bottom_right_indices=[]
        bottom_left_values=[]
        bottom_left_indices=[]
        top_indices=[]
        top_values=[]
        bottom_indices=[]
        bottom_values=[]
        halfindices_top_bottom=0
        halfindices_right_left=0
        if(self.length%2==0):
            halfindices_top_bottom=self.length/2
        else:
            halfindices_top_bottom=(self.length+1)/2
        for i in self.indices:
            if(i<halfindices_top_bottom):
                top_indices.append(i)
                top_values.append(self.vector_values[self.vector_indices.index(i)])
            else:
                bottom_indices.append(i)
                bottom_values.append(self.vector_values[self.vector_indices.index(i)])
        x=0
        if(len(self.vector_values[0])%2==0):
            halfindices_right_left=len(self.vector_values[0])/2 
        else:
            halfindices_right_left=(len(self.vector_indices[0])+1)/2
        count_sub_list=0
        for x in top_indices:
                j=0
                top_left_values.append([])
                while(j< halfindices_right_left):
                    top_left_indices.append(x)
                    top_left_values[count_sub_list].append(top_values[top_indices.index(x)][j])
                    j+=1
                top_right_values.append([])
                while(j<len(self.vector_values[0])):
                    top_right_indices.append(x)
                    top_right_values[count_sub_list-1].append(top_values[top_indices.index(x)][j])
                    j+=1
                    count_sub_list+=1
                count_sub_list+=1
        count_sub_list1=0
        for y in bottom_indices:
            k=0
            bottom_left_values.append([])
            while(k<halfindices_right_left):
                bottom_left_indices.append(y)
                bottom_left_values[count_sub_list1].append(bottom_values[bottom_indices(y)][k])
                k+=1
            bottom_right_values.append([])
            while(k<len(self.vector_values[0])):
                bottom_right_indices.append(y)
                bottom_right_values[count_sub_list1].append(bottom_values[bottom_indices(y)][k])
            count_sub_list1+=1
        return (((top_left_indices,top_left_values),(top_right_indices,top_right_values)),((bottom_left_indices,bottom_left_values),(bottom_right_indices,bottom_right_values)))
