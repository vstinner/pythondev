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

