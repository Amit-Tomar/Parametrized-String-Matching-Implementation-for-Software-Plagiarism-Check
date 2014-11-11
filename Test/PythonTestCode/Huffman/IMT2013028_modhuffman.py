'''
Created on 28-Oct-2013

@author: raghavan
'''
import modheap

codes = {}

def build_char_table(filename):
    '''
    Build and return a hash that maps every character in the file 'filename' to the
    number of occurences of that char in the file
    '''
    # Your code
    occur = {}
    fileptr = open(filename)
    string = fileptr.read()
    for i in string:
        if not(i in occur):
            occur[i] = 1
        else:
            occur[i] += 1
    return occur


def cmp_freq(char_tup1, char_tup2):
    '''
    Comparison function - compares two tuples (char, freq) on the frequency
    This is the function to be used to initialize the heap
    '''
    # Your code


def pad_to_nbits(bitstr, pre_post, nbits = 8):
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
    stack = []
    for i in freq_table:
        stack.append([freq_table[i], i])
    modheap.initialize_heap(True, arity_exp)
    modheap.import_list(stack)
    modheap.heapify()
    new_stack = []    
    while(modheap.size()>= 2):
        tup1 = modheap.pop()
        tup2 = modheap.pop()
        add = [tup1[0]+tup2[0], tup1[1]+tup2[1]]
        modheap.add(add)
        new_stack.append([tup1[1], tup1[0], add[1], ""])
        new_stack.append([tup2[1], tup2[0], add[1], ""])
    new_stack.extend(modheap.DATA)
    new_stack[-1] = [new_stack[-1][1]]+new_stack[-1]+[""]
    new_stack[-1][2] = ""

    for j in new_stack:
        if(len(j[0]) == 1):
            form_codes(j, new_stack) 
    
    for i in new_stack:
        if(len(i[0]) == 1):
            codes[i[0]] = i[3]  

    return  new_stack[:-1], new_stack[-1]

def form_codes(root_symbol, char_stack):
#def form_codes(char_stack):
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
    parent = []
    if(len(root_symbol[2])==0):
        return ""
    if(root_symbol[3] != ""):
        return root_symbol[3]
    if(root_symbol == char_stack[-1]):
        return ""
    else:
        for i in char_stack:
            if(i[0] == root_symbol[2]):
                parent = i
        if(parent == []):
            return ""
    if(root_symbol[0] == parent[0][:len(root_symbol[0])]):
        root_symbol[3] = form_codes(parent, char_stack)+"0"
    else:
        root_symbol[3] = form_codes(parent, char_stack)+"1"
    return root_symbol[3]
              

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
    new_str = ""
    
    #Initial reading for finding binary string
    fileptr = open(text_filename, "r")
    string = fileptr.readlines()
    for j in string:
        for i in j:
            new_str = new_str+codes[i]
    #newstr will have a long string of all the binary codes together
    
    #writing codes into file
    binfile = open(huff_filename, 'w')
    binfile.write(chr(len(codes))+" "+str(huff_length)+"\n")#writing number of lines of codes into file
    for i in codes:
        if(i == " "):
            binfile.write("<space>"+" "+codes[i]+"\n")
        elif(i == "\n"):
            binfile.write("<new>"+" "+codes[i]+"\n")            
        elif(i == "\t"):
            binfile.write("<tab>"+" "+codes[i]+"\n")  
        else:
            binfile.write(i+"  "+codes[i]+"  \n")

    count = 0
    temp = ""
    for i in new_str:
        if(count<8):
            temp += i
            count += 1
        if(count == 8):
            count = 0
            binfile.write(chr(int(temp, 2))) 
            temp = "" 
    #padding here
    if(temp != "" and len(temp)<8):
        temp = "00000000000"+temp
        temp = temp[-8:]
        binfile.write(chr(int(temp, 2)))
    binfile.close()
    #now binfile will have charecters coded and written

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
    occur = build_char_table(text_filename)
    stack, stack[-1] = build_huffman_tree(occur, arity_exp)
    stack = stack[:-1]
    count = 0
    for j in stack:
        if(len(j[0]) == 1):
            codes[j[0]] = j[3]
            count = count + (len([j[3]])*j[1])
    write_compressed(text_filename, text_filename+".huff", codes, count)
    return text_filename + ".huff"


def read_codes(huff):
    '''
    Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
    this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
    Return a hash of codes (code -> original char) and the compressed length
    '''
    # Your code
    rev_codes = {}
    readfile = open(huff, 'r')
    lines = readfile.readline()
    number_of_lines = ord(lines[0])+1
    string = ""
    for i in range(number_of_lines):
        string += readfile.readline()
    string = string.split()
    count = 0
    while(count<len(string)-1):
        rev_codes[string[count+1]] = string[count]
        if(string[count] == '<space>'):
            rev_codes[string[count+1]] = " "
        if(string[count] == '<new>'):
            rev_codes[string[count+1]] = "\n"
        if(string[count] == '<tab>'):
            rev_codes[string[count+1]] = "\t"
        count += 2          
    return rev_codes
    
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
    rev_codes = read_codes(huff_filename)
    
    readfile = open(huff_filename, 'r')
    writefile = open("text_new.txt", "w")
    
    #dummy reading past the codes
    readfile = open(huff_filename, 'r')
    lines = readfile.readline()
    number_of_lines = ord(lines[0])
    for i in range(number_of_lines):
        readfile.readline()
    
    binstr = readfile.read(1)
    
    new_str = ""
    while(binstr != ""):
        temp = bin(ord(binstr))[2:]
        if(len(temp)<8):
            temp = "000000000000"+temp
            temp = temp[-8:]
        new_str += temp
        binstr = readfile.read(1)
    
    temp = new_str[-8:]
    for i in temp:
        if(i == "0" and ("0" in rev_codes)):
            temp = temp[1:]
        else:
            break
    new_str = new_str[:-8]+temp
    #this will get back THAT long original binary string
    
    read_data = ""
    for i in new_str:
        read_data += i
        if read_data in rev_codes:
            writefile.write(rev_codes[read_data])
            read_data = ""
    writefile.close()
    
    return "text_new.txt"

if __name__ ==  '__main__':
    pass
    compress("text3", 1)
    uncompress("text3"+".huff")