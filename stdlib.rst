.. _stdlib:

+++++++++++++++++++++++
Python standard library
+++++++++++++++++++++++

See also :ref:`Supported platforms and architectures <platforms>`,
:ref:`History of Python <history>`, and :ref:`Python Import <import>`.

sys.stdlib_module_names
=======================

* Python 3.14: 290 modules

  * Add (1): ``annotationlib``

* Python 3.13: 289 modules

  * Add (10):

    * ``_android_support``,
    * ``_colorize``,
    * ``_interpchannels``,
    * ``_interpqueues``,
    * ``_interpreters``,
    * ``_ios_support`` (:pep:`730`),
    * ``_opcode_metadata``,
    * ``_pyrepl`` (:pep:`762`),
    * ``_suggestions``,
    * ``_sysconfig``.

  * Remove (22): ``_crypt``, ``_msi``, ``aifc``, ``audioop``, ``cgi``,
    ``cgitb``, ``chunk``, ``crypt``, ``imghdr``, ``lib2to3``, ``mailcap``,
    ``msilib``, ``nis``, ``nntplib``, ``ossaudiodev``, ``pipes``, ``sndhdr``,
    ``spwd``, ``sunau``, ``telnetlib``, ``uu``, ``xdrlib``.

* Python 3.12: 301 modules

  * Add (4):

    * ``_sha2``,
    * ``_pylong``,
    * ``_pydatetime``,
    * ``_wmi``.

  * Remove (8): ``_bootsubprocess``, ``_sha256``, ``_sha512``, ``asynchat``, ``asyncore``, ``distutils``, ``imp``, ``smtpd``

* Python 3.11: 305 modules

  * Add (3):

    * ``tomllib`` (:pep:`680`),
    * ``_tokenize``,
    * ``_typing``.

  * Remove (1): ``binhex``.

* Python 3.10: 303 modules

`sys.stdlib_module_names
<https://docs.python.org/dev/library/sys.html#sys.stdlib_module_names>`_ was
added to Python 3.10. For Python 2.6 to 3.9, the 3rd party `stdlib-list
<https://pypi.org/project/stdlib-list/>`_ module can be used.


Talks
=====

* 2023: `Language Summit 2023: What is the stdlib for?
  <https://us.pycon.org/2023/events/language-summit/>`_
  by Brett Cannon
* 2021: `The 2021 Python Language Summit: What Is the stdlib?
  <https://pyfound.blogspot.com/2021/05/the-2021-python-language-summit-what-is.html>`_
  by Brett Cannon
* 2019: `Batteries Included, But They're Leaking
  <https://pyfound.blogspot.com/2019/05/amber-brown-batteries-included-but.html>`_
  by Amber Brown

Maintain the stdlib outside Python?
===================================

* 2021: `cpython_hack <https://github.com/dabeaz/cpython_hack>`_:
  David Beazley's experiment to make the Python stdlib as small as possible.
  The stdlib is made of 7 Python modules and 3 C extensions.

  stdlib Python modules:

  * ``genericpath``
  * ``io``
  * ``os``
  * ``posixpath``
  * ``site``
  * ``stat``
  * ``types``

  stdlib C extensions:

  * ``_stat``
  * ``posix``
  * ``readline``

  There is an extra ``Lib/__phello__.foo.py`` module, but it's only used for tests.

* 2019: `If Python started moving more code out of the stdlib and into PyPI
  packages, what technical mechanisms could packaging use to ease that
  transition?
  <https://discuss.python.org/t/if-python-started-moving-more-code-out-of-the-stdlib-and-into-pypi-packages-what-technical-mechanisms-could-packaging-use-to-ease-that-transition/1738>`_
  by Nathaniel J. Smith
* `PEP 360 – Externally Maintained Packages
  <https://peps.python.org/pep-0360/>`_

Stdlib history
==============

Python 3.13
-----------

Python 3.13 removed 20 module:

