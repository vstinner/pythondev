++++++++++++++++++++++
Python Subinterpreters
++++++++++++++++++++++

See also :ref:`Python Finalization <finalization>`.

* https://github.com/ericsnowcurrently/multi-core-python/
* https://bugs.python.org/issue36476
* https://bugs.python.org/issue36724

Limitations
===========

Not supported in subinterpreter:

* os.fork(): it may be possible to fix it.
* signal.signal()
* static types

Current workarounds:

* Disable GC
* Disable many caches like frame free list
* etc.

Multiphase initialization (PEP 489)
===================================

See _abc module.

* PyInit__abc() calls PyModuleDef_Init
* PyModuleDef has slots, at least Py_mod_exec.

Get module
==========

Create module::

    _PyModule_CreateInitialized(struct PyModuleDef* module, int module_api_version)

Members:

* PyModuleDef.m_base.m_index: int
* PyInterpreterState.modules_by_index: list

PyModuleDef_Init() assigns an unique index to a PyModuleDef. It is called
by _PyModule_CreateInitialized().

_PyImport_FixupExtensionObject() and import_find_extension() call::

    _PyState_AddModule(PyThreadState *tstate, PyObject* module, struct PyModuleDef* def)

Modules with slots must not be added to PyInterpreterState.modules_by_index.

Module State
============

Find a module::

    m = PyState_FindModule(&posixmodule);

From a module::

    void *state = PyModule_GetState(module);
