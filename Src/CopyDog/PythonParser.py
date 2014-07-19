# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 21:08:01 2014

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


class StripWhiteSpaceParser(ast.NodeVisitor):

    def __init__(self):
        pass


def parseAndStripWhiteSpaceComments(code):

    try:
        tree = ast.parse(code)
     #   print ast.dump(tree)
    except:
        return "Error"  # Empty String = Error flag

     # creating object of FirstParser class
    objStripWhiteSpaceParser = StripWhiteSpaceParser()

    # calling the function & modifying identifier to "P".
    objStripWhiteSpaceParser.visit(tree)

    # Creating a temporary file.
    filePtr = open("temp" , "w")

    #Unparsing the modified tree, which writes onto temp file
    Unparse.Unparser(tree, filePtr )

    #Opening the temp file
    filePtr = open("temp", "r")

    #Reading the contents of temp file onto ModifiedCodeInString
#    CodeInString = filePtr.read()


    '''
    1. Vertical and horizontal extra spacing removed.
    2. # comments removed.
    3. all \''' type comments is reduced to a single line \' comment

    To make code comment free we need to remove \' *\' comment
    '''

    #holds first character
    firstChar = ""

    CodeInString = ""

    with open("temp") as f:
        for line in f:
            for ch in line:
                if ch == ' ':
                    pass
                else:
                    firstChar = ch
                    break;

            if firstChar == "'" or firstChar == "\"":
                pass
            else:
                CodeInString = CodeInString + line



    # deleting the temp file
    os.remove("./temp")

    return CodeInString


def createSuffixCompatibleSource(code ):

    # builds a parse tree.
    try:
        tree = ast.parse(code)
     #   print ast.dump(tree)
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



def getPlainText(programCode, suffixCode):

 #   print suffixCode

    SourceCode = createSuffixCompatibleSource(programCode)
    print " MODIFIED SOURCE CODE: \n ",SourceCode

    loc = SourceCode.find(suffixCode)
#    print "\n FOUND AT: Character No.", loc

 #   print "LOC = ",loc

    newLine = '\n'
    noOfLines = SourceCode.count(newLine,0,loc)

    print noOfLines

 #   print "len of suffix ",len(suffixCode)
    count = 0
    ptrChar = 0;

    for ch in programCode:
        if ch == '\n':
            count=count+1

        if count == noOfLines:
            break;

        ptrChar = ptrChar+1

    return programCode[ptrChar:ptrChar+len(suffixCode)+10]
