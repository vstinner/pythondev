+++++++++++++++++++
Python Finalization
+++++++++++++++++++

At exit, Python calls ``Py_Finalize()`` which is responsible to stop
Python and cleanly all states, variables, modules. etc. This code is
very fragile.

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
