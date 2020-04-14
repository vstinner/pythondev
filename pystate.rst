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


Main thread and main interpreter
================================

* ``PyInterpreterState_Main()``: get ``_PyRuntime.interpreters.main``
* ``_PyOS_IsMainThread()``: call ``_Py_ThreadCanHandleSignals(_PyInterpreterState_GET())``
* ``_Py_IsMainThread()``: Check if the current thread is the main thread.
* ``_Py_IsMainInterpreter(tstate)``
* ``_Py_ThreadCanHandleSignals(interp)``: added by https://bugs.python.org/issue40010
* ``_Py_ThreadCanHandlePendingCalls()``: see https://bugs.python.org/issue40231

Identifier of the main thread (of the main interpreter):
``_PyRuntime.main_thread``.  Identifier read by
``PyThread_get_thread_ident()``, it's not a Python thread state. Used
by ``_Py_IsMainThread()``.

Main interpreter: ``_PyRuntime.interpreters.main``.


GIL
===


``take_gil()`` and ``drop_gil()`` stores the Python thread state into
``_PyRuntime.ceval.gil.last_holder``.


Signal handler
==============

trip_signal() of signalmodule.c
-------------------------------

Python 3.9 always uses the main interpreter (``_PyRuntime.interpreters.main``),
it no longer tries to get the current Python thread state.

``_PyEval_SignalReceived(interp)`` sets ``signals_pending`` and
``eval_breaker`` to 1.

Call ``_PyEval_AddPendingCall(interp, ...)`` if writing into the wakeup fd
fails.

Python 3.9 made ``eval_breaker`` and pending calls per interpreter.

faulthandler
------------

``faulthandler_fatal_error()`` and ``faulthandler_user()`` signal handlers use
``PyGILState_GetThisThreadState()`` to get the current Python thread state::

    /* SIGSEGV, SIGFPE, SIGABRT, SIGBUS and SIGILL are synchronous signals and
       are thus delivered to the thread that caused the fault. Get the Python
       thread state of the current thread.

       PyThreadState_Get() doesn't give the state of the thread that caused the
       fault if the thread released the GIL, and so this function cannot be
       used. Read the thread specific storage (TSS) instead: call
       PyGILState_GetThisThreadState(). */
    tstate = PyGILState_GetThisThreadState();

``enable()`` and ``register()`` use ``_PyThreadState_UncheckedGet()`` and then
store ``PyThreadState_GetInterpreter(tstate)`` to use it from signal handlers.


tracemalloc
===========

Hooks on memory allocators use ``PyGILState_GetThisThreadState()`` to get the
current Python thread state. ``PyMem_RawMalloc()`` can be called without
holding the GIL.

``PyMem_RawMalloc()`` hook uses ``PyGILState_Ensure()`` and
``PyGILState_Release()`` to hold the GIL.


PyGILState and subinterpreters
==============================

* https://bugs.python.org/issue1021318
* https://bugs.python.org/issue10915
* https://bugs.python.org/issue15751


subinterpreters
===============

It is currently possible for a single native thread to be associated to
multiple Python thread states: one per interpreter.

Extract of ``_testcapi.run_in_subinterp()`` implementation::


    PyThreadState *mainstate = PyThreadState_Get();

    PyThreadState_Swap(NULL);

    PyThreadState *substate = Py_NewInterpreter();
    ...
    Py_EndInterpreter(substate);

    PyThreadState_Swap(mainstate);

``Py_NewInterpreter()`` creates a new Python thread state. Extract of its
implementation::

    PyInterpreterState *interp = PyInterpreterState_New();
    ...
    PyThreadState *tstate = PyThreadState_New(interp);
    ..
    PyThreadState_Swap(tstate);


Pass tstate explicitly
======================

`Pass the Python thread state explicitly
<https://vstinner.github.io/cpython-pass-tstate.html>`_ (January 2020) by
Victor Stinner.


Move global variables into PyInterpreterState
=============================================

``PyLong_FromLong()`` now requires to get the current interpreter to access
``PyInterpreterState.small_ints`` singletons.


Thread-local storage
====================

Mark Shannon: experiment to moving the Python thread state to thread-local
storage (TLS):

* https://mail.python.org/archives/list/python-dev@python.org/thread/RPSTDB6AEMIACJFZKCKIRFTVLAJQLAS2/
* https://github.com/python/cpython/compare/master...markshannon:threadstate_in_tls
