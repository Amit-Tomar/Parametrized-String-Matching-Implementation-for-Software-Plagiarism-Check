#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QObject>
#include <QMainWindow>
#include <FileBrowser.h>
#include <QQuickView>
#include <QuickViewHolder.h>
#include <QQuickItem>

extern QuickViewHolder viewHolder;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

public slots:
    void openFileBrowser(unsigned int = 0);

private slots:
    void on_selectAllFiles_clicked();
    void on_decompressSelect_clicked();
    void on_selectFilesManual_clicked();

private:
    Ui::MainWindow *ui;
    FileBrowser fileBrowser;
    std::map <std::vector<unsigned int>, std::string> plagDetails ;
};

#endif // MAINWINDOW_H
