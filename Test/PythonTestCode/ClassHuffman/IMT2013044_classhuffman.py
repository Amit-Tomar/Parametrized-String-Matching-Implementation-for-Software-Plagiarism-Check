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
    
    def build_char_table(self, filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurrences of that char in the file
        '''
        # Your code
        inp = file(filename,'r')
        c_hash = {}
        for lines in inp.readlines():
            for letter in lines:
                if letter in c_hash.keys():
                    c_hash[letter] = c_hash[letter] + 1
                else:
                    c_hash[letter] = 1
        inp.close()
        return c_hash
    
    def cmp_freq(self, char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        return cmp(char_tup1[1], char_tup2[1])

    def pad_to_nbits(self, bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code
        
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
        (vii) Return the s\tack along with the top root element of the heap
        '''
        # Your code
        freq_list = []
        for letter, number in freq_table.items():
            freq_list.append( (letter, number) )
        heap = Heap( True, arity_exp, self.cmp_freq )
        heap.data = freq_list
        heap.heapify()
        stack = []
        while(heap.size()>1):
            element1 = heap.pop()
            element2 = heap.pop()
            parent = element1[0] + element2[0]
            combined_freq = element1[1] + element2[1]  
            heap.add( (parent, combined_freq) )
            stack.append((element1[0], element1[1], parent, '0')) 
            stack.append((element2[0], element2[1], parent, '1')) 
        return stack, heap.data[0]
    
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
        codes = {}
        codes[root_symbol[0]] = ''
        compressed_length = 0
        while( code_stack!=[] ):
            tup = code_stack.pop()
            codes[tup[0]] = codes[tup[2]] + tup[3]
            if(len(tup[0])<=1):
                compressed_length = compressed_length + tup[1]*len(codes[tup[0]])       
        for key, val in codes.items():
            if len(key)>1:
                del codes[key]
            val = val
        return codes, compressed_length 
        
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
        # Your code
        out = file(huff_filename,'w')
        inp = file(text_filename)
        out.write(str(len(codes)))
        out.write(' ')
        out.write(str(huff_length))
        for key, values in codes.items():
            out.write('\n')
            out.write(values)
            out.write(' ')
            if(key==' '):
                out.write('')
            elif(key=='\n'):
                out.write("\\n")
            elif(key=='\t'):
                out.write("\\t")
            else:
                out.write(key)
        out.write('\n')
        compressed_str = ''
        for char in inp.read():
            compressed_str = compressed_str + codes[char]
            while (len(compressed_str) >= 8):
                compressed_char = compressed_str[:8]
                compressed_str = compressed_str[8 : len(compressed_str)]
                int_val = int(compressed_char, 2)
                out.write(chr(int_val))
        if(len(compressed_str)!=0):
            length = len(compressed_str)
            extra = 8 - length
            compressed_str = compressed_str + '0' * extra
            int_val = int(compressed_str, 2)
            out.write(chr(int_val))
        out.close()
        inp.close()
            
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
        c_hash = self.build_char_table(text_filename)
        code_stack, root_symbol = self.build_huffman_tree(c_hash, arity_exp)
        codes, huff_length = self.form_codes(root_symbol, code_stack)
        self.write_compressed(text_filename, text_filename + '.huff', codes, huff_length)
        self.uncompress(text_filename+ '.huff')
        return text_filename + '.huff'
    
    def read_codes(self, huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
        c_hash = {}
        i = 1
        first_line = huff.readline()
        first_line = first_line.split()
        count = int(first_line[0])
        length = int(first_line[1])
        while( i <= count ):
            line = huff.readline()
            line = line.split()
            if(len(line)==1):
                line += [' ']
            if(line[1]=='\\n'):
                line[1] = '\n'
            elif(line[1]=='\\t'):
                line[1] = '\t'
            c_hash[line[0]] = line[1]
            i = i+1
        return c_hash, length
        
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
        inp = file(huff_filename,'r')
        out = file(huff_filename + '1','w')
        c_hash, length = self.read_codes(inp)
        prev_residue = ''
        p_str = ''
        for char in inp.read():
            char = ord(char)
            temp = bin(char)
            temp = temp[ 2 : len(temp) ]
            if(len(temp)<8):
                extra = 8 - len(temp)
                temp = extra * '0' + temp
            prev_residue = prev_residue + temp
        prev_residue = prev_residue[ 0 : length ]
        for num in prev_residue:
            p_str = p_str + num
            if p_str in c_hash.keys():
                out.write(c_hash[p_str])
                prev_residue = prev_residue[ len(p_str) : len(prev_residue) ]
                p_str = ''
        return huff_filename + '1'

if __name__ == '__main__':
    pass