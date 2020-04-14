+++++++++++++++++++
Python Thread State
+++++++++++++++++++

Get the current Python Thread State (tstate)
============================================

* ``_PyRuntimeState_GetThreadState(runtime)``:
  read ``runtime->gilstate.tstate_current``
* ``_PyThreadState_GET()``: internal C API,
  call ``_PyRuntimeState_GetThreadState(&_PyRuntime)``, new in Python 3.8.
* ``PyThreadState_Get()``: opaque function call
* ``_PyThreadState_UncheckedGet()``: added to Python 3.5.2
  (`bpo-26154 <https://bugs.python.org/issue26154>`_)
* ``PyGILState_GetThisThreadState()``
* ``PyThreadState_GET()``: macro, alias to PyThreadState_Get().
  When pycore_pystate.h is included: macro redefined as an alias to
  _PyThreadState_GET().

There was also ``_PyThreadState_Current``: removed from Python 3.5.1.

History:

* Python 3.7: ``PyThreadState_GET()`` reads ``_PyThreadState_Current`` (atomic
  variable).
* Python 3.8: ``_PyThreadState_Current`` moves as
  ``_PyRuntime.gilstate.tstate_current``


Get the current interpreter (interp)
====================================

* ``PyInterpreterState_Get()``: limited C API. new in Python 3.8.
  Known as ``_PyInterpreterState_Get()`` in Python 3.8.
  Implemented as ``_PyThreadState_GET()->interp``.
* ``_PyInterpreterState_GET()``: internal C API, added to Python 3.8.
  Known as ``_PyInterpreterState_GET_UNSAFE()`` in Python 3.8.
* ``_PyGILState_GetInterpreterStateUnsafe()``: read
  ``_PyRuntime.gilstate.autoInterpreterState``, new in Python 3.6.

Python 3.9 also defines ``_PyInterpreterState_Get()`` as an alias to
``PyInterpreterState_Get()`` for backward compatibility.


PyGILState and subinterpreters
==============================

* https://bugs.python.org/issue1021318
* https://bugs.python.org/issue10915
* https://bugs.python.org/issue15751
