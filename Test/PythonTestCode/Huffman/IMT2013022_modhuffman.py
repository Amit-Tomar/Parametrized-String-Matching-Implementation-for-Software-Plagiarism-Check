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
    test_file = open(filename, 'r')
    fread=test_file.read()
    freq_table = {}
    for char in fread:
            
        if (freq_table.has_key(char)):
            freq_table[char] += 1
        else:
            freq_table[char] = 1
        
        
    test_file.close()
    return freq_table


def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    if(char_tup1[1]>char_tup2[1]):
        return 1
    elif(char_tup1[1]<char_tup2[1]):
        return -1
    else:
        return 0
    
    # Your code


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
    
    new_list = []
    
    for i in freq_table:
        new_list.append((i, freq_table[i]))
        
    modheap.initialize_heap(True, arity_exp , cmp_freq)
    modheap.import_list(new_list)
    modheap.heapify()
    stack = []
    
    while(modheap.size()>1):
        
        element1 = modheap.pop()
        element2 = modheap.pop()
        
        modheap.add((element2[0]+element1[0], element1[1]+element2[1]))
        stack.append((element1[0], element1[1], element2[0]+element1[0], '1'))
        stack.append((element2[0], element2[1], element2[0]+element1[0], '0'))
        

    #stack.append((modheap.DATA[0][0], modheap.DATA[0][1], "root", '1'))
    #stack.append((modheap.DATA[1][0], modheap.DATA[1][1], "root", '0'))
    
    return stack,modheap.DATA[0][0]
    print stack,modheap.DATA[0][0]
    # Your code


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
   
    i = len(code_stack)-1
    comp_len=0
    code_hash={root_symbol:''}
    while(i>=0):
        elem = code_stack.pop()
        code_hash[elem[0]] = code_hash[elem[2]] + elem[3]
        if(len(elem[0])==1):
            comp_len += len(code_hash[elem[0]]) * elem[1]
        i -= 1
        
    len_code_stack = len(code_stack)-1
    i = len_code_stack
    while(i>=0):
        len_code_stack += len(code_hash[code_stack[i][0]])
        i -= 1
    for inter_symbols in code_hash.keys():
        if len(inter_symbols)>1:
            del code_hash[inter_symbols]
    return code_hash, comp_len 

def excessfunc(num):
    global excess
    excess = num 

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
    
    input_text = open ( text_filename, 'r')
    input_write = open (huff_filename , 'w')
    input_write.write("%d %d\n" %(len(codes) , huff_length))
    for key in codes.keys():
        if key == ' ':
            input_write.write(codes[key]+' space\n')
        elif key == '\n':
            input_write.write(codes[key]+' new\n')
        elif key == '\t':
            input_write.write(codes[key]+' tab\n')
        else:
            input_write.write(codes[key]+' '+key+'\n')
        '''elif key == '\\':
            input_write.write(codes[key]+' back\n')'''
    prim = ''
    for i in input_text.read():
        prim = prim + str(codes[i])
    buff = ''
    comp_str = ''
    for i in prim:
        buff += i
        if len(buff) == 8:
            comp_str += chr(int(buff, 2))
            buff = ''
    if len(buff) != 0:
        excessfunc(8 - len(buff))
        comp_str +=  buff+ excess*'0'
    input_write.write(comp_str)
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
    code_stack , root = build_huffman_tree(build_char_table(text_filename), arity_exp)
    
    code , count = form_codes(root, code_stack)
    file_new = text_filename + '.huff'
    write_compressed(text_filename, file_new , code, count)
    return file_new
    # Your code


def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    input_file = huff.readline()
    input_file = input_file.split()
    code_hash = {}
    comp_len=int(input_file[1])
    for i in range(int(input_file[0])):
        huff_read = huff.readline()
        huff_read = huff_read.split()
        if huff_read[1] == 'space':
            code_hash[huff_read[0]] = ' '
        elif huff_read[1] == 'back':
            code_hash[huff_read[0]] = '\\'
        elif huff_read[1] == 'tab':
            code_hash[huff_read[0]] = '\t'
        elif huff_read[1] == 'new':
            code_hash[huff_read[0]] = '\n'
        else:
            code_hash[huff_read[0]] = huff_read[1]
    return code_hash ,comp_len
    # Your code
    

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
    global excess
    file_text_input = open(huff_filename,'r')
    code,comp_len = read_codes(file_text_input)
    temp = ''
    bin_code = ''
    for bit in file_text_input.read(): 
        bin_code = bin(ord(bit))[2:]
        temp += pad_to_nbits(bin_code, -1, 8-len(bin_code))
    prim1 = ''
    seco1 = ''
    temp = temp[:comp_len]

    for cds in temp:
        prim1 += cds
        if prim1 in code.keys():
            seco1 += code[prim1]
            prim1 = ''  
    new_file = huff_filename+'1'
    uncomp_file = open(new_file,'w')
    uncomp_file.write(seco1)
    excess = 0
    return new_file    
    # Your code


if __name__ == '__main__':
    pass
    """
    a =build_char_table("text1")
    b,c=build_huffman_tree(a,1)
    print
    """
    #t b,c