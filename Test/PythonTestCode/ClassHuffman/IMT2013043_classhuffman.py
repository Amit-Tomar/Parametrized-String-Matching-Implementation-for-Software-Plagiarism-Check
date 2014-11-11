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
      
    def build_char_table(self,filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        # Your code
        inp = open( filename , "r" )
        string = inp.read()
        freq = {}
        for i in string:
            if i not in freq:
                freq[i] = 0
            freq[i] += 1
        return freq
    
    
    def cmp_freq( self,char_tup1, char_tup2 ):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        temp = cmp( char_tup1, char_tup2)
        return temp
        
    def pad_to_nbits(self,bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code 
        bit_length = len( bitstr )
        extra_length = nbits - bit_length
        if pre_post < 0:
            bitstr = "0" * extra_length + bitstr
        else:
            bitstr =  bitstr + "0" * extra_length
        
        return bitstr
        
    def build_huffman_tree(self, freq_table, arity_exp ):
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
        # temp = []
    
        stack = []
        temp = [(y,x) for (x,y) in freq_table.items()]
        obj = Heap(True, arity_exp, self.cmp_freq)
        obj.import_list( temp )
        obj.heapify()
        heap = obj.data
        while obj.size() > 1 :
            heap[0] , heap[len(heap)-1] = heap[len(heap) - 1] , heap[0]
            t1 = heap.pop()
            obj.heapify()
            heap = obj.data
            heap[0], heap[len(heap) - 1] = heap[len(heap) - 1], heap[0]
            t2 = heap.pop()
            composite = (t1[0] + t2[0], t1[1] + t2[1])
            t1 = (t1[1],t1[0],composite[1],'0')
            t2 = (t2[1],t2[0],composite[1],'1')
            heap += [ composite ]
            obj.heapify()
            heap = obj.data
            stack += [ t1 , t2 ]
        return stack, heap[0]
                    
        
    def form_codes(self,root_symbol,code_stack):
        
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
        
        code = {}
        compressed_length = 0
        while ( len(code_stack) ) > 0:
            tup = code_stack.pop()
            char = tup[0]
            freq = tup[1]
            parent = tup[2]
            bit = tup[3]
            if parent in code:
                code[char] = code[parent] + bit
                if len(char) == 1:
                    compressed_length += freq * len(code[char])
            else:
                code[char] = bit
                if len(char) == 1:
                    compressed_length += freq * len( code[char] )
        code_final = {}
        
        for i in code:
            if len(i) <= 1:
                code_final[i] = code[i]
        
        return code_final,compressed_length
                    
            
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
        
        inp = open(text_filename,"r")
        code_length = str(len(codes))
        huff = str(huff_length)
        out = open(huff_filename,"w")
        out.write(code_length + ' ' + huff + '\n')
        for i in codes:
            if i == '\n':
                out.write(codes[i] + ' ' + '\\n' + '\n')
            elif i=='\t':
                out.write(codes[i] + ' ' + '\\t' + '\n')
            else:
                out.write(codes[i] + ' ' + i + '\n')
        Str = ''
        text = inp.read()
        for i in text:
            Str += codes[i]
            
        temp = ''
        for i in Str:
            temp += i
            if len(temp) >= 8:
                out.write(chr(int(temp,2)))
                temp =''
                
        temp = self.pad_to_nbits(temp,3,8)
        out.write( chr( int(temp,2) ) )
                
    
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
        
        table = self.build_char_table(text_filename)
        
        stack, root = self.build_huffman_tree(table,arity_exp)
        
        code, compressed_length = self.form_codes(root,stack)
        
        self.write_compressed( text_filename , text_filename + '.huff' , code , compressed_length)
        
        return text_filename + '.huff'
    
    def read_codes(self,huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        ''' 
        # Your code
        
        line = huff.readline()
        line = line.split()
        no_char = int(line[0])
        compressed_length = int(line[1])
        codes = {}
        i = 0
        
        while i < no_char:
            line = huff.readline()
            line = line.split()
            if len(line) == 1:
                codes[line[0]]=' '
            elif line[1] == '\\t':
                codes[line[0]]='\t'
            elif line[1] == '\\n':
                codes[line[0]]='\n'
            else:
                codes[line[0]]=line[1]
            i+=1
            
        return codes , compressed_length
        
        
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
    
        huff = open(huff_filename,"r")
        codes , compressed_length = self.read_codes(huff)
        string = ''
        bit_string = huff.read()
        for i in bit_string:  
            temp = bin( ord(i) )
            temp = temp[2:]
            if(len( temp ) < 8):
                extra_bit = 8 - len(temp)
                temp = '0' * extra_bit + temp
            string += temp
        string=string[0:compressed_length]
        temp = ''
        decompressed_filename = huff_filename + '1'
        decompressed_file = open(decompressed_filename , "w")
        for i in string:
            temp+=i
            if temp in codes:
                decompressed_file.write( codes[temp] )
                temp = ''
        return decompressed_filename
        huff.close()
        decompressed_file.close()
        return decompressed_filename

         

if __name__ == '__main__':
    pass
