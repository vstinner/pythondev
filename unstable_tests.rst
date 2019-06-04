++++++++++++++
Unstable tests
++++++++++++++

The multiprocessing tests leaked a lot of resources. Victor Stinner and others
fixed dozens of bugs in these tests.

See also: :ref:`Enable tracemalloc to get ResourceWarning traceback
<res-warn-tb>`.

Open issues
===========

* 2018-12-05, **multiprocessing**: `test_multiprocessing_fork: test_del_pool()
  leaks dangling threads and processes on AMD64 FreeBSD CURRENT Shared 3.x
  <https://bugs.python.org/issue35413>`_
* 2018-07-03, **asyncio**: `asyncio: BaseEventLoop.close() shutdowns the
  executor without waiting causing leak of dangling threads
  <https://bugs.python.org/issue34037>`_
* 2017-07-19, **multiprocessing**: `multiprocessing.queues.SimpleQueue leaks 2
  fds <https://bugs.python.org/issue30966>`_

Fixed issues
============

* 2018-05-28, **test_multiprocessing**: `test_multiprocessing_fork: dangling
  threads warning <https://bugs.python.org/issue33676>`_
  (`commit
  <https://github.com/python/cpython/commit/b7278736b3ae158a7738057e3045bc767ced019e>`__:
  call Pool.join)
* 2018-05-16, **socketserver**: `socketserver: Add an opt-in option to get Python 3.6
  behavior on server_close() <https://bugs.python.org/issue33540>`_
* 2017-08-18, **support**: `Make support.threading_cleanup() stricter
  <https://bugs.python.org/issue31234>`_ (**big issue with many fixes**)
* 2017-08-18, **test_logging**: `test_logging: ResourceWarning: unclosed
  socket <https://bugs.python.org/issue31235>`_
* 2017-08-18, **socketserver**: `socketserver.ThreadingMixIn leaks running threads after
  server_close() <https://bugs.python.org/issue31233>`_
* 2017-08-09, **socketserver**: `socketserver.ForkingMixIn.server_close() leaks zombie
  processes <https://bugs.python.org/issue31151>`_
* 2017-07-28: `test_multiprocessing_spawn and test_multiprocessing_forkserver
  leak dangling processes <https://bugs.python.org/issue31069>`_
  (`commit
  <https://github.com/python/cpython/commit/17657bb9458ff8f8804b7637d61686a68f4b9471>`__:
  remove Process.daemon=True, call Process.join)
* 2017-07-24, **multiprocessing**: `multiprocessing.Pool should join "dead"
  processes <https://bugs.python.org/issue31019>`_
  (`commit
  <https://github.com/python/cpython/commit/2db64823c20538a6cfc6033661fab5711d2d4585>`__)
* 2017-07-09, **multiprocessing**: `multiprocessing.Queue.join_thread() does nothing if
  created and use in the same process <https://bugs.python.org/issue30886>`_
  (`commit
  <https://github.com/python/cpython/commit/3b69d911c57ef591ac0c0f47a66dbcad8337f33a>`__)
* 2017-06-08, **multiprocessing**: `Add close() to multiprocessing.Process
  <https://bugs.python.org/issue30596>`_
* 2016-04-15, **multiprocessing**: `test_multiprocessing_spawn leaves processes
  running in background <https://bugs.python.org/issue26762>`_. **Add more
  checks** to _test_multiprocessing to **detect dangling processes and
  threads**.
* 2015-11-18, **multiprocessing**: `test_multiprocessing_spawn ResourceWarning
  with -Werror <https://bugs.python.org/issue25654>`_
  (`commit
  <https://github.com/python/cpython/commit/a6d865c128dd46a067358e94c29ca2d84205ae89>`__:
  use closefd=False)
* 2011-08-18: `Warning -- multiprocessing.process._dangling was modified by
  test_multiprocessing <https://bugs.python.org/issue12774>`_
  (`commit
  <https://github.com/python/cpython/commit/225cb8d077b9d34ec20480aad3cbd9018798546f>`__:
  test_multiprocessing.py calls the terminate() method of all classes).

Rejected, Not a Bug, Out of Date
================================

* 2018-07-18: `test_multiprocessing_spawn: Dangling processes leaked on AMD64
  FreeBSD 10.x Shared 3.x <https://bugs.python.org/issue34150>`_
* 2017-05-03: `Emit a ResourceWarning in concurrent.futures executor
  destructors <https://bugs.python.org/issue30244>`_
* 2017-04-26: `Emit ResourceWarning in multiprocessing Queue
  destructor <https://bugs.python.org/issue30171>`_
* 2016-03-25: `Replace stdout and stderr with simple standard printers at
  Python exit <https://bugs.python.org/issue26642>`_

Windows handles
===============

Abandonned attempt to hunt for leak of Windows handles:

* https://github.com/python/cpython/pull/7827 from https://bugs.python.org/issue18174
* https://github.com/python/cpython/pull/7966 from https://bugs.python.org/issue33966

Unlimited recursion
===================

Some specific unit tests rely on the exact C stack size and how Python detects
stack overflow. These tests are fragile because each platform uses a different
stack size and behaves differently on stack overflow. For example, the stack
size can depend if Python is compiled using PGO or not (depend on functions
inlining).

``_Py_CheckRecursiveCall()`` is a portable but not reliable test: basic counter
using ``sys.getrecursionlimit()``.

MSVC allows to implement ``PyOS_CheckStack()`` (``USE_STACKCHECK`` macro is
defined) using ``alloca()`` and catching ``STATUS_STACK_OVERFLOW`` error.
If uses ``_resetstkoflw()`` to reset the stack overflow flag.

Tests
-----

* test_pickle: test_bad_getattr()
* test_marshal: test_recursion_limit()

History
-------

* 2019-04-29: macOS no longer specify stack size. Previously, it was set
  to 8 MiB (``-Wl,-stack_size,1000000``).

  * https://github.com/python/cpython/commit/883dfc668f9730b00928730035b5dbd24b9da2a0
  * https://bugs.python.org/issue34602

* 2018-07-05: test_marshal: "Improve tests for the stack overflow in
  marshal.loads()"

  * https://bugs.python.org/issue33720
  * https://github.com/python/cpython/commit/fc05e68d8fac70349b7ea17ec14e7e0cfa956121

* 2018-06-04: test_marshal: "Reduces maximum marshal recursion depth on release
  builds" on Windows

  * https://github.com/python/cpython/commit/2a4a62ba4ae770bbc7b7fdec0760031c83fe1f7b
  * https://bugs.python.org/issue33720

* 2014-11-01: MAX_MARSHAL_STACK_DEPTH sets to 1000 instead of 1500 on Windows

  * https://github.com/python/cpython/commit/f6c69e6cc9aac35564a2a2a7ecc43fa8db6da975
  * https://bugs.python.org/issue22734

* 2013-07-07: Visual Studio project (PCbuild) now uses 4.2 MiB stack, instead
  of 2 MiB

  * https://github.com/python/cpython/commit/24e33acf8c422f6b8f84387242ff7874012f7291
  * https://bugs.python.org/issue17206

* 2013-05-30: macOS sets the stack size to 8 MiB

  * https://github.com/python/cpython/commit/335ab5b66f432ae3713840ed2403a11c368f5406
  * https://bugs.python.org/issue18075

* 2007-08-29: test_marshal: MAX_MARSHAL_STACK_DEPTH set to 1500 instead of 2000
  on Windows for debug build

  * https://github.com/python/cpython/commit/991bf5d8c8fdd94c3b9238d7111c0dfb41973804
  * https://bugs.python.org/issue1050
