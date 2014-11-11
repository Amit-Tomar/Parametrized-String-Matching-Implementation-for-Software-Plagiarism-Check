'''
Created on 28-Oct-2013

@author: raghavan
'''
import modheap
global nbits

def char_finder(freq_table,search_freq):
    for char,freq in freq_table.iteritems():
        if freq == search_freq:
            return char
    
def build_char_table(filename):
    '''
    Build and return a hash that maps every character in the file 'filename' to the
    number of occurences of that char in the file
    '''
    s=open(filename,"r")
    f=s.read()
    if(len(f)==0):
        return None
    else:
        freq_table={}
        for x in f:
            if x in freq_table:
                freq_table[x]+=1
            else:
                freq_table[x]=1
    return freq_table


def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    if(char_tup1[1]>char_tup2[1]):
        return 1
    elif(char_tup1[1]==char_tup2[1]):
        return 0
    if(char_tup1[1]<char_tup2[1]):
        return -1


def pad_to_nbits(bitstr, pre_post, nbits = 8):
    '''
    Pad a bit string with 0's - to make it a string of length nbits.
    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
    This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
    '''
    if(pre_post<0):
        return (nbits*'0')+bitstr
    else:
        return bitstr+(nbits*'0')

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
    code_stack = [] 
    modheap.initialize_heap(True, arity_exp, cmp_freq)
    modheap.DATA = freq_table.items()
    modheap.heapify()
    element1 = modheap.pop()
    element2 = modheap.pop()
    code_stack.append(element1[0],element1[1],element1[0]+element2[0],'1')
    code_stack.append(element2[0],element2[1],element1[0]+element2[0],'1')
    parent_element=(element1[0]+element2[0],element1[1]+element2[1])
    modheap.add(parent_element)
    while(len(modheap.DATA)!=0):
        pop_element = modheap.pop()
        code_stack.append(pop_element[0],pop_element[1],pop_element[0]+parent_element[0],'1')
        parent_element=(parent_element[0]+pop_element[0],parent_element[1]+pop_element[1])
        modheap.add(parent_element)
    return code_stack,''
        
        
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
    '''code={}
    i=len(code_stack)
    code[code_stack[-1][2]]=''
    while(i>0):
        code[code_stack[i-1][0]]=code_stack[i-1][3]+code[code_stack[i-1][2]]
        root_symbol=root_symbol+code_stack[i-1][3]
    return code,len(root_tmbol)'''
    huffman_dict={}
    i=0
    compressed_length=0
    while(i<len(code_stack)):
        j=0
        while(j<len(code_stack)):
            if(code_stack[i][2]==code_stack[j][0]):
                huffman_dict[code_stack[i][0]]=code_stack[i][3]+code_stack[j][3]
                compressed_length+=code_stack[i][1](len(huffman_dict[code_stack[i][0]]))
            j+=1
        i+=1
    k=0
    while(len(code_stack[k][2])!=1):
        del huffman_dict[code_stack[k][0]]
    return huffman_dict,compressed_length


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
    f=open(text_filename,"r")
    fi=open(huff_filename,"w")
    f_str=f.read()
    bit_str=''
    fi.write("%d %d\n",len(codes),huff_length)
    for key in codes:
        fi.write("%s %s\n",codes[key],key)
        if(key==" "):
            fi.write("%s %s\n",codes[key],"SPACE")
        elif(key=="\t"):
            fi.write("%s %s\n",codes[key],"TAB")
        elif(key=="\n"):
            fi.write("%s %s\n",codes[key],"NEWLINE")
    for x in f_str:
        bit_str+=codes[x]
        nbits=8-(len(bit_str)%8)
        pad_to_nbits(bit_str)
    bitstr1=''
    for i in bit_str:
        bitstr1+=i
        if(len(bitstr1)==8):
            fi.write(chr(bitstr1))
            bitstr1=''


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
    freq_table=build_char_table(text_filename)
    code_stack,root=build_huffman_tree(freq_table,arity_exp)
    huffman_dict,compressed_length=form_codes(root,code_stack)
    write_compressed(text_filename,"compressed_huffman",huffman_dict,compressed_length)


def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    list=[]
    str=huff.read()
    list=str.split()
    for i in range((int)list[1]):
        if()
    
    

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


if __name__ == '__main__':
    pass
