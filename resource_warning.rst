+++++++++++++++
ResourceWarning
+++++++++++++++

The multiprocessing tests leaked a lot of resources. Victor Stinner and others
fixed dozens of bugs in these tests.

See also: :ref:`Enable tracemalloc to get ResourceWarning traceback
<res-warn-tb>`.

Open issues:

* 2018-12-05, **multiprocessing**: `test_multiprocessing_fork: test_del_pool()
  leaks dangling threads and processes on AMD64 FreeBSD CURRENT Shared 3.x
  <https://bugs.python.org/issue35413>`_
* 2017-07-19, **multiprocessing**: `multiprocessing.queues.SimpleQueue leaks 2
  fds <https://bugs.python.org/issue30966>`_

Merged bugfixes:

* 2017-08-18, **support**: `Make support.threading_cleanup() stricter
  <https://bugs.python.org/issue31234>`_ (**big issue with many fixes**)
* 2017-08-18, **test_logging**: `test_logging: ResourceWarning: unclosed
  socket <https://bugs.python.org/issue31235>`_
* 2017-08-18, **socketserver**: `socketserver.ThreadingMixIn leaks running threads after
  server_close() <https://bugs.python.org/issue31233>`_
* 2017-08-09, **socketserver**: `socketserver.ForkingMixIn.server_close() leaks zombie
  processes <https://bugs.python.org/issue31151>`_
* 2017-07-09, **multiprocessing**: `multiprocessing.Queue.join_thread() does nothing if
  created and use in the same process <https://bugs.python.org/issue30886>`_
* 2017-07-24, **multiprocessing**: `multiprocessing.Pool should join "dead"
  processes <https://bugs.python.org/issue31019>`_
* 2018-05-28, **test_multiprocessing**: `test_multiprocessing_fork: dangling
  threads warning <https://bugs.python.org/issue33676>`_
* 2018-05-16, **socketserver**: `socketserver: Add an opt-in option to get Python 3.6
  behavior on server_close() <https://bugs.python.org/issue33540>`_
* 2016-04-15, **multiprocessing**: `test_multiprocessing_spawn leaves processes
  running in background <https://bugs.python.org/issue26762>`_
* 2015-11-18, **multiprocessing**: `test_multiprocessing_spawn ResourceWarning
  with -Werror <https://bugs.python.org/issue25654>`_

Rejected / Not a Bug:

* 2017-05-03: `Emit a ResourceWarning in concurrent.futures executor
  destructors <https://bugs.python.org/issue30244>`_
* 2017-04-26: `Emit ResourceWarning in multiprocessing Queue
  destructor <https://bugs.python.org/issue30171>`_
* 2016-03-25: `Replace stdout and stderr with simple standard printers at
  Python exit <https://bugs.python.org/issue26642>`_
