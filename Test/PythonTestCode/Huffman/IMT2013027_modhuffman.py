'''
Created on 28-Oct-2013

@author: raghavan

Last modified on 14-Nov-2013

@modifier: Nigel Steven Fernandez (IMT2013027)
'''

import modheap, string
    
def build_char_table(filename):
    '''
    Build and return a hash that maps every character in the file 'filename' to the
    number of occurences of that char in the file
    '''
    c_hash = {}
    fread = open(filename, 'r')
    data = fread.read()
    
    for i in range(0, len(data)):
        if (not c_hash.has_key(data[i])):
            c_hash[data[i]] = 0
        c_hash[data[i]] += 1 
            
    fread.close()
    
    return c_hash
    

def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    #Takes two elements - e1, e1 - of the heap as arguments and
    #retuns 1 if e1 > e2, -1 if e1 < e2 and 0 otherwise
    if (char_tup1[1] > char_tup2[1]): 
        return 1
    elif (char_tup1[1] < char_tup2[1]): 
        return -1
    else: 
        return 0


def pad_to_nbits(bitstr, pre_post, nbits = 8):
    '''
    Pad a bit string with 0's - to make it a string of length nbits.
    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
    This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
    '''
    if(pre_post < 0): 
        return string.rjust(bitstr, nbits, '0')
    else: 
        return string.ljust(bitstr, nbits, '0')
    

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
    modheap.initialize_heap(True, arity_exp, cmp_freq)
    modheap.import_list([(char, freq) for char, freq in freq_table.items()])
    modheap.heapify()
    
    code_stack = []
    
    while(modheap.size() > 1):
        tuple1 = modheap.pop()
        tuple2 = modheap.pop()
        parent_symbol = tuple1[0] + tuple2[0]
        parent_freq = tuple1[1] + tuple2[1]
        modheap.add((parent_symbol, parent_freq))
        code_stack.append((tuple1[0], tuple1[1], parent_symbol, '1')) 
        code_stack.append((tuple2[0], tuple2[1], parent_symbol, '0'))
    
    return code_stack, modheap.pop()[0]


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
    huff_length = 0
    codes = {}
    codes[root_symbol] = ''
    
    while(len(code_stack) > 0):
        tup = code_stack.pop()
        codes[tup[0]] = codes[tup[2]] + tup[3]
        if(len(tup[0]) == 1):
            huff_length += len(codes[tup[0]]) * tup[1]
    
    for symbol in codes.keys():
        if(not len(symbol) == 1):
            del codes[symbol]
    
    return codes, huff_length
        

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
    fread = open(text_filename, "r")
    huff = open(huff_filename, "w")
    data = fread.read()
    chunk = ""
    
    huff.write("{} {}\n".format(len(codes.keys()), huff_length))
    
    for char, code in codes.items():
        if(char == '\n'):
            huff.write("{} {}\n".format(code, str('\\n')))
        elif(char == '\t'):
            huff.write("{} {}\n".format(code, str('\\t')))
        elif(char == ' '):
            huff.write("{} {}\n".format(code, str('\/')))
        else:
            huff.write("{} {}\n".format(code, char))
    
    for i in range(0, len(data)):
        chunk += codes[data[i]]
        while(len(chunk) >= 8):
            huff.write("{}".format(chr(int(chunk[0 : 8], 2))))
            chunk = chunk[8 : ]
    
    if(len(chunk) > 0):
        huff.write("{}".format(chr(int(pad_to_nbits(chunk, 1, 8), 2))))
    
    fread.close()
    huff.close()
    
    return None
      
        
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
    c_hash = build_char_table(text_filename)
    code_stack, root_symbol = build_huffman_tree(c_hash, arity_exp)
    codes, huff_length = form_codes(root_symbol, code_stack)
    
    huff_filename = text_filename.split('.')[0] + ".huff"
    write_compressed(text_filename, huff_filename, codes, huff_length)
    
    return huff_filename


def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    lines = huff.readlines()
    first_line = lines[0]
    codes = {}
    
    for i in range(1, int(first_line.split()[0]) + 1):
        code = lines[i].split()[0]
        char = lines[i].split()[1]
        if(char == '\\n'):
            codes[code] = '\n'
        elif(char == '\\t'):
            codes[code] = '\t'
        elif(char == '\/'):
            codes[code] = ' '
        else:
            codes[code] = char
         
    return codes, first_line.split()[1]
    
    
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
    bin_code = ""
    valid_code = ""
    huff = open(huff_filename, "r")
    text_filename1 = huff_filename.split('.')[0] + "1"
    unhuff = open(text_filename1, "w")
    
    codes, huff_length = read_codes(huff)
    
    huff.seek(0, 0)
    i = int(huff.readline().split()[0])
    
    #moves file pointer to compressed data
    for _ in range(0, i):
        huff.readline()
    
    compress_data = huff.read()
     
    for i in range(0, len(compress_data)):
        bin_code += pad_to_nbits(bin(ord(compress_data[i]))[2:], -1, 8)
    
    if((int(huff_length) % 8) != 0):
        bin_code = bin_code[0 : -(8 - (int(huff_length) % 8))]
    
    for bit in bin_code:
        valid_code += bit
        if(codes.has_key(valid_code)):
            unhuff.write(codes[valid_code])
            valid_code = ""
    
    huff.close()
    unhuff.close()
    
    return text_filename1
    

if __name__ == '__main__':
    pass