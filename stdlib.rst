+++++++++++++++++++++++
Python standard library
+++++++++++++++++++++++

sys.stdlib_module_names
=======================

`sys.stdlib_module_names
<https://docs.python.org/dev/library/sys.html#sys.stdlib_module_names>`_ was
added to Python 3.10. For Python 2.6 to 3.9, the 3rd party `stdlib-list
<https://pypi.org/project/stdlib-list/>`_ module can be used.

``len(sys.stdlib_module_names)``:

* Python 3.11: 304 modules (add ``_tokenize`` and ``_typing``,
  remove ``binhex``)
* Python 3.10: 303 modules


Removed modules
===============

Python 3.11
-----------

Python 3.11 removed 1 module:

* ``binhex``: deprecated in Python 3.9

Note: ``asyncore``, ``asynchat``, ``smtplib`` were removed but then `the SC
asked to add them back <https://github.com/python/steering-council/issues/86>`_

Python 3.10
-----------

Python 3.10 removed 2 modules:

* ``formatter``: deprecated in Python 3.4
* ``parser``: deprecated in Python 3.9, removal related to PEP 617
  (PEG parser)

Python 3.9
----------

Python 3.9 removed 2 modules:

* ``dummy_threading``, ``_dummy_thread``: deprecated in Python 3.7;
  Python 3.7 requires threads to build: `bpo-31370
  <https://bugs.python.org/issue31370>`_.

Python 3.8
----------

Python 3.8 removed 1 module:

  * ``macpath``: deprecated in Python 3.7, Mac OS 9 is not longer used.

Python 3.7
----------

Python 3.7 removed 1 module:

* ``fpectl``: it was never enabled by default, never worked correctly on
  x86-64, and it changed the Python ABI in ways that caused unexpected
  breakage of C extensions
  (`bpo-29137 <https://bugs.python.org/issue29137>`_).

Python 3.6
----------

Python 3.6 removed 6 modules:

* ``CDIO``, ``CDROM``, ``DLFCN``, ``IN``, ``STROPTS``, ``TYPES``:
  undocumented, they had been available in the platform specific
  ``Lib/plat-*/`` directories, but were chronically out of date,
  inconsistently available across platforms, and unmaintained.

Python 3.0
==========

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
