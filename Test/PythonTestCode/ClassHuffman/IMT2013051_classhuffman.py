'''
Created on 23-Oct-2013

@author: raghavan
'''
# Importing the Heap class from classheap
from classheap import Heap

class Huffman(object):
    '''
    Huffman coding class
    This class does not need an explicit constructor --- the class does not have any attributes to be initialized
    So a constructor method __init__ is not given - python will use a default constructor for such classes
    
    Methods will be the same as the functions in the modhuffman module
    '''
        
    def build_char_table(self,filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        freq_table={}
        f=open(filename,'r')
        s=f.read()
        for x in s:
            i=s.count(x)
            freq_table[x]=i
        return freq_table
    
    def cmp_freq(self,char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        if char_tup1[1]>char_tup2[1]:
            return 1
        elif char_tup1[1]<char_tup2[1]:
            return -1
        else :
            return 0
    
    def pad_to_nbits(self,bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code
        
    
    def build_huffman_tree(self,freq_table, arity_exp):
        '''
        Build the huffman tree for the input textfile and return a stack (maybe along with the character at the root node)
        Algo: (i) Start by making a heap out of freq_table using modheap
        (ii) Pop two elements out of the heap at a time
        (iii) Form a composite character that is the concatenation of the two and the combined frequency of the two
        (iv) Add the new composite character with its frequency to the heap
        (v) Add the two popped elements to a stack - simply append to a list
        Elements of the stack are of the form (element, frequency, parent, additional_code_bit)
        (vi) Repeat the above four steps till the heap has only the root element left
        (vii) Return the stack along with the top root element of the heap
        '''
        stack=[]
        
        heap=Heap(True,arity_exp,self.cmp_freq)
        for x in freq_table:
            heap.add((x,freq_table[x]))
        while(len(heap.data)>1):
            tup1=heap.pop()        
            tup2=heap.pop()
            combine_char=tup1[0]+tup2[0]
            combine_freq=tup1[1]+tup2[1]
            heap.add((combine_char,combine_freq))        
            stack.append((tup1[0],tup1[1],combine_char,'1'))
            stack.append((tup2[0],tup2[1],combine_char,'0'))  
        return stack,heap.data[0]    # Your code
    # Add all the Huffman class methods here


if __name__ == '__main__':
    pass