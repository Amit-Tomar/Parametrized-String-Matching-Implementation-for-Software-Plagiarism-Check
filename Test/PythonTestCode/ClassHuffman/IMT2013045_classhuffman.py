'''
Created on 23-Oct-2013

@author: raghavan
'''
# Importing the modheap class from classmodheap
from classheap import Heap

class Huffman(object):
    '''
    Huffman coding class
    This class does not need an explicit constructor --- the class does not have any attributes to be initialized
    So a constructor method __init__ is not given - python will use a default constructor for such classes
    
    Methods will be the same as the functions in the modhuffman module
    '''
    
    # Your code
    import modheap
    def build_char_table(self, filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        # Your code
        hash_char = {}
        fptr = open ( filename , 'r' )
        for line in fptr.readlines():
            for letters in line:
                if letters in hash_char.keys():
                    hash_char[letters] += 1
                else:
                    hash_char[letters] = 1
        fptr.close()
        return hash_char
        
        
    def cmp_freq(self, char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the modheap
        '''
        # Your code
        return ( 1 if( char_tup1[1] > char_tup2[1] ) else ( -1 if( char_tup1[1] < char_tup2[1] ) else 0) )
    
    
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
        Algo: (i) Start by making a modheap out of freq_table using modheap
        (ii) Pop two elements out of the modheap at a time
        (iii) Form a composite character that is the concatenation of the two and the combined frequency of the two
        (iv) Add the new composite character with its frequency to the modheap
        (v) Add the two popped elements to a stack - simply append to a list
        Elements of the stack are of the form (element, frequency, parent, additional_code_bit)
        (vi) Repeat the above four steps till the modheap has only the root element left
        (vii) Return the stack along with the top root element of the modheap
        '''
        # Your code
        heap_list = []
        code_stack = []
        for char, freq in freq_table.items():
            heap_list.append((char, freq))
        self.modheap.initialize_heap(True, arity_exp, self.cmp_freq)
        self.modheap.import_list(heap_list)
        self.modheap.heapify()
        while ( len(self.modheap.DATA) <> 1 ):
            child1 = self.modheap.pop()
            child2 = self.modheap.pop()
            parent = ( child1[0]+child2[0], child1[1]+child2[1] )
            self.modheap.DATA.append(parent)
            code_stack.extend( [ ( child1[0], child1[1], parent[0], '1' ), ( child2[0], child2[1], parent[0], '0' ) ] )
        return code_stack, self.modheap.DATA[0]    
            
    
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
        codes = {root_symbol[0]:''}
        huff_length = 0
        index_list = []
        while( code_stack != [] ):
            element = code_stack.pop()
            binary_code = codes[element[2]] + element[3] 
            codes[element[0]] =  binary_code
            if(len(element[0]) == 1):
                huff_length += ( element[1] * len(binary_code))
            if( len ( element[2] ) > 1 ):
                index_list.append(element[2])
        while ( index_list != [] ):
            element = index_list.pop()
            element = index_list.pop()
            del codes[element]
        return codes, huff_length   
    
    
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
        compressed_str = ''
        distinct_input = len(codes)
        fptr = open (text_filename,'r')
        fout = open (huff_filename,'w')
        fout.write(str(distinct_input))
        fout.write(' ')
        fout.write(str(huff_length))
        fout.write('\n')
        for char, num in codes.items():
            fout.write(num)
            fout.write(' ')
            if(char == '\n'):
                fout.write('\\n')
            elif(char == '\t'):
                fout.write('\\t')
            else:
                fout.write(char)
            fout.write('\n')
        for character in fptr.read():
            compressed_str = compressed_str + codes[character]
        while( len(compressed_str) >= 8 ):
            compressed_char = chr( int( compressed_str[:8], 2 ) )
            compressed_str = compressed_str[8:]
            fout.write(compressed_char)
        if( len(compressed_str) < 8 ):
            while( len(compressed_str) != 9 ):
                compressed_str += '0'
            fout.write( chr( int( compressed_str[:8], 2 ) ) )    
        fout.close()
        fptr.close()
        
        
    
    def compress(self, text_filename, arity_exp):
        '''
        Compress a given text file 'text_filename' using a modheap with arity 2^arity_exp
        Algo: (i) Build the frequency table
        (ii) Build code stack by building the huffman tree from the frequency table
        (iii) Form the codes from the code stack
        (iv) Write out the compressed file
        Return the name of the compressed file. Might help to have a convention here - the original file name without the extension
        appended with '.huff' could be one way.
        '''
        # Your code
        freq_table = self.build_char_table( text_filename )
        code_stack, top_root_element = self.build_huffman_tree( freq_table , arity_exp )
        codes, huff_length = self.form_codes( top_root_element , code_stack )
        self.write_compressed( text_filename, text_filename+".huff" , codes, huff_length )
        return text_filename+".huff"
    
        
    def read_codes(self, huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
        hash_of_codes = {}
        line = huff.readline()
        templist = line.split()
        distinct_input, compressed_length = templist[0], templist[1]  
        i = int(distinct_input)
        while( i > 0 ):
            templist = huff.readline()
            templist = templist.split()
            if(len(templist)==1):
                hash_of_codes[templist[0]] = ' '
            else:
                hash_of_codes[templist[0]] = templist[1]
            i -= 1
        return hash_of_codes, compressed_length
        
    
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
        newstr = ''
        decode_str = ''
        huff_ptr = open(huff_filename,'r')
        newptr = open(huff_filename+'1','w')
        hash_codes, compressed_length = self.read_codes(huff_ptr)
        for character in huff_ptr.read():
            temp_str = bin(ord(character))
            temp_str = temp_str[2:]
            i = 8-len(temp_str)
            temp_str = '0'*i + temp_str 
            newstr += str(temp_str)
        newstr = newstr[:int(compressed_length)]
        for bit in newstr:
            decode_str += bit
            if decode_str in hash_codes:
                if(hash_codes[decode_str]=='\\n'):
                    newptr.write('\n')
                elif(hash_codes[decode_str]=='\\t'):
                    newptr.write('\t')
                else:
                    newptr.write(hash_codes[decode_str])
                decode_str = ''
        return huff_filename+'1'        



if __name__ == '__main__':
    pass