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
};

#endif // PYTHONPARSER_H
