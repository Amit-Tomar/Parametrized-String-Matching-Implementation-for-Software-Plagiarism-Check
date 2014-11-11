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
    # Add all the Huffman class methods here
    
    
    def __init__(self):
        self.top_parent = 0
        self.test_file = ''
        self.last = 0
    
    
    def build_char_table(self , filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        dic = {}
        
        self.test_file = filename
        fil = open(filename , "r")
        
        for char in fil.read():
            if char in dic:
                dic[char] = dic[char]+1
            else:
                dic[char] = 1
        fil.close()
        
        return dic
    
    
    


    def build_huffman_tree(self, freq_table, arity_exp):
    #def build_huffman_tree():
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
        
        cmp_function = lambda x, y : (1 if (x > y) else (-1 if (x < y) else 0))
        obj = Heap(True, arity_exp, cmp_function )
        stack = []
        
        for i in freq_table:
            obj.add((freq_table[i] , i))
        
        len_chash = len(obj.data)
    
        while(len_chash > 1):
            
            pop1 = obj.pop()
            pop2 = obj.pop()
            
            comp_char = pop1[1] + pop2[1]
            comp_freq = pop1[0] + pop2[0]
            
            obj.add((comp_freq , comp_char))
            
            stack.append((pop1[1] , pop1[0] , comp_char , '0'))
            stack.append((pop2[1] , pop2[0] , comp_char , '1'))
            
            len_chash = len_chash - 1 
    
    
        self.top_parent = obj.data[0]
        return stack , self.top_parent
    
                
        
        
    
    def form_codes(self, root_symbol, code_stack):
        '''
        Return a hash with the huffman code for each input character
        Algo: (i) Start from the root symbol - has code '' (empty string)
        (ii) For every element of the code_stack (starting from the end) - form its code by appending the additional bit to 
        the code of its parent (to be got from the hash already built)
        (iv) Keep count of the total compressed length as the codes are being created
        (iii) At the end, remove all the intermediate symbols created while forming the huffman tree from the hash,
        before returning the hash and the compressed length
        '''
    
        
        freq_table = self.build_char_table(self.test_file)
        list_char = freq_table.keys()
        
        hash_bin = {}
        #Top = modheap.DATA[0]
        
        for i in list_char:
            
            for j in code_stack:
                
                if(i == j[0]):
                    root_symbol = j[3]
                    parent = j[2]
                    
                    while(parent != self.top_parent[1]):
                        for k in code_stack:
                            if(k[0] == parent):
                                root_symbol = k[3] + root_symbol
                                parent = k[2]
                                break
                            
                    hash_bin[i] = root_symbol 
        
        
        compressed_len = 0
    
    
        for i in list_char:
            compressed_len = compressed_len + len(hash_bin[i]) * freq_table[i]
    
    
        return hash_bin , compressed_len
    
    
    
    
    
        
        
    def write_compressed(self,text_filename, huff_filename, codes, huff_length):
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
    
        
        f_read = open(text_filename , 'r')
        f_write = open(huff_filename , 'w')
        distinct_char = len(codes)
        f_stream = open("encrypted" , "w")
        
        
        string = str(distinct_char) + ' ' + str(huff_length) + '\n'
        f_write.write(string)
        codes_tup = codes.items()
    
    
        for i in codes_tup:
            
            string = ''
            if(i[0] == '\n'):
                string = str('\\n') + ' ' + str(i[1]) + '\n'
            elif(i[0] == '\t'):
                string = str('\\t') + ' ' + str(i[1]) + '\n'
            else:
                string = str(i[0]) + ' ' + str(i[1]) + '\n'
            f_write.write(string)
        
        
        f_write.write('\n')
        fil = open("temp" , 'w')
        
        
        for i in f_read.read():
            fil.write(codes[i])
        
        
        fil.close()
        f_read.close()
        
        f_read = open("temp" , 'r')
        count = 0
        set_8 = ''
        
        
        for i in f_read.read():
            
            count = count + 1
            set_8 = set_8 + i
            
            if(count == 8):
                f_write.write(chr(int(set_8 , 2)))
                f_stream.write(chr(int(set_8 , 2)))            
                set_8 = ''
                count = 0
        
        
        last_8 = '00000000'
        set_8 = set_8 + last_8[count:]
        
        
        self.last = len(last_8[count:])
        f_write.write(chr(int(set_8 , 2)))
        f_stream.write(chr(int(set_8 , 2)))
        f_read.close()
        f_write.close()
        f_stream.close()
        
        
        
        
        
        
        
        
    def compress(self, text_filename, arity_exp):
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
        code_stack , parent = self.build_huffman_tree(freq_table , arity_exp)
        
        hash_bin , compressed_len = self.form_codes('' , code_stack)
        huff_filename = str(text_filename) + ".huff"
        
        self.write_compressed(text_filename , huff_filename , hash_bin , compressed_len)
        
        return huff_filename
        
        
        
        
        
    def read_codes(self, huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        line_split = []
        hash_of_codes = {}
        count = 0
        comp_len = 0
        
        for line in huff.readlines():
            
            line_split = line.split(" ")
            count = count + 1
            
            if(line == '\n'):
                break
            
            line_split[1] = line_split[1][:-1]
            
            if(count == 1):
                comp_len = line_split[1]
            
            elif(line_split[0] == ''):
                hash_of_codes[line_split[2][:-1]] = " "
            
            else:
                hash_of_codes[line_split[1]] = line_split[0]
            
            line_split = []
        
        
        huff.close()
        return hash_of_codes , comp_len
    
    
    
    
    
    def uncompress(self, huff_filename):
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
        f_read = open(huff_filename , 'r')
        f_write = open("temp1" , 'w')
        f_stream = open("encrypted" , 'r')
        
        hash_of_codes , comp_len = self.read_codes(f_read)
    
        zero = '00000000'
        comp_len = (int(comp_len) / 8) + 1
        
        
        for char in f_stream.read():
            
            bin_ascii = bin(ord(char))[2:]
            
            if(len(bin_ascii) != 8 and comp_len != 1):
                bin_ascii = zero[ : 8 - len(bin_ascii)] + bin_ascii
            
            if(comp_len == 1):
                bin_ascii = bin_ascii[ : (8 - self.last)]
            
            f_write.write(bin_ascii)
            comp_len = comp_len - 1 
               
               
                       
        f_write.close()
        f_read.close()
        f_stream.close()
        
        f_read = open("temp1" , 'r')
        f_write = open("uncompressed" , 'w')
        string = ''
        
        
        for char in f_read.read():
            string = string + str(char)
         
            if string in hash_of_codes:
                
                if(hash_of_codes[string] == '\\n'):
                    f_write.write('\n')
                
                elif(hash_of_codes[string] == '\\t'):
                    f_write.write('\t')
                
                else:
                    f_write.write(hash_of_codes[string])
                
                
                string = ''
                
        
        f_write.close()
        f_read.close()
        
        return "uncompressed"
        
    
    
