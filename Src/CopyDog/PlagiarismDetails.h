#ifndef PLAGIARISMDETAILS_H
#define PLAGIARISMDETAILS_H

#include <iostream>
#include <algorithm>
#include <map>
#include <vector>
#include <Tree.h>

extern Tree suffixTree;

#define MINIMUM_COPY_LENGTH 10
#define MINIMUM_DEPTH_TO_CHECK 5

class PlagiarismDetails
{
public:
    PlagiarismDetails();
    void extractPlagiarismInformation();
    void printPlagiarismInformation();
    std::map <std::vector<unsigned int>, std::string> getPlagiarismCombination() { return plagiarismCombination ; }

private:
    std::map <std::vector<unsigned int>, std::string> plagiarismCombination ;
    void updatePlagiarismInformation(std::vector<unsigned int>,std::string);
};

#endif // PLAGIARISMDETAILS_H
