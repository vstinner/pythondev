.. _python:

+++++++++++++++++++++++++++++++
The Python programming language
+++++++++++++++++++++++++++++++

.. image:: python.png
   :alt: Python logo
   :align: right
   :target: http://www.python.org/

History of Python releases
==========================

See also `Status of Python branches
<https://docs.python.org/devguide/#status-of-python-branches>`_.

* Python 3.5: September 2015
* Python 3.4: March 2014
* Python 3.3: September 2012
* Python 3.2: February 2011
* Python 2.7: July 2010
* Python 3.1: June 2009
* Python 3.0: December 2008
* Python 2.6: October 2008
* Python 2.5: September 2006
* Python 2.0: October 2000
* Python 1.5: April 1999



History of the Python language (syntax)
=======================================

* *(Python 3.4: no change)*
* Python 3.3:

  * ``yield from``: `PEP 380 "Syntax for Delegating to a Subgenerator"
    <http://legacy.python.org/dev/peps/pep-0380/>`_
  * ``u'unicode'`` syntax is back: `PEP 414 "Explicit Unicode literals"
    <http://legacy.python.org/dev/peps/pep-0414/>`_

* *(Python 3.2: no change)*
* Python 2.7:

  * all changes of Python 3.1

* Python 3.1:

  * dict/set comprehension
  * set literals
  * multiple context managers in a single with statement

* Python 3.0:

  * all changes of Python 2.6
  * new ``nonlocal`` keyword
  * ``raise exc from exc2``: `PEP 3134 "Exception Chaining and Embedded
    Tracebacks" <http://legacy.python.org/dev/peps/pep-3134/>`_
  * ``print`` and ``exec`` become a function
  * ``True``, ``False``, ``None``, ``as``, ``with`` are reserved words
  * Change from ``except exc, var`` to ``except exc as var``:
    `PEP 3110 "Catching Exceptions in Python 3000"
    <http://legacy.python.org/dev/peps/pep-3110/>`_
  * Removed syntax: ``a <> b``, ```a```, ``123l``, ``123L``, ``u'unicode'``,
    ``U'unicode'`` and ``def func(a, (b, c)): pass``

* Python 2.6:

  * with: `PEP 343 "The "with" Statement"
    <http://legacy.python.org/dev/peps/pep-0343/>`_
  * ``b'bytes'`` syntax: `PEP 3112 "Bytes literals in Python 3000" <http://legacy.python.org/dev/peps/pep-3112/>`_


Python builtin types
====================

Builtin scalar types:

* bool, int, float, complex, bytes, str

Builtin container types:

* Sequence: tuple, list
* Mapping: dict
* Set: frozenset, set

Singletons:

* None, Ellipsis (``...``), False (``bool(0)``), True (``bool(1)``)


Python platforms
================

========  =================================================  =========
Platform  sys.platform                                       os.name
========  =================================================  =========
AIX       ``aix3``, ``aix4``                                 ``posix``
Cygwin    ``cygwin``                                         ?
FreeBSD   ``freebsd5``, ``freebsd6``, ...                    ``posix``
Java      ``java`` (with a suffix?)                          ?
Linux     ``linux`` on Python 3, ``linux2`` on Python 2 (*)  ``posix``
macOS     ``darwin``                                         ``posix``
NetBSD    ``netbsd`` (with a suffix?)                        ``posix``
OpenBSD   ``openbsd5``                                       ``posix``
Solaris   ``sunos5``                                         ``posix``
Windows   ``win32``                                          ``nt``
========  =================================================  =========

``sys.platform`` comes from the ``MACHDEP`` variable which is built by the
configure script using:

* ``uname -s`` command output converted to lowercase, with some special rules
  (ex: ``linux3`` is replaced with ``linux`` on Python 3)
* ``uname -r`` command output (or ``uname -v`` on AIX, UnixWare or OpenUNIX)
* ``$host`` variable (``./configure --host=xxx`` parameter)
  when cross-compiling

(*) ``sys.platform`` was also ``linux3`` on old versions of Python 2.6 and
Python 2.7 with Linux kernel 3.x.


pytracemalloc
=============

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

See also:

* `pytracemalloc <http://pytracemalloc.readthedocs.org/>`_
* :ref:`Python Memory <memory>`


Zero copy
=========

Python3::

    offset = 0
    view = memoryview(large_data)
    while True:
        chunk = view[offset:offset + 4096]
        offset += file.write(chunk)

This copy creates views on ``large_data`` without copying bytes, no bytes is
copied in memory.


pudb
====

Put a breakpoint:

* hit 'm', search 'test_api' to open glance.tests.unit.test_api


datetime strptime
=================

Documentation: https://docs.python.org/dev/library/datetime.html#strftime-and-strptime-behavior

Code::

    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S %z')

year-month-day hour:minute:second timezone::

    %Y-%m-%d %H:%M:%S %z
