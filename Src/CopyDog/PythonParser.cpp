#include "PythonParser.h"

PythonParser::PythonParser()
{
} 

/**
 * @brief  Creates and instance to execute some Python code. Passes the source code, and then
 *         gets back the stripped down suffix compatible code.
 */
std::string PythonParser::createSuffixCompatibleSource(std::string inputSourceCode)
{
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;

    Py_Initialize();

    PyObject *sys = PyImport_ImportModule("sys");
    PyObject *path = PyObject_GetAttrString(sys, "path");
    PyList_Append(path, PyString_FromString("."));

    pName = PyString_FromString("PythonParser");

    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != NULL)
    {
        pFunc = PyObject_GetAttrString(pModule, "parseAndStripWhiteSpaceComments");

        if (pFunc && PyCallable_Check(pFunc))
        {
            pArgs = PyTuple_New(1);

            pValue = PyString_FromString(inputSourceCode.c_str());
            if (!pValue)
            {
                //Py_DECREF(pArgs);
                //Py_DECREF(pModule);
                fprintf(stderr, "Cannot convert argument\n");
                return "";
            }
            PyTuple_SetItem(pArgs, 0, pValue);
            pValue = PyObject_CallObject(pFunc, pArgs);
            //Py_DECREF(pArgs);
            if (pValue != NULL)
            {
                // printf("Result of call: %s\n", PyString_AsString(pValue));
                // Py_DECREF(pValue);
                //return PyString_AsString(pValue);

                inputSourceCode = PyString_AsString(pValue);
            }
            else
            {
                //Py_DECREF(pFunc);
                //Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return "";
            }
        }
        else
        {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"%s\"\n", "createSuffixCompatibleSource");
        }

       //

        pFunc = PyObject_GetAttrString(pModule, "createSuffixCompatibleSource");

        if (pFunc && PyCallable_Check(pFunc))
        {
            pArgs = PyTuple_New(1);

            pValue = PyString_FromString(inputSourceCode.c_str());
            if (!pValue)
            {
                //Py_DECREF(pArgs);
                //Py_DECREF(pModule);
                fprintf(stderr, "Cannot convert argument\n");
                return "";
            }
            PyTuple_SetItem(pArgs, 0, pValue);
            pValue = PyObject_CallObject(pFunc, pArgs);
            //Py_DECREF(pArgs);
            if (pValue != NULL)
            {
                // printf("Result of call: %s\n", PyString_AsString(pValue));
                // Py_DECREF(pValue);
                return PyString_AsString(pValue);
            }
            else
            {
                //Py_DECREF(pFunc);
                //Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return "";
            }
        }
        else
        {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"%s\"\n", "createSuffixCompatibleSource");
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else
    {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", "PythonParser");
        return "";
    }
    Py_Finalize();
}


/**
 * @brief  Creates an instance for Python execution and converts the P-Code if Python to the
 *         Python code.
 */
std::string PythonParser::convertPCodeToSource(std::string completeSourceCode, std::string inputPCode)
{
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;

    Py_Initialize();

    PyObject *sys = PyImport_ImportModule("sys");
    PyObject *path = PyObject_GetAttrString(sys, "path");
    PyList_Append(path, PyString_FromString("."));

    pName = PyString_FromString("PythonParser");

    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != NULL)
    {
        pFunc = PyObject_GetAttrString(pModule, "parseAndStripWhiteSpaceComments");

        if (pFunc && PyCallable_Check(pFunc))
        {
            pArgs = PyTuple_New(1);

            pValue = PyString_FromString(completeSourceCode.c_str());
            if (!pValue)
            {
                //Py_DECREF(pArgs);
                //Py_DECREF(pModule);
                fprintf(stderr, "Cannot convert argument\n");
                return "";
            }
            PyTuple_SetItem(pArgs, 0, pValue);
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);
            if (pValue != NULL)
            {
                // printf("Result of call: %s\n", PyString_AsString(pValue));
                // Py_DECREF(pValue);
                // return PyString_AsString(pValue);

                pValue = PyString_FromString( PyString_AsString(pValue) );
            }
            else
            {
                //Py_DECREF(pFunc);
                //Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return "";
            }
        }
        else
        {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"%s\"\n", "parseAndStripWhiteSpaceComments");
        }

       //

        pFunc = PyObject_GetAttrString(pModule, "getPlainText");

        if (pFunc && PyCallable_Check(pFunc))
        {
            pArgs = PyTuple_New(2);

            //pValue = PyString_FromString(inputSourceCode.c_str());
            if (!pValue)
            {
//                Py_DECREF(pArgs);
//                Py_DECREF(pModule);
                fprintf(stderr, "Cannot convert argument\n");
                return "";
            }

            PyTuple_SetItem(pArgs, 0, pValue);
            PyTuple_SetItem(pArgs, 1, PyString_FromString(inputPCode.c_str()));

            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);
            if (pValue != NULL)
            {
                // printf("Result of call: %s\n", PyString_AsString(pValue));
                // Py_DECREF(pValue);
                return PyString_AsString(pValue);
            }
            else
            {
//                Py_DECREF(pFunc);
//                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return "";
            }
        }
        else
        {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"%s\"\n", "getPlainText");
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else
    {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", "PythonParser");
        return "";
    }
    Py_Finalize();
}
