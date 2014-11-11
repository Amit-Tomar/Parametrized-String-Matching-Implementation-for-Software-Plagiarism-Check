'''
Created on 28-Oct-2013

@author: raghavan
'''
import modheap

len_char_added = 0
   
def build_char_table(filename):
    '''
    Build and return a hash that maps every character in the file 'filename' to the
    number of occurences of that char in the file
    '''
    # Your code
    chash = {}
    
    file_ptr = open(filename, "r")
    char_array = file_ptr.read()
    file_ptr.close()
    
    for char_arr in char_array :
        chash[char_arr] = 0        
    
    for char_arr in char_array :       
        chash[char_arr] += 1
        
    return chash
    

def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    # Your code    
    if char_tup1[1] > char_tup2[1] :
        return 1
    elif char_tup1[1] < char_tup2[1] :
        return -1
    elif char_tup1[1] == char_tup2[1] :
        return 0            

def build_huffman_tree(freq_table, arity_exp):
    '''
    Build the huffman tree for the input textfile and return a stack (maybe along with the character at the root node)
    Algo: (i) Start by making a heap out of freq_table using modheap
    (ii) Pop two elements out of the heap at a time
    (iii) Form a composite character thsorted_list = [] at is the concatenation of the two and the combined frequency of the two
    (iv) Add the new composite character with its frequency to the heap
    (v) Add the two popped elements to a stack - simply append to a list
    Elements of the stack are of the form (element, frequency, parent, additional_code_bit)
    (vi) Repeat the above four steps till the heap has only the root element left
    (vii) Return the stack along with the top root element of the heap
    '''
    # Your code            
    modheap.initialize_heap(True, arity_exp, cmp_freq)
    
    for elem in freq_table :
        modheap.add((elem, freq_table[elem]))
               
    code_stack = []
    pop_1 = ()
    pop_2 = ()
    
    while modheap.size() > 1: 
        pop_1 = modheap.pop()
        pop_2 = modheap.pop()
                
        comb_ele  = pop_1[0] + pop_2[0]
        comb_freq = pop_1[1] + pop_2[1]
        
        modheap.add((comb_ele, comb_freq))
        
        code_stack.append((pop_1[0], pop_1[1], comb_ele, "0"))
        code_stack.append((pop_2[0], pop_2[1], comb_ele, "1"))
        
    return code_stack, modheap.DATA[0]    
    
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
    huff_hash = {}  
    compress_length = 0
    
    huff_hash[root_symbol[0]] = ""
    len1 = len(code_stack)-1
    
    while len1 >= 0 :
        elem  = code_stack[len1]
        huff_hash[elem[0]] = huff_hash[elem[2]] + elem[3]
        if len(elem[0]) == 1 :
            compress_length += len(huff_hash[elem[0]]) * elem [1]
        len1 -= 1    
    
    for key, code in huff_hash.items() :
        if len(key) != 1 :
            del huff_hash[key]
            
    return huff_hash, compress_length

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
    global len_char_added
    text_write = open(huff_filename,"w")
    text_file = open(text_filename,"r")
    all_char = text_file.read()
    code = ""
    asc = 0
    len_char_added = 0
    
    distinct_char = len(codes)
    text_write.write(str(distinct_char) + " " + str(huff_length) + "\n")    
    
    code_tuples = codes.items()
    
    for tuple_code in code_tuples :
        string = "" 
        if(tuple_code[0] == '\n'):
            string = str('\\n') + ' ' + str(tuple_code[1]) + '\n'
        elif(tuple_code[0] == '\t'):
            string = str('\\t') + ' ' + str(tuple_code[1]) + '\n'
        else:
            string = str(tuple_code[0]) + ' ' + str(tuple_code[1]) + '\n'
                           
        text_write.write(string)
    
    for char_r in all_char :
        code += codes[char_r]
           
        while len(code) >= 8 :
            write_char = code[:8]
            asc = int(write_char, 2)
            write_char = (chr(asc))      
            text_write.write(write_char)                      
            code = code[8:]
    
    if len(code) >= 0 :
        if (len(code)  <= 8)  :
            len_char_added = 8 - len(code)            
            code += "0"*len_char_added
            
        asc  = int (code, 2)
        write_char = chr(asc)
        text_write.write(write_char)
        
        if len(code) >8:
            code = code[8:]
        
    text_write.close()
    text_file.close()    
    
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
    freq_table               = build_char_table(text_filename)
    code_stack, root_symbol  = build_huffman_tree(freq_table, 1)
    huff_hash, compress_len  = form_codes(root_symbol, code_stack)
    
    huff_filename = text_filename + ".txt" 
    write_compressed(text_filename, huff_filename, huff_hash, compress_len )
    
    return huff_filename    
    
def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    # Your code
    chash = {}
    first_line = (huff.readline()).split()
    compress_len = int(first_line[1])
    distinct_char = int(first_line[0])
    
    while (distinct_char > 0) :
        line_element_list = (huff.readline()).split()
        if len(line_element_list) == 1 :
            chash[line_element_list[0]] = chr(32)            
        elif line_element_list[0] == "\\n":
            chash[line_element_list[1]] = "\n"
        elif line_element_list[0] == "\\t":
            chash[line_element_list[1]] = "\t"
        
        else :
            chash[line_element_list[1]] = line_element_list[0]
        distinct_char -= 1
    return chash, compress_len 

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
    character = 'a'
    huff = open(huff_filename,"r")
    
    chash, compress_len = read_codes(huff)
    
    text_write = open("uncompressed", "w")
    code = ""
    i = 0
    
    rest_line = huff.read()
    
    length       = len(rest_line)-1
    
    while  length >= 0 :
        character = rest_line[i]
        
        asc    = ord(character)
        string = bin(asc)
        string = string[2:]
        string = "0"*(8-len(string)) + string
        
        if length == 0:
            string = string[: 8 - len_char_added]    
            
        for charac in string :
            code += charac
            if code in chash :
                text_write.write(chash[code])
                code = ""       
        i += 1 
        length -= 1
    
    huff.close()
    text_write.close()
    return "uncompressed"
    
if __name__ == '__main__':
    pass