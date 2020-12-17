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

* 2020-11-03: `bpo-41796: Make _ast module state per interpreter
  <https://bugs.python.org/issue41796>`_: test_ast leaks.

  * FIX: Call _PyAST_Fini() earlier
    (`commit <https://github.com/python/cpython/commit/fd957c124c44441d9c5eaf61f7af8cf266bafcb1>`__).

    Python types contain a reference to themselves in in their
    ``PyTypeObject.tp_mro`` member. ``_PyAST_Fini()`` must called before the
    last GC collection to destroy AST types.

    ``_PyInterpreterState_Clear()`` now calls ``_PyAST_Fini()``. It now also
    calls ``_PyWarnings_Fini()`` on subinterpeters, not only on the main
    interpreter.

    Add an assertion in AST ``init_types()`` to ensure that the ``_ast`` module
    is no longer used after ``_PyAST_Fini()`` has been called.

* 2020-03-24: `bpo-40050: Port _weakref to multiphase init
  <https://bugs.python.org/issue40050>`_: test_importlib started to leak.

  * FIX/WORKAROUND: remove unused _weakref (and _thread) import in
    ``importlib._bootstrap_external``
    (`commit <https://github.com/python/cpython/commit/83d46e0622d2efdf5f3bf8bf8904d0dcb55fc322>`__)

* 2020-04-02: `bpo-40149: Convert _abc module to use PyType_FromSpec()
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

* 2019-11-22: `bpo-36854: Make GC module state per-interpreter
  <https://bugs.python.org/issue36854>`_: test_atexit started to leak.

  * FIX: Fix refleak in PyInit__testcapi()
  * WORKAROUND: clear manually the interpreter codecs attributes (search path,
    search cache, error registry)
  * `commit <https://github.com/python/cpython/commit/310e2d25170a88ef03f6fd31efcc899fe062da2c>`__


Reorder Python finalization
===========================

* `bpo-41796: Make _ast module state per interpreter
  <https://bugs.python.org/issue41796>`__

  * 2020-11-03: Call ``_PyAST_Fini()`` earlier
    (`commit <https://github.com/python/cpython/commit/fd957c124c44441d9c5eaf61f7af8cf266bafcb1>`__).

    ``_PyInterpreterState_Clear()`` now calls ``_PyAST_Fini()``.

* `bpo-42208: Using logging or warnings during Python finalization does crash Python
  <https://bugs.python.org/issue42208>`_

  * 2020-10-30: Call GC collect earlier in ``PyInterpreterState_Clear()``
    (`commit <https://github.com/python/cpython/commit/eba5bf2f5672bf4861c626937597b85ac0c242b9>`__).

    The last GC collection is now done before clearing ``builtins`` and ``sys``
    dictionaries. Add also assertions to ensure that ``gc.collect()`` is no
    longer called after ``_PyGC_Fini()``.

* `bpo-40887: Free lists are still used after being finalized (cleared)
  <https://bugs.python.org/issue40887>`__

  * 2020-06-08: Fix ``finalize_interp_clear()`` for free lists
    (`commit <https://github.com/python/cpython/commit/7907f8cbc6923240edb0b5b63adafb871c4c8875>`__).

    Reorganize code to ensure that free lists are cleared in the right order.
    Call ``_PyWarnings_Fini()`` before ``_PyList_Fini()``.

* `bpo-19466: Clear state of threads earlier in Python shutdown
  <https://bugs.python.org/issue19466>`_

  * 2020-03-09: ``Py_Finalize()`` clears daemon threads earlier
    (`commit <https://github.com/python/cpython/commit/9ad58acbe8b90b4d0f2d2e139e38bb5aa32b7fb6>`__).

    Clear the frames of daemon threads earlier during the Python shutdown to
    call objects destructors. So "unclosed file" resource warnings are now
    emitted for daemon threads in a more reliable way.

* bpo-39511

  * 2020-02-01: PyThreadState_Clear() calls on_delete
    (`commit <https://github.com/python/cpython/commit/4d96b4635aeff1b8ad41d41422ce808ce0b971c8>`__).

    ``PyThreadState.on_delete`` is a callback used to notify Python when a
    thread completes. ``_thread._set_sentinel()`` function creates a lock which
    is released when the thread completes. It sets on_delete callback to the
    internal ``release_sentinel()`` function. This lock is known as
    ``Threading._tstate_lock`` in the threading module.

    The ``release_sentinel()`` function uses the Python C API. The problem is
    that on_delete is called late in the Python finalization, when the C API is
    no longer fully working.

    The ``PyThreadState_Clear()`` function now calls the
    ``PyThreadState.on_delete callback``. Previously, that happened in
    ``PyThreadState_Delete()``.

    The ``release_sentinel()`` function is now called when the C API is still
    fully working.

* `bpo-36854: Make GC module state per-interpreter
  <https://bugs.python.org/issue36854>`__

  * 2019-11-20: Clear the current thread later in the Python finalization
    (`commit <https://github.com/python/cpython/commit/9da7430675ceaeae5abeb9c9f7cd552b71b3a93a>`__).

    The ``PyInterpreterState_Delete()`` function is now responsible to call
    ``PyThreadState_Swap(NULL)``.

    The ``tstate_delete_common()`` function is now responsible to clear the
    ``autoTSSKey`` thread local storage and it only clears it once the thread
    state is fully cleared. It allows to still get the current thread from TSS
    in ``tstate_delete_common()``.

* `bpo-38858: new_interpreter() should reuse more Py_InitializeFromConfig() code
  <https://bugs.python.org/issue38858>`__

  * 2019-11-20: Call ``_PyExc_Fini()`` and ``_PyGC_Fini()`` later in the finalization
    (`commit <https://github.com/python/cpython/commit/7eee5beaf87be898a679278c480e8dd0df76d351>`__).


Release objects at exit
=======================

Main issue: bpo-1635741.

* bpo-1635741: Release Unicode interned strings at exit
  (`commit <https://github.com/python/cpython/commit/666ecfb0957a2fa0df5e2bd03804195de74bdfbf>`__).


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
