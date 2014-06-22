# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 11:06:50 2014

@author: vaidya
"""

import ast
import Unparse
import os

class FirstParser(ast.NodeVisitor):

    def __init__(self):
        pass

    def visit_Name(self, node): 
        node.id = "P"
 
def createSuffixCompatibleSource(code ):                            

    # builds a parse tree.
    try:
        tree = ast.parse(code)
    except:
        return ""  # Empty String = Error flag
            
    # creating object of FirstParser class
    parser = FirstParser()
            
    # calling the function & modifying identifier to "P".
    parser.visit(tree)

    # Creating a temporary file.        
    filePtr = open("temp" , "w")
        
    #Unparsing the modified tree, which writes onto temp file
    Unparse.Unparser(tree, filePtr )
        
    #Opening the temp file
    filePtr = open("temp", "r")

    #Reading the contents of temp file onto ModifiedCodeInString
    ModifiedCodeInString = filePtr.read()
        
    # deleting the temp file
    os.remove("./temp")
        
    return ModifiedCodeInString
