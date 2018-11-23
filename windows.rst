.. _windows:

++++++++++++++++++++++++++
Compile CPython on Windows
++++++++++++++++++++++++++

http://bugs.python.org/issue30350


People
======

People who understands these things.

* Steve Dower: employed by Microsoft, he is the maintainer of the Windows
  installer for 2.7, 3.6, 3.7 and master branches
* Zachary Ware
* Jeremy Kloth knows the ``PC\VS9.0\`` directory of Python 2.7!


Build a Windows VM
==================

* Windows 10 or newer is recommended. Get a "multi-version" of Windows 10
  (no N, KN or VL variant) and use a "Pro - Retail" product key.
* At least 60 GB of disk space is needed: Windows needs 15-20 GB,
  Visual Studio needs 10 GB. Having at least 60 GB is recommended to be
  able to compile multiple Python versions, install other tools, upgrade
  Windows, etc.


Python and Visual Studio version matrix
=======================================

For Python 3.7 and later, VS 2017 is recommended (Community Edition is plenty),
minimum installer options:

* Workload: only [x] "Desktop development with C++"
* Language pack: [x] "English"

===================  =======================
Python version       Visual Studio
===================  =======================
Python 2.7           VS 2008 **and** VS 2010
Python 3.4           VS 2010
Python 3.5 and 3.6   VS 2015 (or newer)
Python 3.7           VS 2017
Python 3.8 (master)  VS 2017
===================  =======================

python.exe binaries delivered by python.org:

* Python 2.7.x (64-bit): [MSC v.1500 64 bit (AMD64)] on win32 -- VS 2008
* Python 3.4.x (64-bit): [MSC v.1600 64 bit (AMD64)] on win32 -- VS 2010
* Python 3.5.x (64-bit): [MSC v.1900 64 bit (AMD64)] on win32 -- VS 2015
* Python 3.6.x (64-bit): [MSC v.1900 64 bit (AMD64)] on win32 -- VS 2015
* Python 3.7.x (64-bit): [MSC v.1914 64 bit (AMD64)] on win32 -- VS 2017


Dependencies
============

Python master needs binary dependencies from
`github.com/python/cpython-bin-deps
<https://github.com/python/cpython-bin-deps>`_ and source dependencies
from `github.com/python/cpython-source-deps
<https://github.com/python/cpython-source-deps>`_.
``PCbuild\get_externals.bat``, which is called automatically by
``PCbuild\build.bat``, will take care of fetching these for you if you have any
of Git, Python, NuGet, or PowerShell available.

See ``PCbuild\get_externals.bat`` to learn what to put where if you aren't
using ``PCbuild\build.bat``.


Compile the master branch
=========================

To build the Python interpreter and all extension modules, including the ssl
extension:

Requirements:

* Visual Studio 2015 or newer (VS 2017 recommended)
* CPython source code: get it using Git, or download a ZIP on GitHub.com

Compile 64-bit Debug Python in the command line::

   PCBuild\build.bat -p x64 -d

Compile Python in the IDE: open the ``PCbuild\pcbuild.sln`` solution in Visual
Studio.

See also: ``PCbuild\readme.txt``.


Compile CPython 2.7
===================

Python 2.7 is stuck forever on Visual Studio 2008 to not break the ABI, to keep
the backward compatibility with all built extensions on the Python cheeseshop
(PyPI).  Obtaining VS 2008 is not nearly as simple or straightforward as it
used to be and Python 2.7 is rapidly approaching the end of its support period.
If you don't absolutely have to, we recommend not bothering to set things up to
build 2.7!


Compile CPython 2.7 on Windows using Visual Studio 2008 and 2010
----------------------------------------------------------------

While Visual Studio 2008 alone is enough to build a full Python 2.7 binary with
all standard extension modules, the standard method used to build 2.7 now
requires installing both Visual Studio 2008 **and** Visual Studio 2010.

Requirements:

* MSDN account to get Visual Studio 2008. Maybe it's possible to build Python
  using the Express edition of VS 2008 and 2010, but in 2017, it became
  difficult to get VS 2008 and 2010 Express.
* Windows 10 or newer is recommended, even if Python 2.7 is supposed to support
  Windows XP!
* Visual Studio 2008 Professional. Visual Studio 2008 Express works too, but
  doesn't provide a 64-bit compiler.
* Visual Studio 2010 Professional. Maybe a lighter flavor works, I didn't try.

Compile 64-bit Debug Python in the command line::

   PCBuild\build.bat -p x64 -d

Compile Python in the IDE: open the ``PCbuild\pcbuild.sln`` solution in Visual
Studio.

See also: ``PCbuild\readme.txt``.


Compile CPython 2.7 on Windows using only Visual Studio 2008
------------------------------------------------------------

Similar to the previous section, but don't install Visual Studio 2010: only
install Visual Studio 2008.

Compile 64-bit Debug Python in the command line::

   PC\VS9.0\build.bat -p x64 -d -e

Compile Python in the IDE: open the ``PC\VS9.0\pcbuild.sln`` solution in Visual
Studio.

See also: ``PC\VS9.0\readme.txt``.

Note that this configuration is not well tested.  Everything *should* work, but
if it does not, please feel free to submit a patch!  Also, if you use both
methods and notice significant differences between them, we'd like to hear
about those as well.


Windows Subsystem for Linux: WSL
================================

Ubuntu running on Windows 10 using a thin layer to emulate the Linux kernel on
top of the Windows kernel.
