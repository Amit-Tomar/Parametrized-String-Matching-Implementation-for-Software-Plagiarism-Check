#include "Tree.h"

Tree::Tree()
{
    //sourceCode = "The Akhilesh Yadav-government ithat we were in power and lost now and are searching for reasons. We started off with one MP and one MLA, went up to two MPs and 20 MLAs and we now have eight MPs and 67 MLAs in Seemandhra and nine MPs and 70 MLAs as a whole, Our graph has been on the rise. What we n Uttar Pradesh brought about a major reshuffle of top bureaucracy and police officials on Saturday, transferring over 100 IAS and IPS officers at one go.           As many as 66 IAS officers including principal secretaries, secretaries and district magistrates and 42 IPS officers including IGs, DIGs and district police chiefs were transferred. In a departure from practice, the transfer of IPS officers was announced by state chief secretary Alok Ranjan in a press conference on Saturday after a long discussion with the CM on law and order situation in the state. The Samajwadi Party government was in the line of fire following a drubbing in the Lok Sabha elections followed by a sudden plunge in law and order situation across Ps and 20 MLAs and we now have eight MPs and 67 MLAs in Seemandhra and nine MPs and 70 MLAs as a whole, Our graph has been on the rise. What we have reviewed is if there is any lacuna in organisational matters so that corrective measures will  the state. khilesh Yadav had begun a cleansing process by first shunting out chief secretary Jawed Usmani, principal secretPs and 20 MLAs and we now have eight MPs and 67 MLAs in Seemandhra and nine MPs and 70 MLAs as a whole, Our graph has been on the rise. What we have reviewed is if there is any lacuna in organisational matters so that corrective measures will ary, home, AK Gupta and principal secretary, finance, Anand Mishra. f the 66 IAS officers transferred, 12 are of principal secretary rank, 28 are district magistrates and others are of secretary and other ranks. even the police said they were taken aback when first reports of the attack reached them. Local policemen were dealing with tension elsewhere following some objectionable posts on social networking sites. Shahin Anjuman Masjid Trust has demanded that Satav Plot's Lane No 2, where Mohsin was murdered, be named after him. ";
    rootNode = NULL;
    sourceFromFileNumber = 1;
    rootNode = new Node();
}

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
}
