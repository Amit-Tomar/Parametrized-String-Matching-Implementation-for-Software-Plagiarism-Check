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
    file1 = open(filename,"r")
    string = file1.read()
    hash1 = {}
    for char in string:
        hash1[char] = 0
    for char in string:
        hash1[char] += 1
    return hash1

def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tups (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    # Your code
    if(char_tup1[1]>char_tup2[1]):
        return 1
    elif(char_tup1[1]<char_tup2[1]):
        return -1
    else:
        return 0 

def pad_to_nbits(bitstr , pre_post, nbits = 8):
    '''
    Pad a bit string with 0's - to make it a string of length nbits.
    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
    This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
    '''
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
    # Your code
    modheap.initialize_heap(True , arity_exp , cmp_freq )
    tupheap = []
    stack = []
    for char in freq_table:
        #tupheap=modheap.add((x,freq_table[x]))
        tupheap = modheap.add((char , freq_table[char]))
    i = len(tupheap)
    while(i!=1):
        pop1 = modheap.pop()
        pop2 = modheap.pop()
        com_sym = pop1[0] + pop2[0]
        com_count = pop1[1] + pop2[1]
        tupheap = modheap.add((com_sym , com_count))
        stack.append((pop1[0] , pop1[1] , com_sym , '0'))
        stack.append((pop2[0] , pop2[1] , com_sym , '1'))
        i = i - 1
    
    #print stack
    print tupheap
    return stack , tupheap[0][0]

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
    codes = {}
    realcodes = {}
    comp_len = 0
    #tup=code_stack.pop()
    codes[root_symbol] = ''
    while(len(code_stack)!=0):
        tup = code_stack.pop()
        codes[tup[0]] = codes[tup[2]] + tup[3]
        if (len(tup[0])==1):
            
            realcodes[tup[0]] = codes[tup[0]]
            comp_len += ( ( len( realcodes[ tup[0] ] ) )*tup[1] )
  
    return realcodes, comp_len

def write_compressed(text_filename , huff_filename , codes, huff_length):
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
    fo2 = open(huff_filename , "w+")
    fo1 = open(text_filename , "r")
    huff = fo1.read()
    freq_table = build_char_table(text_filename)
    count = 0
    for char in freq_table:
        if(freq_table[char]>=1):
            count += 1
    count = str(count)
    huff_length = str(huff_length)
    fo2.write(count+' '+huff_length+'\n')
    for var in codes:
        if(var=='\n'):
            fo2.write(codes[var]+' '+'\\n'+'\n')
        elif(var=='\t'):
            fo2.write(codes[var]+' '+'\\t'+'\n')
        elif(var==' '):
            fo2.write(codes[var]+' '+var+'\n')
        else:
            fo2.write(codes[var]+' '+var+'\n')
    code = ''
    for x_1 in huff:
        code = code + codes[x_1]
    x_2 = len(code)%8
    i = 1
    if(x_2==0):
        while(len(code)!=0):
            b_1 = ''
            b_1 = b_1 + code[:8]
            code = code[8:]
            s_1 = int(b_1 , 2)
            fo2.write(chr(s_1))
    else:
        while(len(code)!=x_2):
            b_1 = ''
            b_1 = b_1 + code[:8]
            code = code[8:]
            s_1 = int(b_1 , 2)
            fo2.write(chr(s_1))
        while(i <= (8 - x_2)):
            code = code + '0'
            i += 1
        c_1 = int(code , 2)
        fo2.write(chr(c_1))
         

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
    code_stack , last_ele = build_huffman_tree(frequency_table , arity_exp)
    #print code_stack
    codes , comp_len = form_codes(last_ele , code_stack)
    write_compressed(text_filename , "huffman.txt" , codes , comp_len)
    return "huffman.txt"
def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    # Your code
    
    s_1 = huff.readline()
    s_1 = s_1.split()
    len1 = (int)(s_1[0])
    len2 = (int)(s_1[1])
    j = 0
    codes = {}
    while(j<len1):
        w_1 = huff.readline()
        d_1 = w_1.split()
        if(len(d_1)==1):
            codes[d_1[0]] = ' '
        elif(d_1[1]=='\\n'):
            codes[d_1[0]] = '\n'
        elif(d_1[1]=='\\t'):
            codes[d_1[0]] = '\t'
        else:
            codes[d_1[0]] = d_1[1]
        j += 1
    return codes , len2

def uncompress(huff_filename):
    '''
    Uncompress a file that has been compressed using compress. Return the name of the uncompressed file.
    Add a '1' or something to the new file name so it does not overwrite the original.
    Algo: (i) Read the code from the first part of the compressed file.
    (ii) Read the rest of the file one bit at a time - every time you get a valid code, write the corresponding
    text character out to the uncompressed file.
    (iii) You need to use the compressed size appropriately - remember the last character that was written
    during .
    Hint: the built-in function 'bin' can be used: bin(n) - returns a 0-1 string corresponding to the binary representation
    of the number n. However the 0-1 string has a '0b' prefixed to it to indicate that it is binary, so you will have to 
    discard the first two chars of the string returned.
    '''
    # Your code
    huff = open(huff_filename , "r")
    new_file = open(huff_filename + '1' , "w")
    codes , comp_len = read_codes(huff)
    code = huff.read()
    bitstr = ''
    for char in code:
        bit = (bin(ord(char))[2:])
        if(len(bit)<8):
            bit = '0' * (8-len(bit)) + bit         
        bitstr = bitstr + bit
#     print a
    bitstr = bitstr[:comp_len]
    c_1 = ''
    for num in bitstr:
        c_1 = c_1 + num
        if c_1 in codes:
            new_file.write(codes[c_1])
            bitstr = bitstr[len(c_1):]
            c_1 = ''
     
    return huff_filename+'1'

if __name__ == '__main__':
    pass
# f=build_char_table("text41")
# print f
# d,e=build_huffman_tree(f,1)
# print d,e
# realcodes,comp_len=form_codes(e,d)
# print realcodes,comp_len
# write_compressed("text41","huffman.txt",realcodes,comp_len)
# filename=compress("text41",1)
# filename2=uncompress("huffman.txt")