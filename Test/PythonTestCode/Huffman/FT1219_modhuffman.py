'''
Created on 28-Oct-2013

@author: raghavan
'''
import modheap
    
def build_char_table(filename):
    '''
    Build and return a hash that maps every character in the file 'filename' to the
    number of occurences of that char in the file
    '''
    char_freq = {}
    input_file = open(filename, "r")
    for line in input_file:
        for char in line:
            char_freq[char] = (char_freq[char]+1) if char_freq.has_key(char) else 1
    input_file.close()
    return char_freq


def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    return 1 if (char_tup1[1] > char_tup2[1]) else (
                -1 if (char_tup1[1] < char_tup2[1]) else 0)


def pad_to_nbits(bitstr, pre_post, nbits = 8):
    '''
    Pad a bit string with 0's - to make it a string of length nbits.
    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
    '''
    padding = ('0' * (nbits - len(bitstr)))
    return ((padding + bitstr) if (pre_post < 0) else (bitstr + padding))
    

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
    for char in freq_table:
        modheap.add((char, freq_table[char]))
    code_stack = []
    while (modheap.size() > 1):
        chr_freq1 = modheap.pop()
        chr_freq2 = modheap.pop()
        composite_char = chr_freq1[0] + chr_freq2[0]
        composite_char_freq = chr_freq1[1] + chr_freq2[1]
        modheap.add((composite_char, composite_char_freq))
        code_stack.append((chr_freq1[0], chr_freq1[1], composite_char, '0'))
        code_stack.append((chr_freq2[0], chr_freq2[1], composite_char, '1'))
    
    root_char_freq = modheap.pop()
    return code_stack, root_char_freq[0]


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
    huff_code = {}
    huff_code[root_symbol] = ''
    compressed_length = 0
    while (len(code_stack) > 0):
        char_parent_code = code_stack.pop()
        symbol = char_parent_code[0]
        huff_code[symbol] = (huff_code[char_parent_code[2]] + char_parent_code[3])
        if (len(symbol) == 1):
            compressed_length += (len(huff_code[symbol]) * char_parent_code[1])
    
    composites = []
    for key in huff_code:
        if (len(key) > 1):
            composites.append(key)
    
    for key in composites:
        huff_code.pop(key)

    return huff_code, compressed_length


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
    textfile = open(text_filename, 'r')
    compressed = open(huff_filename, 'wb')
    compressed.write('%d %d\n' % (len(codes), huff_length))
    for char in codes:
        compressed.write('%s %d\n' % (codes[char], ord(char)))
    outstr = ''
    for char in textfile.read():
        outstr += codes[char]
        while (len(outstr) >= 8):
            outchar = chr(int(outstr[:8], 2))
            compressed.write(outchar)
            outstr = outstr[8:]
    if (outstr != ''):
        outstr = pad_to_nbits(outstr, 1)
        compressed.write(chr(int(outstr, 2)))
    textfile.close()
    compressed.close()
    

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
    huff_stack, root_symb = build_huffman_tree(freq_table, arity_exp)
    codes, huff_length = form_codes(root_symb, huff_stack)
    huff_flname = text_filename.split('.')[0] + '.huff'
    write_compressed(text_filename, huff_flname, codes, huff_length)
    return huff_flname


def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    codes = {}
    first_line = huff.readline().split()
    ncodes, huff_length = int(first_line[0]), int(first_line[1])
    for _ in range(ncodes):
        line = huff.readline().split()
        codes[line[0]] = chr(int(line[1]))
    return codes, huff_length
    

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
    huff_file = open(huff_filename, 'r')
    text_filename = huff_filename.split('.')[0] + '1.txt'
    textfile = open(text_filename, 'w')
    codes, huff_length = read_codes(huff_file)
    huff_code = ''
    for char in huff_file.read():
        compressed_char = bin(ord(char))[2:]
        compressed_char = pad_to_nbits(compressed_char, -1)
        while (compressed_char != '' and huff_length > 0):
            huff_code += compressed_char[:1]
            compressed_char = compressed_char[1:]
            if codes.has_key(huff_code) and (huff_length > 0):
                textfile.write(codes[huff_code])
                huff_length -= len(huff_code)
                huff_code = ''
    huff_file.close()
    textfile.close()
    return text_filename


if __name__ == '__main__':
    pass