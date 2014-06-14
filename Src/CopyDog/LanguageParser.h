#ifndef LANGUAGEPARSER_H
#define LANGUAGEPARSER_H

#include <string>

class LanguageParser
{
public:
    LanguageParser();

    virtual std::string createSuffixCompatibleSource(std::string inputSourceCode) = 0 ;
};

#endif // LANGUAGEPARSER_H
