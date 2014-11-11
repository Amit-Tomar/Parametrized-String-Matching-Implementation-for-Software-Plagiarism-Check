''''

Created on 28-Oct-2013




@author: raghavan

'''

import modheap

NBITS = 0

def initialize(nbits):
    global NBITS
    NBITS = nbits    

def build_char_table(filename):

    '''

    Build and return a hash that maps every character in the file 'filename' to the

    number of occurences of that char in the file'''

    file_table = open(filename,"r")

    hash1 = {}

    for char in file_table.read():

        if char in hash1.keys():

            hash1[char] = hash1[char] + 1

        else:

            hash1[char] = 1

    return hash1

  

def cmp_freq(char_tup1, char_tup2):

    '''

    Comparison function - compares two tuples (char, freq) on the frequency

    This is the function to be used to initialize the heap

    '''

    if(char_tup1[1] < char_tup2[1]):

        return -1

    elif(char_tup1[1] == char_tup2[1]):

        return 0

    else:

        return 1




def pad_to_nbits(bitstr, pre_post, nbits = 8):

    '''

    Pad a bit string with 0's - to make it a string of length nbits.

    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end

    This might be a good helper function to have -- this function is just a suggestion, it is not mandatory

    '''

    if pre_post < 0:

        return (nbits * '0') + bitstr

    else:

        return bitstr + (nbits * '0')

        

        
def build_huffman_tree(freq_table, arity_exp):

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

    s = []

    freq_list = freq_table.items()

    modheap.initialize_heap(True, arity_exp, cmp_freq)

    modheap.import_list( freq_list )

    modheap.restore_heap(0)

    while(len(modheap.DATA)>2):

        t1 = modheap.pop()

        t2 = modheap.pop()

        cs = t1[0] + t2[0]

        cs = ' ' + cs

        modheap.DATA.append((cs, t1[1] + t2[1]))

        modheap.restore_subtree(0)

        s.append((t1[0], t1[1], cs, '0'))

        s.append((t2[0], t2[1], cs, '1'))

    s.append((modheap.DATA[0][0], modheap.DATA[0][1], 'rt', '0'))

    s.append((modheap.DATA[1][0], modheap.DATA[1][1], 'rt', '1'))
    
    return s, ''





def form_codes(root_symbol, code_stack):

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

        dict_codes[i[0]] = dict_codes[i[2]]+str(i[3])
            
        compressed_length += len(dict_codes[i[0]])
    
    for key in dict_codes.keys():
        if len(key) > 1:
            del dict_codes[key]
            
    return dict_codes, compressed_length 




def write_compressed(text_filename, huff_filename, codes, huff_length):

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
   
    compressed_code = ''

    binary_str = ''

    fi = open(text_filename,"r")

    fread = fi.read()

    huff_file = open(huff_filename,"w")

    huff_file.write('%d %d\n' %(len(codes), huff_length))

    for key in codes.keys():

        if(key == ' '):

            huff_file.write('%s %s %s\n'%(codes[key]," " ,"SPACE"))

        elif(key == '\n'):

            huff_file.write('%s %s %s\n'%(codes[key]," ","NEWLINE"))

        elif(key == '\t'):

            huff_file.write('%s %s %s\n'%(codes[key]," ","TAB"))

        else:

            huff_file.write('%s %s %s\n'%(codes[key]," ",key))

    

    for charcter in fread:    

            binary_str += str(codes[character])  
 
    nbits = 8-len(binary_str)% 8
    
    initialize(nbits)

    binary_str = pad_to_nbits(binary_str,1,nbits)

    ascii_str = ''

    for bitstr in binary_str:

        ascii_str += bitstr

        if len(ascii_str) == 8:

            compressed_code += (chr(int(ascii_str, 2)))

            ascii_str = ''
   
    huff_file.write(compressed_code)

    return huff_filename




def compress(text_filename, arity_exp):

    '''

    Compress a give text file 'text_filename' using a heap with arity 2^arity_exp

    Algo: (i) Build the frequency table

    (ii) Build code stack by building the huffman tree from the frequency table

    (iii) Form the codes from the code stack

    (iv) Write out the compressed file

    Return the name of the compressed file. Might help to have a convention here - the original file name without the extension

    appended with '.huff' could be one way.

    '''

    freq_table = build_char_table(text_filename)

    code_stack , root = build_huffman_tree(freq_table , arity_exp)

    codes , huff_length = form_codes(root , code_stack)

    write_compressed(text_filename ,'compressed.huff', codes , huff_length)

    return 'compressed.huff'


def read_codes(huff):

    '''

    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -

    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.

    Return a hash of codes (code -> original char) and the compressed length

    '''

    l = []

    decode_dict = {}

    fin = huff.readline()

    l = fin.split()
    
    compressed_length = l[1]

    for i in range(int(l[0])):

        eachLine = huff.readline()

        charcode = eachLine.split()
        
        if charcode[1] == 'SPACE':
            decode_dict[charcode[0]] = ' '
        elif charcode[1] == 'NEWLINE':
            decode_dict[charcode[0]] = '\n'
        elif charcode[1] == 'TAB':
            decode_dict[charcode[0]] = '\t'
        else:
            decode_dict[charcode[0]] = charcode[1]
    
    return decode_dict , compressed_length
    



def uncompress(huff_filename):

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

    huff = open(huff_filename,"r")
    decode_dict , compressed_length = read_codes(huff)    
    finalbit = ''
    for char in huff.read():

            bit_str = ''
            
            bit_str = bin((ord(char)))

            bit_str = bit_str[2:]
            
            bit_str = pad_to_nbits(bit_str, -1, 8 - len(bit_str))

            finalbit += bit_str

    finalbit = finalbit[:len(finalbit)-NBITS]
    str1 = ''
    uncompresscode = ''
    for i in finalbit:

        str1 += i

        if str1 in decode_dict.keys():
            uncompresscode += decode_dict[str1]
            str1 = ''
    text = open ('UNCOMP.txt' , 'w')
    
    text.write(uncompresscode)
    text.close()
    
    return 'UNCOMP.txt'

if __name__ == "__main__":
    pass

