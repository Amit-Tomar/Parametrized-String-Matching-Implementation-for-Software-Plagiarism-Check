#include "Node.h"

Node::Node(string suffix, Node *parent , unsigned int fileNumber)
{
    this->suffix = suffix ;
    this->parentPtr = parent;
    this->fileNumber = fileNumber;
}

void Node::addChild(Node * child)
{
    childList.push_back(child);
}

/**
 * @brief  Trim a sub part of suffix string and add it as a child.
 *
 */

void Node::trimAndAddSelfChild(unsigned int position, unsigned int fileNumber)
{
    if( position > suffix.length()-2 )
    {
        std::cerr << "Not a valid position in suffix" << std::endl;
    }

    std::string temp = suffix.substr(position+1,suffix.length());
    suffix = suffix.substr(0,position);

    Node * newNode = new Node(temp,this,fileNumber);
    addChild(newNode);
}

unsigned int Node::getSuffixLength()
{
    return suffix.length();
}

/**
 * @brief  Returns the position at which match occurs.
 *         -2 : Complete match. -1 : No match at all.
 */
int Node::getMatchPosition(string matchingString)
{
    if( 0 == matchingString.compare(suffix) )
        return -2;

    int position = -1 ;

    for( int i = 0 ; i < suffix.length() ; ++ i )
    {
        if( suffix[i] == matchingString[i] )
            ++ position;
        else
            break;
    }

    return position;
}

