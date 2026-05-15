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
* Mapping: dict, frozendict
* Set: frozenset, set

Singletons:

* None, Ellipsis (``...``), False (``bool(0)``), True (``bool(1)``)
* Small integers: [-5; 1024], or [-5; 256] on Python 3.14 and older
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

Install Python dependencies in 32-bit::

    sudo dnf install glibc-devel.i686 libatomic.i686 bzip2-devel.i686 libffi-devel.i686 libuuid-devel.i686 ncurses-devel.i686 openssl-devel.i686 readline-devel.i686 xz-devel.i686 zlib-ng-compat-devel.i686

Build Python::

    ./configure CFLAGS="-m32" LDFLAGS="-m32"
    sed -i -e 's!#define PY_HAVE_PERF_TRAMPOLINE 1!#undef PY_HAVE_PERF_TRAMPOLINE!g' pyconfig.h
    make

I have to disable ``PY_HAVE_PERF_TRAMPOLINE`` to workaround a build issue.


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

Emscripten
==========

Documentation: https://devguide.python.org/getting-started/setup-building/#emscripten

Install Emscripten::

    cd ~/dev/
    git clone https://github.com/emscripten-core/emsdk
    ./emsdk/emsdk install 4.0.12
    ./emsdk/emsdk activate 4.0.12

Build Python (commands based on ``.github/workflows/reusable-emscripten.yml``)::

    cd ~/python/main

    # Configure build Python
    python3 Platforms/emscripten configure-build-python -- --config-cache --with-pydebug
    # Make build Python
    python3 Platforms/emscripten make-build-python

    # Make dependencies
    python3 Platforms/emscripten make-dependencies
    # Configure host Python
    source ~/dev/emsdk/emsdk_env.sh
    python3 Platforms/emscripten configure-host --host-runner node -- --config-cache
    # Make host Python
    python3 Platforms/emscripten make-host

Run Python with a script::

    python3 Platforms/emscripten run script.py

Run the test suite::

    python3 Platforms/emscripten run --test

Free Threading internals
========================

* PEPs:

  * PEP 683 "Immortal Objects, Using a Fixed Refcount"
  * PEP 703 "Making the Global Interpreter Lock Optional in CPython" design document
  * PEP 779 "Criteria for supported status for free-threaded Python"
  * PEP 803: “abi3t”: Stable ABI for Free-Threaded Builds

* Quiescent-State Based Reclamation (QSBR)

  * https://github.com/python/cpython/blob/main/InternalDocs/qsbr.md
  * https://github.com/python/cpython/commit/113de8545ffe74a4a1dddb9351fa1cbd3562b621
  * ``_PyObject_GC_SET_SHARED(obj)`` sets ``_PyGC_BITS_SHARED`` bit of
    ``obj->ob_gc_bits`` (``uint8_t``)
  * setobject.c ``ensure_shared_on_read()`` comment::

        // The first time we access a set from a non-owning thread we mark it
        // as shared. This ensures that a concurrent resize operation will
        // delay freeing the old entries using QSBR, which is necessary
        // to safely allow concurrent reads without locking...

* ``list`` uses QSBR with ``_PyListArray`` type

  * ``_PyListArray``::

        typedef struct {
            Py_ssize_t allocated;
            PyObject *ob_item[];
        } _PyListArray;

  * ``_Py_CONTAINER_OF()`` gets ``_PyListArray`` from ``PyListObject.ob_item``

* ``set`` uses QSBR: ``set_table_resize()`` delays ``PyMem_Free(oldtable)``
  using ``_PyMem_FreeDelayed()``.

* ``dict`` uses QSBR for lock-less lookup

  * ``PyDict_GetItemRef()`` calls ``_Py_dict_lookup_threadsafe()``
  * ``PyDict_SetItem()`` calls ``insertdict()``
  * ``PyDict_SetItem()`` calls ``insertion_resize()`` if the ``dict`` needs to
    grow. Use ``_PyMem_FreeDelayed()`` on old keys and values if the dict
    is shared.
  * use QSBR (``_PyObject_GC_SET_SHARED()``)

* Deferred ref counting

  * ``PyUnstable_Object_EnableDeferredRefcount(obj)`` sets ``_PyGC_BITS_DEFERRED`` bit of ``obj->ob_gc_bits``
  * ``_PyObject_HasDeferredRefcount()``
  * Only types with ``Py_TPFLAGS_HAVE_GC`` flag.
  * Biased reference counting (BRC) inter-thread queue: ``Python/brc.c``
  * ``PyInterpreterState.brc`` state

* PyMutex: use a single byte

  * ``Include/cpython/pylock.h`` defines ``PyMutex``
  * Parking lot
  * WebKit WTF Lock

    * https://webkit.org/blog/6161/locking-in-webkit/
    * https://github.com/WebKit/WebKit/blob/main/Source/WTF/wtf/Lock.h

