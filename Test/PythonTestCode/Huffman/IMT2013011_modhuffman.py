'''
Created on 28-Oct-2013

@author: raghavan
'''
import modheap
EXTRA = 0 


def init(extra):
    global EXTRA
    EXTRA = extra 


def build_char_table(filename):
    '''
    Build and return a hash that maps every character in the file 'filename' to the
    number of occurences of that char in the file
    '''
    c_hash = {}
    testfile = open(filename , "r")
    for i in testfile.read():
        if c_hash.has_key(i):
            c_hash[i] = c_hash[i]+1
        else:
            c_hash[i] = 1
    testfile.close()
    return c_hash


def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    return cmp(char_tup1[1], char_tup2[1])


def pad_to_nbits(bitstr, pre_post, nbits = 8):
    '''
    Pad a bit string with 0's - to make it a string of length nbits.
    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
    This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
    '''
    if pre_post < 0:
        return '0'*nbits + bitstr
    else:
        return bitstr + '0'*nbits 
    

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
    stack = []
    List = []
    for i in freq_table:
        List.append((i, freq_table[i]))
    modheap.initialize_heap(True, arity_exp , cmp_freq)
    modheap.import_list(List)
    modheap.heapify()
    while(modheap.size()>2):
        tup1 = modheap.pop()
        tup2 = modheap.pop()
        stack.append((tup1[0], tup1[1], tup2[0]+tup1[0], '1'))
        stack.append((tup2[0], tup2[1], tup2[0]+tup1[0], '0'))
        modheap.add((tup2[0]+tup1[0], tup1[1]+tup2[1]))
    stack.append((modheap.DATA[0][0], modheap.DATA[0][1], "root", '1'))
    stack.append((modheap.DATA[1][0], modheap.DATA[1][1], "root", '0'))
    return stack,""
    

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
    huffman_code = {'root' : root_symbol}
    count = 0
    l = range(len(code_stack))
    for i in l[::-1] :
        huffman_code[code_stack[i][0]] = huffman_code[code_stack[i][2]] + code_stack[i][3]
        count += len(huffman_code[code_stack[i][0]]) 
    for key in huffman_code.keys():
        if len(key)>1:
            del huffman_code[key]
    return huffman_code , count

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
    dist_no = len(codes)
    read_text = open (text_filename, 'r')
    write_huff = open (huff_filename , 'w')
    write_huff.write("%d %d\n" %(dist_no , huff_length))
    for key in codes.keys():
        if key == ' ':
            write_huff.write(codes[key]+' space\n')
        elif key == '\n':
            write_huff.write(codes[key]+' new\n')
        elif key == '\t':
            write_huff.write(codes[key]+' tab\n')
        elif key == '\\':
            write_huff.write(codes[key]+' back\n')
        else:
            write_huff.write(codes[key]+' '+key+'\n')
    temp = ''
    for i in read_text.read():
        temp = temp + str(codes[i])
    btoa = ''
    compressed = ''
    for i in temp:
        btoa += i
        if len(btoa) == 8:
            compressed += chr(int(btoa, 2))
            btoa = ''
    if len(btoa) != 0:
        init(8 - len(btoa))
        compressed += chr(int(pad_to_nbits(btoa, 1, 8-len(btoa)), 2))
    write_huff.write(compressed+'\n')
    

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
    code_stack , root = build_huffman_tree(build_char_table(text_filename), arity_exp)
    code , count = form_codes(root, code_stack)
    write_compressed(text_filename, "testfile.huff", code, count)
    return 'testfile.huff'


def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    number = huff.readline()
    number = number.split()
    hash_code = {}  
    for i in range(int(number[0])):
        x = huff.readline()
        x = x.split()
        if x[1] == 'space':
            hash_code[x[0]] = ' '
        elif x[1] == 'new':
            hash_code[x[0]] = '\n'
        elif x[1] == 'tab':
            hash_code[x[0]] = '\t'
        elif x[1] == 'back':
            hash_code[x[0]] = '\\'
        else:
            hash_code[x[0]] = x[1]
    return hash_code 
    

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
    huff = open(huff_filename,'r')
    code = read_codes(huff)
    temp = ''
    par = ''
    for bit in huff.read(): 
        par = bin(ord(bit))[2:]
        temp += pad_to_nbits(par, -1, 8-len(par))
    temp1 = ''
    temp2 = ''
    temp = temp[:(len(temp)-EXTRA-8)]
    for i in temp:
        temp1 += i
        if temp1 in code.keys():
            temp2 += code[temp1]
            temp1 = ''  
    unc = open("testfile1",'w')
    unc.write(temp2)
    return 'testfile1'    


if __name__ == '__main__':
    pass
