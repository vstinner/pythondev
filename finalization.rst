.. _finalization:

+++++++++++++++++++
Python Finalization
+++++++++++++++++++

At exit, Python calls ``Py_Finalize()`` which is responsible to stop
Python and cleanly all states, variables, modules. etc. This code is
very fragile.

Issues with clearing memory at exit
===================================

Since Python 3.6, a big refactoring started in CPython to clear more and more
variables and states at Python exit: in ``Py_FinalizeEx()``, but also in Python
``main()`` (for variables which cannot be cleared in ``Py_FinalizeEx()``.

Sadly, it caused some nasty issues:

* `The os module should unset() environment variable at exit
  <https://bugs.python.org/issue39395>`_
* `Make struct module PEP-384 compatible
  <https://bugs.python.org/issue38076#msg351608>`_


Weird GC behavior during Python finalization
============================================

When an extension module is converted to the multiphase initialization API (PEP
489), sometimes tests using subinterpreters start to leak.

* `bpo-36854: Make GC module state per-interpreter
  <https://bugs.python.org/issue36854>`_: test_atexit started to leak.

  * Fix refleak in PyInit__testcapi()
  * WORKAROUND: clear manually the interpreter codecs attributes (search path,
    search cache, error registry)
  * https://github.com/python/cpython/commit/310e2d25170a88ef03f6fd31efcc899fe062da2c

* `bpo-40050: Port _weakref to multiphase init
  <https://bugs.python.org/issue40050>`_: test_importlib started to leak.

  * FIX/WORKAROUND: remove unused _weakref (and _thread) import in
    ``importlib._bootstrap_external``.
  * https://github.com/python/cpython/commit/83d46e0622d2efdf5f3bf8bf8904d0dcb55fc322

* `bpo-40149: Convert _abc module to use PyType_FromSpec()
  <https://bugs.python.org/issue40149>`_: test_threading leaks.

  * WORKAROUND 1 (not merged): add a second ``_PyGC_CollectNoFail()`` call in
    ``finalize_interp_clear()``.
  * FIX 1: Implement traverse in _abc._abc_data
    (`commit <https://github.com/python/cpython/commit/9cc3ebd7e04cb645ac7b2f372eaafa7464e16b9c>`__)
  * WORKAROUND 2 (not merged): add ``Py_VISIT(Py_TYPE(self));`` in ``abc_data_traverse()``.
  * Regression caused by `bpo-35810: Object Initialization does not incref
    Heap-allocated Types <https://bugs.python.org/issue35810>`_?
  * `bpo-40217: The garbage collector doesn't take in account that objects of
    heap allocated types hold a strong reference to their type
    <https://bugs.python.org/issue40217>`_
  * FIX 2 (bpo-40217): inject a magic function to visit the heap type in traverse functions
    (`commit <https://github.com/python/cpython/commit/0169d3003be3d072751dd14a5c84748ab63a249f>`__)
  * FIX 3 (bpo-40217): Revert FIX 2 and traverse functions must explicitly
    visit their type
    (`commit <https://github.com/python/cpython/commit/1cf15af9a6f28750f37b08c028ada31d38e818dd>`__).
    ``abc_data_traverse()`` now calls ``Py_VISIT(Py_TYPE(self))``.


Prevent deadlock in io.BufferedWriter
=====================================

https://bugs.python.org/issue23309

Commit::

    commit 25f85d4bd58d86d3e6ce99cb9f270e96bf5ba08f
    Author: Antoine Pitrou <solipsis@pitrou.net>
    Date:   Mon Apr 13 19:41:47 2015 +0200

        Issue #23309: Avoid a deadlock at shutdown if a daemon thread is aborted
        while it is holding a lock to a buffered I/O object, and the main thread
        tries to use the same I/O object (typically stdout or stderr).  A fatal
        error is emitted instead.

Code::

    relax_locking = _Py_IsFinalizing();
    Py_BEGIN_ALLOW_THREADS
    if (!relax_locking)
        st = PyThread_acquire_lock(self->lock, 1);
    else {
        /* When finalizing, we don't want a deadlock to happen with daemon
         * threads abruptly shut down while they owned the lock.
         * Therefore, only wait for a grace period (1 s.).
         * Note that non-daemon threads have already exited here, so this
         * shouldn't affect carefully written threaded I/O code.
         */
        st = PyThread_acquire_lock_timed(self->lock, (PY_TIMEOUT_T)1e6, 0);
    }
    Py_END_ALLOW_THREADS
    if (relax_locking && st != PY_LOCK_ACQUIRED) {
        PyObject *msgobj = PyUnicode_FromFormat(
            "could not acquire lock for %A at interpreter "
            "shutdown, possibly due to daemon threads",
            (PyObject *) self);
        const char *msg = PyUnicode_AsUTF8(msgobj);
        Py_FatalError(msg);
    }


Notes
=====

To workaround `bpo-19565 <https://bugs.python.org/issue19565>`_ on Windows,
multiprocessing crash at exit, ``_winapi.Overlapped`` deallocator leaves
the overlapped handle open if Python is exiting, see the `commit
<https://github.com/python/cpython/commit/633db6f6a69fd44b4a27e7e216ff7a138f69aaf3>`__::

    commit 633db6f6a69fd44b4a27e7e216ff7a138f69aaf3
    Author: Richard Oudkerk <shibturn@gmail.com>
    Date:   Sun Nov 17 13:15:51 2013 +0000

        Issue #19565: Prevent warnings at shutdown about pending overlapped ops.

Python issues
=============

* 2013-10-31: `Clear state of threads earlier in Python shutdown
  <https://bugs.python.org/issue19466>`_. Call
  ``_PyThreadState_DeleteExcept(tstate)`` in ``Py_Finalize()``. This issue
  introduced corrupted a Python frame of an asyncio daemon thread which leaded
  to a crash: `bpo-20526 <https://bugs.python.org/issue20526>`__. I had to
  revert the ``_PyThreadState_DeleteExcept(tstate)`` change.

Cython
======

`__dealloc__()
<https://cython.readthedocs.io/en/latest/src/userguide/special_methods.html#finalization-method-dealloc>`_:

    By the time your ``__dealloc__()`` method is called, the object may already
    have been partially destroyed and may not be in a valid state as far as
    Python is concerned, so you should avoid invoking any Python operations
    which might touch the object. In particular, don’t call any other methods
    of the object or do anything which might cause the object to be
    resurrected. It’s best if you stick to just deallocating C data.


Daemon threads
==============

* Subinterpreters cannot spawn daemon threads anymore, since Python 3.9:
  https://bugs.python.org/issue37266

* In Python 3.8, daemon threads now exit immediately when they attempt to
  acquire the GIL, after Py_Finalize() has been called:

  * https://bugs.python.org/issue36475 with https://github.com/python/cpython/commit/f781d202a2382731b43bade845a58d28a02e9ea1
  * https://bugs.python.org/issue39877 with https://github.com/python/cpython/commit/eb4e2ae2b8486e8ee4249218b95d94a9f0cc513e

* `change <https://hg.python.org/cpython/rev/c2a13acd5e2b>`_ of `bpo-19466
  <https://bugs.python.org/issue19466>`_ caused `bpo-20526
  <https://bugs.python.org/issue20526>`_ regression
