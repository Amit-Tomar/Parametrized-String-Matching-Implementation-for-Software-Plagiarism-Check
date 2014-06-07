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

    std::cout << "ORIGNIALSUFFIX: " << suffix << std::endl;


    std::string temp = suffix.substr(position+1);
    std::cout << "SUBORIGNIALSUFFIX: " << suffix << std::endl;


    std::cout << "TEMP: " << temp << std::endl;

    suffix = suffix.substr(0,position+1);   // Self Trim

    std::cout << "SUFFIX: " << suffix << std::endl;


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

void Node::setSuffix(string suffix)
{
        this->suffix = suffix;
}

/**
 * @brief  Returns the position at which match occurs.
 *         -2 : Complete match. -1 : No match at all.
 */
Match Node::getMatchPosition(string matchingString)
{
    Match objMatch;

    if( 0 == matchingString.compare(suffix) )
    {
           std::cout << "__" << std::endl ;
        objMatch.matchingType = eFullMatch;
        objMatch.position = suffix.length()-1;
        objMatch.lengthMatchType = eStringSuffixSame;
        return objMatch;
    }

    int position = -1 ;

    for( int i = 0 ; i < suffix.length() ; ++ i )
    {
        //std::cout << "__" << suffix[i] << " " <<  matchingString[i]  << std::endl ;
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
