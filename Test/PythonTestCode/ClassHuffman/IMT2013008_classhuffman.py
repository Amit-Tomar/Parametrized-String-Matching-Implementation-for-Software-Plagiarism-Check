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
    nbit = 0
    def initialize(self, nbit):
        '''Used to initialize the n bits appended at the end 
        of the compressed string'''
        self.nbit = nbit
    
    def build_char_table(self,filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
    # Your code
        char_hash = {}
        file_pointer = open(filename, 'r')
        file_data = file_pointer.read()
        for letter in file_data :
            if letter not in char_hash.keys():
                char_hash[letter] = 1
            else:
                char_hash[letter] += 1
        return char_hash 

    def cmp_freq(self, char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
    # Your code
        tup1_freq = char_tup1[1]
        tup2_freq = char_tup2[1]
        if tup1_freq > tup2_freq:
            return 1
        elif tup1_freq < tup2_freq:
            return -1
        else:
            return 0

    def pad_to_nbits(self, bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code
        if pre_post < 0:
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
        Elements ofdef the stack are of the form (element, frequency, parent, additional_code_bit)
        (vi) Repeat the above four steps till the heap has only the root element left
        (vii) Return the stack along with the top root element of the heap
        '''
    # Your code
        # Your code
        stack = []
        freq_table = freq_table.items()
        heap = Heap(True, arity_exp, self.cmp_freq)
        for elem in freq_table:
            heap.add(elem)
        while(len(heap.data)>2):
            pop1 = heap.pop()
            pop2 = heap.pop()
            stack.append((pop1[0], pop1[1], pop2[0]+pop1[0], 1))
            stack.append((pop2[0], pop2[1], pop2[0]+pop1[0], 0))
            heap.add((pop2[0]+pop1[0], pop1[1]+pop2[1]))

        stack.append((heap.data[0][0], heap.data[0][1], 'root', 1))
        stack.append((heap.data[1][0], heap.data[1][1], 'root', 0))
        return stack, ''

    
    def form_codes(self,root_symbol, code_stack):
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
        codes = {'root':root_symbol}
        counter = 0
        code_stack = code_stack[::-1]
        for i in range(len(code_stack)):
            codes[code_stack[i][0]] = (codes[code_stack[i][2]] + str(code_stack[i][3]))
            counter += len(codes[code_stack[i][0]])
        for k in codes.keys():
            if len(k)>1:
                del codes[k]
        return codes, counter
         
    

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
    # Your code
        original_file = open(text_filename, "r")
        compressed_file = open(huff_filename, "w")
        compressed_file.write('%d %d\n' % (len(codes), huff_length))
        for ele in codes.keys():
            if ele == ' ':
                compressed_file.write(codes[ele]+' space\n')
            elif ele == '\n':
                compressed_file.write(codes[ele]+' nextline\n')
            elif ele == '\t':
                compressed_file.write(codes[ele]+' tab\n')
            else:
                compressed_file.write(codes[ele]+' '+ele+'\n')
        file_data = original_file.read()
        original_file.close()
        compressed = ''
        binary = ''
        temp = ''
        for char in file_data:
            if char in codes.keys():
                binary = binary+str(codes[char])
                no_of_bits = 8-len(binary)%8
        self.initialize(no_of_bits)
        binary = self.pad_to_nbits(binary, 1, no_of_bits)
        for i in binary:
            temp += i
            if len(temp) == 8:
                compressed += chr(int(temp, 2))
                temp = ''
        if len(temp) != 0:
            compressed += chr(int(temp, 2))    
        compressed_file.write(compressed)
        compressed_file.close()

    def compress(self,text_filename, arity_exp):
        '''
        Compress a give text file 'text_filename' using a heap with arity 2^arity_exp
        Algo: (i) Build the frequency table
        (ii) Build code s-tack by building the huffman tree from the frequency table
        (iii) Form the codes from the code stack
        (iv) Write out the compressed file
        Return the name of the compressed file. Might help to have a convention here - the original file name without the extension
        appended with '.huff' could be one way.
        '''
        # Your code
        freq = self.build_char_table(text_filename)
        stack, root_symbol = self.build_huffman_tree(freq, arity_exp)
        codes, counter = self.form_codes('', stack)
        self.write_compressed(text_filename, 'comp.huff', codes, counter)
        return 'comp.huff'
    


    def read_codes(self,huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
    
        code_dict = huff.read().split()
        distinct = code_dict[0]
        comp_len = code_dict[1]
        codes = {}
        for i in range(2, 2*int(distinct)+1, 2):
            if code_dict[i+1] == 'space':
                codes[code_dict[i]] = ' '
            elif code_dict[i+1] == 'nextline':
                codes[code_dict[i]] = '\n'
            elif code_dict[i+1] == 'tab':
                codes[code_dict[i]] = '\t'
            elif code_dict[i+1] == 'backspace':
                codes[code_dict[i]] = '\\'
            else:
                codes[code_dict[i]] = code_dict[i+1]
        huff.close()
        return codes, comp_len

    

    def uncompress(self,huff_filename):
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
        binary = ''
        temp = ''
        lines = []
        compressed_file = open(huff_filename, "r")
        codes, comp_length = self.read_codes(compressed_file)
        no_of_distinct = len(codes.keys()) + 1
        compressed_file = open(huff_filename, "r")
        uncompressed_file = open("uncompressed.txt", "w")
        for i in range(no_of_distinct):
            compressed_file.readline()
        lines.append(compressed_file.readline())   
        while lines[-1]:
            lines.append(compressed_file.readline())
        for eachline in lines:
            for char in eachline:
                binary += self.pad_to_nbits(bin(ord(char))[2:], -1, 8-len(bin(ord(char))[2:]))
        binary = binary[:len(binary)-self.nbit]
        for bits in binary:
            temp += bits
            if temp in codes.keys():
                uncompressed_file.write(codes[temp])
                temp = ''
        compressed_file.close()
        uncompressed_file.close()
        return "uncompressed.txt" 
            
        
    
    
if __name__ == '__main__':
    pass
