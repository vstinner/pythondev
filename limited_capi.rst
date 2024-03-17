++++++++++++++++++++
Python Limited C API
++++++++++++++++++++

Use the limited C API::

    ``#define Py_LIMITED_API 0x030c0000``

Replace
=======

=========================================  ========================================
Regular C API                              Limited C API
=========================================  ========================================
``"%s", Py_TYPE(obj)->tp_name``            ``"%T", obj``
``PyBytes_GET_SIZE(bytes)``                ``PyBytes_Size(bytes)``
``PyList_GET_ITEM(list, index)``           ``PyList_GetItem(list, index)``
``PyList_SET_ITEM(list, index, item)``     ``PyList_SetItem(list, index, item)``
``PyTuple_GET_SIZE(tuple)``                ``PyTuple_Size(tuple)``
``PyTuple_SET_ITEM(tuple, index, item)``   ``PyTuple_SetItem(tuple, index, item)``
``PyUnicode_GET_LENGTH(str)``              ``PyUnicode_GetLength(str)``
``PyUnicode_READ_CHAR(str, index)``        ``PyUnicode_ReadChar(str, index)``
=========================================  ========================================

Port stdlib extensions to the limited C API
===========================================

* _csv: need PyType_GetModuleByDef()
* _curses_panel, dbm, _gdbm: AC doesn't support @defining_class
* _json: need _PyUnicodeWriter
* _operator: need _PyArg_NoKwnames()
* _testbuffer: static types
* md5, sha1: need PyMutex
* syslog: need PyInterpreterState_Main()
* overlapped: need _PyBytes_Resize()
* winreg: need Py_HashPointer()
