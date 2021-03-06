#ifndef PLAGIARISMDETAILS_H
#define PLAGIARISMDETAILS_H

#include <iostream>
#include <algorithm>
#include <map>
#include <vector>
#include <Tree.h>

extern Tree suffixTree;

#define MINIMUM_DEPTH_TO_CHECK 5

class PlagiarismDetails
{
public:
    PlagiarismDetails();
    void extractPlagiarismInformation();
    void printPlagiarismInformation();
    bool comparePlagirismInformation(std::vector<unsigned int>, std::string,std::vector<unsigned int>, std::string);
    std::map <std::vector<unsigned int>, std::string> getPlagiarismCombination() { return plagiarismCombination ; }

private:
    std::map <std::vector<unsigned int>, std::string> plagiarismCombination ;
    void updatePlagiarismInformation(std::vector<unsigned int>,std::string);
};

#endif // PLAGIARISMDETAILS_H
