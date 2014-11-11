
#include "Tree.h"

Tree::Tree()
{    
    rootNode = NULL;
    sourceFromFileNumber = 1;
    rootNode = new Node();
}

/**
 * @brief  Creates a new node based on the given source code and adds it to the Suffix tree.
 */
void Tree::updateSuffixTree(std::string sourceCode)
{

    Node * newNode = new Node(sourceCode.substr(sourceCode.length()-1),rootNode,sourceFromFileNumber);
    rootNode->addChild(newNode);

    for( unsigned int i = 1 ; i < sourceCode.length() ; ++i )
    {
        std::string suffix = sourceCode.substr(sourceCode.length()-i-1);
        insertSuffix(rootNode,suffix,sourceFromFileNumber);
    }

    ++ sourceFromFileNumber;
}

/**
 * @brief  Inserts a given suffix at a node.
 */
void Tree::insertSuffix(Node* nodeToInsertAt, std::string incomingSuffixToInsert, unsigned int fileNumber)
{
    if(NULL == nodeToInsertAt)
    {
        std::cerr << "Null node" << std::endl;
        return;
    }

    nodeToInsertAt->addDescendentFileNumber(fileNumber);

    Match objMatch;

    for( unsigned int i = 0 ; i < nodeToInsertAt->totalChildren() ; ++ i )
    {
        objMatch = nodeToInsertAt->getChildList()[i]->getMatchPosition(incomingSuffixToInsert);

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
            // Once partially matched, update the matched child node's descendent list
            nodeToInsertAt->addDescendentFileNumber(fileNumber);

            if( eStringLarger == objMatch.lengthMatchType)
            {
                // Chop-off the incoming string
                incomingSuffixToInsert = incomingSuffixToInsert.substr(objMatch.position+1 );

                // Suffix exhausted
                if( objMatch.position == nodeToInsertAt->getChildList()[i]->getSuffixLength()-1 )
                {
                    nodeToInsertAt->getChildList()[i]->addDescendentFileNumber(fileNumber);
                    insertSuffix(nodeToInsertAt->getChildList()[i],incomingSuffixToInsert, fileNumber);
                    return;
                }
                // Suffix not exhausted
                else
                {
                    nodeToInsertAt->getChildList()[i]->trimAndAddSelfChild(objMatch.position, nodeToInsertAt->getChildList()[i]->getDescendentList());
                    nodeToInsertAt->getChildList()[i]->addDescendentFileNumber(fileNumber);
                    insertSuffix(nodeToInsertAt->getChildList()[i],incomingSuffixToInsert, fileNumber);

                    return;
                }
            }
            else if( eSuffixLarger == objMatch.lengthMatchType )
            {
                // Chop-off the incomgng string
                incomingSuffixToInsert = incomingSuffixToInsert.substr(objMatch.position+1 );
                nodeToInsertAt->getChildList()[i]->trimAndAddSelfChild(objMatch.position, nodeToInsertAt->getChildList()[i]->getDescendentList());

                // IncomingString exhausted
                if( objMatch.position == incomingSuffixToInsert.length()-1  )
                {
                    nodeToInsertAt->getChildList()[i]->addDescendentFileNumber(fileNumber);
                    return;
                }
                // IncomingString not exhausted
                else
                {
                    nodeToInsertAt->getChildList()[i]->addDescendentFileNumber(fileNumber);
                    insertSuffix(nodeToInsertAt->getChildList()[i],incomingSuffixToInsert, fileNumber);
                    return;
                }
            }
            return;
        }
    }

    Node * newNode = new Node(incomingSuffixToInsert,nodeToInsertAt,fileNumber);
    nodeToInsertAt->addChild(newNode);
    newNode->getDescendentList().push_back(fileNumber);
}

/**
 * @brief  Prints Suffix tree information. Enable the debug mode for printf to work.
 */
void Tree::printTree()
{

#ifdef TREE_DEBUG_MODE

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
        std::cout << "--------------------------------------------\n\n" << bfsQueue[0]->getSuffix() << std::endl ;
        std::cout << "\n\nDescendents : [ " ;

        for( int k = 0 ; k < bfsQueue[0]->getDescendentList().size() ; ++k )
        {
            std::cout << bfsQueue[0]->getDescendentList()[k] << " " ;
        }

        std::cout << "]" << std::endl;

        // Remove the first node from queue
        bfsQueue.erase(bfsQueue.begin());
    }
#endif

}
