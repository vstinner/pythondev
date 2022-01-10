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

* Remove again "U" mode of open()
* Hide static types from the limited C API: https://bugs.python.org/issue40601

Debug ref leak: play with GC
============================

gc.get_referrers().

Common referrers of a type:

* globals(): current namespace
* module.__dict__
* type.__dict__
* type methods: C function with a reference to the type instance
* type.__mro__

Example with ``_multibytecodec.MultibyteCodec`` type::

    import _codecs_jp
    codec = _codecs_jp.getcodec('cp932')
    t = type(codec)

    >>> import gc
    >>> refs=gc.get_referrers(t)
    >>> refs[0]
    {'__name__': '__main__', '__doc__': None, ...
    >>> sorted(refs[0].keys())
    ['__builtins__', ..., '_codecs_jp', 'codec', 'encodings', 'gc', 'refs', 't']

    # "t" variable sounds like the current namespace
    >>> refs[0] is globals()
    True

    >>> refs[1]
    <module '_multibytecodec' from '/home/vstinner/python/master/build/lib.linux-x86_64-3.10-pydebug/_multibytecodec.cpython-310d-x86_64-linux-gnu.so'>
    >>> import _multibytecodec
    >>> refs[1] is _multibytecodec
    True

    >>> refs[2]
    <method 'encode' of '_multibytecodec.MultibyteCodec' objects>
    >>> refs[2] is t.encode
    True

    >>> refs[3]
    <method 'decode' of '_multibytecodec.MultibyteCodec' objects>
    >>> refs[3] is t.decode
    True

    >>> refs[4]
    (<class '_multibytecodec.MultibyteCodec'>, <class 'object'>)
    >>> refs[4] is t.__mro__
    True

    >>> refs[5]
    <slot wrapper '__getattribute__' of '_multibytecodec.MultibyteCodec' objects>
    >>> refs[5] is t.__getattribute__
    True

There are 6 objects which have a reference to ``t```:

* ``globals()`` namespace
* ``_multibytecodec``: in the module state (see the C implementation)
* ``t.encode``, ``t.decode`` and ``t.__getattribute__`` methods
* ``t.__mro__`` tuple

Bug only reproduced on Windows
==============================

* flake8: https://bugs.python.org/issue44184
* subinterpreter crash: https://bugs.python.org/issue46070
