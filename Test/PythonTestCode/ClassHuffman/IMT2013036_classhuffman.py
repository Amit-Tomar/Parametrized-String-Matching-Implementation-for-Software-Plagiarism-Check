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
    NBITS=0
    def initialize(self,nbit):
       
        NBITS=nbit
    
    def build_char_table(self,filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        # Your code
        f=open(filename,"r")
        freq_table = {}
        for i in f.read():
            if (freq_table.has_key(i)):
                freq_table[i] += 1
            else:
                freq_table[i] = 1
               
        f.close()
        return freq_table
    
    def cmp_freq(self,char_tup1, char_tup2):
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
    
    def pad_to_nbits(self,bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code
        if pre_post<0:
            return '0'*nbits+bitstr
        else:
            return bitstr+'0'*nbits
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
        stack=[]
        heap=Heap(True,arity_exp,self.cmp_freq)
        #heap.initialize_heap(True,arity_exp,self.cmp_freq)
        for ele in freq_table:
            heap.add((ele,freq_table[ele]))
        
        while (len(heap.DATA)>2):
            pop=heap.pop()
            pop1=heap.pop()
            composite=(pop[0]+pop1[0],pop[1]+pop1[1])
            stack.append((pop[0],pop[1],composite[0],'0'))
            stack.append((pop1[0],pop1[1],composite[0],'1'))
            heap.add(composite)
           
        stack.append((heap.DATA[0][0],heap.DATA[0][1],'root','0'))
        stack.append((heap.DATA[1][0],heap.DATA[1][1],'root','1'))
       
        return stack,''
    
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
        code={'root':root_symbol}
        compressed_length=0
        code_stack=code_stack[::-1]
        for c in range(len(code_stack)):
            code[code_stack[c][0]]=code[code_stack[c][2]]+code_stack[c][3]
            compressed_length+=len(code[code_stack[c][0]])*code_stack[c][1]
           
        for i in code.keys():
            if(len(i)>1):
                del code[i]
        return code, compressed_length
    
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
        text_read=open(text_filename,"r")
        text_write=open(huff_filename,"w")
        text_write.write('%d %d \n' %(len(codes),huff_length))
        for k in codes.keys():
            if k==' ':
                text_write.write(codes[k]+' space\n')
            elif k=='\n':
                text_write.write(codes[k]+' newline\n')
            elif k=='\t':
                text_write.write(codes[k]+' tab\n')
            elif k=='\\':
                text_write.write(codes[k]+' back\n')
            else:
                text_write.write(codes[k]+' '+k+'\n')
        binary=''
        temp=''
        compressed=''
        for char in text_read.read():
            temp=temp+str(codes[char])
        for i in temp:
            binary+=i
            if len(binary)==8:
                compressed+=chr(int(binary,2))
                binary=''
        if len(binary)!=0:
            compressed += chr(int(self.pad_to_nbits(binary , 1 , 8-len(binary)) , 2))
        text_write.write(compressed)
        text_write.close()
           
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
        freq_table=self.build_char_table(text_filename)
        code_stack , root =self.build_huffman_tree(freq_table, arity_exp)
        code,count=self.form_codes(root,code_stack)
        self.write_compressed(text_filename, 'huff_test.huff', code, count)
        return 'huff_test.huff'
    
    def read_codes(self,huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
        huff_list = huff.readline()
        huff_list = huff_list.split()
        compressed_length = huff_list[1]
        code_dict = {}
        for i in range(int(huff_list[0])):
            l = huff.readline()
            l = l.split()
            if l[1] == 'space':
                code_dict[l[0]] = ' '
            elif l[1] == 'newline':
                code_dict[l[0]] = '\n'
            elif l[1] == 'tab':
                code_dict[l[0]] = '\t'
            elif l[1] == 'back':
                code_dict[l[0]] = '\\'
            else:
                code_dict[l[0]]=l[1]
        return code_dict,compressed_length
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
        huff=open(huff_filename,'r')
        codes , length =self.read_codes(huff)
        t=''
        p=''
        for i in huff.read():
            p=bin(ord(i))[2:]
            t+=self.pad_to_nbits(p,-1,8-len(p))
        t1=''
        t2=''
        t=t[:len(t)-self.NBITS-6]
        for i in t:
            t1+=i
            if t1 in codes.keys():
                t2+=codes[t1]
                t1=''
        uncompress_file=open("huff_write",'w')
        uncompress_file.write(t2)
        return 'huff_write'

if __name__ == '__main__':
    pass