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
    
        
    def build_char_table(self,filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        # Your code
        letter_frequency={}
        f=open(filename,"r")
        characters=f.read()
        for i in characters:
            letter_frequency[i]=0
        for i in characters:
            letter_frequency[i]+=1
        return letter_frequency
     
    def cmp_freq(self,char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        e1=char_tup1[1]
        e2=char_tup2[1]
        if (e1>=e2):
            return False
        elif (e1<e2):
            return True
        else:
            return 0
    
    def pad_to_nbits(self,bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code
        bits=bitstr.bit_length()
        print bits
        k=nbits-bits
        if(pre_post<0 and k>=0):
            bitstr='0'*k + bitstr
        elif(pre_post>0 and k>=0):    
            bitstr=bitstr<<k
        
        return bitstr   
            
        
        
    
    def build_huffman_tree(self,freq_table, arity_exp):
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
        #1
        cmp_function = lambda x, y : (1 if (x > y) else (-1 if (x < y) else 0))
        freq_list=[]
        for i in freq_table:
            freq_list.append((freq_table[i],i))
        heap=Heap(True, arity_exp,cmp_function)    
        heap.import_list(freq_list)  
        freq_list=heap.data  
        heap.heapify()
        #2
        stack=[]
        while(len(freq_list)>1):
            a=heap.pop()
            b=heap.pop()
        #3
            ab_name=a[1]+b[1]
            ab_freq=a[0]+b[0]
        #4
            heap.add((ab_freq,ab_name))
        #5        
            stack.append((a[1],a[0],ab_name,'1'))
            stack.append((b[1],b[0],ab_name,'0'))
        return stack, freq_list[0]
    
    def form_codes(self,root_symbol, code_stack):
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
        compressed_frequency=0
        temp={}
        huffman_code={}
        huffman_code[root_symbol]=''
        k=len(code_stack)
        while(k>0):
            t=code_stack.pop()
            if t[2] in huffman_code:
                huffman_code[t[0]]=huffman_code[t[2]]+t[3]
                if(len(t[0])==1):
                    compressed_frequency+=t[1]*len(huffman_code[t[0]])
            else:
                huffman_code[t[0]]=t[3]    
                if(len(t[0])==1):
                    compressed_frequency+=t[1]*len(t[3])
            k-=1        
        for i in huffman_code:
            if (len(i)==1):
                temp[i]=huffman_code[i]
                        
        return temp, compressed_frequency        
    
    def write_compressed(self,text_filename, huff_filename, codes, huff_length):
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
        c=open(huff_filename,"w")
        f=open(text_filename,"r")
        characters=f.read()
        c.write(str(len(codes))+' '+str(huff_length)+'\n')
        for i in codes:
            if i == '\t':
                c.write(codes[i]+' '+'\\t'+'\n')
            elif i=='\n':
                c.write(codes[i]+' '+'\\n'+'\n')
            else:
                c.write(codes[i]+' '+i+'\n')
        compressedstr=''        
        for i in characters:
            compressedstr+=codes[i]  
        compressedchar=''
        for i in compressedstr:
            compressedchar+=i
            if(len(compressedchar)==8):
                c.write(chr(int(compressedchar,2)))  
                compressedchar=''
        last_chunk=8-len(compressedchar)
        compressedchar+='0'*last_chunk
        c.write(chr(int(compressedchar,2)))         
        
        
        
    
    def compress(self,text_filename, arity_exp):
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
        freq_table=self.build_char_table(text_filename)
        stack,last_elem=self.build_huffman_tree(freq_table,arity_exp)
        code_stack,comp_len=self.form_codes(last_elem,stack)
        self.write_compressed(text_filename,text_filename+'.huff',code_stack,comp_len)
        return text_filename+'.huff'
        
    
    
    def read_codes(self,huff):
        ''' 
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        ''' 
        # Your code
        no_of_char,length = huff.readline().split()
        no_of_char,length=int(no_of_char),int(length)
        codes={}
        i=0
        while i < no_of_char:
            line=huff.readline().split()
            if(len(line)==1):
                codes[line[0]]=' '
            elif(line[1]=='\\n'):
                codes[line[0]]='\n'
            elif(line[1]=='\\t'):
                codes[line[0]]='\t'
            else:
                codes[line[0]]=line[1]
            i+=1
        return codes , length
        
    
    def uncompress(self,huff_filename):
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
        huff = open(huff_filename,"r")
        huff1=open(huff_filename+'1',"w")
    #     line = huff.readline()
    #     line = line.split()
    #     no_char = int(line[0])
    #     compressed_length = int(line[1])
    #     codes={}
    #     i=0
    #     while i < no_char:
    #         line=huff.readline()
    #         line=line.split()
    #         if(len(line)==1):
    #             codes[line[0]]=' '
    #         elif(line[1]=='\\t'):
    #             codes[line[0]]='\t'
    #         elif(line[1]=='\\n'):
    #             codes[line[0]]='\n'
    #         else:
    #             codes[line[0]]=line[1]
    #         i+=1
        codes, compressed_length = self.read_codes(huff)
        bit_string = huff.read()
        temp=''
        bit_string1=''
        for i in bit_string:
            temp=bin((ord(i)))
            temp=temp[2:]         
            if (len(temp)<8):
                chunk=8-len(temp)
                temp='0'*chunk+temp
            bit_string1+=temp 
        bit_string1=bit_string1[:compressed_length]    
        temp=''
        for i in bit_string1:
            temp+=i
            if temp in codes:
                huff1.write(codes[temp])
                temp=''
        huff.close()
        huff1.close()        
        return huff_filename+'1'
      
        
    if __name__ == '__main__':
        pass