+++++++++++++
Python builds
+++++++++++++

Release build
=============

Python is built using -O3.

LTO
---

Use ``gcc -flto``

Maybe also: ``-fuse-linker-plugin -ffat-lto-objects -flto-partition=none``.

PGO
---

* Build Python with ``gcc -fprofile-generate``
* Run the test suite: ``make run_profile_task`` uses ``PROFILE_TASK`` variable
  of Makefile. configure uses ``./python -m test --pgo`` by default.
  List of test used with ``--pgo``: see `libregrtest/pgo.py
  <https://github.com/python/cpython/blob/master/Lib/test/libregrtest/pgo.py>`.
* Rebuild Python with ``gcc -fprofile-use``

PGO + LTO
---------

Use PGO and add LTO flags.

Debug build
===========

* ``./configure --with-pydebug``
* Python built using ``-Og`` if available, or ``-O0`` otherwise.


Special builds
==============

`Read Misc/SpecialBuilds.txt
<https://github.com/python/cpython/blob/master/Misc/SpecialBuilds.txt>`_.
