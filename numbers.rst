++++++++++++++
Python Numbers
++++++++++++++

Types
=====

* ``int``: integral number
* ``float``: floating point number, usually IEEE 754 (64 bits, base 2)
* ``complex``: complex number, implemented as two floats
* ``decimal.Decimal``: floating point number stored in base 10, arbitrary
  precision
* ``fractions.Fraction``: rational, numerator/denominator; automatically
  compute the greatest common divisor (GCD) to simplify the fraction

Number Tower
============

The `numbers module <https://docs.python.org/3/library/numbers.html>`_
specified by the `PEP 3141 -- A Type Hierarchy for Numbers
<https://www.python.org/dev/peps/pep-3141/>`_.

* numbers.Number: base class
* numbers.Complex: Add ``real``, ``imag``, ``conjugate()``
* numbers.Real: subclass of Complex; add many float operations.
* numbers.Rational: subclass of Real; add ``numerator`` and ``denominator``
  attributes
* numbers.Integral: subclass of Rational

int, float, complex methods and attributes:

* num.conjugate
* num.imag
* num.real

int and Fraction attributes:

* num.denominator
* num.numerator


Conversions in Python
=====================

* ``int(obj)`` accepts int, float, decimal.Decimal, fractions.Fraction, bytes, str,
  etc. Floats are rounded towards zero (ROUND_DOWN, ex: ``int(0.9) == 0`` and
  ``int(-0.9) == 0``).
* ``float(obj)`` accepts int, float, decimal.Decimal, fractions.Fraction, bytes, str,
  etc.

int
===

Examples::

    >>> (123).bit_length()
    7
    >>> sys.int_info
    sys.int_info(bits_per_digit=30,
                 sizeof_digit=4)

Serialization as bytes::

    >>> (123).to_bytes(4, 'little')
    b'{\x00\x00\x00'
    >>> int.from_bytes(b'{\x00\x00\x00', 'little')
    123

int(obj) calls ``PyNumber_Long()``. For float, it uses

Rounding:

* ``int(float)`` calls ``float.__trunc__()``, so rounds towards zero
  (ROUND_DOWN)

float
=====

Examples::

    >>> sys.float_info
    sys.float_info(max=1.7976931348623157e+308,
                   max_exp=1024,
                   max_10_exp=308,
                   min=2.2250738585072014e-308,
                   min_exp=-1021,
                   min_10_exp=-307,
                   dig=15,
                   mant_dig=53,
                   epsilon=2.220446049250313e-16,
                   radix=2,
                   rounds=1)
    >>> sys.float_repr_style
    'short'
    >>> (1.2).as_integer_ratio()
    (5404319552844595, 4503599627370496)

Formatting as hexadecimal (base 16)::

    >>> (1.1).hex()
    '0x1.199999999999ap+0'
    >>> float.fromhex('0x1.199999999999ap+0')
    1.1

Rouding:

* float.__trunc__(): Round towards zero (ROUND_DOWN)
* float.__round__(): Round to nearest with ties going to nearest even integer
  (ROUND_HALF_EVEN).
* float.__int__() is an alias to float.__trunc__() (ROUND_DOWN)

Fraction
========

::

    >>> fractions.Fraction(5, 10)   # int / int
    Fraction(1, 2)
    >>> fractions.Fraction(1.2)   # float
    Fraction(5404319552844595, 4503599627370496)

C API
=====

Convert a Python object to an integer. Methods:

* ``__int__()``: slot ``type->tp_as_number->nb_int``
* ``__index__()``: slot ``type->tp_as_number->nb_index``
* ``__trunc__()`` (no slot)

``PyNumber_Long(obj)``:

* Call ``obj.__trunc__()``
* or: If ``obj`` type is bytes or str, parse the string in decimal (base 10)
* or: error!

``PyNumber_Index()``:

* Call ``obj.__index__()``: the result type must be exactly
  the int type (but Python tolerates int suclasses)
* or: error!

``_PyLong_FromNbInt()``:

* Call ``obj.__int__()``: the result type must be exactly
  the int type)

``_PyLong_FromNbIndexOrNbInt(x)``:

* return ``x`` if type(x) == int (``PyLong_CheckExact()``)
* call ``type(x).__index__()`` is defined: the result type must be exactly
  the int type
* call ``_PyLong_FromNbInt()``: the result type must be exactly
  the int type (but again Python tolerates int suclasses...)
* error if it is not a int subclass, and the type don't define ``__index__()``
  nor ``__int__()`` method

PyLong_FromLong():

* call ``_PyLong_FromNbIndexOrNbInt()``

Special case: ``__int__()`` or ``__index__()`` return a int subclass. This
feature is deprecated since Python 3.3 (see `commit 6a44f6ee
<https://github.com/python/cpython/commit/6a44f6eef3d0958d88882347190b3e2d1222c2e9>`_).
This feature may be removed from Python 3.9: see `bpo-17576
<https://bugs.python.org/issue17576>`_.

PyArg_ParseTuple, Py_BuildValue
===============================

Reference documentation: `Parsing arguments and building values
<https://docs.python.org/dev/c-api/arg.html>`_.

* PyArg_ParseTuple implementation: Python/getargs.c. Core function:
  ``convertsimple()``.
* Py_BuildValue is implemented in ``Python/modsupport.c``, core function:
  ``do_mkvalue()``.
* Functions behave differently if ``PY_SSIZE_T_CLEAN`` is defined:

    For all ``#`` variants of formats (``s#``, ``y#``, etc.), the type of the
    length argument (int or :c:type:`Py_ssize_t`) is controlled by defining the
    macro :c:macro:`PY_SSIZE_T_CLEAN` before including ``Python.h``.

Examples:

* ``PyArg_ParseTuple("i")``: convert a Python int to a C ``int``. It explicitly
  rejects float using ``PyFloat_Check(arg)`` and uses ``PyLong_AsLong()``.

getargs.c formats:

* ``l``: ``PyLong_AsLong()`` which uses ``obj.__int__()``, error if float
* ``n``: ``PyNumber_Index()``

XXX behaviour of undefined formats as ``k`` on integer overflow?


Script to update this page
==========================

number_tower.py:

.. literalinclude:: number_tower.py
