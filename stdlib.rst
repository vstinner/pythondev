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
----------

Python 3.0 removed 58 modules, related to `PEP 3108
<https://www.python.org/dev/peps/pep-3108/#modules-to-remove>`_:

* ``aepack``
* ``aetools``
* ``aetypes``
* ``al``
* ``autogil``
* ``bastion``
* ``bsddb``
* ``carbon``
* ``cd``
* ``colorpicker``
* ``commands``
* ``compiler``
* ``dbhash``
* ``dircache``
* ``dl``
* ``dummy_thread``
* ``easydialogs``
* ``fl``
* ``fm``
* ``fpectl``
* ``fpformat``
* ``framework``
* ``future_builtins``
* ``gensuitemodule``
* ``gl``
* ``hotshot``
* ``htmllib``
* ``ic``
* ``imageop``
* ``imgfile``
* ``imputil``
* ``jpeg``
* ``mac``
* ``macos``
* ``macosa``
* ``macostools``
* ``md5``
* ``mhlib``
* ``mimetools``
* ``mimewriter``
* ``mimify``
* ``miniaeframe``
* ``multifile``
* ``mutex``
* ``new``
* ``popen2``
* ``posixfile``
* ``restricted``
* ``rexec``
* ``rfc822``
* ``sgi``
* ``sgmllib``
* ``sha``
* ``someos``
* ``statvfs``
* ``sun``
* ``sunaudio``
* ``user``
