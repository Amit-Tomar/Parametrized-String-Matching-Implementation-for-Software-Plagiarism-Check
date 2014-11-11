'''
Created on 28-Oct-2013

@author: raghavan
'''
import modheap

NBITS = 0
def initialize(nbit):
    global NBITS
    NBITS = nbit

def build_char_table(filename):
    '''
    Build and return a hash that maps every character in the file 'filename' to the
    number of occurences of that char in the file
    '''
    freq_table = {}
    file_name = open(filename, 'r')
    freq_table = {}   
    for char in file_name.read():
        if char in freq_table.keys():
            freq_table[char] = freq_table[char] + 1
        else:
            freq_table[char] = 1
    file_name.close()
    return freq_table
 
def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    if (char_tup1[1] > char_tup2[1]):
        return 1
    elif(char_tup1[1] < char_tup2[1]):
        return -1
    else:
        return 0
       
def pad_to_nbits(bitstr, pre_post, nbits = 8):
    '''
    Pad a bit string with 0's - to make it a string of length nbits.
    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
    This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
    '''
    if pre_post > 0:
        return bitstr + '0'*nbits
    else:
        return '0'*nbits + bitstr
   
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
    
    code_stack = [] 
    modheap.initialize_heap(True, arity_exp, cmp_freq)
    modheap.DATA = freq_table.items()
    modheap.heapify() 
    
    while(len(modheap.DATA)>2):
        element1 = modheap.pop()
        element2 = modheap.pop()
        father = ( element1[0]+element2[0], element1[1]+element2[1] )
        modheap.add(father)
        code_stack.append((element1[0], element1[1], father[0], '0' ))
        code_stack.append((element2[0], element2[1], father[0], '1' ))
        
    code_stack.append((modheap.DATA[0][0], modheap.DATA[0][1], "root", '0'))
    code_stack.append((modheap.DATA[1][0], modheap.DATA[1][1], "root", '1'))
    return code_stack , '' 
            
def form_codes(root_symbol, code_stack):
    '''
    Return a hash with the huffman code for each input character
    Algo: (i) Start from the root symbol - has code '' (empty string)
    (ii) For every element of the code_stack (starting from the end) - form its code by appending the additional bit to
    the code of its parent (to be got from the hash already built)
    (iv) Keep count of the total compressed length as the code test_file = open(self.RANDOM_FILENAME, 'w')
        freq_table = {}
        for _ in range(filesize):
            randchar = chr(self.FIRST_PRINTABLE_ORD + randrange(self.N_PRINTABLE_CHARS))
            if (freq_table.has_key(randchar)):
                freq_table[randchar] += 1
            else:
                freq_table[randchar] = 1
            test_file.write(randchar)
        test_file.close()
        return freq_tables are being created
    (iii) At the end, remove all the intermediate symbols created while forming the huffman tree from the hash,
    before returning the hash and the compressed length
    '''
    code_hash = {'root':root_symbol}
    
    i = len(code_stack)-1
    huff_length = 0
    while(i>=0):
        code_hash[code_stack[i][0]] = code_hash[code_stack[i][2]] + code_stack[i][3]
        huff_length += len(code_hash[code_stack[i][0]])
        i = i-1
            
    for symbols in code_hash.keys():
        if len(symbols)>1:
            del code_hash[symbols]
    return code_hash, huff_length   
    
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
 
    text_file1 = open(text_filename , "r")
    text_file2 = open(huff_filename , "w")
    text_file2.write("%d %d \n"%(len(codes) , huff_length))
          
    for element in codes.keys():
        
        if element == '\n':
            text_file2.write(codes[element]+' newline\n')
        elif element == ' ':
            text_file2.write(codes[element]+' space\n')    
        elif element == '\t':
            text_file2.write(codes[element]+' tab\n')
        else:
            text_file2.write(codes[element]+' '+element+'\n')
   
    binary_form = ''
    variable = ''
    compressed_form = ''
    
    for char in text_file1.read():
        if char in codes.keys():
            binary_form = binary_form + str(codes[char])
           
    for i in binary_form:
        variable = variable+i
        if(len(variable)==8):
            compressed_form += chr(int(variable , 2))
            variable = ''
   
    if(len(variable)!=0):
        initialize( 8 - len(variable))
        compressed_form += chr(int(pad_to_nbits(variable, 1 , 8-len(variable)) , 2))
   
    text_file2.write(compressed_form + '\n')
    return text_file2.write
 
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
    code_stack , root_element = build_huffman_tree(freq_table , arity_exp)
    codes, huff_length = form_codes(root_element, code_stack)
    huff_file = text_filename + '.huff'
    write_compressed(text_filename , huff_file , codes , huff_length)
    return huff_file
 
def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    dictionary = {}
   
    files = huff.readline()
    lists = files.split()
    elements = lists[0]
    length_compress = lists[1]
   
    i = 0    
    while(i<int(elements)):
        files = huff.readline()
        lists = files.split()
        if lists[1] == 'space':
            dictionary[lists[0]] = ' '
        elif lists[1] == 'newline':
            dictionary[lists[0]] = '\n'
        elif lists[1] == 'tab':
            dictionary[lists[0]] = '\t'   
        else:
            dictionary[lists[0]] = lists[1]
        i += 1
        
    return dictionary , length_compress
 
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
    files = open(huff_filename,"r")
    uncompressed = open("output",'w')
    code , length_compress = read_codes(files)
    variable = ''
    variable1 = ''
    variable2 = ''
    variable3 = ''
    for bits in files.read():
        variable1 = bin(ord(bits))[2:]
        variable += pad_to_nbits(variable1, -1, 8-len(variable1))
    variable = variable[:(len(variable)-NBITS-8)]
    for key in variable:
        variable2 += key
        if variable2 in code.keys():
            variable3 += code[variable2]
            variable2 = '' 
    
    uncompressed.write(variable3)
    return 'output'

if __name__ == '__main__':
    pass
