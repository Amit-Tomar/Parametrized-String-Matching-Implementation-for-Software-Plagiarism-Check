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
        insertSuffix(rootNode,suffix,1); // @TBD Pass File number properly
    }
}

void Tree::insertSuffix(Node* nodeToInsertAt, std::string incomingSuffixToInsert, unsigned int fileNumber)
{
    if(NULL == nodeToInsertAt)
    {
        std::cerr << "Null node" << std::endl;
        return;
    }

    Match objMatch;

    for( unsigned int i = 0 ; i < nodeToInsertAt->totalChildren() ; ++ i )
    {
        objMatch = nodeToInsertAt->getMatchPosition(incomingSuffixToInsert);

        // Total Match
        if( eFullMatch == objMatch.matchingType )
        {
           nodeToInsertAt->getChildList()[i]->addDescendentFileNumber(fileNumber);
           return;
        }

        // No match
        else if( eNoMatch == objMatch.matchingType )
        {
            continue;
        }

        // Partial match
        else
        {
            if( eStringLarger == objMatch.lengthMatchType)
            {
                nodeToInsertAt->addDescendentFileNumber(fileNumber);
                incomingSuffixToInsert = incomingSuffixToInsert.substr(objMatch.position+1 );

                // Suffix exhausted
                if( objMatch.position == incomingSuffixToInsert.length()-1  )
                {
                    insertSuffix(nodeToInsertAt->getChildList()[i],incomingSuffixToInsert, fileNumber);
                    return;
                }
                // Suffix not exhausted
                else
                {
                    insertSuffix(nodeToInsertAt->getChildList()[i],incomingSuffixToInsert, fileNumber);
                    nodeToInsertAt->getChildList()[i]->trimAndAddSelfChild(objMatch.position, fileNumber);
                    insertSuffix(nodeToInsertAt->getChildList()[i],incomingSuffixToInsert, fileNumber);
                    return;
                }
            }
            else if( eSuffixLarger == objMatch.lengthMatchType )
            {

            }
            return;
        }
    }
}

void Tree::printTree()
{
    std::vector<Node*> bfsQueue ;

    for( int i = 0 ; i < rootNode->totalChildren() ; ++ i )
    {
        bfsQueue.push_back(rootNode->getChildList()[i]);
    }

    while( !bfsQueue.empty() )
    {
        // Push all children of the element into queue
        for( int j = 0 ; j < bfsQueue[0]->totalChildren() ; ++ j )
        {
            bfsQueue.push_back(bfsQueue[0]->getChildList()[j]);
        }

        // Print current node
        std::cout << bfsQueue[0] << " " ;

        // Remove the first node from queue
        bfsQueue.erase(bfsQueue.begin());
    }
}
