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

    
    def build_char_table(self,filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        # Your code
        
        chash = {}
        fopen = open(filename, 'r')
        chash1 = list(fopen.read())
        
        for i in chash1:
            chash[i] = 0
            
        for i in chash1:
            chash[i] = chash[i] + 1
        fopen.close()    
        return chash
    
    def cmp_freq(self,char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        a = char_tup1[1]
        b = char_tup2[1]
        if (a > b):
            return a
        else :
            return b
        
    def pad_to_nbits(self,bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code
        if (pre_post < 0):
            if (len(bitstr) < nbits):
                a = nbits - len(bitstr)
                while (len(str) < 8):
                    bitstr = '0' + bitstr
                    a = a - 1
            return bitstr       
                     
        elif (pre_post > 0):
            if (len(bitstr) < nbits):
                a = nbits - len(bitstr)
                while (len(str) <= 8):
                    bitstr = bitstr + '0'
                    a = a - 1
            return bitstr
            
        
    
    def build_huffman_tree(self,freq_table, arity_exp):
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
    
        return_list = [(y,x) for (x,y) in freq_table.items()]
        heap=Heap(True,arity_exp,self.cmp_freq)
        
        return_stack = []
       
        heap.data = return_list
        heap.heapify()
        while(len(return_list) > 1):
            heap1 = return_list.pop()
            heap.heapify()
            heap2= return_list.pop()
            heap.heapify()
            new = (heap1[0]+heap2[0], heap1[1]+heap2[1])
            return_stack.append((heap1[1], heap1[0], heap1[1] + heap2[1], '0'))
            return_stack.append((heap2[1], heap2[0], heap1[1] + heap2[1], '1'))
            return_list.append(new)
        
        return (return_stack,return_list[0])
    
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
        main_hash = {}
        return_stack = code_stack[0]
        return_stack.reverse()
        final_hash = {}
        code_hash = {}
        code_hash[return_stack[0][2]] = ''
        for element in return_stack:
            code_hash[element[0]] = code_hash[element[2]] + element[3]
            if len(element[0]) <= 1:
                main_hash[element[0]] = element[1]
        for key,value in code_hash.items():
            if len(key) <= 1:
                final_hash[key] = value
                
        compressed_length  = 0
        for key in main_hash:
            temp = main_hash[key]*len(final_hash[key])
            compressed_length = compressed_length + temp
            
        return final_hash, compressed_length  
       
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
           
        fopen = open(text_filename,"r")
        fwrite = open(huff_filename,"w")
        fopen = fopen.read()
        
        blank = ''
        for a in codes:
            if (a == '\n'):
                fwrite.write(codes[a] + ' ' + '\\n' + '\n')
            elif (a == '\t'):
                fwrite.write(codes[a] + ' ' + '\\n' + '\n')
            else:
                fwrite.write(codes[a] + ' ' + a + '\n')
        for i in fopen:
            blank = blank + codes[i]
        final = ''
        for i in blank:
            final = final + i
            if (len(final) == 8):
                y = int(final,2)
                fwrite.write(chr(y))
                final = ''
                
        finalise = 8 - len(final)
        final = final + '0'*finalise
        fwrite.write(chr(int(final,2)))
        
    
    def compress(self,text_filename, arity_exp):
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
        frequency_table = self.build_char_table(text_filename)
        code_stack = self.build_huffman_tree(frequency_table,arity_exp)
        codes = self.form_codes('',code_stack)[0]
        compressedfile = text_filename + '.huff'
        huff_length = len(codes)
        self.write_compressed(text_filename,compressedfile,codes,huff_length)
        return text_filename + '.huff'
        
        
    
    
    def read_codes(self,huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
        global var
        hashcodes = {}
        a = 0
        rlist = []
        readin = huff.readlines()
        for i in readin:
            rlist.split()
            a = a + 1
            if (a == 1):
                var = rlist[0]
            elif (len(rlist) == 1):
                hashcodes[rlist[0]] = ''
            else:
                hashcodes[rlist[1]] = rlist[0]
            if (a > int(var)):
                break
        return hashcodes
             
        
    
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
        fopen = open(huff_filename,"r")
        writein = open(huff_filename+'new',"w")
        line_elements = fopen.readline()
        line_elements = line_elements.split()
        comp_len = int(line_elements[1])
        comp_char = int(line_elements[0])
        binary_string = ''
        a = 0
        while(a < comp_char):
            fopen.readline()
            a = a + 1
        newfile = fopen.read()
    
        for a in newfile:
            ascii_code = ord(a)
            binary_conversion = bin(ascii_code)[2:]
            binary_length = len(binary_conversion)
            a = 8 - binary_length
            while (a < 0):
                binary_conversion = '0' + binary_conversion
                a = a - 1
            binary_string = binary_string + str(binary_conversion)
        binary_string = binary_string[:comp_len]
        fopen.close()
        empty = ''
        fopen = open(huff_filename,'r')
        code_hash = self.read_codes(fopen)
        for a in binary_string:
            empty = empty + a
            if empty in code_hash:
                if(code_hash[empty] == '\\t'):
                    writein.write('\t')
                elif(code_hash[empty] == '\\n'):
                    writein.write('\n')
                else:
                    writein.write(code_hash[empty])
                empty = ''
                
        fopen.close()
        writein.close()
        return huff_filename + 'new'
    if __name__ == '__main__':
        pass
        