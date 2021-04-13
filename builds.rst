.. _python-builds:

+++++++++++++
Python builds
+++++++++++++

See also :ref:`Analysis of CPython binary assembly <assembly>` and :ref:`C
compilers <c-compilers>`.

.. _release-build:

Release build
=============

In release mode, Python is built with ``-O3 -DNDEBUG`` compiler flags; defining
``NDEBUG`` macro removes assertions.

LTO
---

Use ``gcc -flto``

Maybe also: ``-fuse-linker-plugin -ffat-lto-objects -flto-partition=none``.

PGO
---

* Build Python with ``gcc -fprofile-generate``
* Run the test suite: ``make run_profile_task`` uses ``PROFILE_TASK`` variable
  of Makefile. configure uses ``./python -m test --pgo`` by default.
  List of test used with ``--pgo``: see `libregrtest/pgo.py
  <https://github.com/python/cpython/blob/master/Lib/test/libregrtest/pgo.py>`_.
* Rebuild Python with ``gcc -fprofile-use``

PGO + LTO
---------

Use PGO and add LTO flags.

.. _pydebug:

Debug build
===========

* Fedora: ``dnf install python3-debug`` to get the ``python3-debug`` program:
  run it instead of running ``python3``.
* ``./configure --with-pydebug``
* Python built using ``-Og`` if available, or ``-O0`` otherwise.
* Define the ``Py_DEBUG`` macro which enables many runtime checks to ease
  debug.

Python built in debug mode is very effecient to detect bugs in C extensions.

Effects of the Debug Mode:

* Build Python with assertions (don't set ``NDEBUG`` macro):

  * ``assert(...);``
  * ``_PyObject_ASSERT(...);``
  * etc.

* Install `debug hooks on memory allocators
  <https://docs.python.org/dev/c-api/memory.html#c.PyMem_SetupDebugHooks>`_ to
  detect buffer overflow and other memory errors.
* Add runtime checks, code surroundeded by ``#ifdef Py_DEBUG`` and ``#endif``.
* Unicode and int objects are created with their memory filled with a pattern
  to help detecting uninitialized bytes.
* Many functions ensure that are not called with an exception raised, since
  they can clear or replace the current exception:
  ``assert(!_PyErr_Occurred(tstate));``.

Checks in the GC:

* The GC ``visit_decref()`` function checks if an object was freed using
  ``_PyObject_IsFreed()``. This function is used internally during a GC
  collection on all Python objects tracked by the GC to break reference
  cycles.
* ``PyObject_GC_Track()`` checks if the object was freed using
  ``_PyObject_IsFreed()``.
* GC ``gc_decref()`` function checks if the GC reference count is valid.

Check if Python is built in debug mode
======================================

Py_DEBUG adds ``sys.gettotalrefcount()`` function::

    $ python3 -c "import sys; print('Debug build?', hasattr(sys, 'gettotalrefcount'))"
    Debug build? False
    $ python3-debug -c "import sys; print('Debug build?', hasattr(sys, 'gettotalrefcount'))"
    Debug build? True

or: Check ``sysconfig.get_config_var('Py_DEBUG')`` value::

    $ python3 -c "import sysconfig; print('Debug build?', bool(sysconfig.get_config_var('Py_DEBUG')))"
    Debug build? False
    $ python3-debug -c "import sysconfig; print('Debug build?', bool(sysconfig.get_config_var('Py_DEBUG')))"
    Debug build? True


Extra debug
===========

* ``Objects/dictobject.c``: define DEBUG_PYDICT macro to add
  ``_PyDict_CheckConsistency()`` checks to debug corrupted dictionaries.
* ``Objects/obmalloc.c``: define PYMEM_DEBUG_SERIALNO to store a serial number
  in allocated memory blocks.

Special builds
==============

`Read Misc/SpecialBuilds.txt
<https://github.com/python/cpython/blob/master/Misc/SpecialBuilds.txt>`_.
