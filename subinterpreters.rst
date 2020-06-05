++++++++++++++++++++++
Python Subinterpreters
++++++++++++++++++++++

See also :ref:`Python Finalization <finalization>`.

* https://github.com/ericsnowcurrently/multi-core-python/
* `bpo-36476: Runtime finalization assumes all other threads have exited
  <https://bugs.python.org/issue36476>`_
* `bpo-1635741: Py_Finalize() doesn't clear all Python objects at exit
  <https://bugs.python.org/issue1635741>`_ created in 2007
* `LWN: Subinterpreters for Python <https://lwn.net/Articles/820424/>`_
  (May 13, 2020) By Jake Edge


TODO list for per-interpreter GIL
=================================

`Search for Subinterpreters issues at bugs.python.org
<https://bugs.python.org/issue?%40search_text=&ignore=file%3Acontent&title=&%40columns=title&id=&%40columns=id&stage=&creation=&creator=&activity=&%40columns=activity&%40sort=activity&actor=&nosy=&type=&components=35&versions=&dependencies=&assignee=&keywords=&priority=&status=1&%40columns=status&resolution=&nosy_count=&message_count=&%40group=&%40pagesize=50&%40startwith=0&%40sortdir=on&%40queryname=&%40old-queryname=&%40action=search>`_.

`Meta issue: per-interpreter GIL <https://bugs.python.org/issue40512>`_.
Issues:

* parser_init(): _PyArg_Parser
* Disble lzma, bz2

  * lzma: https://github.com/python/cpython/pull/19382
  * bz2: https://github.com/python/cpython/commit/5d38517aa1836542a5417b724c093bcb245f0f47 (this fix is not enough)

* Workaround: __bases__
* Free lists

  * float: DONE
  * slice: DONE
  * frame: DONE
  * list: DONE
  * async gen: DONE
  * context: DONE
  * dict: https://github.com/python/cpython/pull/20645

* _PyUnicode_FromId(): https://bugs.python.org/issue39465
* Unicode interned strings: https://github.com/python/cpython/pull/20085
* Singletons

  * None, True, False, Ellipsis: https://bugs.python.org/issue39511
  * bytes: empty string and single character singletons
  * str: empty string and single latin1 character singletons
  * empty frozenset singleton

* Type method cache
* Heap types

  * https://bugs.python.org/issue40077
  * https://bugs.python.org/issue40601

* pymalloc
* Workarounds

  * bpo-40533: Make PyObject.ob_refcnt atomic in subinterpreters: https://github.com/python/cpython/pull/19958
  * _dictkeysobject.dk_refcnt made _Atomic
  * Disable GC: https://github.com/python/cpython/commit/d8135e913ab7c694db247c86d0a84c450c32d86e

* tstate: get/set TSS: https://bugs.python.org/issue40522
* Per-interpreter GIL: https://bugs.python.org/issue40512

Enhancements:

* Debug: ensure that an object is not accessed by two interpreters: https://bugs.python.org/issue33607
* _xxsubinterpreters.run_string(): release the GIL: https://github.com/python/cpython/commit/fb2c7c4afbab0514352ab0246b0c0cc85d1bba53
* subprocess: close_fds=False, posix_spawn() is safe in subinterpreters

Limitations
===========

Not supported in subinterpreter:

* os.fork(): it may be possible to fix it.
* signal.signal()
* static types

Current workarounds:

* Disable GC
* Disable many caches like frame free list
* etc.

Heap allocated types
====================

Modules/_randommodule.c::

    PyObject *Random_Type = PyType_FromSpec(&Random_Type_spec);

Example::

    $ ./python
    Python 3.9.0a6+ (heads/frame_getback:6bde4d96c7, Apr 29 2020, 03:02:24)
    >>> import _random as mod1
    >>> import sys; del sys.modules['_random']
    >>> import _random as mod2
    >>> mod2.Random is mod1.Random
    False
    >>> mod1.Random.x=1
    >>> mod2.Random.x
    AttributeError: type object '_random.Random' has no attribute 'x'


Multiphase initialization (PEP 489)
===================================

See _abc module.

* PyInit__abc() calls PyModuleDef_Init
* PyModuleDef has slots, at least Py_mod_exec.


Get module
==========

Create module::

    _PyModule_CreateInitialized(struct PyModuleDef* module, int module_api_version)

Members:

* PyModuleDef.m_base.m_index: int
* PyInterpreterState.modules_by_index: list

PyModuleDef_Init() assigns an unique index to a PyModuleDef. It is called
by _PyModule_CreateInitialized().

_PyImport_FixupExtensionObject() and import_find_extension() call::

    _PyState_AddModule(PyThreadState *tstate, PyObject* module, struct PyModuleDef* def)

Modules with slots must not be added to PyInterpreterState.modules_by_index.

Module State
============

Find a module::

    m = PyState_FindModule(&posixmodule);

From a module::

    void *state = PyModule_GetState(module);
