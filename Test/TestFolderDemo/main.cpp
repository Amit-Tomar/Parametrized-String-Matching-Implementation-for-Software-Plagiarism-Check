#include "glsl.h"
#include <QApplication>
#include <QDesktopWidget>
#include <QWidget>
#include <QPushButton>
#include "GLRenderer.h"
#include "Window.h"
#include <QFileDialog>
#include "RgbImage.h"

QString fileName;

int main(int argc, char *argv[])
{

//  RgbImage objRgbImage;
//  QString fileName = QFileDialog::getOpenFileName(NULL, ("Open File"), "",("Files (*.*)"));

    QApplication app(argc, argv);

    Window window;
    window.resize(window.sizeHint());
    //window.glWidget->objPLYParser.startParsing(fileName.toStdString());
    window.glWidget->objPLYParser.startParsing("");
    window.setGeometry(0,0,1200,800);
    window.show();

//   window.glWidget->initShaders();

//    cwc::glShaderManager SM;
//    cwc::glShader *shader;

//    cwc::InitOpenGLExtensions();

//    shader = SM.loadfromFile("vshader.glsl","fshader.glsl"); // load (and compile, link) from file
//    if (shader==0)
//       std::cout << "Error Loading, compiling or linking shader\n";

//    shader->begin();

  //objRgbImage.loadTextureFromFile( "fur3.bmp" );

    return app.exec();
}
