++++++++++++++++++++++++
Python garbage collector
++++++++++++++++++++++++

Reference documentation by Pablo Galindo Salgado: https://devguide.python.org/garbage_collector/

Py_TPFLAGS_HAVE_GC
==================

The garbage collector does not track objects if their type don't have the
``Py_TPFLAGS_HAVE_GC`` flag.

If a type has the ``Py_TPFLAGS_HAVE_GC`` flag, when an object is allocated, a
``PyGC_Head`` structure is allocated at the beginning of the memory block, but
``PyObject*`` points just after this structure. The ``_Py_AS_GC(obj)`` macro
gets a ``PyGC_Head*`` pointer from a ``PyObject*`` pointer using pointer
arithmetic: ``((PyGC_Head *)(obj) - 1)``.

See also the ``PyObject_IS_GC()`` function which uses the
``PyTypeObject.tp_is_gc`` slot. An object has the ``PyGC_Head`` header if
``PyObject_IS_GC()`` returns true. For a type, the ``tp_is_gc`` slot function
checks if the type is a heap type (has the ``Py_TPFLAGS_HEAPTYPE`` flag):
static types don't have the ``PyGC_Head`` header.

Implement the GC protocol in a type
===================================

* Set ``Py_TPFLAGS_HAVE_GC`` flag
* Define a ``tp_traverse`` function.
* Define a ``tp_clear`` function.
* For heap types, the traverse function **must** visit the type, and the
  dealloc function must call ``Py_DECREF(Py_TYPE(self))``. Otherwise, the GC is
  unable to collect the type once the last instance is deleted (and the type
  was already deleted).
* If ``PyObject_New()`` is used to allocate an object, replace it with
  ``PyObject_GC_New()``.
* If the dealloc function calls ``PyObject_Free()``: replace it
  with ``type->tp_free(self)``.
* The constructor should call ``PyObject_GC_Track(self)`` (or not, it depends
  how the object was created) and the deallocator should call
  ``PyObject_GC_UnTrack(self)``.

Example of dealloc function::

    static void
    abc_data_dealloc(_abc_data *self)
    {
        PyTypeObject *tp = Py_TYPE(self);
        // ... release resources ...
        tp->tp_free(self);
    #if PY_VERSION_HEX >= 0x03080000
        Py_DECREF(tp);
    #endif
    }

On Python 3.7 and older, ``Py_DECREF(tp);`` is not needed: it changed in Python
3.8, see `bpo-35810 <https://bugs.python.org/issue35810>`_.


gc.collect()
============

CPython uses 3 garbage collector generations. Default thresholds
(``gc.get_threshold()``):

* Generation 0 (youngest objects): 700
* Generation 1: 10
* Generation 2 (oldest objects): 10

The main function of the GC is ``gc_collect_main()`` in ``Modules/gcmodule.c``:
it collects objects of a generation. The function relies on the ``PyGC_Head``
structure. Simplified algoritm:

* Merge younger generations with one we are currently collecting.
* Deduce unreachable.

  * Copy object reference count into PyGC_Head.
  * Traverse objects using visit_decref(); ignore objects which are not part of
    the currently collected GC collection.
  * Move objects with a reference count (PyGC_Head) of 0 to an "unreachable"
    list.

* Move reachable objects to next generation.
* Clear weak references and invoke callbacks as necessary.
* Call ``tp_finalize`` on objects which have one.
* Handle any objects that may have resurrected.
* Call ``tp_clear`` on unreachable objects.
* If the DEBUG_SAVEALL flags is set, move uncollectable garbage (cycles with
  ``tp_del`` slots, and stuff reachable only from such cycles) to the
  ``gc.garbage`` list.

The exact implementation is more complicated.

.. _gc-bugs:

GC bugs
=======

See also the :ref:`Python finalization <finalization>`.

* `bpo-42972: Heap types (PyType_FromSpec) must fully implement the GC protocol
  <https://bugs.python.org/issue42972>`_

* `bpo-40217: The garbage collector doesn't take in account that objects of
  heap allocated types hold a strong reference to their type
  <https://bugs.python.org/issue40217>`_: Bug fixed in Python 3.9.

* `bpo-38006 <https://bugs.python.org/issue38006>`_: issue with weak references
  and types which don't implement tp_traverse.

  * GC fix for weak references:
    `commit <https://github.com/python/cpython/commit/bcda460baf25062ab68622b3f043f52b9db4d21d>`__
  * Remove a closuse in weakref.WeakValueDictionary:
    `commit <https://github.com/python/cpython/commit/a2af05a0d3f0da06b8d432f52efa3ecf29038532>`__
  * PyFunctionType.tp_clear:
    `removed
    <https://github.com/python/cpython/commit/ccaea525885e41c5f1e566bb68698847faaa82ca>`__
    temporarily, and then `added again
    <https://github.com/python/cpython/commit/b3612070b746f799901443b65725008bc035872b>`__
  * cffi type missing a tp_traverse function:
    `bug report <https://foss.heptapod.net/pypy/cffi/-/issues/416>`_
    (still open at 2021-09-24)

* `bpo-35810: Object Initialization does not incref Heap-allocated Types
  <https://bugs.python.org/issue35810>`_:
  `commit <https://github.com/python/cpython/commit/364f0b0f19cc3f0d5e63f571ec9163cf41c62958>`__
  ``PyObject_Init()`` now calls ``Py_INCREF(Py_TYPE(op))`` if the object type
  is a heap type. Traverse functions must now visit the type and dealloc
  functions must now call ``Py_DECREF()`` on the type.

Reference cycles
================

* C function (PyCFunctionObject): C function <=> module

  * PyCFunctionObject.m_module => module
  * module => module.__dict__
  * module.__dict__ => PyCFunctionObject

* PyTypeObject

  * type->tp_mro => type: the MRO tuple contains the type
