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
    # Your code
    
    file_input = open(filename, 'r')
    
    char_count = {}
    
    data = file_input.read()
    
    for character in data:
        
        if character in char_count.keys():
            char_count[character] += 1
        else:
            char_count[character] = 1
    
    return char_count

def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    # Your code
    
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
    # Your code
    if pre_post < 0:
        new = ''
        new += (nbits-len(bitstr))*'0'
        
        return new + bitstr
    
    else:
        bitstr += (nbits-len(bitstr))*'0'
        
        return bitstr

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
    # Your code
    
    modheap.initialize_heap(True, arity_exp, cmp_freq)
    tuples = freq_table.items()
    modheap.import_list(tuples)
    modheap.heapify()
    
    stack = []
    
    while modheap.size()>1:
        new_char = ''
        
        pop1 = modheap.pop()
        pop2 = modheap.pop()
        
        new_char += pop1[0]
        new_char += pop2[0]
        
        modheap.add((new_char, pop1[1]+pop2[1]))
        
        stack.append((pop1[0], pop1[1], new_char, '0'))
        stack.append((pop2[0], pop2[1], new_char, '1'))
    
    return stack, modheap.DATA[0]

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
    
    length = 0
    code_hash = {}
    temp_hash = {}
    temp_hash[root_symbol[0]] = ''
    
    while len(code_stack) >= 1:
        element = code_stack.pop()
        temp_hash[element[0]] = temp_hash[element[2]] + element[3]
        
        if len(element[0]) == 1:
            length += element[1] * len(temp_hash[element[0]])
    
    for entry in temp_hash:
        if len(entry) == 1:
            code_hash[entry] = temp_hash[entry]
    
    del temp_hash
    
    return code_hash, length


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
    
    txt = open(text_filename, 'r')
    huff = open(huff_filename, 'w')
    
    huff.write((str(len(codes))+' '+str(huff_length)+'\n'))
    
    for entry in codes:
        if entry == '\n':
            huff.write(('\\n'+' '+codes[entry]+'\n'))
        
        elif entry == '\t':
            huff.write(('\\t'+' '+codes[entry]+'\n'))
        
        elif entry == ' ':
            huff.write(('space '+codes[entry]+'\n'))
        
        else:
            huff.write((str(entry)+' '+codes[entry]+'\n'))
    
    string = ''
    bitstr = ''
    count = 0
    
    data = txt.read()
    
    for char in data:
        string += codes[char]

    txt.close()
    
    for char in string:
        count += 1
        bitstr += char
        if count == 8:
            huff.write(chr(int(bitstr, 2)))
            bitstr = ''
            count = 0
    
    huff.write(chr(int(pad_to_nbits(bitstr, 1, 8), 2)))
    
    huff.close()

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

    freq_table = build_char_table(text_filename)
    
    codes, root = build_huffman_tree(freq_table, arity_exp)
    
    c_hash, length = form_codes(root, codes)
    
    write_compressed(text_filename, text_filename + '.huff', c_hash, length)
    
    return text_filename + '.huff'

def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    # Your codes
    
    data = huff.readline().split()

    ref_code = {}
    
    for i in range(int(data[0])):
        temp = huff.readline().split()
        ref_code[temp[1]] = temp[0]
        
    
    huff.close()

    return ref_code, int(data[1])

def uncompress(huff_filename):
    '''
    Uncompress a file that has been compressed using compress. Return the name of the uncompressed file.
    Add a '1' or something to the new file name so it does not overwrite the original.
    Algo: (i) Read the code from the first part of the compressed file.
    (ii) Read the rest of the file one bit at a time - every time you get a valid code, write the corresponding
    text character out to the uncompressed file.
    (iii) You need to use the compressed size appropriately - remember the last character that was written
    during compression.
    Hint: the built-in function 'bin' caprint modheap.DATA, stackn be used: bin(n) - returns a 0-1 string corresponding to the binary representation
    of the number n. However the 0-1 string has a '0b' prefixed to it to indicate that it is binary, so you will have to 
    discard the first two chars of the string returned.
    '''
    # Your code
    readfile = open(huff_filename, 'r')
    
    ref, length = read_codes(readfile)
    readfile = open(huff_filename, 'r')
    
    data = readfile.readline().split()
    
    for i in range (int(data[0])):
        readfile.readline()

    data = readfile.read()
    
    readfile.close()
    
    bin_code = ''
    new_file = open(huff_filename + '_uncompress', 'w')
    
    for char in data:        
        temp = bin(ord(char))[2:]
        
        if len(temp) < 8 :
            temp = pad_to_nbits(temp, -1, 8)
               
        bin_code += temp        
        
    
    code = ''
          
    for bit in bin_code[:length]:        
        code += bit
        
        if code in ref.keys():
            if ref[code] == '\\n':
                new_file.write('\n')
            
            elif ref[code] == '\\t':
                new_file.write('\t')
            
            elif ref[code] == 'space':
                new_file.write(' ')
            
            else:
                new_file.write(ref[code])
            
            code = ''
    
    new_file.close()
    
    return huff_filename + '_uncompress'		


if __name__ == '__main__':
    pass
