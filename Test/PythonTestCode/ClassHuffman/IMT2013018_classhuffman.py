'''
Created on 13-Nov-2013

@author: k.vasundhara
'''
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
    def initialise(self, size_str):
        self.size_str=size_str
        
    def build_char_table(self,filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        # Your code
        f=open(filename,'r')
        s=f.read()
        freq_table={}
        for i in s:
            if i not in freq_table.keys():
                freq_table[i]=1
            else:
                freq_table[i]+=1
        return freq_table
            
    def cmp_freq(self, char_tup1, char_tup2):
        '''
        Companotrison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        if char_tup1[1]>char_tup2[1]:
            return 1
        elif char_tup1[1]<char_tup2[1]:
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
        if pre_post<0:
            return (nbits-len(bitstr))*'0'+bitstr
        else:
            return bitstr + (nbits-len(bitstr))*'0'

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
        # Your code
        heap=Heap(True,arity_exp,self.cmp_freq)  
        s=[]
        freq_list=freq_table.items()
        heap.import_list( freq_list )
        heap.restore_heap(0)
        while(len(heap.DATA)>2):
            t1=heap.pop()
            t2=heap.pop()
            cs=t1[0]+t2[0]
            cs=' '+cs
            heap.DATA.append((cs, t1[1]+t2[1]))
            heap.restore_subtree(0)
            s.append((t1[0], t1[1], cs, '0'))
            s.append((t2[0], t2[1], cs, '1'))
        s.append((heap.DATA[0][0], heap.DATA[0][1], 'rt', '0'))
        s.append((heap.DATA[1][0], heap.DATA[1][1], 'rt', '1'))
    
    
        return s,''
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
        code_hash={'rt':''}
        compressed_length=0
        code_stack.reverse()
        for tup in code_stack:
            code_hash[tup[0]]=code_hash[tup[2]]+tup[3]
            compressed_length+=len(code_hash[tup[0]])
        for k in code_hash.keys():
            if len(k)>1:
                del code_hash[k]
        return code_hash,compressed_length
    

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
        temp=''
        code=''
        ascii_code=''
        fpw=open(huff_filename, "w")
        fpr=open(text_filename, "r")
        fpw.write('%d %d\n' % (len(codes), huff_length))
        for key in codes.keys():
                if key == ' ':
                    fpw.write("%s space\n" % codes[key])
                elif key == '\n':
                    fpw.write("%s new\n" % codes[key])
                elif key == '\t':
                    fpw.write("%s tab\n" % codes[key])
                elif key == '\\':
                    fpw.write("%s back\n" % codes[key])
                elif key == '\r':
                    fpw.write("%s rrr\n" % codes[key])
                else:
                    fpw.write("%s %s\n" % (codes[key], key))
        for i in fpr.read():
            temp+=codes[i]
        size_str = len(temp)
        self.initialise(size_str)
        for i in temp:
            code+=i
            
            if len(code)==8:
                ascii_code+=chr(int(code,2))
                code=''
        
        if len(code) != 8:     
            code=self.pad_to_nbits(code, 1, 8)
            ascii_code+=chr(int(code,2))
        
        fpw.write(ascii_code)
        fpw.close()
        fpr.close()
        
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
        code_stack, root_symbol=self.build_huffman_tree(freq_table, arity_exp)
        codes,huff_length=self.form_codes(root_symbol, code_stack)
        self.write_compressed(text_filename, text_filename+'huff', codes, huff_length) 
        
        return text_filename+'huff'

    def read_codes(self, huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
        code_hash={}
        line=huff.readline()
        line=line.split()
        count=int(line[0])
        compressed_length=int(line[1])
        for i in range(count):
            s=huff.readline()
            s=s.split()
            if s[1] == 'space':
                code_hash[s[0]] = ' '
            elif s[1] == 'new':
                code_hash[s[0]] = '\n'
            elif s[1] == 'tab':
                code_hash[s[0]] = '\t'
            elif s[1] == 'back':
                code_hash[s[0]] = '\\'
            elif s[1] == 'rrr':
                code_hash[s[0]] = '\r'
            else:
                code_hash[s[0]]=s[1]
        huff.close()
        return code_hash, int(compressed_length)
    
    

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
        char=''
        fp_write=open(huff_filename+'1', "w")
        fp_read=open(huff_filename, "r")
        binary_letter_hash, compressed_length=self.read_codes(fp_read)
        fp_read=open(huff_filename, "r")
        for i in range(len(binary_letter_hash)+1):
            fp_read.readline()
        s=fp_read.read()
        bits=''
        for code in s:
            bin_str=bin(ord(code))
            binary_str=bin_str[2:]
            binary_str=self.pad_to_nbits(binary_str, -1, 8)
            bits+=binary_str
        temp=''
        bits=bits[:(self.size_str)]
    
        for b in bits:
            temp+=b
            if temp in binary_letter_hash.keys():
                    char=binary_letter_hash[temp]
                    temp=''
                    fp_write.write(char)
        fp_read.close()
        fp_write.close()
        return huff_filename+'1'
    

if __name__ == '__main__':
    pass
#h=Huffman()
#h.compress('text3',1)