* ``lib2to3``:
  `deprecated in Python 3.11 <https://github.com/python/cpython/issues/84540>`_,
  `issue #104780 <https://github.com/python/cpython/issues/104780>`_,
  `PEP 617`_
* ``aifc``: `PEP 594`_
* ``audioop``: `PEP 594`_
* ``cgi``: `PEP 594`_
* ``cgitb``: `PEP 594`_
* ``chunk``: `PEP 594`_
* ``crypt``: `PEP 594`_
* ``imghdr``: `PEP 594`_
* ``mailcap``: `PEP 594`_
* ``msilib``: `PEP 594`_
* ``nis``: `PEP 594`_
* ``nntplib``: `PEP 594`_
* ``ossaudiodev``: `PEP 594`_
* ``pipes``: `PEP 594`_
* ``sndhdr``: `PEP 594`_
* ``spwd``: `PEP 594`_
* ``sunau``: `PEP 594`_
* ``telnetlib``: `PEP 594`_
* ``uu``: `PEP 594`_
* ``xdrlib``: `PEP 594`_

Python 3.12
-----------

Python 3.12 removed 5 module:

* ``asynchat``: deprecated in Python 3.6, `PEP 594`_
* ``asyncore``: deprecated in Python 3.6, `PEP 594`_
* ``distutils``:
  deprecated in Python 3.10,
  `PEP 632 - Deprecate distutils module <https://peps.python.org/pep-0632/>`_
* ``imp``:
  deprecated in Python 3.5,
  `issue #98040 <https://github.com/python/cpython/issues/98040>`_,
  `PR #98573 <https://github.com/python/cpython/pull/98573>`_,
  replaced with ``importlib``
* ``smtpd``: deprecated in Python 3.6, `PEP 594`_

PEP 594
^^^^^^^

`PEP 594 – Removing dead batteries from the standard library
<https://peps.python.org/pep-0594/>`_ scheduled the removal of many stdlib
modules in Python 3.12 and 3.13.

Python 3.11
-----------

Python 3.11 added 1 module:

* ``tomllib``:
  `PEP 680 – tomllib: Support for Parsing TOML in the Standard Library
  <https://peps.python.org/pep-0680/>`_

Python 3.11 added 1 sub-module to existing packages:

* ``wsgiref.types``

Python 3.11 removed 1 module:

* ``binhex``:
  `deprecated in Python 3.9 <https://github.com/python/cpython/issues/83534>`_,
  `issue #89248 <https://github.com/python/cpython/issues/89248>`_.

Note: ``asyncore``, ``asynchat``, ``smtplib`` were removed in Python 3.11,
but then `the SC asked to add them back
<https://github.com/python/steering-council/issues/86>`_

Python 3.10
-----------

Python 3.10 removed 3 modules:

* ``formatter``:
  `deprecated in Python 3.4 <https://github.com/python/cpython/issues/62916>`_,
  `issue #86465 <https://github.com/python/cpython/issues/86465>`_,
  `python-dev thread <https://mail.python.org/archives/list/python-dev@python.org/thread/ZEDIBBYCWI34GVOXDEUYXQY3LYXOFHA2/>`_
* ``parser``: deprecated in Python 3.9, `PEP 617`_
  (PEG parser)
* ``symbol``: deprecated in Python 3.9, `PEP 617`_

.. _PEP 617: https://peps.python.org/pep-0617/

Python 3.9
----------

Python 3.9 added 2 modules:

* ``graphlib``
* ``zoneinfo``

Python 3.9 removed 2 modules:

* ``dummy_threading``: deprecated in Python 3.7;
  Python 3.7 requires threads to build: `bpo-31370
  <https://bugs.python.org/issue31370>`_.
* ``_dummy_thread``: same.

Python 3.8
----------

Python 3.8 added 1 sub-module to existing packages:

* ``importlib.metadata``

Python 3.8 removed 1 module:

