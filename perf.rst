.. _python-perf:

++++++++++++++++++
Python performance
++++++++++++++++++

Codespeed websites
==================

* `speed.python.org <https://speed.python.org/>`_: CPython benchmarks,
  run `performance <http://pyperformance.readthedocs.io/>`_
  and `(tobami's) codespeed <https://github.com/tobami/codespeed/>`_
* `speed.pypy.org <http://speed.pypy.org/>`_: PyPy benchmarks, run
  `PyPy benchmarks <https://bitbucket.org/pypy/benchmarks>`_
* `speed.pyston.org <http://speed.pyston.org/>`_: Pyston benchmarks,
  run `pyston-perf <https://github.com/dropbox/pyston-perf>`_

Projects
========

Python benchmarks:

* `performance <http://pyperformance.readthedocs.io/>`_
  (`GitHub project <https://github.com/python/performance>`__):
  Python benchmark suite
* `perf <http://perf.readthedocs.io/>`_
  (`GitHub project <https://github.com/vstinner/perf>`__):
  Python module to run, analyze and compare benchmarks
* `performance_results <https://github.com/vstinner/performance_results>`_:
  Results of the of performance benchmark suite
* `pymicrobench <https://github.com/vstinner/pymicrobench>`_: Collection
  of Python microbenchmarks written for CPython.
* `PyPy benchmarks <https://bitbucket.org/pypy/benchmarks>`_: PyPy benchmark
  suite
* `Codespeed (tobami's flavor) <https://github.com/tobami/codespeed/>`_:
  Django application to explose benchmark results. Pages: Homepage, Changes,
  Timeline, Compare.
* `pyston-perf <https://github.com/dropbox/pyston-perf>`_: Pyston benchmark
  suite

Other Python Benchmarks:

* `Numba benchmarks <http://numba.pydata.org/numba-benchmark/>`_
* `Cython Demos/benchmarks
  <https://github.com/cython/cython/tree/master/Demos/benchmarks>`_
* `pythran numpy-benchmarks
  <https://github.com/serge-sans-paille/numpy-benchmarks>`_

Old deprecated projects:

* `benchmarks <https://hg.python.org/benchmarks>`_:
  the old and deprecated Python benchmark suite

Mailing list
============

* `Python speed mailing list
  <https://mail.python.org/mailman/listinfo/speed>`_

Old Python benchmarks
=====================

The following benchmarks were removed from pyperformance:

* `bm_rietveld.py
  <https://hg.python.org/benchmarks/file/198c43ca2f5b/performance/bm_rietveld.py>`_:
  use Google AppEngine and Rietveld application which are not available on PyPI
* `bm_spitfire.py
  <https://hg.python.org/benchmarks/file/198c43ca2f5b/performance/bm_spitfire.py>`_:
  Spitfire project is not available on PyPI
* `bm_threading.py
  <https://github.com/python/performance/blob/d9e9b4b075f43f7c81e31062a398054703f5e00e/performance/benchmarks/bm_threading.py>`_
  (``threading_iterative_count``, ``threading_threaded_count``)
* `gcbench.py
  <https://hg.python.org/benchmarks/file/198c43ca2f5b/performance/gcbench.py>`_
* `pystone.py
  <https://hg.python.org/benchmarks/file/198c43ca2f5b/performance/pystone.py>`_
* `tuple_gc_hell.py
  <https://hg.python.org/benchmarks/file/198c43ca2f5b/performance/tuple_gc_hell.py>`_


Zero copy
=========

Python3::

    offset = 0
    view = memoryview(large_data)
    while True:
        chunk = view[offset:offset + 4096]
        offset += file.write(chunk)

This copy creates views on ``large_data`` without copying bytes, no bytes is
copied in memory.


