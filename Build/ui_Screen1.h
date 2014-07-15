/********************************************************************************
** Form generated from reading UI file 'Screen1.ui'
**
** Created by: Qt User Interface Compiler version 5.2.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SCREEN1_H
#define UI_SCREEN1_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Form
{
public:
    QLabel *label_5;
    QWidget *verticalLayoutWidget;
    QVBoxLayout *verticalLayout;
    QLabel *label_3;
    QLabel *label_2;
    QLabel *label;
    QWidget *verticalLayoutWidget_2;
    QVBoxLayout *verticalLayout_2;
    QCheckBox *checkBox_3;
    QCheckBox *checkBox_2;
    QCheckBox *checkBox;

    void setupUi(QWidget *Form)
    {
        if (Form->objectName().isEmpty())
            Form->setObjectName(QStringLiteral("Form"));
        Form->resize(760, 508);
        label_5 = new QLabel(Form);
        label_5->setObjectName(QStringLiteral("label_5"));
        label_5->setGeometry(QRect(360, 20, 57, 15));
        verticalLayoutWidget = new QWidget(Form);
        verticalLayoutWidget->setObjectName(QStringLiteral("verticalLayoutWidget"));
        verticalLayoutWidget->setGeometry(QRect(10, 100, 351, 351));
        verticalLayout = new QVBoxLayout(verticalLayoutWidget);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        label_3 = new QLabel(verticalLayoutWidget);
        label_3->setObjectName(QStringLiteral("label_3"));

        verticalLayout->addWidget(label_3);

        label_2 = new QLabel(verticalLayoutWidget);
        label_2->setObjectName(QStringLiteral("label_2"));

        verticalLayout->addWidget(label_2);

        label = new QLabel(verticalLayoutWidget);
        label->setObjectName(QStringLiteral("label"));

        verticalLayout->addWidget(label);

        verticalLayoutWidget_2 = new QWidget(Form);
        verticalLayoutWidget_2->setObjectName(QStringLiteral("verticalLayoutWidget_2"));
        verticalLayoutWidget_2->setGeometry(QRect(390, 100, 91, 351));
        verticalLayout_2 = new QVBoxLayout(verticalLayoutWidget_2);
        verticalLayout_2->setObjectName(QStringLiteral("verticalLayout_2"));
        verticalLayout_2->setContentsMargins(0, 0, 0, 0);
        checkBox_3 = new QCheckBox(verticalLayoutWidget_2);
        checkBox_3->setObjectName(QStringLiteral("checkBox_3"));

        verticalLayout_2->addWidget(checkBox_3);

        checkBox_2 = new QCheckBox(verticalLayoutWidget_2);
        checkBox_2->setObjectName(QStringLiteral("checkBox_2"));

        verticalLayout_2->addWidget(checkBox_2);

        checkBox = new QCheckBox(verticalLayoutWidget_2);
        checkBox->setObjectName(QStringLiteral("checkBox"));

        verticalLayout_2->addWidget(checkBox);


        retranslateUi(Form);

        QMetaObject::connectSlotsByName(Form);
    } // setupUi

    void retranslateUi(QWidget *Form)
    {
        Form->setWindowTitle(QApplication::translate("Form", "Form", 0));
        label_5->setText(QApplication::translate("Form", "TextLabel", 0));
        label_3->setText(QApplication::translate("Form", "Analize all files in folder", 0));
        label_2->setText(QApplication::translate("Form", "Analize manually files", 0));
        label->setText(QApplication::translate("Form", "Decompress and analize all files in folder", 0));
        checkBox_3->setText(QApplication::translate("Form", "CheckBox", 0));
        checkBox_2->setText(QApplication::translate("Form", "CheckBox", 0));
        checkBox->setText(QApplication::translate("Form", "CheckBox", 0));
    } // retranslateUi

};

namespace Ui {
    class Form: public Ui_Form {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SCREEN1_H
