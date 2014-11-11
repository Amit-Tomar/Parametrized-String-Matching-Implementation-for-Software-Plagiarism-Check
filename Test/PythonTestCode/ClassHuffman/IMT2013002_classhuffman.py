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
        number of occurences of that char in the file
        '''
        # Your code
        file=open(filename,"r")
        i=0
        char_table={}
        for i in file.read():
            if i in char_table:
                char_table[i]+=1
            else:
                char_table[i]=1 
        return char_table      
    
    
    def cmp_freq(self, char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        
        if char_tup1[1]<char_tup2[1]:
            return -1
        elif char_tup1[1]==char_tup2[1]:
            return 0
        else:
            return 1
    
    
    def pad_to_nbits(self, bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code
        str_add= '0'
        
        if pre_post<0:
            while len(bitstr) < nbits:
                bitstr=str_add + bitstr
                
        elif pre_post>0:
            while len(bitstr) < nbits:
                bitstr = bitstr +str_add
        
    
    def build_huffman_tree(self, freq_table, arity_exp):
        '''
        Build the huffman tree for the input textfile and return a stack (maybe along with the character at the root node)
        Algo: (i) Start by making a heap out of freq_table using Heap
        (ii) Pop two elements out of the heap at a time
        (iii) Form a composite character that is the concatenation of the two and the combined frequency of the two
        (iv) Add the new composite character with its frequency to the heap
        (v) Add the two popped elements to a stack - simply append to a list
        Elements of the stack are of the form (element, frequency, parent, additional_code_bit)
        (vi) Repeat the above four steps till the heap has only the root element left
        (vii) Return the stack along with the top root element of the heap
        '''
        # Your code
        stack=[]
        lst=freq_table.items()
            
        obj=Heap(True ,arity_exp , self.cmp_freq)
        obj.import_list(lst)
        obj.heapify()
        while obj.size()>1:
            item1=obj.pop()
            item2=obj.pop()
            character_concat=(item1[0]+item2[0],item1[1]+item2[1])
            obj.data.append(character_concat)
            obj.heapify()
            stack.append((item1[0],item1[1],character_concat[0],'1'))
            stack.append((item2[0],item2[1],character_concat[0],'0'))
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
        # Your code
        codes={}
        codes[root_symbol] = '' 
        
        i=len(code_stack)-1
        compressed_length=0
        while i>=0:
            parent=code_stack[i][2]
            codes[code_stack[i][0]]=codes[parent] + code_stack[i][3]
            if len(code_stack[i][0]) == 1:
                compressed_length+= (code_stack[i][1] * len(codes[code_stack[i][0]]))
            i=i-1
            
        temp={}
        for j in codes:
            if len(j) == 1:
               temp[j] = codes[j]
               
        return temp, compressed_length
        
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
        string = ''
        text_file = open(text_filename,"r")
        huff_file=open(huff_filename,"w")
        huff_file.write(str(len(codes)) + ' ' + str(huff_length)+'\n')
        for i in codes:
            if i =='\n':
                huff_file.write(codes[i] + ' ' + '\\n' + '\n')
            elif i == '\t':
                huff_file.write(codes[i] + ' '  + '\\t' + '\n') 
            else:
                huff_file.write(codes[i] + ' ' + i + '\n')
        for char in text_file.read():
            string+=codes[char]
            
        temp=''
        for i in string:
            temp+=i
            if len(temp) == 8:
                huff_file.write(chr(int(temp,2)))
                temp = ''
        
        if len(temp)!=8:
            temp += '0' * (8-(len(temp)))
            huff_file.write(chr(int(temp,2)))
            
            
            
    
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
        freq_table=self.build_char_table(text_filename)
        code_stack, root_symbol=self.build_huffman_tree(freq_table,arity_exp)
        codes,compressed_length=self.form_codes( root_symbol , code_stack)
        huff_filename = text_filename + '.huff'
        self.write_compressed(text_filename, huff_filename, codes, compressed_length)
        return huff_filename
        
    
    def read_codes(self, huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
        first_line = huff.readline()
        first_line = first_line.split()
        total_character = int(first_line[0])
        compressed_length = int(first_line[1])
        i=0
        ahash ={}
        while i < total_character:
            line = huff.readline()
            line = line.split()
            if len(line) == 1:
                ahash[line[0]] = ' '
            elif line[1] == '\\t':
                ahash[line[0]] = '\t'
            elif line[1] == '\\n':
                ahash[line[0]] = '\n'
            else:
                ahash[line[0]] = line[1]
            i+=1
    
        return ahash, compressed_length
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
        string = ''
        huff_file = open(huff_filename,"r")
        ahash , compressed_length = self.read_codes(huff_file)
        bit_string = huff_file.read()
        for i in bit_string:  
            var = bin( ord(i) )
            var = var[2:]
            if(len( var ) < 8):
                extra_bit = 8 - len(var)
                var = '0' * extra_bit + var
            string += var
        string=string[0:compressed_length]
        var = ''
        filename_decompressed = huff_filename + '1'
        file_decompressed = open(filename_decompressed , "w")
        for i in string:
            var+=i
            if var in ahash:
                file_decompressed.write( ahash[var] )
                var = ''
        return filename_decompressed
        huff_file.close()
        file_decompressed.close()
if __name__ == '__main__':
    pass