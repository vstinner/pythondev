+++++++++++++++
ResourceWarning
+++++++++++++++

The multiprocessing tests leaked a lot of resources. Victor Stinner and others
fixed dozens of bugs in these tests.

See also: `Enable tracemalloc to get ResourceWarning traceback <res-warn-tb>`.

Issues:

* 2017-04-26, NOTABUG: `Emit ResourceWarning in multiprocessing Queue
  destructor <https://bugs.python.org/issue30171>`_

Merged bugfixes:

* 2018-05-16, **socketserver**: `socketserver: Add an opt-in option to get Python 3.6
  behavior on server_close() <https://bugs.python.org/issue33540>`_
* 2017-08-18: `Make support.threading_cleanup() stricter
  <https://bugs.python.org/issue31234>`_ (**big issue with many fixes**)
* 2017-08-18, **socketserver**: `socketserver.ThreadingMixIn leaks running threads after
  server_close() <https://bugs.python.org/issue31233>`_
* 2017-08-09, **socketserver**: `socketserver.ForkingMixIn.server_close() leaks zombie
  processes <https://bugs.python.org/issue31151>`_
* 2017-07-09, **multiprocessing**: `multiprocessing.Queue.join_thread() does nothing if
  created and use in the same process <https://bugs.python.org/issue30886>`_
* 2017-07-24, **multiprocessing**: `multiprocessing.Pool should join "dead"
  processes <https://bugs.python.org/issue31019>`_
* 2016-04-15, **multiprocessing**: `test_multiprocessing_spawn leaves processes
  running in background <https://bugs.python.org/issue26762>`_
