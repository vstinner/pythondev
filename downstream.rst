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

  * `python38 <https://src.fedoraproject.org/rpms/python38/tree/master>`__
    (2019-08-12: 7 patches; Python 3.8.0b3)
  * `python3 <https://src.fedoraproject.org/rpms/python3/tree/master>`__
  * `python2 <https://src.fedoraproject.org/rpms/python2/tree/master>`__

* Guix

  * http://git.savannah.gnu.org/cgit/guix.git/tree/gnu/packages/patches/python-3-deterministic-build-info.patch
  * http://git.savannah.gnu.org/cgit/guix.git/tree/gnu/packages/patches/python-3-fix-tests.patch
  * http://git.savannah.gnu.org/cgit/guix.git/tree/gnu/packages/patches/python-3-search-paths.patch

See also :ref:`Python on Android <android>`.
