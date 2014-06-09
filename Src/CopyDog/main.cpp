#include "MainWindow.h"
#include <QApplication>
#include "Tree.h"
#include <QTime>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    //MainWindow w;
    //w.show();
    QTime myTimer;
    myTimer.start();
    Tree tree;
    tree.createSuffixTree();
    tree.printTree();
    std::cout << "-- Finished --" << std::endl ;

    // do something..
    int nMilliseconds = myTimer.elapsed();
    std::cout << nMilliseconds << " Milli Seconds" <<  std::endl;
    return a.exec();
}
