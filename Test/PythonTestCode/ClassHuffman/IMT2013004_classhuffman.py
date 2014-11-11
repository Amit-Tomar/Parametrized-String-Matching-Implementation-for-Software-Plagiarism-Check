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
    import modheap
    # Your code
    # Add all the Huffman class methods here
    COMPARE_FN = lambda x, y : (1 if (x > y) else (-1 if (x < y) else 0))
    def make_heap(self , lst):
        self.modheap.initialize_heap(True, 1, self.COMPARE_FN)
        self.modheap.import_list(lst)
        self.modheap.heapify()
        lst = self.modheap.DATA
        return lst
        
    def build_char_table(self , filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        # Your code
        char_table = {}
        file_huff = file(filename).read()
        for i in file_huff:
            if i not in char_table:
                char_table[i] = 0
            char_table[i] += 1
        return char_table
    
    
    def cmp_freq(self , char_tup1 , char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        
    
    def pad_to_nbits(self , bitstr , pre_post , nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code
        
    
    def build_huffman_tree(self , freq_table , arity_exp):
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
        # Your code
        m_h = []
        stack = []
        for i in freq_table:
            m_h += [(freq_table[i] , i)]
        m_h = self.make_heap(m_h)
        while(len(m_h) > 1):
            m_h[0] , m_h[len(m_h)-1] = m_h[len(m_h)-1] , m_h[0]
            f_tuple = m_h.pop()
            m_h = self.make_heap(m_h)
            m_h[0] , m_h[len(m_h)-1] = m_h[len(m_h)-1] , m_h[0]
            s_tuple = m_h.pop()
            comb_tuple = (f_tuple[0] + s_tuple[0] , f_tuple[1] + s_tuple[1] , '')
            f_tuple = (f_tuple[1] , f_tuple[0] , comb_tuple[1] , '0')
            s_tuple = (s_tuple[1] , s_tuple[0] , comb_tuple[1] ,'1')
            m_h += [comb_tuple]
            m_h = self.make_heap(m_h)
            stack += [f_tuple , s_tuple]
        return stack , m_h[0]
           
            
    
    def form_codes(self , root_symbol , code_stack):
        '''
        Return a hash with the huffman code for each input character
        Algo: (i) Start from the root symbol - has code '' (empty string)
        (ii) For every element of the code_stack (starting from the end) - form its code by appending the additional bit to 
        the code of its parent (to be got from the hash already built)
        (iv) Keep count of the total compressed length as the codes are being created
        (iii) At the end, remove all the intermediate symbols created while forming the huffman tree from the hash,
        before returning the hash and the compressed length
        '''
        # Your code
        codes = {}
        comp_length = 0
        while(len(code_stack) != 0):
            tup = code_stack.pop()
            original_char = tup[0]
            freq = tup[1]
            parent = tup[2]
            relative_bit = tup[3]
            if parent in codes:
                codes[original_char] = codes[parent] + relative_bit
                if(len(original_char) <= 1):
                    comp_length += freq * len(codes[original_char])
            else:
                codes[original_char] = relative_bit
                if(len(original_char) <= 1 ):
                    comp_length += freq * len(codes[original_char])
        codes2 = {}
        for i in codes:
            if(len(i) <= 1):
                codes2[i] = codes[i]
        return codes2 , comp_length
                  
    def write_compressed(self , text_filename , huff_filename , codes, huff_length):
        '''
        Write the encoded (compressed) form of the text in 'text_filename' to 'huff_filename'. 'huff_length' is the compressed
        length of the contents of the text file. 'codes' is the hash that gives the huffman code for each input character
        Algo: (i) Write the number of distinct input chars and the compressed length in one line
        (ii) For each distinct input char, Write the code followed by the char (separated by a space) on separate lines
        (iii) Aggregate/Split the codes for the characters in the text file into 8-bit chunks
        and write each 8-bit chunk out as an ascii character.
        (iv) Careful about the last chunk that is written - the relevant bits left to be written out may be less than 8
        Hint: given a 0-1 string s - int(s, 2) gives the integer treating 's' as a binary (bit) string. (the 2 refers to the
        conversion base.
        '''
        # Your code
        comp_filename = open(huff_filename , "w")
        text_file = open(text_filename , "r").read()
        string = ''
        comp_filename.write(str(len(codes))+' '+str(huff_length)+'\n')
        for i in codes:
            if i == '\n':
                comp_filename.write(codes[i]+' '+'\\n'+'\n')
            elif i == '\t':
                comp_filename.write(codes[i]+' '+'\\t'+'\n')
            else:
                comp_filename.write(codes[i]+' '+i+'\n')
        for i in text_file:
            string += codes[i]
        temp = ''
        for i in string:
            temp += i
            if(len(temp)==8):
                comp_filename.write(chr(int(temp , 2)))
                temp = ''
        extra = 8-len(temp)
        temp = temp + '0'*extra
        comp_filename.write(chr(int(temp , 2)))
                
    def compress(self , text_filename, arity_exp):
        '''
        Compress a give text file 'text_filename' using a heap with arity 2^arity_exp
        Algo: (i) Build the frequency table
        (ii) Build code stack by building the huffman tree from the frequency table
        (iii) Form the codes from the code stack
        (iv) Write out the compressed file
        Return the name of the compressed file. Might help to have a convention here - the original file name without the extension
        appended with '.huff' could be one way.
        '''
        # Your code
        char_table = self.build_char_table(text_filename)
        stack, root = self.build_huffman_tree(char_table , arity_exp)
        codes , comp_len = self.form_codes(root , stack)
        self.write_compressed(text_filename , text_filename + '.huff' , codes , comp_len)
        return text_filename+'.huff'
         
    def read_codes(self , huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
        
    
    def uncompress(self , huff_filename):
        '''
        Uncompress a file that has been compressed using compress. Return the name of the uncompressed file.
        Add a '1' or something to the new file name so it does not overwrite the original.
        Algo: (i) Read the code from the first part of the compressed file.
        (ii) Read the rest of the file one bit at a time - every time you get a valid code, write the corresponding
        text character out to the uncompressed file.
        (iii) You need to use the compressed size appropriately - remember the last character that was written
        during compression.
        Hint: the built-in function 'bin' can be used: bin(n) - returns a 0-1 string corresponding to the binary representation
        of the number n. However the 0-1 string has a '0b' prefixed to it to indicate that it is binary, so you will have to 
        discard the first two chars of the string returned.
        '''
        # Your code
        comp_file = file(huff_filename)
        recv_file = file(huff_filename+'1',"w")
        no_of_char , length = comp_file.readline().split()
        no_of_char , length = int(no_of_char) , int(length)
        codes = {}
        i = 0
        while i < no_of_char:
            line = comp_file.readline().split()
            if(len(line)==1):
                codes[line[0]] = ' '
            elif(line[1]=='\\n'):
                codes[line[0]] = '\n'
            elif(line[1]=='\\t'):
                codes[line[0]] = '\t'
            else:
                codes[line[0]] = line[1]
            i += 1
        string = ''
        for j in comp_file.readlines():
            for i in j:
                temp = bin(ord(i))[2:]
                if(len(temp)<8):
                    extra = 8-len(temp)
                    temp = '0'*extra+temp
                string += temp
        string = string[:length]
        temp = ''
        for i in string:
            temp += i
            if temp in codes:
                recv_file.write(codes[temp])
                temp = ''
        return huff_filename+'1'



if __name__ == '__main__':
    pass