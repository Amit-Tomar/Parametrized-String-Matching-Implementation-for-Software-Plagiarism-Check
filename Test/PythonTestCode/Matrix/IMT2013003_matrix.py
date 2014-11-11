'''
Created on 16-Nov-2013

@author: raghavan
'''
zero_test = lambda x :(x==0)
from bisect import bisect_left
from vector import make_vector, SIZE_THRESHOLD, DENSITY_THRESHOLD,is_long_and_sparse,Vector


def make_matrix(vector_list):
    '''
    Make a matrix out of a list of vectors 'vector_list'
    Just like make_vector in the vector module, this decides whether to instantiate the FullMatrix or SparseMatrix class
    by using the is_zero method of the Vector class
    '''
    # Your Code
    worth=0
    total=0
    for a in vector_list:
        total+=1
        if(is_long_and_sparse(a,zero_test)==True):
            worth+=1
            
            
    if(worth/total>=1-DENSITY_THRESHOLD):
        Mat_obj=FullMatrix(vector_list)
    else:
        Mat_obj=SparseMatrix(vector_list)
    return Mat_obj
                    


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
        self.row=rows
        self.min=5
        


    def __len__(self):
        '''
        Return the number of rows of the matrix - equivalent to len(mat) where mat is an instance of the Matrix class
        '''
        # Your Code
        return len(self.row)
        
        

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
        if (type(key)==tuple):
            return self.row[key[0]][key[1]]
        else:
            return self.row[key]
        

    def is_small(self):
        '''
        Small enough that recursive operations do not make sense anymore - direct arithmetic is done on matrices
        that are small (is_small() returns True)
        '''
        # Your Code
        if len(self.row<5 ):
            return True
        else:
            return False
    

    def __add__(self, mat):
        '''
        Return the sum of this matrix with 'mat' - (allows use of + operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        add_mat=[]
        sublist=[]
        temp=0
        ref=0
        if(len(mat)!=len(self.row)):
            return None
        else:
            while(temp<len(self.row)):
                while(ref<len(self.row[0])):
                    sublist.append(mat[temp][ref]+self.row[temp][ref])
                    ref+=1
                    if(ref==len(self.row)):
                        add_mat.append(sublist)
                        sublist=[]
                temp+=1        
                ref=0
                
    def __sub__(self, mat):
        '''
        Return the difference between this matrix and 'mat' - (allows use of - operator between matrices)
        Return None if the number of rows do not match
        '''
        # Your Code
        sub_mat=[]
        sublist=[]
        temp=0
        ref=0
        if(len(mat)!=len(self.row)):
            return None
        else:
            while(temp<len(self.row)):
                while(ref<len(self.row[0])):
                    sublist.append(mat[temp][ref]-self.row[temp][ref])
                    ref+=1
                    if(ref==len(self.row)):
                        sub_mat.append(sublist)
                        sublist=[]
                temp+=1        
                ref=0


    def __iadd__(self, mat):
        '''
        Implements the += operator with another matrix 'mat'
        Assumes that the elements of the matrices have a + operator defined between them (if they are not numbers)
        Add corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        least=min(len(mat),len(self.row))
        iadd_mat=[]
        sublist=[]
        temp=0
        ref=0
        if(len(mat)!=len(self.row)):
            return None
        else:
            while(temp<least):
                while(ref<len(self.row[0])):
                    sublist.append(mat[temp][ref]+self.row[temp][ref])
                    ref+=1
                    if(ref==len(self.row)):
                        iadd_mat.append(sublist)
                        sublist=[]
                temp+=1        
                ref=0


    def __isub__(self, mat):
        '''
        Implements the -= operator with another matrix 'mat'
        Assumes that the elements of the matrices have a - operator defined between them (if they are not numbers)
        Subtract corresponding elements upto the min of the number of rows in each (in case the matrices
        have different numbers of rows)
        '''
        # Your Code
        least=min(len(mat),len(self.row))
        isub_mat=[]
        sublist=[]
        temp=0
        ref=0
        if(len(mat)!=len(self.row)):
            return None
        else:
            while(temp<least):
                while(ref<len(self.row[0])):
                    sublist.append(mat[temp][ref]-self.row[temp][ref])
                    ref+=1
                    if(ref==len(self.row)):
                        isub_mat.append(sublist)
                        sublist=[]
                temp+=1        
                ref=0


    def left_right_split(self):
        '''
        Split the matrix into two halves - left and right - and return the two matrices
        Split each row (use the split method of Vector) and put them together into the
        left and right matrices
        Use the make_matrix method for forming the new matrices
        '''
        # Your Code
        ref=0
        mat_left=[]
        mat_right=[]
        
        var=len(self.row)
        while(ref<var):
            obj=Vector(self.row[ref],zero_test)
            split=obj.split()
            mat_left.append(make_matrix(split[0]))
            mat_right.append(make_matrix(split[1]))
            ref+=1
        return mat_left,mat_right
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        ref=0
        temp=0
        topleft=[]
        topright=[]
        bottomleft=[] 
        bottomright=[]
        left=self.left_right_split()[0]
        right=self.left_right_split()[1] 
        len_left=len(left)
        len_right=len(right)
        while(ref<len_left/2):
            topleft.append(left[ref])
            ref+=1
        while(ref<len_left and ref>=len_left/2):
            bottomleft.append(left[ref])
            ref+=1
        while(temp<len_right/2):
            topright.append(right[temp])
            temp+=1
        while(temp<len_right and temp>=len_right/2):
            bottomright.append(right[temp])
            temp+=1
        
        return topleft, topright, bottomleft, bottomright
        
                
        
    def merge_cols(self, mat):
        '''
        Return the matrix whose rows are rows of this merged with the corresponding rows of mat (columnwise merge)
        '''
        # Your Code
        merge=[]
        sublist=[]
        ref=0
        temp=0
        temp1=0
        while(ref<len(self.row)):
            while(temp<len(self.row[0])):
                sublist.append(self.row[ref][temp])
                temp+=1
        
            while(temp1<len(mat[0])):
                sublist.append(mat[ref][temp1])
                temp1+=1
            
            merge.append(sublist)
            sublist=[]
            ref+=1    
            temp1=0
            temp=0
        return merge
    def merge_rows(self, mat):
        '''
        Return the matrix with rows of mat appended to the rows of this matrix
        '''
        # Your Code
        merge=[]
        sublist=[]
        ref=0
        temp=0
        temp1=0
        while(ref<len(self.row[0])):
            while(temp<len(self.row)):
                sublist.append(self.row[temp][ref])
                temp+=1
            
           
            
        
            while(temp1<len(mat)):
                sublist.append(mat[temp1][ref])
                temp1+=1
            
            merge.append(sublist)
            sublist=[]
            ref+=1    
            temp1=0
            temp=0
        return merge

    def __rmul__(self, vec):
        '''
        Returns a vector that is the product of 'vec' (taken as a row vector) and this matrix using the * operator
        If the two are incompatible return None
        Return vec*self
        '''
        # Your Code
        sum_l=0
        ref=0
        temp=0
        mult=[]
        sublist=[]
        sx=0
        adi=0
        ok=[]
        fine=0
        k=0
        lis=[]
        if(len(vec[0])!=len(self.row)):
            print None
        else:
            while(ref<len(vec)):
                while(sx<len(self.row)):
                    while(temp<len(vec[0])):
                        sublist.append(vec[ref][temp]*self.row[temp][sx])
                    
                        temp+=1
                    while(adi<len(sublist)):
                        sum_l+=sublist[adi]
                        adi+=1
                      
                    
                    sx+=1
                    temp=0
                    ok.append(sum_l)
                    sum_l=0
                    sublist=[]
                    adi=0
                
                ref+=1
                sx=0
            while(k<len(ok)):
                while(fine<len(self.row[0])):
                    lis.append(ok[k])
                    k+=1
                    fine+=1
                mult.append(lis)
                lis=[]
                fine=0
            return make_matrix(mult)

    def __mul__(self, mat):
        '''
        Multiplication of two matrices using Strassen's algorithm
        If either this matrix or mat is a 'small' matrix then do regular multiplication
        topleft, topright, bottomleft, bottomright
        Else use recursive Strassen's algorithm
        '''
        # Your Code
        obj=Matrix(mat)
        sum_l=0
        ref=0
        temp=0
        mult=[]
        sublist=[]
        sx=0
        adi=0
        ok=[]
        fine=0
        k=0
        lis=[]
        if (obj.is_small()==True):
           
            if(len(mat[0])!=len(self.row)):
                print None
            else:
                while(ref<len(mat)):
                    while(sx<len(self.row)):
                        while(temp<len(mat[0])):
                            sublist.append(mat[ref][temp]*self.row[temp][sx])
                    
                            temp+=1
                        while(adi<len(sublist)):
                            sum_l+=sublist[adi]
                            adi+=1
                      
                        sx+=1
                        temp=0
                        ok.append(sum_l)
                        sum_l=0
                        sublist=[]
                        adi=0
                
                    ref+=1
                    sx=0
                while(k<len(ok)):
                    while(fine<len(self.row[0])):
                        lis.append(ok[k])
                        k+=1
                        fine+=1
                    mult.append(lis)
                    lis=[]
                    fine=0
                return make_matrix(mult)
        else:
            quarter_mat=obj.get_quarters
            quarter_self= self.get_quarters()

    def __eq__(self, mat):
        '''
        Check if this matrix is identical to mat - allows use of operator == to compare matrices
        '''
        # Your Code
        if(mat==self.row):
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
        # Your Code
        self.lenh=length
        self.vec=vectors
        self.inds=indices
        super(SparseMatrix, self).__init__(vectors)
        
        

    def __len__(self):
        '''
        Overriding the default __len__ method with behavior specific to sparse Matrices
        '''
        # Your Code
        return self.lenh

    def __getitem__(self, key):
        '''
        Overriding the default __getitem__ method with behavior specific to sparse matrices
        '''
        # Your Code
        if key in self.inds:
            return self.lenh[self.inds.index(key)]

    def merge_rows(self, mat):
        '''
        Overriding the merge rows method of the parent Matrix class
        '''
        # Your Code
        obj=Matrix(self.vec)
        merge=obj.merge_rows(mat)
        return merge
    def get_quarters(self):
        '''
        Get all 4 quarters of the matrix - get the left-right split
        Then split each part into top and bottom
        Return the 4 parts - topleft, topright, bottomleft, bottomright - in that order
        '''
        # Your Code
        obj=Matrix(self.vec)
        quarters= obj.get_quarters()
        return quarters
        