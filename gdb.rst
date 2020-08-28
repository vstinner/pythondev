.. _gdb:

++++++++++++++++++++++
Debug CPython with gdb
++++++++++++++++++++++

Current Python thread state
===========================

Read ``tstate_current``, if the GIL is held::

    p ((PyThreadState*)_PyRuntime.gilstate.tstate_current)

Thread Local Storage (TLS)::

    p (PyThreadState *)PyThread_tss_get(&_PyRuntime.gilstate.autoTSSkey)

See also :ref:`Python Thread State <pystate>`.


Put a breakpoint on the next exception
======================================

Put a breakpoint on the next exception: ``break _PyErr_SetObject``
(or ``break PyErr_SetObject`` in Python 3.7 and older).

Then use ``condition`` to only break at the expected exception.


Watch when reference count changes
==================================

Use a memory breakpoint like::

    watch ((PyObject*)MEMORY_ADDRESS)->ob_refcnt

where ``MEMORY_ADDRESS`` is the address of a Python object.

Analyze a coredump
==================

Current Python thread state, like ``PyThreadState_GET()``::

    p ((PyThreadState*)_PyRuntime.gilstate.tstate_current)

Current error, like ``PyErr_Occurred()``::

    p ((PyThreadState*)_PyRuntime.gilstate.tstate_current)->curexc_type


Load python-gdb.py
==================

Load it manually::

   (gdb) source /path/to/python-gdb.py

Add directory containing Python source code to "safe path", to automatically
load python-gdb.py when debugging Python. Add the following line to your
``~/.gdbinit``::

   add-auto-load-safe-path ~/prog/

In my case, Python is in ``~/prog/python/master``, but I chose to allow to load
any Python script from ``~/prog/``.

On Fedora, the script is provided as::

   /usr/lib/debug/usr/lib64/libpython3.6m.so.1.0-3.6.6-1.fc28.x86_64.debug-gdb.py


