#include "Python.h"
#undef d0
#include "MainWindow.h"
#include "PythonParser.h"
#include <QApplication>
#include "Tree.h"
#include <QTime>
#include <QFileDialog>
#include <fstream>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    //w.show();

    QString fileName = QFileDialog::getOpenFileName(NULL, ("Open File"), "",("Files (*.*)"));
    std::cout << fileName.toStdString() << std::endl ;

    QTime myTimer;
    myTimer.start();

    fstream fileStream(fileName.toStdString().c_str(), fstream::in );
    string sourceCode;
    getline( fileStream, sourceCode, '\0');
    fileStream.close();

    PythonParser objPythonParser;
    std::string suffixCompatibleSource = objPythonParser.createSuffixCompatibleSource(sourceCode);

    assert(""!=suffixCompatibleSource);

    Tree tree;
    tree.createSuffixTree(suffixCompatibleSource);
    //tree.printTree();

    // --

    fileName = QFileDialog::getOpenFileName(NULL, ("Open File"), "",("Files (*.*)"));
    std::cout << fileName.toStdString() << std::endl ;

    fstream fileStream2(fileName.toStdString().c_str(), fstream::in );
    getline( fileStream2, sourceCode, '\0');
    fileStream2.close();

    suffixCompatibleSource = objPythonParser.createSuffixCompatibleSource(sourceCode);

    assert(""!=suffixCompatibleSource);

    tree.createSuffixTree(suffixCompatibleSource);
    tree.printTree();

    std::cout << "-- Finished --" << std::endl ;
    int nMilliseconds = myTimer.elapsed();
    std::cout << nMilliseconds << " Milli Seconds" <<  std::endl;

    return a.exec();
}
