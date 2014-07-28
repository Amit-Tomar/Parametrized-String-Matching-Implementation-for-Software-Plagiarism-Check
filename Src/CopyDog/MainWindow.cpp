#include "MainWindow.h"
#include "ui_MainWindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{

}

/**
 * @brief  Based on the selection in the UI, opens up file browser.
 *         Then constructs a Suffix tree from these files.
 */
void MainWindow::openFileBrowser(unsigned int languageChoice, unsigned int charactersToMatch, unsigned int fileSelectionChoice)
{
    MINIMUM_COPY_LENGTH = charactersToMatch;
    selectedLanguageForPlagiarism = languageChoice;

    if( 0 == languageChoice && 0 == fileSelectionChoice )
    {
        fileBrowser.browseFile(eSelectAllFiles, ePython);
    }

    else if( 0 == languageChoice && 1 == fileSelectionChoice )
    {
        fileBrowser.browseFile(eSelectFilesManually, ePython);
    }

    else if ( 1 == languageChoice && 0 == fileSelectionChoice )
    {
        fileBrowser.browseFile(eSelectAllFiles, eCPP);
    }

    else if ( 1 == languageChoice && 0 == fileSelectionChoice )
    {
        fileBrowser.browseFile(eSelectFilesManually, eCPP);
    }

    else if ( 2 == languageChoice && 0 == fileSelectionChoice )
    {
        fileBrowser.browseFile(eSelectAllFiles, eC);
    }

    else if ( 2 == languageChoice && 1 == fileSelectionChoice )
    {
        fileBrowser.browseFile(eSelectFilesManually, eC);
    }

    plagDetails = fileBrowser.getPlagiarismDetails().getPlagiarismCombination();

    std::string copiedFileslist, sourceCode ;
    for(std::map<std::vector<unsigned int>, std::string>::iterator it = plagDetails.begin(); it != plagDetails.end(); ++it)
    {
        copiedFileslist = "" ;
        sourceCode = "" ;

        // If there is only file in the node, ignore it.
        if( it->first.size() < 2 )
            continue;

        std::string completeFilePath;

        for( int i = 0 ; i < it->first.size() ; ++ i )
        {
            completeFilePath = fileBrowser.getFileList()[it->first[i]-1];
            std::string onlyFileName ;

            // Remove only the filename from the complete file path
            for ( int i = completeFilePath.length()-1 ; i >= 0 ; --i )
            {
                if( '/' == completeFilePath[i] )
                    break;
                onlyFileName +=  completeFilePath[i] ;
            }

            std::string temp = onlyFileName;
            // Reverse the obtained filename to get correct file name
            for ( int i = onlyFileName.length()-1 , j = 0 ; i >=0 ; --i, ++j )
            {
                onlyFileName[j] = temp[i] ;
            }

            copiedFileslist = copiedFileslist + onlyFileName + "\n" ;
        }

        sourceCode = it->second ;

        std::fstream fileStream2(completeFilePath.c_str(), std::fstream::in );
        std::string originalSourceCode;
        getline( fileStream2, originalSourceCode, '\0');
        fileStream2.close();

        // In case of Python, convert the P-Code back to normal source code before displaying it.
        if( 0 == languageChoice )
        {
            PythonParser objPythonParser;
            sourceCode = objPythonParser.convertPCodeToSource(originalSourceCode, sourceCode);
        }

        // Only if there's a non-space, pass this inofrmation to UI
        if(sourceCode.find_first_not_of(' ') != std::string::npos )
        {
            // Call qml function to update list
            QMetaObject::invokeMethod(viewHolder.getView(), "appendPlagiarismInfo",
                    Q_ARG(QVariant, copiedFileslist.c_str()),
                    Q_ARG(QVariant, sourceCode.c_str()));

            contentToExport += "\n\n--------------------------------\n\n" + copiedFileslist + "\n\n" + sourceCode;

        }
    }
}

/**
 * @brief  Exports the plagiarsim information in the current folder.
 *         Exits the application then.
 */
void MainWindow::exportPlagiarismInformation()
{
    std::string copiedFileslist, sourceCode ;
    std::time_t result = std::time(NULL);
    std::string timeStamp = std::asctime(std::localtime(&result));

    std::string exportFilePath = "CopyDogPlagiarismInformation_" ;
    exportFilePath += timeStamp ;

    FILE * fileWritePointer = fopen ( exportFilePath.c_str(), "w" );

    if( NULL == fileWritePointer )
    {
        puts("Error : Export file could not be opened for reading.");
        return ;
    }

    fprintf( fileWritePointer, "%s" , contentToExport.c_str() );

//    for(std::map<std::vector<unsigned int>, std::string>::iterator it = plagDetails.begin(); it != plagDetails.end(); ++it)
//    {
//        copiedFileslist = "" ;
//        sourceCode = "" ;

//        // If there is only file in the node, ignore it.
//        if( it->first.size() < 2 )
//            continue;

//        std::string completeFilePath;

//        for( int i = 0 ; i < it->first.size() ; ++ i )
//        {
//            completeFilePath = fileBrowser.getFileList()[it->first[i]-1];
//            std::string onlyFileName ;

//            // Remove only the filename from the complete file path
//            for ( int i = completeFilePath.length()-1 ; i >= 0 ; --i )
//            {
//                if( '/' == completeFilePath[i] )
//                    break;
//                onlyFileName +=  completeFilePath[i] ;
//            }

//            std::string temp = onlyFileName;
//            // Reverse the obtained filename to get correct file name
//            for ( int i = onlyFileName.length()-1 , j = 0 ; i >=0 ; --i, ++j )
//            {
//                onlyFileName[j] = temp[i] ;
//            }

//            copiedFileslist = copiedFileslist + onlyFileName + "\n" ;
//        }

//        sourceCode = it->second ;

//        std::fstream fileStream2(completeFilePath.c_str(), std::fstream::in );
//        std::string originalSourceCode;
//        getline( fileStream2, originalSourceCode, '\0');
//        fileStream2.close();

//        // In case of Python, convert the P-Code back to normal source code before displaying it.
//        if( 0 == selectedLanguageForPlagiarism )
//        {
//            PythonParser objPythonParser;
//            sourceCode = objPythonParser.convertPCodeToSource(originalSourceCode, sourceCode);
//        }

//        // Only if there's a non-space, pass this information to UI
//        if(sourceCode.find_first_not_of(' ') != std::string::npos )
//        {
//            fprintf( fileWritePointer, "%s\n%s\n\n------------------------\n\n" , copiedFileslist.c_str(), sourceCode.c_str() );
//        }
//    }

    fclose(fileWritePointer);
    exit(0);
}

MainWindow::~MainWindow()
{
}
