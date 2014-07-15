#include "PlagiarismRemortUI.h"
#include "ui_PlagiarismRemortUI.h"

PlagiarismRemortUI::PlagiarismRemortUI(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::PlagiarismRemortUI)
{
    ui->setupUi(this);
}

PlagiarismRemortUI::~PlagiarismRemortUI()
{
    delete ui;
}
