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
