'''
Created on 28-Oct-2013

@author: raghavan
'''
import modheap

def huff_initialize(x):
    global INFO
    INFO=x
    
def build_char_table(filename):
    '''
    Build and return a hash that maps every character in the file 'filename' to the
    number of occurences of that char in the file
    '''
    f=open(filename,"r")
    f_t={}
    ch = f.read()
    for i in ch:     
        if (f_t.has_key(i)):
            f_t[i] += 1
        else:
            f_t[i] = 1
    return f_t        
        
                   
def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    a=char_tup1[1]
    b=char_tup2[1]
    if a<b:
        return -1
    elif a>b:
        return 1
    else:
        return 0
    

def pad_to_nbits(bitstr, pre_post, nbits = 8):
    '''
    Pad a bit string with 0's - to make it a string of length nbits.
    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
    This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
    '''
    if pre_post<0:
        return '0'*nbits + bitstr
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
    Elements of the stack are of the form (element, frequency, parent, additional_code_bit)
    (vi) Repeat the above four steps till the heap has only the root element left
    (vii) Return the stack along with the top root element of the heap
    '''
    stack=[]      
    freq_table=freq_table.items()
    modheap.initialize_heap(True, arity_exp, cmp_freq)
    for i in freq_table:
        modheap.add(i)
 
    while(len(modheap.DATA)>1):
        p1=modheap.pop()
        p2=modheap.pop()
        stack.append((p1[0],p1[1],p2[0]+p1[0],1))
        stack.append((p2[0],p2[1],p2[0]+p1[0],0))
        modheap.add((p2[0]+p1[0],p1[1]+p2[1]))
        
    #stack.append((modheap.DATA[0][0],modheap.DATA[0][1],"root",1))
    #stack.append((modheap.DATA[1][0],modheap.DATA[1][1],"root",0))
 
    return stack, modheap.DATA[0][0] 


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
    count=0
    h_c={'root':root_symbol}
    for x in range(len(code_stack[::-1])):
        h_c[code_stack[x][0]]=h_c[code_stack[x][2]]+code_stack[x][3]
        count+=len(h_c[code_stack[x][0]])
    for a in h_c.keys():
        if len(a)>1:
            del h_c[a]
    return h_c
    return count


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
    f_read=open(text_filename,"r")
    file_read=f_read.read()
    f_write=open(huff_filename,"w")
    f_write.write("%d %d \n" %(len(codes),huff_length))
    for a in codes.keys():
        if a=='':
            f_write.write(codes[a]+' space\n')
        elif a=='\t':
            f_write.write(codes[a]+' tab\n')
        elif a=='\n':
            f_write.write(codes[a]+' newline\n')
        elif a=='\\':
            f_write.write(codes[a]+' backward\n')
        else:
            f_write.write(codes[a]+''+a+'\n')
    comp=''
    bit=''
    a=''
    for x in file_read:
        a=a+str(codes[x])
    for x in a:
        bit+=x
        if len(bit==8):
            comp+=chr(int(bit,2))
            bit=''
    x=(8-len(bit)%8)
    huff_initialize(x)
    if len(bit)>0 and len(bit)<0:
        comp+=chr(int(pad_to_nbits(bit,1,x,2)))
    f_write.write(comp)
    f_write.close()
    f_read.close()
         
               
        

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
    file1=build_char_table(text_filename)
    ar=arity_exp
    code_stack,root_symbol=build_huffman_tree(file1,ar)
    h_c,count=form_codes('',code_stack)
    write_compressed(text_filename,"huffman.compress",h_c,count)
    return 'huffman.compress'
    
    
    
def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    filen=huff.read()
    filen=filen.split()
    len_comp=filen[1]
    h_c={}
    for x in range(filen[0]):
        x=huff.read()
        x=x.split()
        if x[1]=='space':
            h_c[x[0]]=''
        elif x[1]=='newline':
            h_c[x[0]]='\n'
        elif x[1]=='tab':
            h_c[x[0]]='t'
        elif x[1]-'backward':
            h_c[x[0]]='\\'             
        else:
            h_c[x[0]]=x[1]
    huff.close()
    return h_c
    return len_comp
    
    

def uncompress(huff_filename):
    '''
    Uncompress a file that has been compressed using compress. Return the name of the uncompressed file.
    Add a '1' or something to the new file name so it does not overwrite the original.
    Alreturngo: (i) Read the code from the first part of the compressed file.
    (ii) Read the rest of the file one bit at a time - every time you get a valid code, write the corresponding
    text character out to the uncompressed file.
    (iii) You need to use the compressed size appropriately - remember the last character that was written
    during compression.
    Hint: the built-in function 'bin' can be used: bin(n) - returns a 0-1 string corresponding to the binary representation
    of the number n. However the 0-1 string has a '0b' prefixed to it to indicate that it is binary, so you will have to 
    discard the first two chars of the string returned.
    '''
    file1=open(huff_filename,"r")
    file1=file1.read()
    coder=read_codes(file1)
    func=''
    bini=''
    for x in file1:
        bini=bin(ord(x))[2:]
        func+=pad_to_nbits(bini,-1,8-len(bini))
    huff1=''
    huff2=''
    func=func[:(len(func)-INFO-8)]
    for x in func:
        huff1+=x
        if huff1 in coder.keys():
            huff2++coder[huff1]
            huff1=''
    uncomp=open(huff_filename,"w")
    uncomp.write(huff2)
    return huff_filename        
         



if __name__ == '__main__':
    #print build_char_table("text3")
    pass
'''
c=build_char_table("t")
print c
d= build_huffman_tree(c, 1)
print d
'''