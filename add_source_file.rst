+++++++++++++++++
Add a source file
+++++++++++++++++

Add a new C file
================

To add a C file (``.c``) or an header file (``.h``), you have to:

* Create ``Python/config.c``
* Add it to ``Makefile.pre.in``: in PYTHON_OBJS for example
* Add it to ``PCbuild/pythoncore.vcxproj``
* Add it to ``PCbuild/pythoncore.vcxproj.filters``

Add a new C extension
=====================

* Update setup.py
* Update Modules/Setup
