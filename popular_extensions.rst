+++++++++++++++++++++++++++++++++++++
Popular third party extension modules
+++++++++++++++++++++++++++++++++++++

To test C API changes in Python, it's useful to test a bunch of popular
extension modules to check if they still build.

Cython
======

The first important candidate is Cython, many projects use it:

* Cython
* lxml
* numpy (Cython + C API)
* pandas
* pyzmq (for Jupyter)
* scipy

Python C API
============

Use directly the C API:

* Mercurial
* Pillow
* cffi
* psycopg2
