#include "Python.h"
#undef d0
#include "MainWindow.h"
#include "PythonParser.h"
#include <QApplication>
#include "Tree.h"
#include <QTime>
#include <QFileDialog>
#include <fstream>
#include <QtQuick/QQuickView>
#include <QtQml/QQmlContext>
#include <QuickViewHolder.h>
#include <QQmlEngine>

Tree suffixTree;
QuickViewHolder viewHolder;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    //w.show();

    QQuickView view;
    view.setResizeMode(QQuickView::SizeRootObjectToView);
    view.setSource(QUrl("main.qml"));

    QQmlContext *ctxt = view.rootContext();
    ctxt->setContextProperty("mainWindow", &w );

    view.show();
    viewHolder.setView(view.rootObject());

    return a.exec();
}
