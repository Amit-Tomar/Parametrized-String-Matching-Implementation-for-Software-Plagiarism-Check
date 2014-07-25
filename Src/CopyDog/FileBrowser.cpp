#include "FileBrowser.h"

FileBrowser::FileBrowser()
{

}

/**
 * @brief  Based on the parameters, opens up file browser
 *         capable of handling files of particular type and by differnt browsing modes.
 */
void FileBrowser::browseFile(BrowsingType browsingType, LanguageType language)
{
    std::string browsingRegExp;

    if( ePython == language )
        browsingRegExp = "*.py";
    else if( eC == language )
        browsingRegExp = "*.c";
    else if( eCPP == language )
        browsingRegExp = "*.cpp";

    std::string fileName ;

    if( eSelectAllFiles == browsingType )
    {
         QString dir = QFileDialog::getExistingDirectory(NULL, QObject::tr("Open Directory"), "./", QFileDialog::ShowDirsOnly);

         QStringList nameFilter(QString::fromStdString(browsingRegExp));
         QDir directory(dir);
         QStringList txtFilesAndDirectories = directory.entryList(nameFilter);

         for( int i = 0 ; i < txtFilesAndDirectories.length() ; ++ i )
         {
             fileName = dir.toStdString()+ "/"  +(txtFilesAndDirectories[i].toStdString()) ;
             fileList.push_back(fileName);

             std::fstream fileStream2(fileName.c_str(), std::fstream::in );
             std::string sourceCode;
             getline( fileStream2, sourceCode, '\0');
             fileStream2.close();

             std::string suffixCompatibleSource = sourceCode;

             if( ePython == language )
             {
                 PythonParser objPythonParser;
                 suffixCompatibleSource = objPythonParser.createSuffixCompatibleSource(sourceCode);
             }

             if(suffixCompatibleSource.empty())
             {
                std::cerr <<  "Incompatible Python file found, check for PYTHON syntax errors : " << fileName << "\n\n" << std::endl ;
             }

             else
             {
                suffixTree.updateSuffixTree( suffixCompatibleSource );
             }
         }
    }

    else if( eSelectFilesManually == browsingType )
    {
        QFileDialog* fileDialog = new QFileDialog(NULL);
        fileDialog->setFileMode(QFileDialog::ExistingFiles);
        fileDialog->exec();

        QStringList strlist = fileDialog->selectedFiles();

        for( int i = 0 ; i < strlist.length() ; ++ i )
        {
            std::cout << strlist[i].toStdString() << std::endl ;

            fileName = strlist[i].toStdString() ;
            fileList.push_back(fileName);

            std::fstream fileStream2(fileName.c_str(), std::fstream::in );
            std::string sourceCode;
            getline( fileStream2, sourceCode, '\0');
            fileStream2.close();

            std::string suffixCompatibleSource = sourceCode;

            if( ePython == language )
            {
                PythonParser objPythonParser;
                suffixCompatibleSource = objPythonParser.createSuffixCompatibleSource(sourceCode);
            }

            if(suffixCompatibleSource.empty())
            {
               std::cerr <<  "Incompatible Python file found, check for PYTHON syntax errors : " << fileName << "\n\n" <<  std::endl ;
            }

            else
            {
               suffixTree.updateSuffixTree( suffixCompatibleSource );
            }
        }
    }

    else if( eDecompressAndSelectAll == browsingType )
    {
        // @TBD
    }

    else
    {
        std::cerr << "Invalid file browsing type" << std::endl ;
    }

     suffixTree.printTree();
     plagiarsigmDetails.extractPlagiarismInformation();
     plagiarsigmDetails.printPlagiarismInformation();

    std::cout << "Suffix Tree made and information extracted" << std::endl ;

    for( int i =0 ; i < fileList.size() ; ++ i)
    {
        std::cout << fileList[i] << "\n" << std::endl ;
    }
}
