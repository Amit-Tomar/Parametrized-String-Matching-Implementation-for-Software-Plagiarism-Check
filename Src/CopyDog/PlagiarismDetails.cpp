#include "PlagiarismDetails.h"

int MINIMUM_COPY_LENGTH = 200;

PlagiarismDetails::PlagiarismDetails()
{

}

/**
 * @brief  Extracts the plagiarism information from the Suffox tree and stores it in a
 *         new data structure (Map with files copying as key and copied code as value)
 */
void PlagiarismDetails::extractPlagiarismInformation()
{
    std::vector<Node*> bfsQueue ;

    for( int i = 0 ; i < suffixTree.getRootNode()->totalChildren() ; ++ i )
    {
        bfsQueue.push_back( suffixTree.getRootNode()->getChildList()[i]);
    }

    while( !bfsQueue.empty() )
    {
        // Push all children of the element into queue
        for( int j = 0 ; j < bfsQueue[0]->totalChildren() ; ++ j )
        {
            bfsQueue.push_back(bfsQueue[0]->getChildList()[j]);
        }

        unsigned int newSuffixLength = bfsQueue[0]->getSuffix().length();
        unsigned int existingSuffixLength  = plagiarismCombination[bfsQueue[0]->getDescendentList()].length();

        // Push into DS only if length is more than the length of existing suffix
        if( newSuffixLength > MINIMUM_COPY_LENGTH && newSuffixLength > existingSuffixLength)
            updatePlagiarismInformation( bfsQueue[0]->getDescendentList(), bfsQueue[0]->getSuffix());

        // Remove the first node from queue
        bfsQueue.erase(bfsQueue.begin());
    }

    std::cout << "Info extracted" << std::endl ;
}

/**
 * @brief  Add/Updates the plagiarsim info the DS.
 */
void PlagiarismDetails::updatePlagiarismInformation(std::vector<unsigned int> plagiarisedFilesList, std::string commonCode)
{
    std::sort(plagiarisedFilesList.begin(), plagiarisedFilesList.end());
    plagiarismCombination[ plagiarisedFilesList ] = commonCode ;
}

/**
 * @brief  Prints the plagiarism information on console. Enable the debug flag for printign to work.
 */
void PlagiarismDetails::printPlagiarismInformation()
{
#ifdef DEBUG_PLAGIARISM_DETAILS
    std::cout << "\n\n---- Plagiarism Information ----\n\n" << std::endl ;

    for(std::map<std::vector<unsigned int>, std::string>::iterator it = plagiarismCombination.begin(); it != plagiarismCombination.end(); ++it)
    {
        std::cout << "Files copied among : " ;

        for( int i = 0 ; i < it->first.size() ; ++ i )
        {
            std::cout << it->first[i] << "  " ;
        }

        std::cout << "\n\nCopied Code : " << std::endl ;
        std::cout << it->second << std::endl;
    }
#endif
}
