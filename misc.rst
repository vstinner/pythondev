++++++++++
Misc notes
++++++++++

* https://cpython-pulls.herokuapp.com/

datetime strptime
=================

Documentation: https://docs.python.org/dev/library/datetime.html#strftime-and-strptime-behavior

Code::

    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S %z')

year-month-day hour:minute:second timezone::

    %Y-%m-%d %H:%M:%S %z


Python builtin types
====================

Builtin scalar types:

* bool, int, float, complex, bytes, str

Builtin container types:

* Sequence: tuple, list
* Mapping: dict
* Set: frozenset, set

Singletons:

* None, Ellipsis (``...``), False (``bool(0)``), True (``bool(1)``)
* Small integers: [-5; 256]
* Empty bytes and Unicode strings: ``b''`` and ``''``
* Latin-1 single letter, examples: ``'\0'``, ``'a'``, ``'\xe9'``
* Empty tuple
* Empty frozenset: frozenset() (removed from Python 3.10)


Python developer mode
=====================

=> implementated in Python 3.7 as: "python3 -X dev" or PYTHONDEVMODE=1 !

https://mail.python.org/pipermail/python-ideas/2016-March/039314.html

Strict developer mode::

    PYTHONMALLOC=debug python3.6 -Werror -bb -X faulthandler script.py

Developer mode::

    PYTHONMALLOC=debug python3.6 -Wd -b -X faulthandler script.py

* Show ``DeprecationWarning`` and ``ResourceWarning warnings``: ``python -Wd``
* Show ``BytesWarning`` warning: ``python -b``
* Enable ``faulthandler`` to get a Python traceback on segfault and fatal
  errors: ``python -X faulthandler``
* Debug hooks on Python memory allocators: ``PYTHONMALLOC=debug``
* Enable Python assertions (assert) and set ``__debug__`` to ``True``: remove
  (or just ignore) -O or -OO command line arguments

See also ``PYTHONASYNCIODEBUG=1`` for asyncio.

pyupgrade
=========

https://github.com/asottile/pyupgrade

AST changes
===========

* `Removing ast.Param in Python 3.9 <https://bugs.python.org/issue39969>`__
  broke `chameleon <https://github.com/malthe/chameleon/issues/303>`__

Things to do in Python 3.10
===========================

* Convert Py_TYPE() to a static inline function:
  https://bugs.python.org/issue39573
* Modify C functions using Py_UNICODE to raise a DeprecationWarning:
  https://bugs.python.org/issue36346
* Remove again collections.Mapping
* Remove again "U" mode of open()
* Make "from __future__ import annoations" the default
  https://bugs.python.org/issue38605
* Hide static types from the limited C API: https://bugs.python.org/issue40601
