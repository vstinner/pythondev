+++++++++++++++++++
Python Startup Time
+++++++++++++++++++

CPython startup is "slow": takes between 8 ms and 100 ms depending on the
Python version, the operating system, how many .pth files are installed, if
Python runs into a virtual environment, etc.


Raw benchmark
=============

Benchmark::

   python3 -m perf command -o python2.json -- python2 -c pass
   python3 -m perf command -o python3.json -- python3 -c pass
   python3 -m perf command -o python2_nosite.json -- python2 -S -c pass
   python3 -m perf command -o python3_nosite.json -- python3 -S -c pass

Result speed.python.org (July 2017), fatest to slowest:

* ``git --version``: 974 us +- 7 us
* ``perl -e ' '``: 1.18 ms +- 0.01 ms
* Python 2.7: 6.4 ms with site; 3.0 ms without site (-S)
* ``php -r ' '``: 8.57 ms +- 0.05 ms
* Python 3.7: 14.5 ms with site; 8.4 ms without site (-S)
* ``ruby -e ' '``: 32.8 ms +- 0.1 ms
* ``hg version``: 44.6 ms +- 0.2 ms

Reference: `benchmark run at July 2017
<https://mail.python.org/pipermail/python-dev/2017-July/148656.html>`__.


.. _importtime:

importtime
==========

To analyze the startup time of your application, Python 3.7 and newer have
a builtin profiler on import time: ``-X importtime`` option.

Truncated example::

   $ python3.7 -X importtime -c pass
   import time: self [us] | cumulative | imported package
   import time:       274 |        274 | zipimport
   (...)
   import time:       949 |       2055 | io
   import time:       453 |        453 |       _stat
   import time:       701 |       1154 |     stat
   import time:       595 |        595 |       genericpath
   import time:       886 |       1480 |     posixpath
   import time:      3005 |       3005 |     _collections_abc
   import time:      1922 |       7559 |   os
   (...)
   import time:      4325 |      22832 | site

An alternative is to set ``PYTHONPROFILEIMPORTTIME=1`` environment variable.

No surprise, ``site`` has the longest cumulative time. Disable ``site`` to
speedup Python :-) Example::

   $ python3.7 -X importtime -S -c pass
   import time: self [us] | cumulative | imported package
   import time:        88 |         88 | zipimport
   import time:       580 |        580 | _frozen_importlib_external
   import time:        66 |         66 |     _codecs
   import time:       498 |        564 |   codecs
   import time:       411 |        411 |   encodings.aliases
   import time:       678 |       1653 | encodings
   import time:       232 |        232 | encodings.utf_8
   import time:       155 |        155 | _signal
   import time:       341 |        341 | encodings.latin_1
   import time:        56 |         56 |     _abc
   import time:       273 |        329 |   abc
   import time:       298 |        626 | io

`tune <https://github.com/nschloe/tuna>`_ is a Python profile viewer which
accepts importtime logs as input, see `Nico Schlömer's comment on bpo-31415
<https://bugs.python.org/issue31415#msg320841>`_. Extract::

   python -X importprofile application.py 2>import.log
   tuna import.log

Example with ``python3.7 -X importtime -c pass``:

.. image:: images/importtime_tuna.png
   :alt: Screenshot on tuna rendering import time
   :align: right

Links:

* `How to speed up Python application startup time
  <https://dev.to/methane/how-to-speed-up-python-application-startup-time-nkf>`_
  (Jan, 2018) by INADA Naoki.
* `importtime-waterfall (GitHub project)
  <https://github.com/asottile/importtime-waterfall>`_:
  Generate waterfalls from ``-X importtime`` tracing.


Links
=====

* python-dev: `Python startup time
  <https://mail.python.org/pipermail/python-dev/2017-July/148656.html>`__ (July
  2017) by Victor Stinner
* LWN: `Reducing Python's startup time <https://lwn.net/Articles/730915/>`_
  (August 16, 2017) by Jake Edge.
