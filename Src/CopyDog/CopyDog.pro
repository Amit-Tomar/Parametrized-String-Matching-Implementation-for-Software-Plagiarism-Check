#-------------------------------------------------
#
# Project created by QtCreator 2014-06-07T02:27:34
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = CopyDog
TEMPLATE = app


SOURCES += main.cpp\
        MainWindow.cpp \
    Node.cpp \
    Tree.cpp

HEADERS  += MainWindow.h \
    Node.h \
    Tree.h \
    Match.h

FORMS    += MainWindow.ui
