/**
 * @file    MainWindow.cpp
 * @author  Amit Tomar
 * @version 1.0
 *
 * Class definitions for class MainWindow
 */

#include "MainWindow.h"
#include "ui_MainWindow.h"

/*
 * Constructor
 *
 * @param  parent Pointer to parent widget
 */

MainWindow::MainWindow(QWidget *parent) : QWidget(parent),
    ui(new Ui::MainWindow)
{
    drawingSurface = new OpenGlSurface(0,0,800,480,(QGLWidget*)this);
    drawingSurface->show();
    drawingSurface->update();
    ui->setupUi(this);
    ui->topMessage->raise();
    ui->Bernstein->setCheckState(Qt::Checked);
    drawingSurface->update();
}

/*
 * Destructor
 *
 */
MainWindow::~MainWindow()
{
    delete ui;
}

/*
 * Implements functionality to do when Berstein Algo is selected
 *
 */
void MainWindow::on_Bernstein_clicked()
{
    ui->Bernstein->setCheckState(Qt::Checked);
    ui->Casteljau->setCheckState(Qt::Unchecked);
    drawingSurface->setDrawingAlgoBernstein(true);
}

/*
 * Implements functionality to do when Castelju Algo is selected
 *
 */
void MainWindow::on_Casteljau_clicked()
{
    ui->Bernstein->setCheckState(Qt::Unchecked);
    ui->Casteljau->setCheckState(Qt::Checked);
    drawingSurface->setDrawingAlgoBernstein(false);
}

/*
 * Implements functionality to do when scale bar changes
 *
 */
void MainWindow::on_ScaleBar_sliderMoved(int position)
{
    drawingSurface->setScale(position);
}


/*
 * Implements functionality to do when X rotation bar changes
 *
 */
void MainWindow::on_RotateBarX_sliderMoved(int position)
{
    drawingSurface->setRotation(0,position);
}


/*
 * Implements functionality to do when Y rotation bar changes
 *
 */
void MainWindow::on_RorateBarY_sliderMoved(int position)
{
    drawingSurface->setRotation(1,position);
}


/*
 * Implements functionality to do when Z rotation bar changes
 *
 */
void MainWindow::on_RotateBarZ_sliderMoved(int position)
{
    drawingSurface->setRotation(2,position);
}


/*
 * Implements functionality to do when X slider for translation bar changes
 *
 */
void MainWindow::on_TranslateBarX_sliderMoved(int position)
{
    drawingSurface->setTranslateX(position);
}

/*
 * Implements functionality to do when Y slider for translation bar changes
 *
 */
void MainWindow::on_TranslateBarY_sliderMoved(int position)
{
    drawingSurface->setTranslateY(position);
}
