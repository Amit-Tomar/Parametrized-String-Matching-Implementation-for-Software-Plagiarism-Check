'''
Created on 12-Nov-2013

@author: vivek
'''
import modheap
    
def build_char_table(filename):
    
    '''
    Build and return a hash that maps every character in the file 'filename' to the
    number of occurences of that char in the file
    '''
    table={}
    f=open(filename,'r')
    fread=f.read()
    for char in fread:
        if(table.has_key(char)):
            table[char]=table[char]+1
        else:
            table[char]=1
    f.close()
    return table

def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    if char_tup1[1]>char_tup2[1]:
        return 1
    elif char_tup1[1]<char_tup2[1]:
        return -1
    else :
        return 0

def pad_to_nbits(bitstr, pre_post, nbits = 8):
    '''
    Pad a bit string with 0's - to make it a string of length nbits.
    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
    This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
    '''
    # Your code
    

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
    
    stack=[]
    modheap.initialize_heap(True,arity_exp,cmp_freq)
    while(len(modheap.DATA)>1):
        tup1=modheap.pop()
        tup2=modheap.pop()
        combine_char=tup1[0]+tup2[0]
        combine_freq=tup1[1]+tup2[1]
        modheap.DATA.append((combine_char,combine_freq))
        modheap.heapify()
        stack.append((tup1[0],tup1[1],combine_char,'1'))
        stack.append((tup2[0],tup2[1],combine_char,'0'))
    return stack,modheap.DATA[0]

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
    # Your code
    i=len(code_stack)-1
    code={}
    while(i>=0):
        code[code_stack[i][0]]=code[code_stack[i][2]]+code[i][3]
        i=i-1
    lenth_code_stack=len(code_stack)-1
    i=lenth_code_stack
    while(i>=0):
        lenth_code_stack+=len(code[code_stack[i][0]])
        i=i-1
    for symbols in code.keys():
        if len(symbols)>1:
            del code[symbols]
    return code,lenth_code_stack


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
    # Your code
    

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
    # Your code


def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    # Your code
    input_file = huff.readline()
    input_file = input_file.split()
    code = {}
  
    for i in range(int(input_file[0])):
        huff_read = huff.readline()
        huff_read = huff_read.split()
        if huff_read[1] == 'space':
            code[huff_read[0]] = ' '
        elif huff_read[1] == 'back':
            code[huff_read[0]] = '\\'
        elif huff_read[1] == 'tab':
            code[huff_read[0]] = '\t'
        elif huff_read[1] == 'new':
            code[huff_read[0]] = '\n'
        else:
            code[huff_read[0]] = huff_read[1]
    return code 
    

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
    # Your code


if __name__ == '__main__':
    pass