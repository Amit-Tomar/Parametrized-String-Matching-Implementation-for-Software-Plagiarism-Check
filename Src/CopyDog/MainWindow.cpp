#include "MainWindow.h"
#include "ui_MainWindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    ui->selectAllFiles->setChecked( true );
    connect(ui->pushButton, SIGNAL(clicked()), this, SLOT(openFileBrowser()));
}

void MainWindow::openFileBrowser(unsigned int choice)
{
    /*if( ui->selectAllFiles->isChecked() )
    {
        fileBrowser.browseFile(eSelectAllFiles, ePython);
    }

    else if ( ui->selectFilesManual->isChecked() )
    {
        fileBrowser.browseFile(eSelectFilesManually, ePython);
    }

    else if (ui->decompressSelect)
    {
        fileBrowser.browseFile(eDecompressAndSelectAll, ePython);
    }*/

    if( 1 == choice )
    {
        fileBrowser.browseFile(eSelectAllFiles, ePython);
    }

    else if ( 2 == choice )
    {
        fileBrowser.browseFile(eSelectFilesManually, ePython);
    }

    else if ( 3 == choice )
    {
        fileBrowser.browseFile(eSelectFilesManually, ePython);
    }

    plagDetails = fileBrowser.getPlagiarismDetails().getPlagiarismCombination();

    std::string copiedFileslist, sourceCode ;
    for(std::map<std::vector<unsigned int>, std::string>::iterator it = plagDetails.begin(); it != plagDetails.end(); ++it)
    {
        copiedFileslist = "" ;
        sourceCode = "" ;

        for( int i = 0 ; i < it->first.size() ; ++ i )
        {
            copiedFileslist = copiedFileslist + QString::number(it->first[i]).toStdString() + " " ;
        }

        sourceCode = it->second ;

        // Call qml function to update list

        QMetaObject::invokeMethod(viewHolder.getView(), "appendPlagiarismInfo",
                Q_ARG(QVariant, copiedFileslist.c_str()),
                Q_ARG(QVariant, sourceCode.c_str()));

    }
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_selectAllFiles_clicked()
{
    ui->selectAllFiles->setChecked( true );
    ui->decompressSelect->setChecked( false );
    ui->selectFilesManual->setChecked( false );
}

void MainWindow::on_decompressSelect_clicked()
{
    ui->decompressSelect->setChecked( true );
    ui->selectFilesManual->setChecked( false );
    ui->selectAllFiles->setChecked( false );
}

void MainWindow::on_selectFilesManual_clicked()
{
    ui->selectFilesManual->setChecked( true );
    ui->decompressSelect->setChecked( false );
    ui->selectAllFiles->setChecked( false );
}
