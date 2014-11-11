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

    freq = {}
    f = open(filename, "r")
    orig_list = f.read()
    for i in orig_list:
        if i in freq.keys():
            freq[i] += 1
        else:
            freq[i] = 1
    f.close()
    return freq

def cmp_freq(char_tup1, char_tup2):

    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''

    if char_tup1[1] > char_tup2[1]:
        return 1
    elif char_tup1[1] < char_tup2[1]:
        return -1
    else:
        return 0


def pad_to_nbits(bitstr, pre_post, nbits = 8):

    '''

    Pad a bit string with 0's - to make it a string of length nbits.

    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end

    This might be a good helper function to have -- this function is just a suggestion, it is not mandatory

    '''

    if pre_post < 0:

        return '0' * nbits + bitstr

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

    Elements ofdef the stack are of the form (element, frequency, parent, additional_code_bit)

    (vi) Repeat the above four steps till the heap has only the root element left

    (vii) Return the stack along with the top root element of the heap

    '''

    stack = []

    freq_table = freq_table.items()

    modheap.initialize_heap (True, arity_exp, cmp_freq)

    for elem in freq_table:

        modheap.add(elem)

    while(len(modheap.DATA)>2):

        element1 = modheap.pop()

        element2 = modheap.pop()
        
        stack.append((element1[0], element1[1], element2[0] + element1[0],1))

        stack.append((element2[0], element2[1], element2[0] + element1[0],0))

        modheap.add((element2[0] + element1[0], element1[1] + element2[1]))

    stack.append((modheap.DATA[0][0], modheap.DATA[0][1], 'root', 1))

    stack.append((modheap.DATA[1][0], modheap.DATA[1][1], 'root', 0))

    print stack

    return stack, ''

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

    codes = {'root':root_symbol}

    count = 0

    code_stack = code_stack[::-1]

    for i in range(len(code_stack)):

        codes[code_stack[i][0]] = (codes[code_stack[i][2]] + str(code_stack[i][3]))

        count += len(codes[code_stack[i][0]])

    for k in codes.keys():

        if len(k) > 1:

            del codes[k]

    return codes, count

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

    fileread = open(text_filename, "r")

    filewrite = open(huff_filename, "w")

    filewrite.write('%d %d\n' % (len(codes), huff_length))

    for element in codes.keys():

        if element == ' ':

            filewrite.write(codes[element] + ' space\n')

        elif element == '\n':

            filewrite.write(codes[element] + ' nextline\n')

        elif element == '\t':

            filewrite.write(codes[element] + ' tab\n')

        else:

            filewrite.write(codes[element] + ' '+element+'\n')

    fil = fileread.read()

    fileread.close()

    compressed = ''

    binary = ''

    temp = ''

    for char in fil:

        if char in codes.keys():

            binary = binary + str(codes[char])

    NB = 8-len(binary)%8

    initialize(NB)

    binary = pad_to_nbits(binary, 1, NB)

    for i in binary:

        temp += i

        if len(temp) == 8:

            compressed += chr(int(temp,2))

            temp = ''

    if len(temp) <> 0:

        compressed += chr(int(temp,2))    

    filewrite.write(compressed)

    filewrite.close()

def compress(text_filename, arity_exp):
    '''
    Compress a give text file 'text_filename' using a heap with arity 2^arity_exp

    Algo: (i) Build the frequency table

    (ii) Build code s-tack by building the huffman tree from the frequency table

    (iii) Form the codes from the code stack

    (iv) Write out the compressed file

    Return the name of the compressed file. Might help to have a convention here - the original file name without the extension

    appended with '.huff' could be one way.

    '''

    freq = build_char_table(text_filename)

    stack,root_symbol = build_huffman_tree(freq, arity_exp)

    codes,counter = form_codes('', stack)

    write_compressed(text_filename, 'comp.huff', codes, counter)

    return 'comp.huff'

def read_codes(huff):

    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -

    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.

    Return a hash of codes (code -> original char) and the compressed length
    '''
    
    file1 = huff.read().split()

    distinct = file1[0]

    c_len = file1[1]

    codes={}

    for i in range(2,2 * int(distinct) + 1,2):

        if file1[i + 1] == 'space':

            codes[' '] = file1[i]

        elif file1[i+1]=='nextline':

            codes['\n'] = file1[i]

        elif file1[i+1]=='tab':

            codes['\t'] = file1[i]

        else:

            codes[file1[i+1]] = file1[i]

    huff.close()

    return codes, c_len

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
    binary = ''

    temp = ''

    lines = []

    huf1 = open(huff_filename, "r")

    codes,c = read_codes(huf1)

    n = len(codes.keys())+1

    huf1 = open(huff_filename, "r")

    huf2 = open("uncomp.txt", "w")

    for i in range(n):

        huf1.readline()

    lines.append(huf1.readline())    

    for l in lines:

        for char in l:

            binary += pad_to_nbits(bin(ord(char))[2:], -1, 8-len(bin(ord(char))[2:]))

    binary = binary[:len(binary)-NBITS]

    for bits in binary:

        temp += bits

        if temp in codes.values():

            for key in codes.keys():

                if codes[key] == temp :

                    if key == 'nextline':
                        
                        huf2.write('\n')

                    elif key == 'space':

                        huf2.write(' ')

                    elif key == 'tab':
                        huf2.write('\t')

                    else:
                        huf2.write(key)

            temp=''

    huf1.close()

    huf2.close()

    return "uncomp.txt"

  

if __name__ == '__main__':

    pass