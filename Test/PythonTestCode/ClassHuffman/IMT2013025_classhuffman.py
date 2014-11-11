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
    
    # Your code
    # Add all the Huffman class methods here
    
    def __init__(self):
        self.pad = 0
    
    def build_char_table(self, filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        test_file = open(filename, 'r')
        file1 = test_file.read()
        freq_table = {}
        for char in file1:
            if (freq_table.has_key(char)):
                freq_table[char] += 1
            else:
                freq_table[char] = 1
                
        test_file.close()
        return freq_table
        

    def cmp_freq(self, char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        if (cmp(char_tup1, char_tup2) == 1):
            return 1
        elif (cmp(char_tup1, char_tup2) == -1):
            return -1
        elif (cmp(char_tup1, char_tup2) == 0):
            return 0

    
    def build_huffman_tree(self, freq_table, arity_exp):
        '''
        Build the huffman tree for the input textfile and return a stack (maybe along with the character at the root node)
        Algo: (i) Start by making a heap out of freq_table using obj
        (ii) Pop two elements out of the heap at a time
        (iii) Form a composite character that is the concatenation of the two and the combined frequency of the two
        (iv) Add the new composite character with its frequency to the heap
        (v) Add the two popped elements to a stack - simply append to a list
        Elements of the stack are of the form (element, frequency, parent, additional_code_bit)
        (vi) Repeat the above four steps till the heap has only the root element left
        (vii) Return the stack along with the top root element of the heap
        '''
        # Your code
        obj = Heap(True, arity_exp, self.cmp_freq)

        for i in freq_table:
            obj.add((freq_table[i], i))
        obj.heapify()
        pop_stack = [] 
        length = obj.size()
        while length > 1 :
            
            element1 = obj.pop()
            element2 = obj.pop()
            composite = (element1[0]+element2[0], element1[1]+element2[1])
            obj.add(composite)
            pop_stack.append((element1[1], element1[0], composite[1], '1'))
            pop_stack.append((element2[1], element2[0], composite[1], '0'))
            length = length-1
            
        return pop_stack, obj.data[0]
        
    
    
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
        # Your code
        codes = {root_symbol[1] : ''}
        compressed_length = 0
        i = len(code_stack) -1
        
        while i >= 0 :
            codes[code_stack[i][0]] = codes[code_stack[i][2]] + code_stack[i][3]
            if(len(code_stack[i][0])==1):
                add = len(codes[code_stack[i][0]])*code_stack[i][1]
                compressed_length += add
            i = i - 1
            
        for k in codes.keys():
            if len(k) > 1:
                del codes[k]
                
        return codes, compressed_length
        
                 
     
    
    
    def write_compressed(self, text_filename, huff_filename, codes, huff_length):
        '''
        Write the encoded (compressed) form of the text in 'text_filename' to 'huff_filename'. 'huff_length' is the compressed
        length of the contents of the text file. 'codes' is the hash that gives the huffman code for each input character
        Algo: (i) Write the number of distinct input chars and the compressed length in one line
        (ii) For each distinct input char, Write the code followed by the char (separated by a space) on separate lines
        (iii) Aggregate/Split the codes for the characters in the text file into 8-bit chunks
        and write each 8-bit chunk out as an ascii charahttps://www.google.co.in/?gws_rd=cr#q=compare+function+in+pythoncter.
        (iv) Careful about the last chunk that is written - t    he relevant bits left to be written out may be less than 8
        Hint: given a 0-1 string s - int(s, 2) gives the integer treating 's' as a binary (bit) string. (the 2 refers to the
        conversion base.https://www.google.co.in/?gws_rd=cr#q=compare+function+in+python
        '''
        # Your code
        original_file = open(text_filename, 'r')
        compressed_file = open(huff_filename, 'w')
        first_line = str(len(codes)) + ' ' + str(huff_length) + '\n'
        compressed_file.writelines(first_line)
        
        for k in codes.keys():
            if k == '\n':
                code_char_str = codes[k] + ' ' + '\\n' + '\n'
            elif k == '\t':
                code_char_str = codes[k] + ' ' + '\\t' + '\n'
            elif k == ' ':
                code_char_str = codes[k] + ' ' + '\\s' + '\n'
            else :
                code_char_str = codes[k] + ' ' + k + '\n'
            compressed_file.writelines(code_char_str)
            
        content = original_file.read()
        string = ''
        compressed = ''
        for i in content:
            string += codes[i]
            
        self.pad = 8 - (len(string)%8)
        temp_string = ''
        while len(string) >= 8 :
            temp_string = string[0:8]
            integer = int(temp_string, 2)
            ascii = chr(integer)
            compressed += ascii
            string = string[8:]
            
        if (len(string) > 0):
            integer = int(string, 2)
            ascii = chr(integer)
            compressed += ascii
                
        compressed_file.write(compressed)      
        compressed_file.close()
            
        
    
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
        # Your code
        freq_table = self.build_char_table(text_filename) 
        code_stack, top_element = self.build_huffman_tree(freq_table, arity_exp)
        code, huff_length = self.form_codes(top_element, code_stack)
        self.write_compressed(text_filename, 'huff_filename.huff', code, huff_length)
        
        return 'huff_filename.huff'
    
    
    def read_codes(self, huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
        codes = {}
        filep = huff.readline().split()
        length = int(filep[0])
        compressed_length = int(filep[1])
        
        i = 0
        while i < length :
            code_key = huff.readline().split()
            if code_key[1] == '\\s':
                codes[code_key[0]] = ' '
            elif code_key[1] == '\\n':
                codes[code_key[0]] = '\n'
            elif code_key[1] == '\\t':
                codes[code_key[0]] = '\t'
            else:
                codes[code_key[0]] = code_key[1]
            i += 1
       
       
        return codes, compressed_length
    
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
        # Your code
        uncompressed_file = open('final_file', 'w')
        compressed_file = open(huff_filename, 'r')
    
        codes, compressed_length = self.read_codes(compressed_file)
            
        data = compressed_file.read()
        temp_code = ''
        full_code = ''
        last_char = data[-1]
        data = data[:-1]
        for i in data:
            integer = ord(i)
            bin_code = bin(integer)[2:]
            length = len(bin_code)
    
            if length < 8 :
                bin_code = '0'*(8-length) + bin_code
    
            full_code += bin_code     
            bin_code = ''
            
        integer = ord(last_char)
        bin_code = bin(integer)[2:]
    
        if len(bin_code) <= 8 - self.pad :
            bin_code = '0'*(8-self.pad- len(bin_code)) + bin_code
    
        full_code += bin_code     
        uncompressed = ''
    
        for k in full_code :
            temp_code += k
            if temp_code in codes.keys() :
    
                uncompressed += codes[temp_code]
                temp_code = ''
    
        uncompressed_file.write(uncompressed)     
           
        uncompressed_file.close()
        compressed_file.close()
        return 'final_file'
        

if __name__ == '__main__':
    pass