'''
Created on 23-Oct-2013

@author: raghavan
'''
# Importing the Heap class from classheap
from classheap import Heap

class Huffman(object):
    '''
    Created on 28-Oct-2013
    
    @author: raghavan
    '''
    
        
    def build_char_table(self, filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        filer = open(filename,'r')
        fcon = filer.read()
        filer.close()
        freq_table = {}
        for elem in fcon:
            freq_table[elem] = 0
        for elem in fcon:
            freq_table[elem] += 1
        return freq_table
        # Your code
        
    def cmp_freq(self, char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
         '''
        if (char_tup1[1] > char_tup2[1]):
            return 1
        elif (char_tup1[1] < char_tup2[1]):
            return -1
        else :
            return 0
    
    def build_huffman_tree(self, freq_table, arity_exp):
        '''
        Build the huffman tree for the input textfile and return a stack (maybe along with the character at the root node)
        Algo: (i) Start by making a heap out of freq_table using heap
        (ii) Pop two elements out of the heap at a time
        (iii) Form a composite character that is the concatenation of the two and the combined frequency of the two
        (iv) Add the new composite character with its frequency to the heap
        (v) Add the two popped elements to a stack - simply append to a list
        Elements of the stack are of the form (element, frequency, parent, additional_code_bit)
        (vi) Repeat the above four steps till the heap has only the root element left
        (vii) Return the stack along with the top root element of the heap
        '''
        
        heap = Heap(True, arity_exp, self.cmp_freq)
        for elem in freq_table:
            heap.add((elem, freq_table[elem]))
        
        
        stack = []
        
        while (heap.size()>1):
            
            (char1, freq1) = heap.pop()
            (char2, freq2) =  heap.pop()
            new_char = char1+char2
            new_char_freq = freq1+freq2
            heap.add((new_char, new_char_freq))
            stack.append((char1, freq1, new_char,'0'))
            stack.append((char2, freq2, new_char,'1'))
        (finalchar, finalfreq) = heap.pop()
        return stack, (finalchar, finalfreq , None ,'')
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
        final_codes = {}
        final_codes[root_symbol[0]] = ''
        compressed_length = 0
        temp_stack = code_stack[:]
        temp_stack.reverse()
        for elem in temp_stack:
            final_codes[elem[0]] = final_codes[elem[2]]+elem[3]
            if len(elem[0])==1:
                compressed_length += (len(final_codes[elem[0]])*elem[1])
        huffman_hash = {}
        for elem in final_codes:
            if len(elem)==1:
                huffman_hash[elem] = final_codes[elem]
        return huffman_hash, compressed_length
                
        
        # Your code
    
    
    def write_compressed(self, text_filename, huff_filename, \
                          codes, huff_length):
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
        org_file = open(text_filename,'r')
        huff_file = open(huff_filename, 'w')
        huff_file.write(str(len(codes))+' '+str(huff_length)+'\n')
        for code in codes:
            huff_file.write(codes[code] + ' ' + code +'\n')
        fcon = org_file.read()
        bitstring = ''
        for i in fcon:
            bitstring += codes[i]
        if(len(bitstring)%8 != 0):
            bitstring += ('0'*(8-(len(bitstring)%8)))
        agg = ''
        for bit in bitstring:
            agg += bit
            if(len(agg)==8):
                huff_file.write(chr(int(agg, 2)))
                agg = ''
        org_file.close()
        huff_file.close()
        
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
        freq_hash = self.build_char_table(text_filename)
        huffman_stack, root_element = self.build_huffman_tree(freq_hash, \
                                                               arity_exp)
        codes, compressed_length = self.form_codes(root_element, huffman_stack)
        self.write_compressed(text_filename, "huff_file", codes, \
                              compressed_length)
        return "huff_file"
        # Your code
    
    
    def read_codes(self, huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        code_stack = {}
        temp = (huff.readline()).split()
        code_stack_length = int(temp[0])
        compressed_length = int(temp[1])
        i = 0
        while(i<code_stack_length):
            
            temp = (huff.readline()).split(' ')
            if(temp[1]==''):
                code_stack[temp[0]] = chr(32)
            elif(temp[1]=='\n'):
                code_stack[temp[0]] = temp[1]
                huff.readline()
            else:
                temp[1] = temp[1][:1]
                code_stack[temp[0]] = temp[1]
            i += 1
        return code_stack, compressed_length
        
        
    
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
        decode = open(huff_filename, 'r')
        decoded = open('final', 'w')
        codes, compressed_length = self.read_codes(decode)
        compressedcode = decode.read()
        temp_file = open("temp1", 'w')
        for charac in compressedcode:
            temp = str(bin(ord(charac)))
            #print temp,
            temp = temp[2:]
            if len(temp)<8:
                temp = ('0'*(8-len(temp)))+temp
            temp_file.write(temp)
            #print temp
        temp_file.close()
        temp_file = open("temp1", 'r')
        filecontents = temp_file.read()
        string = ''
        count = 0
        for character in filecontents:
            string += character
            count += 1
            #print string, count
            if count == compressed_length:
                decoded.write(codes[string])
                break
            if string in codes:
                decoded.write(codes[string])
                string = ''
        decoded.close()
        return 'final' 
    # Your code
    
    
    # Your code
    # Add all the Huffman class methods here


if __name__ == '__main__':
    pass