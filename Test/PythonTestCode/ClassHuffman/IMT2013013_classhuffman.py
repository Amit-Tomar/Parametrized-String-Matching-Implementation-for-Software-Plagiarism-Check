'''
Created on 23-Oct-2013

@author: raghavan
'''
# Importing the Heap class from classheap
from classheap import Heap

class Huffman(object):
    '''
    Huffman coding class
    This class does not need an explicit constructor --- the class does not have any attributes to be initialized
    So a constructor method __init__ is not given - python will use a default constructor for such classes
    
    Methods will be the same as the functions in the modhuffman module
    '''
    
    
    # Your code
    # Add all the Huffman class methods here
    def build_char_table(self, filename):
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
            
                       
    def cmp_freq(self, char_tup1, char_tup2):
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
        
    
    def pad_to_nbits(self, bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        if pre_post<0:
            return '0'*nbits + bitstr
        else:
            return bitstr + '0'*nbits 
        
    
    def build_huffman_tree(self, freq_table, arity_exp):
        '''
        Build the huffman tree for the input textfile and return a stack (maybe along with the character at the root node)
        Algo: (i) Start by making a heap out of freq_table using heap
        (ii) Pop two elements out of the heap at a time
        (iii) Form a composite character that is the concatenation of the two and the combined frequency of the two
        (iv) Add the new composite character with its frequency to the heap
        (v) Add the two popped elements to a stack - simply append to a list
        Elements of the stack are of the form (element, frequency, parent, additional_code_bit)
        (vi) Repeat the above four steps till the heap has only the root element left
        (vii) Return the stack along with the top root element of the heap
        '''
        stack=[] 
        heap = Heap(True, arity_exp, self.cmp_freq)     
        freq_table=freq_table.items()
        
        for i in freq_table:
            heap.add(i)
     
        while(len(heap.DATA)>1):
            p1=heap.pop()
            p2=heap.pop()
            stack.append((p1[0],p1[1],p2[0]+p1[0],1))
            stack.append((p2[0],p2[1],p2[0]+p1[0],0))
            heap.add((p2[0]+p1[0],p1[1]+p2[1]))
            
        #stack.append((heap.DATA[0][0],heap.DATA[0][1],"root",1))
        #stack.append((heap.DATA[1][0],heap.DATA[1][1],"root",0))
     
        return stack, heap.DATA[0][0] 
    def read_codes(self, huff):
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
    

if __name__ == '__main__':
    pass