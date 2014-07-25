#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QObject>
#include <QMainWindow>
#include <FileBrowser.h>
#include <QQuickView>
#include <QuickViewHolder.h>
#include <QQuickItem>
#include <ctime>

extern QuickViewHolder viewHolder;
extern int MINIMUM_COPY_LENGTH;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

public slots:
    void openFileBrowser(unsigned int, unsigned int, unsigned int);
    void exportPlagiarismInformation();

private:
    FileBrowser fileBrowser;
    std::map <std::vector<unsigned int>, std::string> plagDetails ;
    unsigned int selectedLanguageForPlagiarism;
};

#endif // MAINWINDOW_H
