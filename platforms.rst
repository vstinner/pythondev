+++++++++++++++++++++++++++++++++++++
Supported platforms and architectures
+++++++++++++++++++++++++++++++++++++

See also :ref:`Python on Android <android>`.

Supported architectures
=======================

Well supported architectures:

* Intel x86 (32-bit) and x86_64 (64-bit, aka AMD64)

Best effort support architectures:

* ppc64le: should be well supported in practice
* AArch64
* ARMv7: should be well supported in practice
* s390x


Well supported platforms
========================

Well supported platforms on Python 3.7 and 2.7:

* Linux
* Windows Vista and newer for Python 3.7, Windows XP and newer for Python 2.7
* FreeBSD 10 and newer
* macOS Snow Leopard (macOS 10.6, 2008) and newer

It took 9 years to `fix all compiler warnings on Windows 64-bit
<https://bugs.python.org/issue9566#msg337328>`_! Usually, the fix was to use a
larger type to avoid a downcast. For example replace ``int`` with
``Py_ssize_t``.

Linux
-----

CPython still has compatibility code for Linux 2.6, whereas the
support of Linux 2.6.x ended in August 2011, longer than 6 years ago.

Proposition in January 2018 to drop support for old Linux kernels:
https://mail.python.org/pipermail/python-dev/2018-January/151821.html

Windows
-------

* `Windows Supported Versions in Python
  <https://docs.python.org/dev/using/windows.html#supported-versions>`_
  (in the Python development ``master`` branch)
* Windows Vista support dropped in Python 3.7
* Windows XP support dropped in Python 3.5
* Windows 2000 support dropped in Python 3.4
* `bpo-23451 <https://bugs.python.org/issue23451>`_, 2015-03: "Python 3.5 now
  requires Windows Vista or newer". See `change1
  <https://hg.python.org/cpython/rev/57e2549cc9a6>`_ and `change2
  <https://hg.python.org/cpython/rev/f64d0b99d405>`_.
* Python 2.7 supports Windows XP and newer
* PEP 11 on Windows:

    CPython's Windows support now follows [Microsoft product support
    lifecycle]. A new feature release X.Y.0 will support all Windows releases
    whose extended support phase is not yet expired. Subsequent bug fix
    releases will support the same Windows releases as the original feature
    release (even if the extended support phase has ended).

FreeBSD
-------

* Python 3.7 dropped support for FreeBSD 9 and older.
* FreeBSD 9 buildbot wokers have been removed in 2017

macOS
-----

* 2018-05-28: macOS Snow Leopard (macOS 10.6, 2008) is `currently
  <https://mail.python.org/pipermail/python-dev/2018-May/153725.html>`_ the
  minimum officially supported macOS version.
* February 2018: Tiger (macOS 10.4, 2004) buildbots removed, which indirectly
  means that Tiger is no longer officially supported.

Tested by Travis CI and buildbots.


Best effort and unofficial platforms
====================================

Supported platform with best effort support:

* Android API 24
* OpenBSD
* NetBSD
* AIX 6.1 and newer

Platforms not supported officially:

* Cygwin
* `HP-UX <https://en.wikipedia.org/wiki/HP-UX>`_

  * HP-UX 11i v3 was first released in 2007. Latest HP-UX release: May 2020.
  * test_gdb fix in 2020: commit b2dca49ca3769cb60713f5c2b43e5d5bbdc1f9c7
  * os.chroot fix in 2020: commit a9edf44a2de9b23a1690b36cdfeed7b41ab763bd

* MinGW
* Solaris, OpenIndiana

Unofficial projects:

* `Python for OpenVMS <https://www.vmspython.org/>`_
* `PythonD <http://www.caddit.net/pythond/>`_:  PythonD is a 32-bit,
  multi-threaded, networking- and OpenGL-enabled Python interpreter for DOS and
  Windows.


Removed platforms
=================

PEP 11 lists removal of supported platforms:

* Platforms without threading support removed in Python 3.7

  * https://bugs.python.org/issue31370
  * https://mail.python.org/pipermail/python-dev/2017-September/149156.html
  * https://github.com/python/cpython/commit/a6a4dc816d68df04a7d592e0b6af8c7ecc4d4344

