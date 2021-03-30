.. _debug-tools:

++++++++++++++++++
Python Debug Tools
++++++++++++++++++

Spoiler: Python 3.6 and newer provide a much better debugging experience!

See also :ref:`Debug CPython with gdb <gdb>`.

Take Away
=========

Command to enable debug tools:

* Python 3.7 and newer: ``python3 -X dev``
* Python 3.6 and newer: ``PYTHONMALLOC=debug python3 -Wd -X faulthandler``

Tools:

* faulthandler
* PYTHONMALLOC=debug: builtin memory debugger
* :ref:`tracemalloc <tracemalloc>`
* :ref:`importtime <importtime>`
* Use :ref:`Python built in Debug Mode <pydebug>`

importtime
==========

See :ref:`importtime <importtime>`.


.. _faulthandler:

Get a traceback on a crash
==========================

Example of crash, ``crash.py``::

    import ctypes

    def bug():
        ctypes.string_at(0)

    bug()

Output::

    $ python3 crash.py
    Segmentation fault (core dumped)

... not very helpful :-( Enable faulthandler to get the Python traceback where
the crash occurred. ``python3 -X dev`` (Python 3.7 and newer) enables
automatically faulthandler.

faulthandler provides a traceback on a crash::

    $ python3 -X faulthandler crash.py
    Fatal Python error: Segmentation fault

    Current thread 0x00007f3bb3998700 (most recent call first):
      File "/usr/lib64/python3.6/ctypes/__init__.py", line 487 in string_at
      File "crash.py", line 4 in bug
      File "crash.py", line 6 in <module>
    Segmentation fault (core dumped)

To debug a deadlock, ``faulthandler.dump_traceback_later()`` can be implemented
to implement a "watchdog": dump the traceback where Python is stuck if Python
main code is blocked for longer than N seconds, and exit Python.


See also: `Crash reporting in desktop Python applications
<https://blogs.dropbox.com/tech/2018/11/crash-reporting-in-desktop-python-applications>`_
by Nikhil Marathe and Max Bélanger (November 2018).


.. _res-warn-tb:

ResourceWarning
===============

Example which doesn't close explicitly a file::

    def func():
        f = open(__file__)
        f = None

    func()

Output (or lack of output)::

    $ python3 filebug.py

... ResourceWarning warnings are hidden by default::

    $ python3.6 -c 'import pprint, warnings; pprint.pprint(warnings.filters)'
    [('ignore', None, <class 'DeprecationWarning'>, None, 0),
     ...
     ('ignore', None, <class 'ResourceWarning'>, None, 0)]

Use ``python3 -X dev`` (Python 3.7 and newer) or ``python3 -Wd`` (Python 3.6
and older) to display ``ResourceWarning``::

    $ python3 -Wd filebug.py
    filebug.py:3: ResourceWarning: unclosed file <_io.TextIOWrapper name='filebug.py' mode='r' encoding='UTF-8'>
      f = None

On Python 3.6 and newer, enabling :ref:`tracemalloc` shows where the resource (file in
this example) has been created::

    $ python3 -Wd -X tracemalloc=5 filebug.py
    filebug.py:3: ResourceWarning: unclosed file <_io.TextIOWrapper name='filebug.py' mode='r' encoding='UTF-8'>
      f = None
    Object allocated at (most recent call first):
      File "filebug.py", lineno 2
        f = open(__file__)
      File "filebug.py", lineno 5
        func()


Debug memory errors
===================

PYTHONMALLOC=debug
------------------

Memory managment in C is complex and error-prone.

Python has multiple allocators which are more or less compatible, but not
always. For example, `PyMem_Malloc()
<https://docs.python.org/dev/c-api/memory.html#memory-interface>`_ uses
``malloc()`` in Python 3.5 and older, but ``pymalloc`` in Python 3.6 and newer.
Releasing memory allocated by ``PyMem_Malloc()`` using ``PyObject_Free()``
worked until Python 3.5, but "can" crash on Python 3.6 (depending if the memory
block is longer than 512 bytes or not...).

Since Python 3.6, the new `PYTHONMALLOC environment variable
<https://docs.python.org/dev/using/cmdline.html#envvar-PYTHONMALLOC>`_ allows
to change the memory allocator at runtime (when starting Python).

``PYTHONMALLOC=debug`` enables Python builtin memory debugger:
`PyMem_SetupDebugHooks()
<https://docs.python.org/dev/c-api/memory.html#c.PyMem_SetupDebugHooks>`_.
``python3 -X dev`` (Python 3.7 and newer) enables automatically
``PYTHONMALLOC=debug``.

Example ``membug.py``::

    import _testcapi

    def main():
        _testcapi.pymem_buffer_overflow()

    main()

Output::

    $ PYTHONMALLOC=debug ./python membug.py
    Debug memory block at address p=0x7f7c0ed9f160: API 'm'
        16 bytes originally requested
        The 7 pad bytes at p-7 are FORBIDDENBYTE, as expected.
        The 8 pad bytes at tail=0x7f7c0ed9f170 are not all FORBIDDENBYTE (0xfb):
            at tail+0: 0x78 *** OUCH
            at tail+1: 0xfb
            at tail+2: 0xfb
            at tail+3: 0xfb
            at tail+4: 0xfb
            at tail+5: 0xfb
            at tail+6: 0xfb
            at tail+7: 0xfb
        The block was made by call #28431 to debug malloc/realloc.
        Data at p: cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb cb

    Fatal Python error: bad trailing pad byte

    Current thread 0x00007f7c0ee875c0 (most recent call first):
      File "membug.py", line 4 in main
      File "membug.py", line 6 in <module>
    Aborted (core dumped)

Python dumps the current traceback where the bug has been allocated, but it can
be "too late".

On Python 3.6 and newer, enabling :ref:`tracemalloc` allows to find where the memory
block has been allocated which can help to investigate the bug (truncated
output to highlight the difference)::

    $ PYTHONMALLOC=debug ./python -X tracemalloc=5 membug.py
    (...)
    Memory block allocated at (most recent call first):
      File "membug.py", line 4
      File "membug.py", line 6
    (...)

Traceback with source code recreated manually::

    Memory block allocated at (most recent call first):
      File "membug.py", line 4
        _testcapi.pymem_buffer_overflow()
      File "membug.py", line 6
        main()

On this artificial example, the current Python traceback and memory block
allocation traceback are the same, but usually they are different.

Sadly, on Python 3.5 and older, the only way to get the Python builtin memory
allocator is to recompile Python (ex: using ``./configure --with-pydebug``
which changes the ABI...).

Valgrind
--------

``PYTHONMALLOC=malloc valgrind python3 script.py`` can also be used to debug
C extensions which use directly ``malloc()/free()``, and not
``PyMem_Malloc()/PyMem_Free()``.

Use suppression file which can be found in Misc/valgrind.suppr

`Link Misc/valgrind-python.supp of the master (development) branch
<https://github.com/python/cpython/blob/master/Misc/valgrind-python.supp>`_.


gc.set_threshold(5)
===================

https://mail.python.org/pipermail/python-dev/2018-June/153857.html


Create a core dump file
=======================

Write core dumps on the current directory::

    $ ulimit -c
    unlimited
    $ sudo bash -c 'echo "coredump-%e.%p" > /proc/sys/kernel/core_pattern'

Check that it works::

    $ ./python -c 'import _testcapi, signal; _testcapi.raise_signal(signal.SIGABRT)'
    Aborted (core dumped)
    $ ls coredump*
    coredump-python.23861

    $ gdb ./python -c coredump-python.23861
    GNU gdb (GDB) Fedora 8.0.1-36.fc27
    (...)
    Core was generated by `./python -c import _testcapi, signal; _testcapi.raise_signal(signal.SIGABRT)'.
    Program terminated with signal SIGABRT, Aborted.
    (gdb) where
    #0  0x00007fb0cb3ad050 in raise () from /lib64/libpthread.so.0
    #1  0x00007fb0c3a53006 in test_raise_signal (self=<module at remote 0x7fb0cb624758>,

Ok, Python crashes generate coredump files and gdb is able to load them.


Windows
=======

https://bugs.python.org/issue35418#msg331195


pudb
====

Put a breakpoint:

* hit 'm', search 'test_api' to open glance.tests.unit.test_api

.. _tracemalloc:

tracemalloc
===========

The `tracemalloc module
<https://docs.python.org/dev/library/tracemalloc.html>`__ traces Python memory
allocations. It can be used to find memory leaks, or just to have an accurate
measure of the memory allocated by Python.

Usage:

* Write a scenario to reproduce the memory leak. The ideal is a scenario taking
  only a few minutes
* Enable tracemalloc and replay the scenario
* Take regulary tracemalloc snapshots
* Compare snapshots
* Enjoy!

If your application only uses Python memory allocators, tracemalloc must show
your the exact memory usage counting every single bytes.

If a C extensions uses other memory allocators like ``malloc()``, tracemalloc
is unable to trace these allocations.

If the application allocates a lot of memory to process some data (memory peak)
and then releases almost all memory, except a few small objects, the memory may
become fragmented. For example, the application only uses 20 MB whereas the
operating system see 24 or 30 MB.

See `pytracemalloc <http://pytracemalloc.readthedocs.org/>`_: backport to
Python 2.7 (need to patch and compile Python manually).


Debug crash in garbage collection (visit_decref)
================================================

It's really hard to investigate such crash. Usually a crash in the GC is only
the symptom that something corrupted a Python object, and the crash can occur
very late after the object has been corrupted.

You might attempt:

* Try python3 -X dev.
* Try Python compiled in debug mode.
* Try a more recent Python version. Maybe it's a bug in Python which is
  already fixed?
* List third party C extensions and look first at them. Usually, if
  you are the only one to see a crash, it comes from your bug. Maybe a C
  extension doesn't update reference counters correctly.
* Change GC thresholds: ``gc.set_threshold(5)``. See
  `[Python-Dev] Idea: reduce GC threshold in development mode (-X dev)
  <https://mail.python.org/pipermail/python-dev/2018-June/153857.html>`_.
* Disable completely the GC: ``gc.disable()``. It helped the reporter of
  `bpo-2546 <https://bugs.python.org/issue2546>`__ to find his bug.

Python issues related to visit_decref():

* 2019-10-07: `Python segfaults when configured with --with-pydebug --with-trace-refs
  <https://bugs.python.org/issue38400>`_. ``_PyObject_IsFreed()`` regression,
  it detected ``PyObject._ob_prev=NULL`` or ``PyObject._ob_next=NULL`` as a
  bug (when Python is built using
  ``./configure --with-pydebug --with-trace-refs``). For example, the
  ``Py_None`` object is not tracked by ``sys.getobjects()`` circular list.
  Parent object type: ``dict``.
* 2019-10-07: `Ensure that objects entering the GC are valid
  <https://bugs.python.org/issue38392>`_
* 2019-09-09: `visit_decref(): add an assertion to check that the object is not
  freed
  <https://bugs.python.org/issue38070>`_
* 2019-09-05: `reference counter issue in signal module
  <https://bugs.python.org/issue38037>`_. Missing ``Py_INCREF()`` in the
  initialization of the ``_signal`` module. Crash occurs while
  ``_PyImport_Cleanup()`` is clearing the ``_signal`` module.
  Parent object type: ``dict`` (``_signal`` module namespace).
* 2019-03-21: `Add gc.enable_object_debugger(): detect corrupted Python objects in the GC
  <https://bugs.python.org/issue36389>`_
* 2018-07-10: `int(s), float(s) and others may cause segmentation fault
  <https://bugs.python.org/issue34087>`_. Buffer overflow in an ``int`` object.
  Parent object type: ``list``.
* 2018-06-07: `contextvars: hamt_alloc() must initialize h_root and h_count fields
  <https://bugs.python.org/issue33803>`_. ``hamt_alloc()`` tracks an object in
  the GC before it is fully initialized: ``hamt_tp_traverse()`` visits
  ``h_root`` which is not initialized yet. Parent object type: ``hamt``.
* 2017-08-10: `Segfault in gcmodule.c:360 visit_decref (PyObject_IS_GC(op))
  <https://bugs.python.org/issue31181>`_. Crash occurs in 3rd party project
  pyETL: no reproducer has been provided.
* 2016-07-17: `Segfault in gcmodule.c:360 visit_decref
  <https://bugs.python.org/issue27542>`_. Related to pip, wheel and cffi.
  Parent object type: ``dict``.
* 2014-02-06: `python: Modules/gcmodule.c:379: visit_decref: Assertion
  '((gc)->gc.gc_refs >> (1)) != 0' failed
  <https://bugs.python.org/issue20526>`_. Crash at Python exit related to
  daemon threads spawned by asyncio. Also someone reported a bug in cx_Oracle,
  likely a corrupted exception: crash in visit_decref() called by
  BaseException_traverse().
  Parent object type: ``traceback``, visited object type: ``Frame``.
* 2013-02-19: `python-2.7.3-r3: crash in visit_decref()
  <https://bugs.python.org/issue17234>`_. Application using numpy, matplotlib,
  expat, and cElementTree. Parent object type: ``tuple``.
* 2012-07-01: `SEGFAULT in visit_decref
  <https://bugs.python.org/issue15236>`_. Reference counting issue.
  Parent object type: ``tuple``.
* 2008-04-04: `Python-2.5.2: crash in visit_decref () at Modules/gcmodule.c:270
  <https://bugs.python.org/issue2546>`__.
  Bug in a C extension, ``char*`` string passed as a ``PyObject*``
