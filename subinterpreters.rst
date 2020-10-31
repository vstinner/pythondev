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

DONE
====

* Fix crashes with daemon threads: https://vstinner.github.io/gil-bugfixes-daemon-threads-python39.html
* Per-interpreter free lists (bpo-40521):

  * float
  * slice
  * frame
  * list
  * asynchronous generator
  * context
  * dict
  * tuple
  * MemoryError

* Per-interpreter singletons (bpo-40521):

  * small integer ([-5; 256] range) (bpo-38858)
  * empty bytes string singleton
  * empty Unicode string singleton
  * empty tuple singleton
  * single byte character (``b'\x00'`` to ``b'\xFF'``)
  * single Unicode character (U+0000-U+00FF range)
  * Note: the empty frozenset singleton has been removed.

* Per-interpreter slice cache (bpo-40521).
* Per-interpreter pending calls (bpo-39984).
* Per-interpreter states:

  * warnings (bpo-36737 and bpo-40521)
  * gc (bpo-36854)
  * parser (bpo-36876)

* At 2020-10-06, 76 extensions on a total of 118 use the new multi-phase
  initialization API: **64% (76/118)**. The remaining 42 extensions using the
  old API should be updated (bpo-1635741).


Milestones
==========

* May 2020: `PoC: Subinterpreters 4x faster than sequential execution or
  threads on CPU-bound workaround
  <https://mail.python.org/archives/list/python-dev@python.org/thread/S5GZZCEREZLA2PEMTVFBCDM52H4JSENR/#RIK75U3ROEHWZL4VENQSQECB4F4GDELV>`_

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

* `Free lists <https://bugs.python.org/issue40521>`__:
* _PyUnicode_FromId(): https://bugs.python.org/issue39465
* Unicode interned strings: https://github.com/python/cpython/pull/20085
* None, True, False, Ellipsis singletons: https://bugs.python.org/issue39511
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

Convert static type to heap type
================================

See: `Convert static types to heap types: use PyType_FromSpec()
<https://bugs.python.org/issue40077>`_.

Example: Modules/_abcmodule.c.

Decrement the type reference counter in the dealloc function. Something like::

    static void
    my_dealloc(my_data *self)
    {
        (...)
        PyTypeObject *tp = Py_TYPE(self);
        tp->tp_free(self);
        Py_DECREF(tp);
    }

Add a module state to a module
==============================

Example: Modules/_abcmodule.c.

Add traverse, clear and free functions to the module to better collaborate with
the garbage collector. Otherwise, the GC fails to break reference cycles.

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
