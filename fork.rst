++++++++++++++
Fork in Python
++++++++++++++

The `os.fork() <https://docs.python.org/dev/library/os.html#os.fork>`_ function
causes many implementation issues. It is supposed on most platforms, but
Windows and VxWorks.

posix_spawn() (fork+exec)
=========================

First of all, it's important to know how to avoid fork, especially to spawn
child processes which execute a new program :-)

On Windows, spawning a process can be done using ``CreateProcess()`` which
doesn't use fork. On Unix, ``posix_spawn()`` can avoid fork on some platforms,
and handles the dirty work for us on other platforms which implement it in
userland.

Python 3.8 provides the `os.posix_spawn()
<https://docs.python.org/dev/library/os.html#os.posix_spawn>`_ function. Not
only ``posix_spawn()`` is safer than calling manully ``fork()`` + ``exec()``,
it can also be way faster in some cases.

The ``subprocess`` module can use ``os.posix_spawn()`` under some conditions:

* *close_fds* is false;
* *preexec_fn*, *pass_fds*, *cwd* and *start_new_session* parameters
  are not set;
* the *executable* path contains a directory.


fork() (fork without exec)
==========================

The POSIX standard says only calling exec() is after after calling fork().
Calling any function different than exec() after fork() is unsafe.

Forking a process creates a child process which only has 1 thread: all other
threads are destroyed. The whole memory is duplicated. For performance, usually
memory is copied using "copy-on-write": physical memory pages are marked as
read-only and shared between the parent and the child process.  When one
process modify a memory page, the page is really duplicated and is no longer
read-only.

See `os.fork() function documentation
<https://docs.python.org/dev/library/os.html#os.fork>`_.

Reinitialize all locks after fork
=================================

When fork is called, all threads are destroyed immediately except of the
thread which called fork(). Locks can be in an inconsistent state. Using
a lock after a fork can lead to a hang or to a crash.

The meta-issue `bpo-6721 <https://bugs.python.org/issue6721>`_ "Locks in the
standard library should be sanitized on fork" tracks this problem.

The `bpo-40089 <https://bugs.python.org/issue40089>`_ added
``_PyThread_at_fork_reinit()`` function to reinitialize a lock to the unlocked
state. It can be called after a fork to prevent the bug.

PyOS_AfterFork_Child()
======================

Python has multiple functions called before and after fork:

* ``PyOS_BeforeFork()``
* ``PyOS_AfterFork_Parent()``
* ``PyOS_AfterFork_Child()``

The importlib lock is acquired before fork and released after fork.

The ``PyOS_AfterFork_Child()`` function is the most important: update Python
internal states after fork in the child process.

* Reset the GIL state
* Reset threads
* Reset importlib lock
* Clear pending signals to prevent to handle the same signal "twice" (once in
  the parent, once in the child)
* Delete Python thread states of other threads which have been destroyed.
* etc.


os.register_at_fork()
=====================

The `os.register_at_fork()
<https://docs.python.org/dev/library/os.html#os.register_at_fork>`_ added to
Python 3.7 allows to register functions which will be called at fork:

* before fork (in the parent process)
* after fork in the parent process
* after fork in the child process


macOS 10.14 (Mojave)
====================

The multiprocessing started to crash randomly on macOS 10.14 (Mojave). The
multiprocessing default start method changed from fork to spawn in Python 3.8:
see `bpo-33725 <https://bugs.python.org/issue33725>`_.


getaddrinfo() and gethostbyname() locks
=======================================

The C library provides getaddrinfo() and gethostbyname() functions which are
not thread-safe on some platforms. Python uses an internal lock on platforms
where these functions are known to not be thread-safe.

There are numerous articles about bugs caused by threads or caused by the lock
added to make the function thread-safe. For example, Python didn't reinitialize
the getaddrinfo() lock at fork in the child process (the lock has been
removed).

A thread-safe gethostbyname_r() function was added to avoid this issue.

The `bpo-25920 <https://bugs.python.org/issue25920>`_ removed the getaddrinfo()
lock.


ssl.RAND_bytes()
================

"Applications must change the PRNG state of the parent process if they use any SSL feature with os.fork()."
https://docs.python.org/dev/library/ssl.html#multi-processing
