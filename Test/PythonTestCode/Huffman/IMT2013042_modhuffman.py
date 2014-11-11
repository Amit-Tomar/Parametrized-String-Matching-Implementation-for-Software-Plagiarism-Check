'''
Created on 28-Oct-2013

@author: raghavan
'''
import modheap
hash_freq = {}
    
def build_char_table(filename):
    '''
    Build and return a hash that maps every character in the file 'filename' to the
    number of occurences of that char in the file
    '''
    # Your code 
    freq_dict = {}
    fopen = open(filename,'r')
    for char in fopen.read():
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1   
    global hash_freq
    hash_freq = freq_dict
    return freq_dict       
    

def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    # Your code
    value = cmp(char_tup1[1] , char_tup2[1])
    return value
 

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
    temp_list = freq_table.items()
    modheap.initialize_heap(True, arity_exp, cmp_freq)
    modheap.import_list(temp_list)
    modheap.heapify()
    while(len(temp_list) > 1):
        tup1 = modheap.pop()
        tup2 = modheap.pop()
        tup3 = tup1[0]+tup2[0], tup1[1]+tup2[1]
        stack.append((tup1[0], tup1[1], tup3[0], '1'))
        stack.append((tup2[0], tup2[1], tup3[0], '0'))
        modheap.add(tup3)
        temp_list = modheap.DATA
    return stack, stack[-1]
    
    
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
    bin_hash = {}
    compressed_length = 0
    for i in hash_freq.keys():
        root_symbol = ''
        for j in code_stack:
            if(i==j[0]):
                root_symbol = j[3]+ root_symbol 
                parent = j[2]
                for k in code_stack:
                    if (parent==k[0]):
                        root_symbol  = k[3] + root_symbol
                        parent = k[2]     
            bin_hash[i] = root_symbol
    for i in hash_freq.items():
        freq = i[1]
        for j in bin_hash.items():
            if(i[0]==j[0]):
                compressed_length += len(j[1])*freq
    return bin_hash, compressed_length


                    

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
    count = 0
    bin_str = ""
    temp_str = ""
    final_str = ""
    temp_codes = codes.items()
    fread = open(text_filename,'r')
    for i in fread.read():
        for j in codes.items():
            if(i==j[0]):
                bin_str += j[1]
                break
    fread.close()      
    for i in bin_str:
        temp_str = temp_str + i
        count += 1
        if(count==8):
            final_str = final_str+ chr(int(temp_str, 2))
            temp_str = ""
            count = 0
    if(count<8):
        while(count<8):
            temp_str = temp_str+'0'
            count += 1 
        ascii = int(temp_str, 2)
        final_str = final_str+chr(ascii)
    fwrite = open(huff_filename,'w')
    uniquecharacter_length = len(temp_codes)
    uniquecharacter_length = str(uniquecharacter_length)
    huff_length = str(huff_length)
    fwrite.write(uniquecharacter_length)
    fwrite.write(" ")
    fwrite.write(huff_length)
    fwrite.write('\n')
    i = 0
    while(i<len(temp_codes)):
        if(temp_codes[i][0]=='\n'):
            fwrite.write('\\n')
        elif(temp_codes[i][0]=='\t'):
            fwrite.write('\\t')
        else:
            fwrite.write(temp_codes[i][0])
        fwrite.write(" ")
        fwrite.write(temp_codes[i][1])
        fwrite.write('\n')
        i += 1
    fwrite.write(final_str)
            
                
                
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
    code_stack, top_element = build_huffman_tree(freq_table, arity_exp)
    bin_hash, compressed_lenght = form_codes('', code_stack)
    write_compressed(text_filename, text_filename+".huff", bin_hash, compressed_lenght)
    return text_filename+'.huff'
    


def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    # Your code
    length = 0
    read_hash = {}
    count = 0
    for i in huff.readlines():
        read_list = i.split()
        count += 1
        if(count==1):
            length = read_list[0]
        elif(len(read_list)==1):
            read_hash[read_list[0]] = ' '
        else:
            read_hash[read_list[1]] = read_list[0]
        if(count>int(length)):
            break
    return read_hash
            
            
            
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
    fread = open(huff_filename,'r')
    fwrite = open(huff_filename+'1','w')
    binary_str = ''
    read_line = (fread.readline()).split()
    length_code = int(read_line[0])
    compressed_length = int(read_line[1])
    for i in range(0, length_code):
        fread.readline()
    read_file = fread.read()
    for i in read_file:
        binary = bin(ord(i))[2:]
        bin_len = len(binary)
        i = 8-bin_len
        while(i>0):
            binary = '0' + binary
            i -= 1
        binary_str = binary_str+str(binary)
    binary_str = binary_str[:compressed_length]
    fread.close()
    fread = open(huff_filename,'r')
    code_hash = read_codes(fread)
    temp_str = ''
    for i in binary_str:
        temp_str = temp_str+i
        if temp_str in code_hash:
            if(code_hash[temp_str]=='\\n'):
                fwrite.write('\n')
            elif(code_hash[temp_str]=='\\t'):
                fwrite.write('\t')
            else:
                fwrite.write(code_hash[temp_str])
            temp_str = ''
    fread.close()
    fwrite.close()
    return huff_filename+'1'


if __name__ == '__main__':
    pass