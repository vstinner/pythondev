.. _windows:

++++++++++++++++++++++++++
Compile CPython on Windows
++++++++++++++++++++++++++

http://bugs.python.org/issue30350

People
======

People who understands these things.

* Steve Dower: employed by Microsoft, he is the maintainer of the Windows
  installer for 2.7, 3.5, 3.6 and master branches
* Zachary Ware
* Jeremy Kloth knows the ``PC\VS9.0\`` directory of Python 2.7!


Build a Windows VM
==================

* Windows 10 or newer is recommanded. Get a "multi-version" of Windows 10
  (no N, KN or VL variant) and use a "Pro - Retail" product key.
* At least 60 GB of disk space is needed: Windows needs 15-20 GB,
  Visual Studio needs 10 GB. Having at least 60 GB is recommended to be
  able to compile multiple Python versions, install other tools, upgrade
  Windows, etc.

Python and Visual Studio version matrix
=======================================

For Python 3.7, the minimum is VS 2017 Community, minimum installer options:

* Workload: only [x] "Desktop development with C++"
* Language pack: [x] "English"

===================  =======================
Python version       Visual Studio
===================  =======================
Python 2.7           VS 2008 **and** VS 2010
Python 3.4           VS 2010
Python 3.5 and 3.6   VS 2015
Python 3.7 (master)  VS 2015 or VS 2017
===================  =======================

python.exe binaries delivered by python.org:

* Python 2.7.13 (64-bit): [MSC v.1500 64 bit (AMD64)] on win32 -- VS 2008
* Python 3.4.3 (64-bit): [MSC v.1600 64 bit (AMD64)] on win32 -- VS 2010
* Python 3.5.1 (64-bit): [MSC v.1900 64 bit (AMD64)] on win32 -- VS 2015
* Python 3.6.2rc2 (64-bit): [MSC v.1900 64 bit (AMD64)] on win32 -- VS 2015
* Python 3.7.0a1 (64-bit): [MSC v.1900 64 bit (AMD64)] on win32 -- VS 2015

Dependencies
============

* Python master needs binary dependencies from
  `github.com/python/cpython-bin-deps
  <https://github.com/python/cpython-bin-deps>`_ and source dependencies
  from `github.com/python/cpython-source-deps
  <https://github.com/python/cpython-source-deps>`_ using Git
* Python 2.7 needs dependencies from `svn.python.org/projects/external
  <http://svn.python.org/projects/external/>`_ using Subversion.

In 2016, Perl was need to build OpenSSL. But it's no more required.

See ``PCBuild/get_externals.bat``.


Compile the master branch
=========================

To build the Python ssl extension:

Requirements:

* Visual Studio 2015
* CPython source code: get it using Git, or download a ZIP on GitHub.com

Commands::

    PCbuild\build -p x64 -d -e

See also: ``PCbuild/readme.txt``.


Compile CPython 2.7
===================

Python 2.7 is stuck forever on Visual Studio 2008 to not break the ABI, to keep
the backward compatibility with all built extensions on the Python cheeseshop
(PyPI).

Compile CPython 2.7 on Windows using Visual Studio 2008 and 2010
----------------------------------------------------------------

While Visual Studio 2008 is enough to build a basic Python 2.7 binary without
OpenSSL nor Tkinter, installing Visual Studio 2008 **and** Visual Studio 2010
is recommended to get all dependencies including Tkinter.

Requirements:

* MSDN account to get Visual Studio 2008. Maybe it's possible to build Python
  using the Express edition of VS 2008 and 2010, but in 2017, it became
  difficult to get VS 2008 and 2010 Express.
* Windows 10 or newer is recommanded, even if Python 2.7 is supposed to support
  Windows XP!
* Visual Studio 2008 Professional. Visual Studio 2008 Express works too, but
  doesn't provide a 64-bit compiler.
* Visual Studio 2010 Professional. Maybe a lighter flavor works, I didn't try.
* TortoiseSVN to get ``svn.exe`` in PATH to download Python dependencies:
  don't forget to check the ``[x] command line tools`` checkbox in the
  installer

Compile Python in the command line:

* Open a Visual Studio 2010 Prompt
* In this prompt, run ``PCBuild\build.bat -e -d -p x64`` to build Python 2.7 in
  debug mode for 64-bit, and install dependencies like OpenSSL, Tcl and Tk
  sources.

Compile Python in the IDE: open the ``PCbuild\pcbuild.sln`` solution in Visual
Studio.

Compile CPython 2.7 on Windows using Visual Studio 2008
-------------------------------------------------------

Similar to the previous section, but don't install Visual Studio 2010: only
install Visual Studio 2008.

Without Visual Studio 2010, some features don't work, like Tkinter.

* Project file: PC\VS9.0\pcbuild.sln
* In this prompt, run ``VS\9.0\build.bat -e -d -p x64`` to build Python 2.7 in
  debug mode for 64-bit, and install dependencies like OpenSSL sources if
  needed


Windows Subsystem for Linux: WSL
================================

Ubuntu running on Windows 10 using a thin layer to emulate the Linux kernel on
top of the Windows kernel.
