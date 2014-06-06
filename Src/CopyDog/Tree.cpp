#include "Tree.h"

Tree::Tree()
{
    fileAsString = "Papau";
    rootNode = NULL;
}

void Tree::createSuffixTree()
{
    rootNode = new Node();

    Node * newNode = new Node(fileAsString.substr(fileAsString.length()-1),rootNode,1);
    rootNode->addChild(newNode);

    for( unsigned int i = 1 ; i < fileAsString.length() ; ++i )
    {
        std::string suffix = fileAsString.substr(fileAsString.length()-i-1);
        insertSuffix(rootNode,suffix);
    }
}

void Tree::insertSuffix(Node* nodeToInsertAt, std::string suffix)
{
    if(NULL == nodeToInsertAt)
    {
        std::cerr << "Null node" << std::endl;
        return;
    }

    for( unsigned int i = 0 ; i < nodeToInsertAt->totalChildren() ; ++ i )
    {
        int positionOfMatch = nodeToInsertAt->getMatchPosition(suffix);

        // Total Match
        if( -2 == positionOfMatch )
        {
           // nodeToInsertAt->getChildList()[i].
        }

        // No match
        else if( -1 == positionOfMatch )
        {

        }

        // Partial match
        else
        {

        }
    }
}

void Tree::printTree()
{

}
