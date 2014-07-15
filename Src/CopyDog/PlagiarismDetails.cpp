#include "PlagiarismDetails.h"

PlagiarismDetails::PlagiarismDetails()
{

}

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

        if( newSuffixLength > MINIMUM_COPY_LENGTH && newSuffixLength > existingSuffixLength)
            updatePlagiarismInformation( bfsQueue[0]->getDescendentList(), bfsQueue[0]->getSuffix());

        // Remove the first node from queue
        bfsQueue.erase(bfsQueue.begin());
    }

    // Remove entries with empty copy strings or just one file

    for(std::map<std::vector<unsigned int>, std::string>::iterator it = plagiarismCombination.begin(); it != plagiarismCombination.end(); ++it)
    {

        if( it->first.size() < 2 || it->second.empty() )
        {
            plagiarismCombination.erase(it);
        }

        else
        {
            unsigned int countWhite = 0 ;
            for( unsigned int i = 0 ; i < it->second.length() ; ++i )
            {
                if( it->second[i] == ' ' )
                    ++countWhite ;
            }

            if( countWhite == it->second.length() )
            {
                plagiarismCombination.erase(it);
            }

            //std::cout << "White: " << countWhite << " Length: " << it->second.length() << std::endl ;
        }
    }

    //std::cout << "Info extreacted" << std::endl ;
}

void PlagiarismDetails::updatePlagiarismInformation(std::vector<unsigned int> plagiarisedFilesList, std::string commonCode)
{
    std::sort(plagiarisedFilesList.begin(), plagiarisedFilesList.end());
    plagiarismCombination[ plagiarisedFilesList ] = commonCode ;
}

void PlagiarismDetails::printPlagiarismInformation()
{
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
}
