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
    

    def initialise(self,nbits):
        self.NBITS=nbits    

    def build_char_table(self,filename):

        '''

        Build and return a hash that maps every character in the file 'filename' to the

        number of occurences of that char in the file'''

        file_pointer = open(filename,"r")

        charcount = {}

        for char in file_pointer.read():

            if char in charcount.keys():

                charcount[char] = charcount[char] + 1

            else:

                charcount[char] = 1

        return charcount

  

    def cmp_freq(self,char_tup1, char_tup2):

        '''

        Comparison function - compares two tuples (char, freq) on the frequency

        This is the function to be used to initialize the heap

        '''

        if(char_tup1[1] < char_tup2[1]):

            return -1

        elif(char_tup1[1]==char_tup2[1]):

            return 0

        else:

            return 1




    def pad_to_nbits(self,bitstr, pre_post, nbits = 8):

        '''

        Pad a bit string with 0's - to make it a string of length nbits.

        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end

        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory

        '''

        if pre_post<0:

            return (nbits*'0')+bitstr

        else:

            return bitstr+(nbits*'0')

        


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
        heap=Heap(True,arity_exp,self.cmp_freq)
        stack=[]
        freq_list=freq_table.items()
        heap.import_list( freq_list )
        heap.restore_heap(0)
        while(len(heap.data)>2):
            t1=heap.pop()
            t2=heap.pop()
            cs=t1[0]+t2[0]
            cs=' '+cs
            heap.data.append((cs, t1[1]+t2[1]))
            heap.restore_subtree(0)
            stack.append((t1[0], t1[1], cs, '0'))
            stack.append((t2[0], t2[1], cs, '1'))
        stack.append((heap.data[0][0], heap.data[0][1], 'rt', '0'))
        stack.append((heap.data[1][0], heap.data[1][1], 'rt', '1'))
    
        return stack,''





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

        dict_codes={'rt':root_symbol}

        code_stack = code_stack[::-1]

        compressed_length = 0

        for i in code_stack:

            dict_codes[i[0]]=dict_codes[i[2]]+str(i[3])
            
            compressed_length+=len(dict_codes[i[0]])
    
        for key in dict_codes.keys():
            if len(key) > 1:
                del dict_codes[key]
            
        return dict_codes,compressed_length 




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
        #print codes
        compressed_code=''

        binary_str=''

        fi=open(text_filename,"r")

        fread=fi.read()

        huff_file=open(huff_filename,"w")

        huff_file.write('%d %d\n' %(len(codes),huff_length))

        for key in codes.keys():

            if(key==' '):

                huff_file.write('%s %s %s\n'%(codes[key]," " ,"SPACE"))

            elif(key=='\n'):

                huff_file.write('%s %s %s\n'%(codes[key]," ","NEWLINE"))

            elif(key=='\t'):

                huff_file.write('%s %s %s\n'%(codes[key]," ","TAB"))

            else:

                huff_file.write('%s %s %s\n'%(codes[key]," ",key))

    

        for i in fread:    

        #if i in codes.keys():

            binary_str+=str(codes[i])    
    #print 'actual ' +binary_str 
        nbits=8-len(binary_str)% 8
        self.initialise(nbits)
    #print NBITS
    
        binary_str = self.pad_to_nbits(binary_str,1,nbits)

        str1=''

        for i in binary_str:

            str1+=i

            if len(str1)==8:

                compressed_code+=(chr(int(str1,2)))

                str1=''
                #print compressed_code
        huff_file.write(compressed_code)

        return huff_filename




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

        freq_table = self.build_char_table(text_filename)

        code_stack, root = self.build_huffman_tree(freq_table,arity_exp)

        codes ,huff_length = self.form_codes(root , code_stack)

        self.write_compressed(text_filename,'compressed.huff',codes,huff_length)

        return 'compressed.huff'


    def read_codes(self, huff):

        '''

        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -

        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.

        Return a hash of codes (code -> original char) and the compressed length

        '''

        l=[]

        decode_dict={}

        file=huff.readline()

        l=file.split()
    
        compressed_length = l[1]

        for i in range(int(l[0])):

            eachLine=huff.readline()

            charcode=eachLine.split()
        
            if charcode[1] == 'SPACE':
                decode_dict[charcode[0]] = ' '
            elif charcode[1] == 'NEWLINE':
                decode_dict[charcode[0]] = '\n'
            elif charcode[1] == 'TAB':
                decode_dict[charcode[0]] = '\t'
            else:
                decode_dict[charcode[0]]=charcode[1]
    #print decode_dict
        return decode_dict , compressed_length




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

        huff=open(huff_filename,"r")
        decode_dict, compressed_length = self.read_codes(huff)
        finalbit=''
        for char in huff.read():
            bit_str=''
            
            bit_str=bin((ord(char)))

            bit_str = bit_str[2:]
            
            bit_str = self.pad_to_nbits(bit_str, -1, 8 - len(bit_str))

            finalbit += bit_str
        finalbit = finalbit[:len(finalbit)-self.NBITS]
        str1 = ''
        uncompresscode = ''
        for i in finalbit:

            str1 += i

            if str1 in decode_dict.keys():
                uncompresscode += decode_dict[str1]
                str1=''
        text = open ('UNCOMP.txt' , 'w') 
        text.write(uncompresscode)
        text.close()  
        return 'UNCOMP.txt'

if __name__ == "__main__":
    pass
#self.compress('TEST',1)
#self.uncompress('compressed.huff')
            
