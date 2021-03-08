++++++++++++++++++++++++++++++++
Bugs found by the Python project
++++++++++++++++++++++++++++++++

CPython has an extensive test suite which sometimes spot bugs in third party
code.

Kernel bugs
===========

* `FreeBSD copy_file_range bug <https://bugs.python.org/issue43233>`_
* `Crash with mmap and sparse files on Mac OS X
  <http://bugs.python.org/issue11277>`_
* test_os on Linux 2.6.?35?
  return code
* Many issues with threads+signals on OpenBSD and old versions of FreeBSD:
  test disabled on these platforms
* FreeBSD: `when close(fd) on a fifo fails with EINTR, the file descriptor is
  not really closed
  <https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=203162>`_

Compiler bugs
=============

* ppc64le double to float cast + memcpy bug

  * https://bugs.python.org/issue35752
  * https://gcc.gnu.org/bugzilla/show_bug.cgi?id=88892

* `Visual Studio: PGO on 64 bits
  <http://bugs.python.org/issue15993>`_
* Visual Studio PGupdate duplicated functions:

  - "Disable COMDAT folding in Windows PGO builds."
  - http://bugs.python.org/issue8847#msg166935
  - http://hg.python.org/cpython/rev/029cde4e58c5

* Error with gcc-4.6 -O1 -ftree-vectorize

  - "Python 3.2 doesn't compile correctly with -O3"
  - http://gcc.gnu.org/ml/gcc-help/2011-01/msg00136.html
  - http://gcc.gnu.org/bugzilla/show_bug.cgi?id=47271
  - http://gcc.gnu.org/viewcvs?view=revision&revision=169233

* Apple Clang bug

  - `llvm-gcc-4.2 miscompiles Python (XCode 4.1 on Mac OS 10.7)
    <http://bugs.python.org/issue13241>`_

