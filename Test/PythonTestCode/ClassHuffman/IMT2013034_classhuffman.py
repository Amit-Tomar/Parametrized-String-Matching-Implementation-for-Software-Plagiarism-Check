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
    
    def build_char_table(self, filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        # Your code
        char_table = {}
        file_f = open(filename,"r")
        for line in file_f.readlines():
            for character in line:
                if character in char_table:
                    char_table[character] += 1
                else :
                    char_table[character] = 1
        file_f.close()
        return char_table
                

    def cmp_freq(self, char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        if char_tup1[1] > char_tup2[1]:
            return 1
        elif char_tup1[1] < char_tup2[1]:
            return -1
        else :
            return 0

    def build_huffman_tree(self, freq_table, arity_exp):
        '''
        Build the huffman tree for the input textfile and return a stack (maybe along with the character at the root node)
        Algo: (i) Start by making a heap out of freq_table using heap_obj
        (ii) Pop two elements out of the heap at a time
        (iii) Form a composite character that is the concatenation of the two and the combined frequency of the two
        (iv) Add the new composite character with its frequency to the heap
        (v) Add the two popped elements to a stack - simply append to a list
        Elements of the stack are of the form (element, frequency, parent, additional_code_bit)
        (vi) Repeat the above four steps till the heap has only the root element left
        (vii) Return the stack along with the top root element of the heap
        '''
        # Your code
        stack = []
        heap_obj = Heap(True, arity_exp, self.cmp_freq)
        heap_obj.data = freq_table.items()
        heap_obj.heapify()
        while heap_obj.size() > 1:
            element1 = heap_obj.pop()
            element2 = heap_obj.pop()
            comp_element_name = element1[0] + element2[0]
            comp_element_freq = element1[1] + element2[1]
            composite_element = (comp_element_name, comp_element_freq)
            heap_obj.add(composite_element)
            stack.append((element1[0], element1[1], composite_element[0], '0'))
            stack.append((element2[0], element2[1], composite_element[0], '1'))
        root = heap_obj.data[0][0]
        return stack, root
    
        
    def form_codes(self, root_symbol, code_stack):
        '''
        Return a hash with the huffman code for each input character
        Algo: (i) Start from thuffman_he root symbol - has code '' (empty string)
        (ii) For every element of the code_stack (starting from the end) - form its code by appending the additional bit to 
        the code of its parent (to be got from the hash already built)
        (iii) Keep count of the total compressed length as the codes are being created
        (iv) At the end, remove all the intermediate symbols created while forming the huffman tree from the hash,
        before returning the hash and the compressed length
        '''
        # Your code
        huffman_code = {}
        temp_dict = {}
        temp_dict[root_symbol] = ''
        index = len(code_stack) - 1
        compressed_length = 0
        while index >= 0:
            element = code_stack[index][0]
            parent = code_stack[index][2]
            add_bit = code_stack[index][3]
            temp_dict[element] = temp_dict[parent] + add_bit
            index -= 1
        index = len(code_stack) - 1
        while index >= 0:
            element = code_stack[index][0]
            freq = code_stack[index][1]
            if len(element) == 1:
                huffman_code[element] = temp_dict[element]
                compressed_length += len(huffman_code[element]) * freq
            index -= 1
        return huffman_code, compressed_length
            
    def write_compressed(self, text_filename, huff_filename, codes, huff_length):
        '''
        Write the encoded (compressed) form of the text in 'text_filename' to 'huff_filename'. 'huff_length' is the compressed
        length of the contents of the text file. 'codes' is the hash that gives the huffman code for each input character
        Algo: (i) Write the huffman_member of distinct input chars and the compressed length in one line
        (ii) For each distinct input char, Write the code followed by the char (separated by a space) on separate lines
        (iii) Aggregate/Split the codes for the characters in the text file into 8-bit chunks
        and write each 8-bit chunk out as an ascii character.
        (iv) Careful about the last chunk that is written - the relevant bits left to be written out may be less than 8
        Hint: given a 0-1 string s - int(s, 2) gives the integer treating 's' as a binary (bit) string. (the 2 refers to the
        conversion base.
        '''
        # Your code
        file_text = open(text_filename, "r")
        file_huff = open(huff_filename, "w")
        data = ""
        string = ""
        file_huff.write(str(len(codes))+' '+str(huff_length)+"\n")
        for key in codes :
            if key == '\n':
                file_huff.write(codes[key]+' '+'\\n'+'\n')
            elif key == '\t':
                file_huff.write(codes[key]+' '+'\\t'+'\n')
            else :
                file_huff.write(codes[key]+' '+key+'\n')
        
        for char in file_text.read():
            string += codes[char]
            file_text.close()
        for char in string :
            data += char 
            if len(data) == 8 :
                file_huff.write(chr(int(data, 2)))
                data = ""
        if len(data) is not 0:
            data += '0'*(8-len(data))
            file_huff.write(chr(int(data, 2)))
                
    

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
        code_stack, root_symbol = self.build_huffman_tree(freq_table, arity_exp)
        codes, huff_length = self.form_codes(root_symbol, code_stack)
        huff_filename = text_filename + '.huff'
        self.write_compressed(text_filename, huff_filename, codes, huff_length)
        return huff_filename
    
    def read_codes(self, huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
        code = {}
        line = huff.readline()
        code_length, compressed_length = line.split()
        code_length = int(code_length)
        compressed_length = int(compressed_length)
        while code_length > 0:
            line = huff.readline().split()
            if len(line) == 1:
                code[line[0]] = ' '
            elif line[1] == '\\n':
                code[line[0]] = '\n'
            elif line[1] == '\\t':
                code[line[0]] = '\t'
            else :
                code[line[0]] = line[1]
            code_length -= 1
        return code, compressed_length
        
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
        huff = open(huff_filename, "r")
        code, compressed_length = self.read_codes(huff)
        data = ""
        decode = ""
        for char in huff.read():
            string = bin(ord(char))
            string = string[2:]
            string = '0' * (8-len(string)) + string
            data += string
        data = data[0:compressed_length]
        huff.close()
        uncompressed_file = huff_filename +'1'
        huff = open(uncompressed_file, "w")
        for char in data :
            decode += char
            if decode in code:
                huff.write(code[decode])
                decode = ""
        huff.close()
        return uncompressed_file


if __name__ == '__main__':
    pass