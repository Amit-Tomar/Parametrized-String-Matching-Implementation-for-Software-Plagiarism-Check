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
    
    chash = {}
    fopen = open(filename, 'r')
    chash1 = list(fopen.read())
    
    for i in chash1:
        chash[i] = 0
        
    for i in chash1:
        chash[i] = chash[i] + 1
    fopen.close()    
    return chash

def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    # Your code
    a = char_tup1[1]
    b = char_tup2[1]
    if (a > b):
        return a
    else :
        return b
    
def pad_to_nbits(bitstr, pre_post, nbits = 8):
    '''
    Pad a bit string with 0's - to make it a string of length nbits.
    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
    This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
    '''
    # Your code
    if (pre_post < 0):
        if (len(bitstr) < nbits):
            a = nbits - len(bitstr)
            while (len(str) < 8):
                bitstr = '0' + bitstr
                a = a - 1
        return bitstr       
                 
    elif (pre_post > 0):
        if (len(bitstr) < nbits):
            a = nbits - len(bitstr)
            while (len(str) <= 8):
                bitstr = bitstr + '0'
                a = a - 1
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
    modheap.initialize_heap(is_min = True, arity_exp = 1, compare_fn = None)
    return_list = [(y,x) for (x,y) in freq_table.items()]
    return_stack = []
   
    modheap.DATA = return_list
    modheap.heapify()
    while(len(return_list) > 1):
        heap1 = modheap.pop()
        modheap.heapify()
        heap2= modheap.pop()
        modheap.heapify()
        new = (heap1[0]+heap2[0], heap1[1]+heap2[1])
        return_stack.append((heap1[1], heap1[0], heap1[1] + heap2[1], '0'))
        return_stack.append((heap2[1], heap2[0], heap1[1] + heap2[1], '1'))
        return_list.append(new)
    
    return (return_stack,return_list[0])

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
    root_hash = {}
    root_symbol = ''
    comp_len = 0
    hashes = code_stack[0]
    hashes.reverse()
    for a in hashes:
        if (len(a[0])== 1):
            root_symbol = root_symbol + '1'
            root_hash[a[0]] = root_symbol + '0'
            var = len(root_hash[a[0]])*a[1]
            comp_len = comp_len + var
            
    return root_hash, comp_len    
   
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
       
    fopen = open(text_filename,"r")
    fwrite = open(huff_filename,"w")
    string = fopen.read()
    fwrite.write(str(len(codes))+" "+str(huff_length) + "\n")
    blank = ''
    for a in codes:
        if (a == '\n'):
            fwrite.write(codes[a] + ' ' + '\\n' + '\n')
        elif (a == '\t'):
            fwrite.write(codes[a] + ' ' + '\\n' + '\n')
        else:
            fwrite.write(codes[a] + ' ' + a + '\n')
     
    for i in string :
        blank = blank + codes[i]
    final = ''
    for i in blank:
        final = final + i
        if (len(final) == 8):
            y = int(final,2)
            fwrite.write(chr(y))
            final = ''
            
    finalise = 8 - len(final)
    final = final + '0'*finalise
    fwrite.write(chr(int(final,2)))
    

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
    code_stack = build_huffman_tree(frequency_table,arity_exp)
    codes = form_codes('',code_stack)[0]
    compressedfile = text_filename + '.huff'
    huff_length = len(codes)
    write_compressed(text_filename,compressedfile,codes,huff_length)
    return text_filename + '.huff'
    
    


def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    # Your code
    global var
    hashcodes = {}
    temp = huff.readline()
    temp = temp.split()
    no_char = int(temp[0])
    comp_length = int(temp[1])
    i = 0
    while i < no_char:
        temp = huff.readline()
        temp = temp.split()
        if len(temp) == 1:
            hashcodes[temp[0]]= " "
        elif temp[1] == '\\n':
            hashcodes[temp[0]] = "\n"
        elif temp[1]=="\\t":
            hashcodes[temp[0]] = "\t"
        else:
            hashcodes[temp[1]] = temp[0]
        i += 1
    return hashcodes,comp_length
         
    

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
    fopen = open(huff_filename,"r")
    writein = open(huff_filename+'new',"w")
    line_elements = fopen.readline()
    line_elements = line_elements.split()
    comp_len = int(line_elements[1])
    comp_char = int(line_elements[0])
    binary_string = ''
    a = 0
    while(a < comp_char):
        fopen.readline()
        a = a + 1
    newfile = fopen.read()

    for a in newfile:
        ascii_code = ord(a)
        binary_conversion = bin(ascii_code)[2:]
        binary_length = len(binary_conversion)
        a = 8 - binary_length
        while (a < 0):
            binary_conversion = '0' + binary_conversion
            a = a - 1
        binary_string = binary_string + str(binary_conversion)
    binary_string = binary_string[:comp_len]
    fopen.close()
    empty = ''
    fopen = open(huff_filename,'r')
    code_hash = read_codes(fopen)
    for a in binary_string:
        empty = empty + a
        if empty in code_hash:
            if(code_hash[empty] == '\\t'):
                writein.write('\t')
            elif(code_hash[empty] == '\\n'):
                writein.write('\n')
            else:
                writein.write(code_hash[empty])
            empty = ''
            
    fopen.close()
    writein.close()
    return huff_filename + 'new'
if __name__ == '__main__':
    pass