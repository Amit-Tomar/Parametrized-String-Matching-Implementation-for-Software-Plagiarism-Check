#ifndef NODE_H
#define NODE_H

#include <string>
#include <vector>
#include <iostream>
#include <algorithm>
#include "Match.h"

class Node
{
public:

    Node(std::string suffix = "\0", Node *parent = NULL , unsigned int fileNumber = -1);

    void addChild(Node*) ;
    void addDescendentFileNumber(unsigned int fileNumber);
    void trimAndAddSelfChild(unsigned int position,std::vector<unsigned int> inheritedFileNumberList);
    unsigned int getSuffixLength();
    std::string getSuffix();
    void setSuffix(std::string);
    Match getMatchPosition(std::string);
    unsigned int totalChildren(){ return childList.size()  ;}
    std::vector<Node*> & getChildList() { return childList ;}
    std::vector<unsigned int> & getDescendentList() { return descendentList ;}

private:

    Node* parentPtr;
    std::vector<Node*> childList;
    std::vector<unsigned int> descendentList;
    std::string suffix;
    int fileNumber;
};

#endif // NODE_H
