'''
Created on 23-Oct-2013

@author: Veda
'''

from classheap import Heap

class Huffman(object):
    '''
    Huffman coding class
    This class does not need an explicit constructor --- the class does not have any attributes to be initialized
    So a constructor method __init__ is not given - python will use a default constructor for such classes
    
    Methods will be the same as the functions in the modhuffman module
    '''
    
    def __init__(self):
        self.pad = 0
        
        
    def build_char_table(self, filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        file1 = open(filename,'r')
        file1_read = file1.read()
        char_frequency = {}
        for char in file1_read:                
            if(char_frequency.has_key(char)):
                char_frequency[char] += 1
            
            else:
                char_frequency[char] = 1
        
        file1.close()
        return char_frequency
    
    
    
    def cmp_freq(self, char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        if(char_tup1[1] > char_tup2[1]):
            return 1
        
        elif(char_tup1[1] < char_tup2[1]):
            return -1
        
        else:
            return 0
    
    def pad_to_nbits(self, bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        if(pre_post < 0):
            return '0'*nbits + bitstr
            
        else:
            return bitstr + '0'*nbits
        
    
    def build_huffman_tree(self, freq_table, arity_exp):
        '''
        Build the huffman tree for the input textfile and return a stack (maybe along with the character at the root node)
        Algo: (i) Start by making a heap out of freq_table using modheap
        (ii) Pop two elements out of the heap at a time
        (iii) Form a composite character that is the concatenation of the two and the combined frequency of the two
        (iv) Add the new composite character with its frequency to the heap
        (v) Add the two popped elements to a stack - simply append to a list
        Elements of the stack are of the form (element, frequency, parent, additional_code_bit)
        (vi) Repeat the above four steps till the heap has only the root element left
        (vi) Return the stack along with the top root element of the heap
        '''
        
        stack = []
        obj = Heap(True, arity_exp, self.cmp_freq)
        freq_table = freq_table.items()
        for element in freq_table:
            obj.add(element)
            
        while(len(obj.data) > 1):
            element1 = obj.pop()
            element2 = obj.pop()
            comp_tup = (element1[0] + element2[0], element1[1] + element2[1])
            obj.add(comp_tup)
            stack.append((element1[0], element1[1], comp_tup[0], '0')) 
            stack.append((element2[0], element2[1], comp_tup[0], '1'))
        
        
        return stack, obj.data[0][0]
            
    
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
        
        count = 0
        code = {}
        code[root_symbol] = ''
        while(code_stack!=[]):
            element = code_stack[-1]
            code_stack = code_stack[0:-1]
            code[element[0]] = code[element[2]]+element[3]
            count += len(code[element[0]]) * element[1]
        
        for k in code.keys():
            if len(k) > 1:
                del code[k]
        
        return code, count
        
    
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
        
        fileread = open(text_filename, 'r')
        filewrite = open(huff_filename, 'w')
        line_one = (str(len(codes)) + ' ' + str(huff_length) + '\n')
        filewrite.writelines(line_one)
        
        for k in codes.keys():
            if (k == '\n'):
                code = codes[k] + ' ' + '\\n' + '\n'
            elif (k == '\t'):
                code = codes[k] + ' ' + '\\t' + '\n'
            elif (k == ' '):
                code = codes[k] + ' ' + '\\s' + '\n'
            else :
                code = codes[k] + ' ' + k + '\n'
                
            filewrite.writelines(code)
            
        file_read = fileread.read()
        binary = ''
        compressed = ''
        
        for i in file_read:
            binary += codes[i]
            
        self.pad = 8 - (len(binary)%8)
        temporary = ''
        while len(binary) >= 8 :
            temporary = binary[0:8]
            inte = int(temporary, 2)
            asc = chr(inte)
            compressed += asc
            binary = binary[8:]
            
        if (len(binary) > 0):
            inte = int(binary, 2)
            asc = chr(inte)
            compressed += asc
                
        filewrite.write(compressed)      
        filewrite.close()
                 
              
    
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

        filewrite = open('final_file', 'w')
        fileread = open(huff_filename, 'r')
    
         
        codes, compressed_length = self.read_codes(fileread)
            
        file_read = fileread.read()
        temporary = ''
        code = ''
        last_ele = file_read[-1]
        file_read = file_read[:-1]
        for i in file_read:
            inte = ord(i)
            binary = bin(inte)[2:]
            length = len(binary)
    
            if (length < 8):
                binary = '0'*(8-length) + binary
    
            code += binary     
            binary = ''
            
        inte = ord(last_ele)
        binary = bin(inte)[2:]
    
        if (len(binary) <= (8 - self.pad)):
            binary = '0'*(8 - self.pad - len(binary)) + binary
    
        code += binary     
        uncompressed = ''
    
        for k in code :
            temporary += k
            if temporary in codes.keys() :
    
                uncompressed += codes[temporary]
                temporary = ''
    
        filewrite.write(uncompressed)     
           
        filewrite.close()
        fileread.close()
        return 'final_file'


if __name__ == '__main__':
    pass