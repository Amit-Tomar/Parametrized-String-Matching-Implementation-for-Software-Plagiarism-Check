'''
Created on Nov 12, 2013

@author: imt2013031
'''
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
    s=open(filename,"r")
    s=s.read()
    s=s.lower()
    numberofletters=dict()
    i=ord('a')
    while(i<=ord('z')):
        numberofletters[chr(i)]=0
        i=i+1
    for c in s:
        z=ord(c)
        if(z<=ord('z') and z>=ord('a')):
            numberofletters[c]=numberofletters[c]+1
    return numberofletters
def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    if(char_tup1[1]>char_tup2[1]):
        return 1
    if(char_tup1[1]==char_tup2[1]):
        return 0
    if(char_tup1[1]<char_tup2[1]):
        return -1
def pad_to_nbits(bitstr, pre_post, nbits = 8):
    '''
    Pad a bit string with 0's - to make it a string of length nbits.
    If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
    This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
    '''
    k=len(bitstr)
    if(pre_post<0):
        while(k<=nbits):
            bitstr=bitstr+'0'
            k=len(bitstr)
    else:
        while(k<=nbits):
            bitstr='0'+bitstr
            k=len(bitstr)
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
    modheap.initialize_heap(True,arity_exp,cmp_freq)
    modheap.DATA=freq_table.values()
    list0=freq_table.items()
    stack=[]
    i=0
    while(len(modheap.DATA)>1):
        n=0
        m=0
        modheap.heapify()
        print modheap.DATA
        a=modheap.pop()
        b=modheap.pop()
        for letter,frequency in list0:
            if(frequency==a):
                a1=letter
                k1=n
            else:
                n=n+1
            if(frequency==b):
                b1=letter
                k2=m
            else:
                m=m+1
        if(k2<k1):
            del list0[k1]
            del list0[k2]
        if(k2>k1):
            del list0[k2]
            del list0[k1]
        list0.append((a1+b1,a+b))
        stack=stack+[(a1,a,0)]+[(b1,b,1)]
        dict2=dict(list0)
        modheap.DATA=dict2.values()
    modheap.DATA=stack
    pi=modheap.get_parent_index(i)
    data=[]
    while(i<=len(stack)-1):
        if(pi!=None):
            data=data+[stack[i][:-1]+(stack[pi][0],)+(stack[i][-1],)]
        if(pi==None):
            data=data+[stack[i][:-1]+('None',)+(stack[i][-1],)]
        i=i+1
        pi=modheap.get_parent_index(i)
    return data
        
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


def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
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
    # Your code


if __name__ == '__main__':
    pass
MIN_TOP=True
dict1={'a': 18, 'c': 22, 'b': 14, 'e': 18, 'd': 23, 'g': 18, 'f': 22, 'i': 21, 'h': 24}
'''av='''
build_huffman_tree(dict1,1)
'''print av'''
