#include "Python.h"
#undef d0
#include "MainWindow.h"
#include <QApplication>
#include "Tree.h"
#include <QTime>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    QTime myTimer;
    myTimer.start();
//    Tree tree;
//    tree.createSuffixTree();
//    tree.printTree();
    std::cout << "-- Finished --" << std::endl ;

// ------------------------------------------




        PyObject *pName, *pModule, *pDict, *pFunc;
        PyObject *pArgs, *pValue;
        int i;

        Py_Initialize();

        PyObject *sys = PyImport_ImportModule("sys");
        PyObject *path = PyObject_GetAttrString(sys, "path");
        PyList_Append(path, PyString_FromString("."));

        pName = PyString_FromString(argv[1]);
        /* Error checking of pName left out */

        pModule = PyImport_Import(pName);
        Py_DECREF(pName);

        if (pModule != NULL) {
            pFunc = PyObject_GetAttrString(pModule, argv[2]);
            /* pFunc is a new reference */

            if (pFunc && PyCallable_Check(pFunc)) {
                pArgs = PyTuple_New(argc - 3);
                for (i = 0; i < argc - 3; ++i) {
                    pValue = PyInt_FromLong(atoi(argv[i + 3]));
                    if (!pValue) {
                        Py_DECREF(pArgs);
                        Py_DECREF(pModule);
                        fprintf(stderr, "Cannot convert argument\n");
                        return 1;
                    }
                    /* pValue reference stolen here: */
                    PyTuple_SetItem(pArgs, i, pValue);
                }
                pValue = PyObject_CallObject(pFunc, pArgs);
                Py_DECREF(pArgs);
                if (pValue != NULL) {
                    printf("Result of call: %ld\n", PyInt_AsLong(pValue));
                    printf("Result of call: %s\n", PyString_AsString(pValue));
                    Py_DECREF(pValue);
                }
                else {
                    Py_DECREF(pFunc);
                    Py_DECREF(pModule);
                    PyErr_Print();
                    fprintf(stderr,"Call failed\n");
                    return 1;
                }
            }
            else {
                if (PyErr_Occurred())
                    PyErr_Print();
                fprintf(stderr, "Cannot find function \"%s\"\n", argv[2]);
            }
            Py_XDECREF(pFunc);
            Py_DECREF(pModule);
        }
        else {
            PyErr_Print();
            fprintf(stderr, "Failed to load \"%s\"\n", argv[1]);
            return 1;
        }
        Py_Finalize();


// -------------------------------------------


    // do something..
    int nMilliseconds = myTimer.elapsed();
    std::cout << nMilliseconds << " Milli Seconds" <<  std::endl;

    return a.exec();
}