* Critical section

  * Py_BEGIN_CRITICAL_SECTION()/Py_END_CRITICAL_SECTION()
  * Py_BEGIN_CRITICAL_SECTION2()/Py_END_CRITICAL_SECTION2()
  * Use ``PyThreadState.critical_section`` tagged pointer
  * ``_Py_CRITICAL_SECTION_INACTIVE``
  * ``_Py_CRITICAL_SECTION_TWO_MUTEXES``
  * ``_Py_CRITICAL_SECTION_MASK``
  * Use ``PyObject.ob_mutex`` (PyMutex)

* Atomic operations: ``Include/cpython/pyatomic.h`` (GCC/Clang, MSVC, std)

  * gcc: use GCC built-in functions such as ``__atomic_load_n()``
  * msc: use MSVC intrinsics such as ``_InterlockedCompareExchange()``
  * std: use C11 or C++11 atomics such as ``atomic_load()``

* Ref counting

  * PyObject has two members::

        uint32_t ob_ref_local;      // local reference count
        Py_ssize_t ob_ref_shared;   // shared (atomic) reference count

  * ``PyObject.ob_tid`` sets using ``_Py_ThreadId()``
  * ``_Py_UNOWNED_TID`` special value for ``ob_tid``
  * ``_Py_IsOwnedByCurrentThread()``
  * ``PyUnstable_Object_IsUniquelyReferenced()``
  * ``PyUnstable_Object_IsUniqueReferencedTemporary()``
  * ``Py_SET_REFCNT()``
  * ``_Py_TryXGetRef()``

* Immortal objects: PEP 683.

  * Py_INCREF/Py_DECREF do nothing if ``_Py_IsImmortal(obj)`` is true.
  * ``PyUnstable_SetImmortal()``
  * Small integers
  * Singletons such as ``()``, True/False, None, empty string.

* Stop the world

  * _PyEval_StopTheWorldAll(), _PyEval_StartTheWorldAll()
  * _PyEval_StopTheWorld(), _PyEval_StartTheWorld()
  * Examples of operations which have to stop/start the world:

    * ``PyRefTracer_SetTracer()``
    * set ``__bases__`` or ``__abstractmethods__`` of a type
    * set ``__class__`` of an object
    * ``faulthandler.dump_traceback()``
    * ``gc.get_referents()``
    * ``PyOS_BeforeFork()``
    * ``_Py_ClearUnusedTLBC()``
    * ``_PyFunction_ClearVersion()``

* mimalloc black magic

  * ``_PyThreadStateImpl.mimalloc`` state
  * ``mi_heap_visit_blocks()``: visit all blocks in a heap
  * ``_mi_abandoned_pool_visit_blocks()``: visit blocks in the per-interpreter
    abandoned pool
  * ``Objects/mimalloc/``: C code
  * ``Include/internal/mimalloc/`` header files

* Thread-local bytecode (TLBC)
* Reenable the GIL if a C extension is not compatible with Free Threading

  * _PyEval_IsGILEnabled()
  * _PyEval_EnableGILTransient()
  * _PyEval_EnableGILPermanent()
  * _PyEval_DisableGIL()

* Garbage collector

  * Python/gc_free_threading.c

* ``_PyStackRef``

  * ``PyStackRef_FromPyObjectSteal()``
  * ``PyStackRef_IsNull()``
  * ``PyStackRef_DUP()``
  * Mostly limited to ``Python/ceval.c``
  * ``_PyCStackRef`` API::

        _PyCStackRef mro_ref;
        _PyThreadState_PushCStackRef(tstate, &mro_ref);
        mro_ref.ref = PyStackRef_FromPyObjectNew(mro);
        ...
        _PyThreadState_PopCStackRef(tstate, &mro_ref);

* Python Thread state

  * ``_PyThreadState_GET()``
  * ``_Py_thread_local PyThreadState *_Py_tss_tstate``
  * ``_Py_thread_local``: ``thread_local``, ``_Thread_local`` (C11),
    ``__declspec(thread)``, ``__thread`` (GCC).
  * ``_PyThreadState_GET()`` implemented as reading the ``_Py_thread_local``
    variable in the common case.
  * Function call for stdlib extension modules built with
    ``Py_BUILD_CORE_MODULE``

* Python C API

  * Extension module: ``{Py_mod_gil, Py_MOD_GIL_NOT_USED}`` slot
  * Critical section
  * https://py-free-threading.github.io/porting-extensions/

* Limited C API

  * WIP in Python 3.15
  * PEP 803: “abi3t”: Stable ABI for Free-Threaded Builds
  * Opaque PyObject
  * Early work to abstract access to PyObject: Py_REFCNT(), Py_SET_REFCNT(),
    Py_TYPE(), Py_SET_TYPE().
  * ``abi3t`` ABI tag

* Gilectomy

  * Challenge of ref counting: "buffered reference count"
  * Issues with obmalloc
  * GC challenge
  * ``_PyThreadState_GET()``: need for Thread Local Storage (TLS)

PyPy project status (December 2025)
===================================

Matti Picus `wrote in the numpy bug tracker
<https://github.com/numpy/numpy/issues/30416>`__:

    PyPy is no longer under active development, and has not released a
    Python3.12 version.

