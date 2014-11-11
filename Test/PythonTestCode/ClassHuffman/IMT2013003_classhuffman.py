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
    import modheap
    
    def build_char_table(self,filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurence`s of that char in the file
        '''
        f=open(filename,"r")
        s=f.read()
        l=[]
        frequency_hash={}
        for c in s:
            l.append(ord(c))
        for var in l:
            frequency_hash[chr(var)]=0
        
        for c in s:
            frequency_hash[c]+=1
        return frequency_hash
        
        
    


    def cmp_freq(self,char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        if(char_tup1[1]>char_tup2[1]):
            return char_tup1[0]
        else:
            return char_tup2[0]

    def cmp_freq_small(self,char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
        if(char_tup1[1]<char_tup2[1]):
            return char_tup1[0]
        else:
            return char_tup2[0]

    def pad_to_nbits(self,bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code
        str_add='0'
   
        if(pre_post>0):
            while(len(bitstr)<nbits):
                bitstr=bitstr+str_add
        elif(pre_post<0):   
            while(len(bitstr)<nbits):
                bitstr=str_add+bitstr
    
        return bitstr


    def pop(self,freq_table):
        ''' Pops the element with highest frequency and returns the most frequent character'''
        if(len(freq_table)!=0):
            ref_min_freq= freq_table[min(freq_table)]
            for c in freq_table:
                    if (freq_table[c]<ref_min_freq):
                        ref_min_freq=freq_table[c]   
    
            for a in freq_table:
                    if (freq_table[a]==ref_min_freq):
                            freq_table.pop(a)
                            return a
       




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
        temp_var=-1
        ref_count=0
        new_heap=[]
        stack_heap=[]
        ref_hash=freq_table.copy()
        len_freqtable=len(freq_table)
        while(len_freqtable>1):
           
            new_heap.append(self.pop(freq_table))
            new_heap.append(self.pop(freq_table))
            pop_first=new_heap.pop(0)
            freq_first=ref_hash[pop_first]
            pop_second=new_heap.pop(0)
            freq_second=ref_hash[pop_second]
            append_composite=pop_first+pop_second
            stack_heap.append((pop_first,freq_first,append_composite,'0'))
            ref_count=ref_count+1        
            stack_heap.append((pop_second,freq_second,append_composite,'1'))
            ref_count=ref_count+1
            freq_table[append_composite]=freq_first+freq_second
            ref_hash[append_composite]=freq_first+freq_second
            len_freqtable=len_freqtable-1
            temp_var=temp_var-1 
    
        ref_tuple=stack_heap[ref_count-1]
        root_element=ref_tuple[2]
        root_frequency=ref_tuple[1]    
            

        return stack_heap,(root_element,root_frequency)


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
        code_hash={}
        count_compressedlength=0
        len_tree=len(code_stack)
        code_hash[code_stack[len_tree-1][0]]='0'
        code_hash[code_stack[len_tree-2][0]]='1'
        i=2
        k=1
        temp_var=len_tree
        code_hash[root_symbol]=''
        while(temp_var>=0):
            while(i<=len_tree):
                if (code_stack[len_tree-i][2]==code_stack[len_tree-k][0]):
                    code_hash[code_stack[len_tree-i][0]]=(str(code_hash[code_stack[len_tree-k][0]])+code_stack[len_tree-i][3])
                    i=i+1
                else:
                    i=i+1
            i=2
            k=k+1
            temp_var=temp_var-1
        copy_hash=code_hash.copy()
        for c in copy_hash:
            if (len(c)!=1):
                code_hash.pop(c)
        for c in code_hash:
            count_compressedlength+=len(code_hash[c])
    
        return code_hash,count_compressedlength

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
        txt_file = open(text_filename, "r")
        file_huffman = open(huff_filename, "w")
        ref_data = ""
        ref_string = ""
        file_huffman.write(str(len(codes))+' '+str(huff_length)+"\n")
        for key in codes :
            if key == '\n':
                file_huffman.write(codes[key]+' '+'\\n'+'\n')
            elif key == '\t':
                file_huffman.write(codes[key]+' '+'\\n'+'\n')
            else :
                file_huffman.write(codes[key]+' '+key+'\n')
        for char in txt_file.read():
            ref_string += codes[char]
        txt_file.close()
        for char in ref_string :
            ref_data += char 
            if len(ref_data) == 8 :
                file_huffman.write(chr(int(ref_data, 2)))
                ref_data = ""
        if len(ref_data) is not 0:
            ref_data += '0'*(8-len(ref_data))
            file_huffman.write(chr(int(ref_data, 2)))
        
                


    def compress(self,text_filename, arity_exp):
        '''
        Compress a give text file 'text_filename' using a heap with arity 2^arity_exp
        Algo: (i) Build the frequency table
        (ii) Build code stack by building the huffman tree from the frequency table
        (iii) Form the codes from the code stack
        (iv) Write out the compressed file
        Return the name of the compressed file. Might help to have a convention here - the original file name without the extension
        appended with '.huff' could be one way.`
        '''
        # Your code
        freq_char = self.build_char_table(text_filename)
        code_stack, root_symb = self.build_huffman_tree(freq_char, arity_exp)
        codes, huff_len = self.form_codes(root_symb, code_stack)
        huff_file = text_filename + '.huff'
        self.write_compressed(text_filename, huff_file, codes, huff_len)
        return huff_file

   
      

    

    def read_codes(self,huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        # Your code
        freq_table=self.build_char_table(huff)
        huffman_tree=self.build_huffman_tree(huff,1)[0]
        ref_hash={}
        assign_codes=self.form_codes(self,'random_rootname',huffman_tree)
        for c in huff:
            ref_hash[c]=assign_codes[c]
        print ref_hash
    

        
        
        

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
        codes , comp_len = self.read_codes(huff)
        str = ''
        bit_str = huff.read()
        for i in bit_str:  
            temp_var = bin( ord(i) )
            temp_var = temp_var[2:]
            if(len( temp_var ) < 8):
                extra_bit = 8 - len(temp_var)
                temp_var = '0' * extra_bit + temp_var
            str += temp_var
        str=str[0:comp_len]
        temp_var = ''
        decomp_name = huff_filename + '1'
        decomp_file = open(decomp_name , "w")
        for i in str:
            temp_var+=i
            if temp_var in codes:
                decomp_file.write( codes[temp_var] )
                temp_var = ''
        return decomp_name
        huff.close()
        decomp_file.close()
        return decomp_name

if __name__ == '__main__':
    pass