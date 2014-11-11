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
    def __init__(self):
        self.NBITS = 0
        
    def initialize(self , nbit):
        self.NBITS = nbit
    
    def build_char_table(self , filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        file_open = open(filename, 'r')
        freq_dict = {}   
        for char in file_open.read():
            if char in freq_dict.keys():
                freq_dict[char] = freq_dict[char] + 1
            else:
                freq_dict[char] = 1
        file_open.close()
        return freq_dict
    
    def cmp_freq(self , char_tup1 , char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        tup1 = char_tup1[1]
        tup2 = char_tup2[1]
        if (tup1 == tup2):
            return 0
        elif(tup1 > tup2):
            return 1
        else:
            return -1
           
    def pad_to_nbits(self , bitstr , pre_post , nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        if pre_post > 0:
            return bitstr + '0'*nbits
        else:
            return '0'*nbits + bitstr
       
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
        
        stack = [] 
        heap = Heap(True, arity_exp, self.cmp_freq)
        heap.data = freq_table.items()
        heap.heapify()
        while(len(heap.data)>2):
            pop1 = heap.pop()
            pop2 = heap.pop()
            parent = ( pop1[0]+pop2[0], pop1[1]+pop2[1] )
            heap.add(parent)
            stack.append((pop1[0], pop1[1], parent[0], '0' ))
            stack.append((pop2[0], pop2[1], parent[0], '1' ))
        stack.append((heap.data[0][0], heap.data[0][1], "root", '0'))
        stack.append((heap.data[1][0], heap.data[1][1], "root", '1'))
        return stack , '' 
                
    def form_codes(self,root_symbol, code_stack):
        '''
        Return a hash with the huffman code for each input character
        Algo: (i) Start from the root symbol - has code '' (empty string)
        (ii) For every element of the code_stack (starting from the end) - form its code by appending the additional bit to
        the code of its parent (to be got from the hash already built)
        (iv) Keep count of the total compressed length as the code test_file = open(self.RANDOM_FILENAME, 'w')
            freq_table = {}
            for _ in range(filesize):
                randchar = chr(self.FIRST_PRINTABLE_ORD + randrange(self.N_PRINTABLE_CHARS))
                if (freq_table.has_key(randchar)):
                    freq_table[randchar] += 1
                else:
                    freq_table[randchar] = 1
                test_file.write(randchar)
            test_file.close()
            return freq_tables are being created
        (iii) At the end, remove all the intermediate symbols created while forming the huffman tree from the hash,
        before returning the hash and the compressed length
        '''
        code_hash = {'root':root_symbol}
        i = len(code_stack)-1
        for j in range(i , -1 , -1):
            code_hash[code_stack[j][0]] = code_hash[code_stack[j][2]] + code_stack[j][3]
            j -= 1
        length = len(code_stack)-1
        i = length
        for j in range(i , -1 , -1):
            length += len(code_hash[code_stack[j][0]])
            j -= 1
        for composite_char in code_hash.keys():
            if len(composite_char)>1:
                del code_hash[composite_char]
        return code_hash, length   
        
    def write_compressed(self, text_filename, huff_filename, codes, huff_length):
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
     
        text_file = open(text_filename , "r")
        huff_file = open(huff_filename , "w")
        huff_file.write ("%d "%(len(codes)))
        huff_file.write ("%d \n"%(huff_length))      
        for ele in codes.keys():
            if ele == ' ':
                huff_file.write(codes[ele]+' space\n')
            elif ele == '\n':
                huff_file.write(codes[ele]+' newline\n')
            elif ele == '\t':
                huff_file.write(codes[ele]+' tab\n')
            else:
                huff_file.write(codes[ele]+' '+ele+'\n')
       
        binary = ''
        temporary = ''
        compressed = ''
        file_read = text_file.read()
       
        for char in file_read:
            if char in codes.keys():
                binary = binary + str(codes[char])
               
        for i in binary:
            temporary = temporary+i
            if(len(temporary)==8):
                compressed += chr(int(temporary , 2))
                temporary = ''
       
        if(len(temporary)!=0):
            self.initialize(8 - len(temporary))
            compressed += chr(int(self.pad_to_nbits(temporary, 1 , 8-len(temporary)) , 2))
       
        huff_file.write(compressed + '\n')
       
        return huff_file.write
     
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
       
        freq_table = self.build_char_table(text_filename)
        code_stack , root_element = self.build_huffman_tree(freq_table , arity_exp)
        codes, huff_length = self.form_codes(root_element, code_stack)
        huff_file = text_filename + '.huff'
        self.write_compressed(text_filename , huff_file , codes , huff_length)
        return huff_file
     
    def read_codes(self , huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        codes = {}
       
        files = huff.readline()
        file_list = files.split()
        length = file_list[0]
        compressed_length = file_list[1]
       
        for i in range(0 , int(length)):
            files = huff.readline()
            file_list = files.split()
            if file_list[1] == 'space':
                codes[file_list[0]] = ' '
            elif file_list[1] == 'newline':
                codes[file_list[0]] = '\n'
            elif file_list[1] == 'tab':
                codes[file_list[0]] = '\t'   
            else:
                codes[file_list[0]] = file_list[1]
      
        return codes , compressed_length
     
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
        huff_file = open(huff_filename,"r")
        code , compressed_length = self.read_codes(huff_file)
        temporary = ''
        string = ''
        for bit in huff_file.read():
            string = bin(ord(bit))[2:]
            temporary += self.pad_to_nbits(string, -1, 8-len(string))
        temporary1 = ''
        temporary2 = ''
        temporary = temporary[:(len(temporary)-self.NBITS-8)]
        for char in temporary:
            temporary1 += char
            if temporary1 in code.keys():
                temporary2 += code[temporary1]
                temporary1 = '' 
        new_file = huff_filename+'1'
        uncompressed = open(new_file,'w')
        uncompressed.write(temporary2)
        return new_file
    
if __name__ == '__main__':
    pass