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
    #Your code
        cHash = {}
        texttmp = open(filename, "r")
        text = texttmp.read()
        for x in text:
            if x in cHash:
                cHash[x] += 1
            else:
                cHash[x] = 1
        return cHash

    def cmp_freq(self, char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        if char_tup1 > char_tup2:
            return 1
        if char_tup1 < char_tup2:
            return -1
        if char_tup1 == char_tup2:
            return 0
        
    def pad_to_nbits(self,bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code
    
        num = nbits - len(bitstr)
        newbitstr = ''
        if pre_post < 0:
            newbitstr = ('0' * num) + bitstr
        else:
            newbitstr = bitstr + ('0' * num)
        return newbitstr
    
    
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
        # Your code
        self.modheap.initialize_heap(True, arity_exp, self.cmp_freq)
        for every_elem in freq_table:
            tup = (freq_table[every_elem], every_elem)
            self.modheap.add(tup)
        stack = []
        while(len(self.modheap.DATA) >= 2):
            s1 = self.modheap.pop()
            s2 = self.modheap.pop()
            t1 = (s1[1], s1[0], s1[1]+s2[1], '1')
            t2 = (s2[1], s2[0], s1[1]+s2[1], '0')
            stack.append(t1)
            stack.append(t2)
            composite_elem = (s1[0]+s2[0], s1[1]+s2[1])
            self.modheap.add(composite_elem)
        lastelem = self.modheap.DATA[0]
        last = (lastelem[0], lastelem[1], None, '')
        return stack, last
           
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
        codes = {}
        codes[root_symbol[1]] = ''
        compressed_len = 0
        for x in range(len(code_stack)):
            elem = code_stack[len(code_stack) - x -1]
            codes[elem[0]] = codes[elem[2]] + elem[3]
            if(len(elem[0])==1):
                compressed_len += len(codes[elem[0]]) * elem[1]
        for i in codes.keys():
            if len(i) > 1:
                del codes[i]
        return codes, compressed_len
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
        compressed_str = open(huff_filename, "w")
        firstline = str(len(codes.keys())) + ' ' + str(huff_length) + '\n'
        compressed_str.write(firstline)
        for x in codes.keys():
            if x == '\n' :
                line = str(codes[x]) + ' ' + '\\n' + '\n'
            elif x == '\t' :
                line = str(codes[x]) + ' ' + '\\t' + '\n'
            else :
                line = str(codes[x]) + ' ' + str(x) + '\n'
            compressed_str.write(line)
        texttmp = open(text_filename, 'r')
        text = texttmp.read()
        bitstring = ''
        count = 0
        for letter in text:
            for x in str(codes[letter]):
                bitstring += x
                count += 1
                if count == 8:               
                    bitstring += ' '
                    count = 0
        chars = bitstring.split()
       
        if len(chars[-1]) < 8:
            chars[-1] = self.pad_to_nbits(chars[-1], 1, 8)
        
        for elem in chars:
            compressed_str.write(chr(int(elem, 2)))
            
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
        freq = self.build_char_table(text_filename)
        the_stack, sym = self.build_huffman_tree(freq, arity_exp)
        code_dict, huff_comp_len = self.form_codes(sym, the_stack)
        self.write_compressed(text_filename, text_filename + ".huff", code_dict, huff_comp_len)
        return text_filename + ".huff"
    
    def read_codes(self,huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
        templist = huff.readline().split()
        uni_elems = int(templist[0])
        code_hash = {}
        comp_length = int(templist[1])
        for x in range(int(uni_elems)):
            code_list = huff.readline().split()
            if len(code_list) == 2:
                code_hash[code_list[0]] = code_list[1]
        return code_hash, comp_length, uni_elems
        
        
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
        '''
        huff_filehandle=open(huff_filename,'r')
        uncompressed_str=open(huff_filename + '1','w')
        hash_codes,compressed_len,no_codes=read_codes(huff_filehandle)
        huff_filehandle.close()
        huff_filehandle=open(huff_filename,'r')
        for i in range(no_codes+1):
            dummy=huff_filehandle.readline()
        compressed_str=huff_filehandle.read()
        bit_str=''
        for c in compressed_str:
            bitstream=bin(ord(str(c)))[2:]
    #         for i in range(2,len(bitstream)):
    #             bit_str+=i
            bit_str+=bitstream
        temp=''
        count=0
        for bit in bit_str:
            temp+=bit
            while(count<=compressed_len):
                if temp in hash_codes.keys():
                    uncompressed_str.write(str(hash_codes[temp]))
                    temp=''
                    count+=1
        return huff_filename + '1'
        '''
        code_file = read_codes(open(huff_filename))
        comp_file = open(huff_filename)
        recv_file = open(huff_filename + '1', "w")
        no_of_char, length = comp_file.readline().split()
        no_of_char, length = int(no_of_char), int(length)
        codes = {}
        i = 0
        while i < no_of_char:
            line = comp_file.readline().split()
            if(len(line) == 1):
                codes[line[0]] = ' '
            elif(line[1] == '\\n'):
                codes[line[0]] = '\n'
            elif(line[1] == '\\t'):
                codes[line[0]] = '\t'
            else:
                codes[line[0]] = line[1]
            i += 1
        string = ''
        for j in comp_file.readlines():
            for i in j:
                temp = bin(ord(i))[2:]
                temp = self.pad_to_nbits(temp, -1)
                string += temp
        string = string[:length]
        temp = ''
        for i in string:
            temp += i
            if temp in codes:
                recv_file.write(codes[temp])
                temp = ''
        return huff_filename + '1'
        
        


if __name__ == '__main__':
    pass