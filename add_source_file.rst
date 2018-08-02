+++++++++++++++++
Add a source file
+++++++++++++++++

To add a C file (``.c``) or an header file (``.h``), you have to:

* Create ``Python/config.c``
* Add it to ``Makefile.pre.in``: in PYTHON_OBJS for example
* Add it to ``PCbuild/pythoncore.vcxproj``
* Add it to ``PCbuild/pythoncore.vcxproj.filters``
