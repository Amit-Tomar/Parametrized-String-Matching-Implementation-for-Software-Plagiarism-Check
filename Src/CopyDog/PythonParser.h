#ifndef PYTHONPARSER_H
#define PYTHONPARSER_H

#include "Python.h"
#undef d0
#include <LanguageParser.h>

class PythonParser : public LanguageParser
{
public:

    PythonParser();

    std::string createSuffixCompatibleSource(std::string inputSourceCode);
    std::string convertPCodeToSource(std::string completeSourceCode, std::string inputPCode);
};

#endif // PYTHONPARSER_H
