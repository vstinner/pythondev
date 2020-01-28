++++++++++++++++++++++++++++++++++++++
External libraries and Generated files
++++++++++++++++++++++++++++++++++++++

Add a new C file
================

To add a C file (``.c``) or an header file (``.h``), you have to:

* Create ``Python/config.c``
* Add it to ``Makefile.pre.in``: in PYTHON_OBJS for example
* Add it to ``PCbuild/pythoncore.vcxproj``
* Add it to ``PCbuild/pythoncore.vcxproj.filters``

When creating a new directory, see also:

* For header files, see also ``Tools/msi/dev/dev.wixproj`` (read `Steve Dower's
  comment
  <https://github.com/python/cpython/pull/10624#issuecomment-441090519>`_).
* "make tags" and "make TAGS" in Makefile.pre.in
* The Windows installer copies Lib/test/ and subdirectories:
  see ``<InstallFiles Include="$(PySourcePath)Lib\test\**\*" ...>``
  in ``Tools/msi/test/test.wixproj``.

New test subdirectories should be added to ``LIBSUBDIRS`` of
``Makefile.pre.in`` (`example
<https://github.com/python/cpython/commit/2528a6c3d0660c03ae43d796628462ccf8e58190>`__).


Add a new C extension
=====================

* Update setup.py
* Update Modules/Setup


Generated files
===============

* make regen-all
* autoconf: Regenerate ``configure`` from ``configure.ac``
* ``install-sh``: ``rm install-sh; automake --add-missing --copy``,
  https://bugs.python.org/issue34765
* ``Lib/distutils/command/wininst-*.exe`` files are binaries of
  the ``PC/bdist_wininst/`` program (in Python source code).
* The frozen ``__phello`` module comes from ``M___hello__`` constant in
  ``Python/frozen.c``. The bytecode is generated
  by ``Tools/freeze/freeze.py Tools/freeze/flag.py``.
* ``Python/dtoa.c`` is based on http://www.netlib.org/fp/dtoa.c
* Unicode: Update the Unicode version in the
  ``Tools/unicode/makeunicodedata.py`` script, run it, and fix what fails
  (`msg318935 <https://bugs.python.org/msg318935>`__).
* ``Lib/keyword.py``: https://bugs.python.org/issue36143


Vendored external libraries
===========================

Update dependencies: https://github.com/python/cpython-source-deps/blob/master/README.rst

See my `external_versions.py
<https://github.com/vstinner/misc/blob/master/cpython/external_versions.py>`_
script: external version of embedded libraries from CPython source code
(locally).

On security branches, some dependencies are outdated because no more macOS nor
Windows installer is built. It was decided to not upgrade outdated zlib 1.2.5
in Python 3.3.7, since it's specific to Windows, and no Windows user is
expected to build his/her own Python 3.3 anymore.

* ``Modules/_ctypes/libffi/``: copy of `libffi <https://sourceware.org/libffi/>`_

  * Removed from Python 3.7: https://bugs.python.org/issue27979

* ``Modules/_ctypes/libffi_osx/``: `libffi <https://sourceware.org/libffi/>`_ for macOS?

  * Version: ``grep PACKAGE_VERSION Modules/_ctypes/libffi_osx/include/fficonfig.h``
  * Python 2.7-3.6 uses libffi 2.1

* ``Modules/_ctypes/libffi_msvc/``: `libffi <https://sourceware.org/libffi/>`_
  for Windows (for Microsoft Visual Studio)?

  * Version: second line of ``Modules/_ctypes/libffi_msvc/ffi.h``
  * Python 2.7-3.6 use libffi 2.0 beta, copied from ctypes-0.9.9.4 in 2006

* ``Modules/expat/``: copy of `libexpat <https://github.com/libexpat/libexpat/>`_

  * ``./configure --with-system-expat``
  * Rationale: https://mail.python.org/pipermail/python-dev/2017-June/148287.html
  * Used on Windows and macOS, Linux distributions use system libexpat
  * Version: search for ``XML_MAJOR_VERSION`` in ``Modules/expat/expat.h``
  * Script to update it: see attached script to https://bugs.python.org/issue30947
  * Recent update: https://bugs.python.org/issue30947
  * Python 2.7, 3.3-3.6 use libexpat 2.2.1

* ``Modules/zlib/``: copy of `zlib <https://zlib.net/>`_

  * Version: ``ZLIB_VERSION`` in ``Modules/zlib/zlib.h``
  * Only used on Windows (system zlib is used on macOS and Linux)
  * Python zlib module not built if system zlib is older than 1.1.3
  * Script to update it: XXX
  * Recent update: https://bugs.python.org/issue29169
  * Python 2.7, 3.4 and 3.5, 3.6 use zlib 1.2.11
  * Python 3.3 uses zlib 1.2.5: https://github.com/python/cpython/pull/3108

* ``Modules/_decimal/libmpdec/``: copy of `libmpdec <http://www.bytereef.org/mpdecimal/>`_

  * Option: ``./configure --with-system-libmpdec``
  * Included since Python 3.3 for _decimal
  * Maintained by Stefan Krah
  * Version: ``MPD_VERSION`` in ``Modules/_decimal/libmpdec/mpdecimal.h``
  * Used on all platforms
  * Script to update: XXX
  * Recent update: https://bugs.python.org/issue26621
  * Python 3.6 uses libmpdec 2.4.2 (released at february 2016)
  * Python 3.4 and 3.5 uses libmpdec 2.4.1
  * Python 3.3 uses libmpdec 2.4.0

* Windows and macOS installers include OpenSSL (binary library)

  * Windows version: search for ``openssl-`` in ``PCbuild/get_externals.bat``
  * macOS version: search for ``openssl-`` in ``Mac/BuildScript/build-installer.py``
  * See: http://python-security.readthedocs.io/ssl.html#openssl-versions
  * See: https://www.python.org/dev/peps/pep-0543/

* Windows and macOS installers include `SQLite <https://www.sqlite.org/>`_

  * Recent update: https://bugs.python.org/issue28791
  * macOS: search for ``SQLite`` in ``Mac/BuildScript/build-installer.py``
  * Windows: search for ``sqlite-`` in ``PCbuild/get_externals.bat``

See also `cpython-bin-deps <https://github.com/python/cpython-bin-deps>`_
and `cpython-source-deps <https://github.com/python/cpython-source-deps>`_.
