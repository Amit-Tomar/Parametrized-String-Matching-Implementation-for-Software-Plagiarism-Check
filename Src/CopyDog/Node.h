#ifndef NODE_H
#define NODE_H

#include <string>
#include <vector>
#include <iostream>
using namespace std;

class Node
{
public:
    Node(string suffix = "\0", Node *parent = NULL , unsigned int fileNumber = -1);
    void addChild(Node*) ;
    void trimAndAddSelfChild(unsigned int,unsigned int);
    unsigned int getSuffixLength();
    int getMatchPosition(std::string);
    unsigned int totalChildren(){ return childList.size()  ;}
    std::vector<Node*> & getChildList() { return childList ;}

private:

    Node* parentPtr;
    std::vector<Node*> childList;
    std::vector<unsigned int> descendentList;
    std::string suffix;
    int fileNumber;
};

#endif // NODE_H
