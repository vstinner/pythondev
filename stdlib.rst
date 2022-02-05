+++++++++++++++++++++++
Python standard library
+++++++++++++++++++++++

Removed modules
===============

* Python 3.11

  * ``binhex``: deprecated in Python 3.9
  * ``asyncore``, ``asynchat``, ``smtplib`` were removed but then
    `the SC asked to add them back
    <https://github.com/python/steering-council/issues/86>`_

* Python 3.10

  * ``formatter``: deprecated in Python 3.4
  * ``parser``: deprecated in Python 3.9, removed related to PEP 617
    (PEG parser)

* Python 3.9

  * ``dummy_threading``, ``_dummy_thread``: deprecated in Python 3.7.
    Python 3.7 requires threads to build: `bpo-31370
    <https://bugs.python.org/issue31370>`_.

* Python 3.8

  * ``macpath``: deprecated in Python 3.7, Mac OS 9 is not longer used.

* Python 3.7

  * ``fpectl``: it was never enabled by default, never worked correctly on
    x86-64, and it changed the Python ABI in ways that caused unexpected
    breakage of C extensions
    (`bpo-29137 <https://bugs.python.org/issue29137>`_).

* Python 3.6

  * ``CDIO``, ``CDROM``, ``DLFCN``, ``IN``, ``STROPTS``, ``TYPES``:
    undocumented, they had been available in the platform specific
    ``Lib/plat-*/`` directories, but were chronically out of date,
    inconsistently available across platforms, and unmaintained.

* Python 3.0

  * ``bsddb3``
  * Many old modules were removed: see https://www.python.org/dev/peps/pep-3108/#modules-to-remove Examples:
  * ``md5``
  * ``mimetools``
  * ``posixfile``
  * ``rfc822``
