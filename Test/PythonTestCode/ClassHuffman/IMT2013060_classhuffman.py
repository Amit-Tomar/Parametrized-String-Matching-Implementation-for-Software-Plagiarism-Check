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

    import modheap

    
        
    def build_char_table(self,filename):
        '''
        Build and return a hash that maps every character in the file 'filename' to the
        number of occurences of that char in the file
        '''
        DICT={}
        fopen=open(filename,'r')
        data=list(fopen.read())
        for element in data:
            DICT[element]=0
        for element in data:
            DICT[element]=DICT[element]+1
        fopen.close()
        return DICT
        # Your code
    
    
    def cmp_freq(self, char_tup1, char_tup2):
        '''
        Comparison function - compares two tuples (char, freq) on the frequency
        This is the function to be used to initialize the heap
        '''
        # Your code
    
    
    def pad_to_nbits(self, bitstr, pre_post, nbits = 8):
        '''
        Pad a bit string with 0's - to make it a string of length nbits.
        If pre_post < 0, add the 0's at the beginning and otherwise add the zeros at the end
        This might be a good helper function to have -- this function is just a suggestion, it is not mandatory
        '''
        # Your code
        
    
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
        
        final_list=[(y,x) for (x,y) in freq_table.items()]
        stack=[]
        heap=Heap(True,arity_exp,self.cmp_freq)
#         heap.init(is_min=True, arity_exp=1, compare_fn=None)
        
        heap.data=final_list
        heap.heapify()
        while(len(final_list)>1):
            a=heap.pop()
            heap.heapify()
            b=heap.pop()
            heap.heapify()
            new = (a[0]+b[0], a[1]+b[1])
            stack.append((a[1], a[0], a[1]+b[1], '0'))
            stack.append((b[1], b[0], a[1]+b[1], '1'))
            final_list.append(new)
        
        return (stack,final_list[0])
        # Your code
    
    
    def form_codes(self,code_stack):
        '''
        Return a hash with the huffman code for each input character
        Algo: (i) Start from the root symbol - has code '' (empty string)
        (ii) For every element of the code_stack (starting from the end) - form its code by appending the additional bit to 
        the code of its parent (to be got from the hash already built)
        (iv) Keep count of the total compressed length as the codes are being created
        (iii) At the end, remove all the intermediate symbols created while forming the huffman tree from the hash,
        before returning the hash and the compressed length
        '''
        data={}
        stack=code_stack[0]
        stack.reverse()
        return_hash={}
        code_hash={}
        code_hash[stack[0][2]]=''
        for element in stack:
            code_hash[element[0]]=code_hash[element[2]]+element[3]
            if len(element[0])<=1:
                data[element[0]]=element[1]
        for key,value in code_hash.items():
            if len(key)<=1:
                return_hash[key]=value
                
        compressed_length =0
        for key in data:
            temp=data[key]*len(return_hash[key])
            compressed_length = compressed_length+temp
            
        return return_hash, compressed_length
        # Your code
    
    
    def write_compressed(self,text_filename, huff_filename, codes, huff_length):
        '''
        Write the encoded (compressed) form of the text in 'text_filename' to 'huff_filename'. 'huff_length' is the compressed
        length of the contents of the text file
        . 'codes' is the hash that gives the huffman code for each input character
        Algo: (i) Write the number of distinct input chars and the compressed length in one line
        (ii) For each distinct input char, Write the code followed by the char (separated by a space) on separate lines
        (iii) Aggregate/Split the codes for the characters in the text file into 8-bit chunks
        and write each 8-bit chunk out as an ascii character.
        (iv) Careful about the last chunk that is written - the relevant bits left to be written out may be less than 8
        Hint: given a 0-1 string s - int(s, 2) gives the integer treating 's' as a binary (bit) string. (the 2 refers to the
        conversion base.
        '''
        code,compressed_length=codes
        
        fopen = open(text_filename,'r')
        data_file = fopen.read()
        fopen.close()
        
        fwrite= open(huff_filename,'w')
        
        count = 0
        old_data = self.build_char_table(text_filename)
        for key,value in old_data.items():
            temp = value * len(code[key])
            count = count+temp
        string=''   
        for i in data_file:
            string+=code[i]
            
          
           
        fwrite.write(str(len(code))+ ' ' +str(compressed_length)+'\n')
        
        for key,value in old_data.items():
            if key==' ':
                fwrite.write( str(code[key])+' '+'blank'+ '\n')
            elif key=='\n':
                fwrite.write( str(code[key])+' '+'\\n'+ '\n')
            elif key=='\t':
                fwrite.write((str(code[key]))+ ' ' + '\\t'+ '\n')
            else:
                fwrite.write((str(code[key]))+' ' + key+ '\n')
        temp=''   
        for i in string:
            temp+=i
            if(len(temp)==8):
                fwrite.write(chr(int(temp,2)))
                temp=''
        ex=8-len(temp)
        temp=temp+'0'*ex
        fwrite.write(chr(int(temp,2)))  
        # Your code
        
    
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
        freq_table = self.build_char_table(text_filename)
        stack=self.build_huffman_tree(freq_table, arity_exp)
        codes=self.form_codes(stack)
        self.write_compressed(text_filename, 'huff', codes, codes[1])
        
        return 'huff'
        # Your code
    
    
    def read_codes(self,huff):
        '''
        Read the huff code from the file handle 'huff' - note that 'huff' here is not the file name -
        this is what is returned by a call to open(). You can directly start reading stuff from the file using 'huff' here.
        Return a hash of codes (code -> original char) and the compressed length
        '''
        temp=huff.readline()
        temp=temp.split()
        hash={}
        count = int(temp[0])
        for i in range(0,count):
            temp1=huff.readline()
            temp1=temp1.split()
            hash[temp1[0]]=temp1[1]
       
        return hash,int(temp[1])
        
        # Your code
        
    
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
        
        file1=open(huff_filename,'r')
        hash,comp_length=self.read_codes(file1)
        
        data=file1.read()
        check_string=''
        for x in data:
            temp=bin(ord(x))
            temp=temp[2:]
            temp=str(temp)
           
            while len(temp)<8:
                temp='0'+temp
            check_string = check_string + temp
        
        
        
        final_file=open('final','wb') 
        
        var='' 
        check_string = check_string[0:comp_length]
        for element in check_string:
            var=var+element
            if var in hash:
                if hash[var]=='blank':
                    final_file.write(' ')
                elif hash[var]=='\\n':
                    final_file.write('\n')
                elif hash[var]=='\\t':
                    final_file.write('\t')
                else:
                    final_file.write(hash[var])
                var=''
            
        
        return 'final'
        
    if __name__ == '__main__':
        pass