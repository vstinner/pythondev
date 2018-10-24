++++++++++++++++++++++++++++++
C hacks in CPython source code
++++++++++++++++++++++++++++++

Detect integer overflows
========================

Before memory allocation.

In overallocate::

    if (newlen <= (PY_SSIZE_T_MAX - newlen / 4))
        newlen += newlen / 4;


Avoid undefined behaviour
=========================

Issue #7406::

    -	x = a + b;
    +	/* casts in the line below avoid undefined behaviour on overflow */
    +	x = (long)((unsigned long)a + b);


Usage of goto
=============

Something like try/finally.


Optimisations
=============

Unicode.

stringlib
---------

 * fastsearch.h: Bloom filter


Computed goto
=============

Python/ceval.c


Python types
============

 * (size_t,) PY_SIZE_MAX
 * Py_ssize_t, PY_SSIZE_T_MAX
 * PY_LONG_LONG (#ifdef HAVE_LONG_LONG)

Type aliasing
=============

PyCompactUnicodeObject::

    typedef struct {
        PyASCIIObject _base;
        Py_ssize_t utf8_length;     /* Number of bytes in utf8, excluding the
                                     * terminating \0. */
        char *utf8;                 /* UTF-8 representation (null-terminated) */
        Py_ssize_t wstr_length;     /* Number of code points in wstr, possible
                                     * surrogates count as two code points. */
    } PyCompactUnicodeObject;

Macros
======

* Add assertions using "a,b" syntax. Ugly example::

   #define PyUnicode_READY(op)                     \
       (assert(PyUnicode_Check(op)),               \
        (PyUnicode_IS_READY(op) ?                  \
         0 : _PyUnicode_Ready((PyObject *)(op))))

* Py_SAFE_DOWNCAST
* Py_ARRAY_LENGTH(array): check at compile time if the argument is an array
* do { ... } while (0), ex: Py_DECREF()

Examples::

    #define Py_RETURN_TRUE return Py_INCREF(Py_True), Py_True
    #define PyBool_Check(x) (Py_TYPE(x) == &PyBool_Type)

Memory allocation
=================

* pymalloc
* :ref:`free list <free-lists>`
* overallocate

  - list: 12.5%
    new_allocated = (newsize >> 3) + (newsize < 9 ? 3 : 6);
  - string formatting: 25%
    newlen += newlen / 4;
  - depend on the performance of realloc(): fast on Linux, slow on Windows
    (older than Windows 7)

* Unicode: PyUnicodeWriter, PyAccu
* preallocated object: MemoryError instances

dict
====

* hash()
* hash vulnerability
