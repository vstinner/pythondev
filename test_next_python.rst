++++++++++++++++++++
Test the next Python
++++++++++++++++++++

To evolve and remain relevant, incompatible changes must happen in Python. The
problem is how to migrate existing code to the "next" Python with these
incompatible changes.

Deprecation warnings
====================

DeprecationWarning and PendingDeprecationWarning warnings are hidden by
default, to not bother users. Developers can use ``-Wd`` (``-Wdefault``)
command line option on Python which displays these warnings.

`Python Development Mode <https://docs.python.org/dev/library/devmode.html>`_.

What's New in Python 3.9: `You should check for DeprecationWarning in your code
<https://docs.python.org/dev/whatsnew/3.9.html#you-should-check-for-deprecationwarning-in-your-code>`_
section.

Fedora COPR
============

Test Rawhide (future Fedora 33) with Python 3.9 as the "system Python":
https://copr.fedorainfracloud.org/coprs/g/python/python3.9/

pythonci project
================

https://github.com/vstinner/pythonci

Projects having "Python nightly in their CI
===========================================

XXX

numpy?

Cython?
