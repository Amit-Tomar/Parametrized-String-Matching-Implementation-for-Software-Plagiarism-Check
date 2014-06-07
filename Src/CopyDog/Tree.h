#ifndef TREE_H
#define TREE_H

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
    void createSuffixTree();
    void insertSuffix(Node* nodeToInsertAt, std::string suffix, unsigned int fileNumber);
    void printTree();

private:

    Node * rootNode;
    std::string fileAsString;
};


#endif // TREE_H
