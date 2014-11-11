'''
Created on 23-Oct-2013

@author: raghavan
'''
# Importing the Heap class from classheap
from classheap import Heap

global extra_bits



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
        fptr=open(filename,"r")
        file_data = fptr.read()
        fptr.close()
        
        freq={}
        
        for i in file_data:
            freq[i] = 0
        
        for i in file_data:
            freq[i] += 1
        
        return freq
        # Your code


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
        # Your code


#def pad_to_nbits(bitstr, pre_post, nbits = 8):
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
        (vii) Return the stack along with the top root element of the heap
        '''
        
        freq_list = []
        
        for key in freq_table:
            freq_list.append((key, freq_table[key]))
        
        stack = []
        
        heap = Heap(True, 1, self.cmp_freq)   
        #heap.initialize_heap(True , arity_exp, cmp_freq)
        heap.import_list(freq_list)
        heap.heapify()
        
        while(heap.size()>1):
            element1 = heap.pop()
            element2 = heap.pop()
            
            parent = element1[0]+element2[0]
            
            heap.add((parent,element1[1]+element2[1]))
               
            stack.append((element1[0],element1[1],parent,'0'))
            stack.append((element2[0],element2[1],parent,'1'))
        
        return stack, heap.get_item_at(0)
        # Your code


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
        
        code_char = {}
        code_char[root_symbol[0]] = ''
        compressed_length = 0
        
        
        i = len(code_stack)-1
        while(i>=0):
            tuple = code_stack[i]
            code_char[tuple[0]] = code_char[tuple[2]]+tuple[3]
                
            if(len(tuple[0])==1):
                compressed_length += len(code_char[tuple[0]])*tuple[1]
            
            
            i -= 1
        
        for key, value in code_char.items():
            if(len(key) != 1):
                del code_char[key]
        
        return code_char, compressed_length
        # Your code

    
    def write_compressed( self, text_filename , huff_filename , codes , huff_length):
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
        
        global extra_bits
        distinct_inputs = 0
        
        fptr=open(text_filename, "r")
        file_content = fptr.read()
        fptr.close()
        
        
        for key in codes:
            distinct_inputs += 1
        
        fptr = open(huff_filename, "w")
        fptr.write(str(distinct_inputs) + ' ' + str(huff_length) + '\n')
        
        for key in codes:
            if(key == '\n'):
                fptr.write('\\n' + ' ' + codes[key] + '\n')
            elif(key == '\t'):
                fptr.write('\\t' + ' ' + codes[key] + '\n')
            else:
                fptr.write(key + ' ' + codes[key] + '\n')
        
        
        converted_code = ''
        val = ''
            
        for elem in file_content:
            converted_code += codes[elem] 
            
            while(len(converted_code)>=8):
                val = converted_code[:8]
                converted_code = converted_code[8:]
                fptr.write(chr(int(val,2)))
        
        extra_bits = 8-len(converted_code)
        converted_code += ('0'*extra_bits)
        fptr.write(chr(int(converted_code, 2)))
               
        fptr.close()    
        
        return huff_filename
        # Your code    
        

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
        freq = self.build_char_table(text_filename)
            
        stack,root_element = self.build_huffman_tree(freq, arity_exp)
        
        code_char,compressd_length = self.form_codes(root_element, stack)
        
        file_name = text_filename + ".txt"
        self.write_compressed(text_filename , file_name , code_char, compressd_length )  
        
        return file_name
        # Your code


    def read_codes(self, huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        
        huff--->file pointer
        '''
        
        #global huff
        codes = {}
        
        content_list = []
        content = huff.readline()
        content_list = content.split()
        
        global codes_length 
               
        codes_length = int(content_list[0])
        compressed_length = int(content_list[0])
        
        i = 0
        while(i<codes_length):
            content_list = (huff.readline()).split()
            if(len(content_list)==1):
                codes[content_list[0]] = ' '
            elif( content_list[0] =='\\n'):
                codes[content_list[1]] = '\n'
            elif( content_list[0] =='\\t'):
                codes[content_list[1]] = '\t'
            else:
                codes[content_list[1]] = content_list[0]
            
            i += 1
        
        return codes
        # Your code
    

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
        
        global extra_bits
        
        uncompressed_file = huff_filename+ "huffcls.txt"
        
        file_pointer = open(huff_filename, "r")
        codes = self.read_codes(file_pointer)
           
        file_content = file_pointer.read()
            
        file_pointer.close()
        
        file_pointer = open(uncompressed_file, "w")
        val = ''
        
       
        code_file = ''
        i = 0
        
        while(i<len(file_content)):
            val = bin(ord(file_content[i]))
            val = val[2:]
            if(len(val)<8):
                val = '0'*(8-len(val))+val
            if((i+1)==len(file_content)):
                val = val[:(8-extra_bits)]
                   
            for elem in val:
                code_file += elem
                if((code_file in codes) == True):
                    file_pointer.write(codes[code_file])
                    code_file = ''
            
            i += 1    
                  
        file_pointer.close()
            
        return uncompressed_file
        # Your code

    
    
    
    
    # Your code
    # Add all the Huffman class methods here


if __name__ == '__main__':
    pass