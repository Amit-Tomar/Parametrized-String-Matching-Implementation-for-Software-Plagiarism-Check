#include "MainWindow.h"
#include <QApplication>
#include "Tree.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    //MainWindow w;
    //w.show();

    Tree tree;
    tree.createSuffixTree();
    tree.printTree();
    return a.exec();
}
