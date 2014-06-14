import ast

class FirstParser(ast.NodeVisitor):

    def __init__(self):
        pass

    def visit_Name(self, node):
        print 'Name:', node.id

def createSuffixCompatibleSource(sourceFile):

    #print 'The source code file is :', sourceFile

    code = "def main(a,b,c):    i=10"

    tree = ast.parse(code)
    parser = FirstParser()
    parser.visit(tree)

    expr_ast = ast.parse(tree)
    print ast.dump(expr_ast)

    return ast.dump(expr_ast)






