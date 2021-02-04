++++++++++++++++++
Downstream patches
++++++++++++++++++

Linux distributions use downstream patches to adapt Python for their needs,
backport bugfixes and security fixes, etc.

* Debian

  * `python3: debian/patches/
    <https://salsa.debian.org/cpython-team/python3/tree/master/debian/patches>`_
    (2019-08-12: 41 files; Python 3.8.0b2)

* Fedora

  * `python3.10 <https://src.fedoraproject.org/rpms/python3.10/tree/rawhide>`__
    (2021-02-04: 4 patches; Python 3.10.0a5)
  * `python3.8 <https://src.fedoraproject.org/rpms/python3.8/tree/rawhide>`__
    (2021-02-04: 8 patches; Python 3.8.7)
  * `python2.7 <https://src.fedoraproject.org/rpms/python2.7/tree/rawhide>`__
    (2021-02-04: 53 patches; Python 2.7.18)

* Guix

  * http://git.savannah.gnu.org/cgit/guix.git/tree/gnu/packages/patches/python-3-deterministic-build-info.patch
  * http://git.savannah.gnu.org/cgit/guix.git/tree/gnu/packages/patches/python-3-fix-tests.patch
  * http://git.savannah.gnu.org/cgit/guix.git/tree/gnu/packages/patches/python-3-search-paths.patch

* FreeBSD

  * https://svnweb.freebsd.org/ports/head/lang/python38/files/
  * https://svnweb.freebsd.org/ports/head/lang/python37/files/
  * https://svnweb.freebsd.org/ports/head/lang/python36/files/
  * https://svnweb.freebsd.org/ports/head/lang/python27/files/

* Gentoo

  * Python 2.7.18: https://gitweb.gentoo.org/fork/cpython.git/log/?h=gentoo-2.7.18-r6
  * All branches: https://gitweb.gentoo.org/fork/cpython.git/refs/?h=gentoo-2.7.18

See also :ref:`Python on Android <android>`.