* `BSD/OS <https://en.wikipedia.org/wiki/BSD/OS>`_, 2017:

  * https://bugs.python.org/issue31624
  * https://github.com/python/cpython/commit/288d1daadaddf6ae35cf666138ba4b5d07449657

* `MS-DOS <https://en.wikipedia.org/wiki/MS-DOS>`_: 2014:
  `bpo-22591: Drop support of MS-DOS (DJGPP compiler)
  <https://bugs.python.org/issue22591>`_,
  `commit b71c7dc9 <https://github.com/python/cpython/commit/b71c7dc9ddd6997be49ed6aaabf99a067e2c0388>`_
* Python 3.4: `VMS <https://en.wikipedia.org/wiki/OpenVMS>`_, `OS/2
  <https://en.wikipedia.org/wiki/OS/2>`_, `Windows 2000
  <https://en.wikipedia.org/wiki/Windows_2000>`_

  * VMS:
    `bpo-16136: Removal of VMS support <https://bugs.python.org/issue16136>`_,
    `main removal commit <https://github.com/python/cpython/commit/af01f668173d4061893148b54a0f01b91c7716c2>`_
    (`remove VMSError doc commit
    <https://github.com/python/cpython/commit/b2788fe854173b6b213010a7462c05594d703c06>`_)

* `IRIX <https://en.wikipedia.org/wiki/IRIX>`_ ("The last major version of IRIX is IRIX 6.5, which was released in May 1998")

  * Python 3.7: `Remove dynload_dl
    <https://github.com/python/cpython/commit/0cafcd3c56c9475913d8d4fd0223c297dbb70ac6>`_
    (2020)

* `AIX 5.3 and below
  <https://github.com/python/cpython/commit/c79667ff7921444911e8a5dfa5fba89294915590>`_

* Mac OS 9:

  * MacOS 9 dropped in Python 2.4 (see PEP 11)
  * `bpo-35346: Drop Mac OS 9 support from platform
    <https://github.com/python/cpython/commit/b0e0877629e3df4bc3042fd424e96f197b2e9fa4>`_
  * `bpo-35471: Remove the macpath module (GH-11129)
    <https://github.com/python/cpython/commit/d7538dd5e3e04a8db22e1470cb2ed696bf3be160>`_


I want CPython to support my platform!
======================================

In short, there are 2 conditions:

* the full test suite have to pass (``./python -m test`` succeess)
* a CPython core developer has to be responsible of the platform to fix issues
  specific to this platform on :ref:`CIs <ci>`.

If it's not possible, the best option is to maintain a fork of CPython (fork
of the Git repository) to maintain patches to top of the master branch
(and maybe also patches on other branches).

More detail in the :pep:`11`.


.. _c-compilers:

C compilers
===========

Python has a good support for:

* GCC
* clang
* Visual Studio MSC

Best effort:

* XLC on AIX 7

Compiler flags:

* Debug build uses -Og
* Release build uses -O3
* clang with LTO
* clang with LTO+PGO
* GCC with LTO
* GCC with LTO+PGO

See :ref:`Python Continuous Integration <ci>` to see exactly which C compilers
and which compiler and linker flags are actually tested.

See also :ref:`Python builds <python-builds>`.

See `PEP 7 <https://www.python.org/dev/peps/pep-0007/>`_ for the minimum C
standard version. In short, it's a subset of C99 with static line functions and
``<stdint.h>``.


sys.platform versus os.name
===========================

Example of ``sys.platform`` and ``os.name`` values:

========  =================================================  =========
Platform  sys.platform                                       os.name
========  =================================================  =========
AIX       ``aix`` on Python3.8+, (**)                        ``posix``
FreeBSD   ``freebsd5``, ``freebsd6``, ...                    ``posix``
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
* ``uname -r`` command output (or ``uname -v`` UnixWare or OpenUNIX)
* ``$host`` variable (``./configure --host=xxx`` parameter)
  when cross-compiling

(*) ``sys.platform`` was also ``linux3`` on old versions of Python 2.6 and
Python 2.7 with Linux kernel 3.x.

(**) On AIX ``sys.platform`` included a release digit, ``aix3``, ...,
``aix7`` on all versions of Python through version Python 3.7.
