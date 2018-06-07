.. _python_packaging:

++++++++++++++++
Python Packaging
++++++++++++++++


Python packaging
================

* `Python Packaging User Guide <https://packaging.python.org/>`_
  (`URL on readthedocs.io
  <http://python-packaging-user-guide.readthedocs.org/>`_)
* `Install pip
  <http://www.pip-installer.org/en/latest/installing.html>`_
* `pip documentation
  <http://www.pip-installer.org/>`_
* `Python Wheels
  <http://pythonwheels.com/>`_
* https://hynek.me/articles/conditional-python-dependencies/


.. _py-windows:

Compile Python extensions on Windows
====================================

* Install Windows SDK
* Run "Windows SDK Command Prompt"
* Type::

    setenv /x64 /release
    set MSSDK=1
    set DISTUTILS_USE_SDK=1

See also :ref:`Windows <windows>`.


Build a Python Wheel package on Windows
=======================================

For Python 2.7, you need: `Download Visual C++ Compiler for Python 2.7
<https://www.microsoft.com/en-us/download/details.aspx?id=44266>`_.

Steps:

* `Install pip
  <http://www.pip-installer.org/en/latest/installing.html>`_
* Install wheel using pip::

    \python27\python.exe -m pip install wheel

* Run "Windows SDK Command Prompt"
* Setup the environment to build code in 64-bit mode (replace ``/x64`` with
  ``/x86`` for 32bit)::

    setenv /x64 /release
    set MSSDK=1
    set DISTUTILS_USE_SDK=1

* Go to your project
* Cleanup the project (is it really needed?)::

    del build\*
    del dist\*

* Build the wheel and upload it::

    \python27\python.exe setup.py bdist_wheel upload

Notes:

* To build a 32-bit wheel, you need 32-bit Python and configure the SDK using
  ``/x86``.
* Python 2.7 requires the Windows SDK v7.0 because Python 2.7 is built using
  Visual Studio 2008 (MSVCR90). Python 3.3 is built using Visual Studio 2010.
* It looks like Python 3.3 doesn't need ``MSSDK`` and ``DISTUTILS_USE_SDK``
  environment variables anymore.

See also :ref:`Windows <windows>`.


Python environment markers
==========================

https://wiki.openstack.org/wiki/Python3#Environment_markers

pip supports environment markers in requirements since pip 6.0, example of
requirement::

    six
    futures; python_version < '3.2'

pip uses ";" (colon) separator but requires "; " (colon, space) if the
requirement uses an URL. A space is added for readability (spaces are ignored).

Environment markers in extra requirements of setup.cfg::

    [extras]
    test =
        six
        futures :python_version < '3.2'

The separator is the ":" (colon), space is only used for readability (spaces
are ignored).

Environment markers in extra requirements of setup.py::

    expected_requirements = {
        "test:python_version < '3.2'": ['futures'],
        "test": ['six']
    }


pip issues
==========

* Upgrading pip3 replaces /usr/bin/pip with the Python 3 pip
* Once, I got two dist-info directories for pip
  (``ls /usr/lib*/python3.4/site-packages/pip-*.dist-info -d``) which broke
  ``python3 -m venv``: ``ensurepip`` was unable to find the system pip and
  Fedora doesn't include bundled wheel packages of ``ensurepip``
  in the ``python3-libs`` package
* With pip 7.0 and newer, ``pip3 install Routes; pip2 install Routes`` installs
  the Python 3 version of Routes on Python 2. pip3 creates a wheel package
  using 2to3 but Routes 2.1 announces universal wheel support which is wrong.
* Wheel caching doesn't work on pip 7.0, 7.0.1 and 7.0.2. It was fixed in pip
  7.0.3.


ensurepip
=========

* Debian doesn't provide ensurepip:
  https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=732703

  - Random workaround: https://gist.github.com/uranusjr/d03a49767c7c307be5ed

* Fedora, random links:

  - https://github.com/fedora-python/rewheel/issues/2
  - https://github.com/fedora-python/rewheel/blob/master/python2-ensurepip-rewheel.patch