* ``macpath``:
  `deprecated in Python 3.7 <https://github.com/python/cpython/issues/54059>`_,
  `issue #79652 <https://github.com/python/cpython/issues/79652>`_,
  Mac OS 9 is no longer used.

Python 3.7
----------

Python 3.7 added 2 modules:

* ``contextvars``:
  `PEP 567 – Context Variables <https://peps.python.org/pep-0567/>`_
* ``dataclasses``:
  `PEP 557 – Data Classes <https://peps.python.org/pep-0557/>`_

Python 3.7 added 1 sub-module to existing packages:

* ``importlib.resources``:
  `issue #76429 <https://github.com/python/cpython/issues/76429>`_

Python 3.7 removed 2 modules:

* ``fpectl``:
  `issue #73323 <https://github.com/python/cpython/issues/73323>`_,
  it was never enabled by default, never worked correctly on x86-64, and it
  changed the Python ABI in ways that caused unexpected breakage of C
  extensions.
* ``macurl2path``:
  `issue #72512 <https://github.com/python/cpython/issues/72512>`_

Python 3.6
----------

Python 3.6 added 1 module:

* ``secrets``:
  `PEP 506 – Adding A Secrets Module To The Standard Library
  <https://peps.python.org/pep-0506/>`_

Python 3.6 removed 6 modules:

* ``CDIO``: `issue #72214`_
* ``CDROM``: `issue #72214`_
* ``DLFCN``: `issue #72214`_
* ``IN``: `issue #72214`_
* ``STROPTS``: `issue #72214`_
* ``TYPES``: `issue #72214`_

`issue #72214`_: These removed modules were undocumented. They had been
available in the platform specific ``Lib/plat-*/`` directories, but were
chronically out of date, inconsistently available across platforms, and
unmaintained.

.. _issue #72214: https://github.com/python/cpython/issues/72214

Python 3.5
----------

Python 3.5 added 2 modules:

* ``typing``
  `PEP 484 – Type Hints
  <https://peps.python.org/pep-0484/>`_
  and
  `PEP 483 – The Theory of Type Hints
  <https://peps.python.org/pep-0483/>`_
* ``zipapp``:
  `PEP 441 – Improving Python ZIP Application Support
  <https://peps.python.org/pep-0441/>`_

Python 3.4
----------

Python 3.4 added 7 modules:

* ``asyncio``:
  `PEP 3156 – Asynchronous IO Support Rebooted: the “asyncio” Module
  <https://peps.python.org/pep-3156/>`_
* ``ensurepip``
* ``enum``:
  `PEP 435 – Adding an Enum type to the Python standard library
  <https://peps.python.org/pep-0435/>`_
* ``pathlib``:
  `PEP 428 – The pathlib module – object-oriented filesystem paths
  <https://peps.python.org/pep-0428/>`_
* ``selectors``: PEP 3156
* ``statistics``:
  `PEP 450 – Adding A Statistics Module To The Standard Library
  <https://peps.python.org/pep-0450/>`_
* ``tracemalloc``:
  `PEP 454 – Add a new tracemalloc module to trace Python memory allocations
  <https://peps.python.org/pep-0454/>`_

Python 3.3
----------

Python 3.3 added 4 modules:

* ``faulthandler``:
  `issue #55602 <https://github.com/python/cpython/issues/55602>`_
* ``ipaddress``:
  `PEP 3144 – IP Address Manipulation Library for the Python Standard Library
  <https://peps.python.org/pep-3144/>`_
* ``lzma``:
  `issue #50964 <https://github.com/python/cpython/issues/50964>`_
* ``venv``:
  `PEP 405 – Python Virtual Environments
  <https://peps.python.org/pep-0405/>`_

Python 3.3 added 1 sub-module to existing packages:

* ``unittest.mock``

Python 3.2
----------

Python 3.2 added 2 modules:

* ``argparse``:
  `PEP 389 – argparse - New Command Line Parsing Module
  <https://peps.python.org/pep-0389/>`_
