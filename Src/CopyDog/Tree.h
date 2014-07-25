#ifndef TREE_H
#define TREE_H

#include "Python.h"

#include <string>
#include <vector>
#include <iostream>
#include "Node.h"
#include "Match.h"

//#define TREE_DEBUG_MODE

class Tree
{
public:

    Tree();

    void updateSuffixTree(std::string sourceCode);
    void insertSuffix(Node* nodeToInsertAt, std::string suffix, unsigned int fileNumber);
    void printTree();
    Node * getRootNode() { return rootNode; }

private:

    Node * rootNode;
    std::string fileAsString;
    unsigned int sourceFromFileNumber;
};


#endif // TREE_H
