#ifndef TREE_H
#define TREE_H

#include "Python.h"

#include <string>
#include <vector>
#include <iostream>
#include "Node.h"
#include "Match.h"
using namespace std;

class Tree
{
public:

    Tree();

    void createSuffixTree(std::string sourceCode);
    void insertSuffix(Node* nodeToInsertAt, std::string suffix, unsigned int fileNumber);
    void printTree();

private:

    Node * rootNode;
    std::string fileAsString;
    unsigned int sourceFeomFileNumber;
};


#endif // TREE_H
