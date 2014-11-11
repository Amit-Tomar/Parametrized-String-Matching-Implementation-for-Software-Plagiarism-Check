'''
Created on 28-Oct-2013

@author: raghavan
'''
import modheap

def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    # Your code
    return cmp(char_tup1[1] , char_tup2[1])


def build_char_table(filename):
    '''
    Build and return a hash that maps every character in the file 'filename' to the
    number of occurences of that char in the file
    '''
    # Your code
    character_hash = {}
    temp_file = open(filename,"r")
    lines = temp_file.readlines()
    
    for words in lines:
        for character in words:
            if character in character_hash:
                character_hash[character] += 1
            else:
                character_hash[character] = 1
    temp_file.close()
    return character_hash


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
    stack = []
    modheap.initialize_heap(True, arity_exp, cmp_freq)
    for i in freq_table:
        modheap.add((freq_table[i], i))
        
    while (len(modheap.DATA)>1):
        element1 = modheap.pop()
        element2 = modheap.pop()
        composite_char = element1[1] + element2[1]
        composite_freq = element1[0] + element2[0]
        modheap.add((composite_freq, composite_char))
        stack.append((element1[1], element1[0], composite_char, '0'))
        stack.append((element2[1], element2[0], composite_char, '1'))        
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
    old_codes = {}
    composite_length = 0
    while(len(code_stack)!=0):
        tuples = code_stack.pop()
        if tuples[2] in old_codes:
            old_codes[tuples[0]] = old_codes[tuples[2]] + tuples[3]
            if(len(tuples[0])<=1 ):
                composite_length += tuples[1] * len(old_codes[tuples[0]])
        else:
            old_codes[tuples[0]] = tuples[3]
            if(len(tuples[0])<=1 ):
                composite_length += tuples[1] * len(old_codes[tuples[0]])
    
    new_codes = {}
    for i in old_codes:
        if(len(i) < 2):
            new_codes[i] = old_codes[i]
    return new_codes, composite_length

    
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
    read_file = open(text_filename, "r").read()
    write_file = open(huff_filename, "w")
    fil_com = open("encrypt","w")
    write_file.write(str(len(codes)) + ' ' + str(huff_length) + '\n')
    for character in codes:
        if character == '\t':
            write_file.write('\\t' + ' ' + codes[character] + '\n')
        elif character == '\n':
            write_file.write('\\n' + ' ' + codes[character] + '\n')
        else:
            write_file.write(character + ' ' + codes[character] + '\n')
            
    string = ''
    for character in read_file:
        string += codes[character]
    temp_string = ''
    for i in string:
        temp_string += i
        if(len(temp_string) == 8):
            char = chr(int(temp_string, 2))
            write_file.write(char)
            fil_com.write(char)
            temp_string = ''
    padding = 8 - len(temp_string)
    temp_string =  temp_string + ('0' * padding)
    write_file.write(chr(int(temp_string, 2)))
    fil_com.write(chr(int(temp_string, 2)))
    
    

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
    frequency_table = build_char_table(text_filename)
    stack, root = build_huffman_tree(frequency_table, arity_exp)
    codes, comp_len = form_codes(root, stack)
    write_compressed(text_filename, text_filename+'.huff', codes, comp_len)
    return text_filename + '.huff'

def read_codes(fil):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    # Your code
    code_hash = {}
    line = fil.readline().split()
    len_file = int(line[0])
    for i in range (0, len_file):
        string = fil.readline()
        words = string.split(" ")
        words[1] = words[1][:-1]
        if words[0] == '':
            code = words[2][:-1]
            code_hash[code] = " "
        else:
            code = words[1]
            code_hash[code] = words[0]
        
    
    return code_hash, int(line[1])  
    
       
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
    fil = open(huff_filename,'r') 
    f_read = open("encrypt","r")
    code_hash, length = read_codes(fil)
    write_file = open("final",'w')
    binary_string = ''
    
    for i in f_read.read():
        ascii_value = ord(i)
        binary_no = bin(ascii_value)[2:]
        bin_len = len(binary_no)
        binary_no = '0'*(8-bin_len) + binary_no
        binary_string = binary_string + binary_no
        
    binary_string = binary_string[:length]
    temp_string = ''
    for i in binary_string:
        temp_string = temp_string + i
        if temp_string in code_hash:
            if(code_hash[temp_string]=='\\n'):
                write_file.write('\n')
            elif(code_hash[temp_string]=='\\t'):
                write_file.write('\t')
            else:
                write_file.write(code_hash[temp_string])
            temp_string = ''
    write_file.close()
    return "final"
            

if __name__ == '__main__':
    pass