* ``concurrent.futures``:
  `PEP 3148 – futures - execute computations asynchronously
  <https://peps.python.org/pep-3148/>`_

Python 3.1
----------

Python 3.1 added 1 module:

* ``importlib``

Python 3.1 added 1 sub-module to existing packages:

* ``tkinter.ttk``

Python 3.0
----------

Python 3.0 removed 74 stdlib modules, related to `PEP 3108
<https://www.python.org/dev/peps/pep-3108/#modules-to-remove>`_.

Moreover, many Python 2.7 modules `have been renamed by PEP 3108
<https://www.python.org/dev/peps/pep-3108/#modules-to-rename>`_.

Removed Mac modules (24):

* ``aepack``
* ``aetools``
* ``aetypes``
* ``buildtools``
* ``Carbon``
* ``cfmfile``
* ``ColorPicker``
* ``EasyDialogs``
* ``findertools``
* ``fm``
* ``FrameWork``
* ``gensuitemodule``
* ``ic``
* ``icopen``
* ``mac``
* ``macerrors``
* ``MacOS``
* ``macosa``
* ``macostools``
* ``macresource``
* ``MiniAEFrame``
* ``Nav``
* ``PixMapWrapper``
* ``videoreader``

Removed IRIX modules (7):

* ``al``
* ``DEVICE``
* ``flp``
* ``gl``: Functions from the Silicon Graphics Graphics Library.
* ``imgfile``: Support for SGI imglib files
* ``jpeg``: Read and write JPEG files
* ``sgi``: random SGI-specific things

Removed modules, replaced by the ``email`` package (5):

* ``mimetools``
* ``MimeWriter``
* ``mimify``
* ``multifile``
* ``rfc822``

Other removed modules (38):

* ``audiodev``: Classes for manipulating audio devices (currently only for Sun and SGI)
* ``Bastion``: Providing restricted access to objects
* ``bsddb``
* ``Canvas`` (tk)
* ``cd``: CD Audio Library
* ``commands``: Utility functions for running external commands
* ``compiler``: analyze Python source code and generating Python bytecode
* ``dircache``: read directory listing with cache
* ``dl``: ``dl.open()``
* ``exceptions``: Standard exception classes
* ``FixTk``: Delay import _tkinter until we have set TCL_LIBRARY, imported by `Tkinter``
* ``fl``: interface to Mark Overmars' FORMS Library
* ``fpformat``: General floating point formatting functions
* ``future_builtins``: Python 3 builtins
* ``ihooks``: Import hook support
* ``imageop``: Manipulate raw image data, replaced with PIL/Pillow
* ``imputil``: Import utilities
* ``linuxaudiodev``: Linux audio device (``/dev/dsp``) for python, replaced by ``ossaudiodev``.
* ``markupbase``: Renamed to ``_markupbase``, used by ``html.parser``
* ``md5``: Replaced by ``hashlib``
* ``mhlib``: Manipulate MH mailboxes from Python
* ``mutex``: Lock and queue for mutual exclusion
* ``new``: Interface to the creation of runtime implementation objects
* ``os2emxpath``: Common operations on OS/2 pathnames
* ``popen2``: Subprocesses with accessible I/O streams
* ``posixfile``: File-like objects with locking support
* ``rexec``: Restricted execution framework
* ``sets``: Unordered collections of unique elements, replaced by ``set()`` built-in type
* ``sgmllib``: Simple SGML parser
* ``sha``: Replaced by ``hashlib``
* ``sre``: Replaced by ``re``
* ``statvfs``: Replaced by ``os.statvfs()``
* ``stringold``: Collection of string operations
* ``strop``: Common string manipulations, optimized for speed (C extension)
* ``sunaudiodev`` (SunOS): Access to Sun audio hardware
* ``toaiff``: Convert "arbitrary" sound files to AIFF (Apple and SGI's audio format)
* ``user``: Hook to allow user-specified customization code to run
* ``xmllib``: Parser for XML, using the derived class as static DTD.
