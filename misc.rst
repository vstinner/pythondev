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
* https://bugs.python.org/issue42846

  * _WindowsConsoleIO
  * sys.stdout uses the cp932 encoding which is a CJK multibyte codec

Vectorcall
==========

* To implement a vectorcall function:

  * ``nargs = PyVectorcall_NARGS(nargs)`` gives you the number of positional
    arguments.
  * Positional arguments for function ``myfunc``::

        if (!_PyArg_CheckPositional("myfunc", nargs, 0, 0)) {
            return NULL;
        }

  * Keyword arguments::

        Py_ssize_t nkwargs = 0;
        if (kwnames != NULL) {
            nkwargs = PyTuple_GET_SIZE(kwnames);
        }

  * No keyword arguments for function ``myfunc``::

        if (!_PyArg_NoKwnames("myfunc", kwnames)) {
            return NULL;
        }

* ``PY_VECTORCALL_ARGUMENTS_OFFSET`` constant is added to ``nargs`` when
  calling a method. In this case, ``self`` is ``args[-1]``.

* Optimize calling an object: ``result = obj()``

  * Add ``vectorcallfunc vectorcall`` to the ``PyCFunctionObject`` structure
  * Add ``tp_vectorcall_offset  = offsetof(PyCFunctionObject, vectorcall)`` to the type
  * Add ``Py_TPFLAGS_HAVE_VECTORCALL`` to the type ``tp_flags``

* Optimize the type creation: ``obj = MyType()``

  * Add ``.tp_vectorcall = (vectorcallfunc)enumerate_vectorcall`` to the type
  * Keep ``.tp_new = enum_new`` in the type

* `PEP 590 -- Vectorcall: a fast calling protocol for CPython
  <https://www.python.org/dev/peps/pep-0590/>`_
* ``METH_FASTCALL`` calling convention

  * `FASTCALL microbenchmarks
    <https://vstinner.github.io/fastcall-issues.html>`__
    (Feb 25, 2017)
  * `FASTCALL microbenchmarks
    <https://vstinner.github.io/fastcall-microbenchmarks.html>`__
    (Feb 24, 2017)
  * `The start of the FASTCALL project
    <https://vstinner.github.io/start-fastcall-project.html>`_
    (Feb 16, 2017)

* Get ``vectorcall`` of a callable object: ``PyVectorcall_Function()``.
  Return ``NULL`` if the type has no ``Py_TPFLAGS_HAVE_VECTORCALL`` flag.
* Call a function in C:

  * ``PyObject_Vectorcall()``
  * ``PyObject_VectorcallDict()``
  * ``_PyObject_FastCall()``
  * ``PyObject_VectorcallMethod()``


Build Python in 32-bit on Fedora
================================

Install the libc in 32-bit::

    sudo dnf install glibc-devel.i686

Edit ``Modules/Setup.local`` to disable extensions which need 3rd libraries
(not available in 32-bit)::

    *disabled*
    _bz2
    _ctypes
    _curses
    _curses_panel
    _elementtree
    _lzma
    _uuid
    binascii
    pyexpat
    readline
    zlib

Build Python::

    ./configure CFLAGS="-m32" LDFLAGS="-m32"
    make


C global variables checker
==========================

``make check-c-globals`` runs ``Tools/c-analyzer/check-c-globals.py --format summary --traceback``.

New global variables can be ignored by modifying
``Tools/c-analyzer/cpython/ignored.tsv``.


Frozen modules
==============

* ``Python/frozen.c``
* ``Tools/build/freeze_modules.py``
* ``Makefile.pre.in``:

  * ``make regen-frozen``
  * ``FROZEN_FILES_IN``
  * ``FROZEN_FILES_OUT``

Old deepfreeze. No longer used in Python 3.13:

* ``PYTHON_FOR_FREEZE``
* ``DEEPFREEZE_C``
* ``DEEPFREEZE_DEPS``


Build Python in an Ubuntu container
===================================

Create an Ubuntu 22.04 container::

    podman run --rm --name ubuntu-dev --hostname ubuntu-dev --interactive --tty ubuntu:22.04

In the container::

    apt update && apt install --yes git make clang libssl-dev readline-dev
    git clone https://github.com/python/cpython --depth=1
    cd cpython
    ./configure --with-pydebug


make check-c-globals
====================

If the test fails, edit ``Tools/c-analyzer/cpython/ignored.tsv``.

See also ``MAX_SIZES`` in ``Tools/c-analyzer/cpython/_parser.py``.


LINK : fatal error LNK1104: cannot open file 'python313.lib'
============================================================

When testing a Python debug build on Windows, the library is called
python313_d.lib, not python313.lib.

Workaround::

    copy PCbuild\amd64\python313_d.lib python313.lib


Free Threading
==============

* https://docs.python.org/dev/howto/free-threading-extensions.html
* https://py-free-threading.github.io/
* https://hugovk.github.io/free-threaded-wheels/

Dashboard
=========

* https://github.com/orgs/python/dashboard

Alpine Linux
============

Install dependencies::

    apk add gcc make musl-dev git
