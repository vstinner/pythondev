.. _embed:

++++++++++++++++++++++++++++++
Embed Python in an application
++++++++++++++++++++++++++++++

See also :ref:`Add a field to PyConfig <pyconfig>`:

Applications embedding Python
=============================

* vim
* OpenOffice
* Blender

Python C API
============

* `New C API (PyConfig) <https://docs.python.org/dev/c-api/init_config.html>`_:


  * ``Py_PreInitialize()`` with ``PyPreConfig``
  * ``Py_InitializeFromConfig()`` with ``PyConfig``
  * ``Py_RunMain()``
  * Design document: `PEP 587 -- Python Initialization Configuration
    <https://www.python.org/dev/peps/pep-0587/>`_.
  * etc.

* `Old C API (Py_Initialize) <https://docs.python.org/dev/c-api/init.html>`_:

  * ``Py_Initialize()``
  * ``Py_Main()``
  * ``Py_SetPath()``
  * ``Py_DecodeLocale()``
  * ``PySys_AddWarnOption()``
  * etc.
