#ifndef FILEBROWSER_H
#define FILEBROWSER_H

#include <QFileDialog>
#include <BrowsingTypes.h>
#include <LanguageType.h>
#include <iostream>
#include <QObject>
#include <Tree.h>
#include <fstream>
#include <PythonParser.h>
#include <PlagiarismDetails.h>

#define DOUBLE_QUOTE_STARTED 4
#define SINGLE_QUOTE_FOUND 3
#define DOUBLE_QUOTE_ENDED 2
#define HASH_FOUND 1

extern Tree suffixTree;

class FileBrowser
{
public:
    FileBrowser();
    void browseFile(BrowsingType,LanguageType=ePython);
    PlagiarismDetails getPlagiarismDetails() { return plagiarsigmDetails; }

private:

    PlagiarismDetails plagiarsigmDetails;
};

#endif // FILEBROWSER_H
