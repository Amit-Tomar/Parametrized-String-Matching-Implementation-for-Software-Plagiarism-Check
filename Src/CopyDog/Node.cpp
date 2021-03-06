#include "Node.h"

Node::Node(std::string suffix, Node *parent , unsigned int fileNumber)
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
 * @brief  Adds the descendent file number to the descendents list
 *
 */

void Node::addDescendentFileNumber(unsigned int fileNumber)
{
    if( descendentList.end() == std::find( descendentList.begin(), descendentList.end(), fileNumber ) )
        descendentList.push_back(fileNumber);
}

/**
 * @brief  Trim a sub part of suffix string and add it as a child.
 *
 */

void Node::trimAndAddSelfChild(unsigned int position, std::vector<unsigned int> inheritedFileNumberList)
{
    if( position > suffix.length()-2 )
    {
        std::cerr << "Not a valid position in suffix" << std::endl;
    }

    std::string temp = suffix.substr(position+1);

    suffix = suffix.substr(0,position+1);   // Self Trim

    // @TBD Remove the filenumber data member, not required
    Node * newNode = new Node(temp,this,fileNumber);

    for( int i = 0 ; i < inheritedFileNumberList.size() ; ++ i )
    {
        newNode->getDescendentList().push_back(inheritedFileNumberList[i]);
    }

    addChild(newNode);
}

unsigned int Node::getSuffixLength()
{
    return suffix.length();
}

std::string Node::getSuffix()
{
    return suffix;
}

void Node::setSuffix(std::string suffix)
{
        this->suffix = suffix;
}

/**
 * @brief  Returns the position at which match occurs.
 *         -2 : Complete match. -1 : No match at all.
 */
Match Node::getMatchPosition(std::string matchingString)
{
    Match objMatch;

    if( 0 == matchingString.compare(suffix) )
    {
        objMatch.matchingType = eFullMatch;
        objMatch.position = suffix.length()-1;
        objMatch.lengthMatchType = eStringSuffixSame;
        return objMatch;
    }

    int position = -1 ;

    for( int i = 0 ; i < suffix.length() ; ++ i )
    {
        if( suffix[i] == matchingString[i] )
            ++ position;
        else
            break;
    }

    if( suffix.length() < matchingString.length() )
        objMatch.lengthMatchType = eStringLarger;
    else
        objMatch.lengthMatchType = eSuffixLarger;

    if( -1 == position )
    {
        objMatch.matchingType = eNoMatch;
        objMatch.position = -1;
    }

    else
    {
        objMatch.matchingType = ePartialMatch;
        objMatch.position = position;
    }

    return objMatch;
}
