++++++++++++++++++++++++++++++++++++
CPython implementation optimizations
++++++++++++++++++++++++++++++++++++

Singletons
==========

* Integers in range [-5; 256]
* Empty string
* Single Latin-1 letter

IO
==

* Efficient buffering: FileIO.read() and FileIO.readall()
* HTTP and socket buffering


.. _free-lists:

Free lists
==========

When a Python object is destroyed, its type can decided to keep the memory
alive to optimize the allocation of future objects. Bultin types using a
free list: see ``clear_freelists()`` in ``Modules/gcmodule.c``.

Python 3.8 types using a free list:

* Common types:

  * dict: PyDictObject
  * float: PyFloatObject
  * list: PyListObject
  * set: PySetObject
  * str: PyUnicodeObject
  * tuple: PyTupleObject

* Other types:

  * async generator value: _PyAsyncGenWrappedValue
  * builtin function: PyCFunctionObject
  * contextvars.Context: PyContext
  * frame: PyFrameObject
  * method: PyMethodObject

Python 2.7 types using a free list:

* builtin function: PyCFunctionObject
* float: PyFloatObject
* frame: PyFrameObject
* method: PyMethodObject
* int (but not long): PyIntObject
* tuple: PyTupleObject
* unicode: PyUnicodeObject


Others
======

* peephole

  - x in {1, 2, 3} => frozenset (constant)

* Overalllocation

  - list
  - bytearray?
  - PyUnicodeWriter

* Free list
* method cache
* stringlib

  - process long per long, instead of byte per byte
  - use goto

ceval.c
=======

* computed goto: label + goto
* fast locals: f_localsplus of a frame

Unicode
=======

* PEP 393: efficient storage for ASCII
* ASCII strings only require to copy N bytes to copy N characters:
  2 or 4 times faster than applications using UTF-16 or UCS-4
* findchar: use memchr(), even for UCS-2 and UCS-4

dict
====

* specialized for int key
* specialized for str key
* hash(str)

list
====

* timsort

implemented in C
================

* decimal of Python 3.3 is 120x faster than the Python implementation of
  Python 3.2

