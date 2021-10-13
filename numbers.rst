++++++++++++++
Python Numbers
++++++++++++++

Number Types
============

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
is specified by the `PEP 3141 -- A Type Hierarchy for Numbers
<https://www.python.org/dev/peps/pep-3141/>`_.

* numbers.Number: base class
* numbers.Complex: Add ``real``, ``imag``, ``conjugate()``
* numbers.Real: subclass of Complex; add many float operations.
* numbers.Rational: subclass of Real; add ``numerator`` and ``denominator``
  attributes
* numbers.Integral: subclass of Rational

Subclasses:

* numbers.Number: int, float, complex, decimal.Decimal, fractions.Fraction
* numbers.Complex: int, float, complex, fractions.Fraction
* numbers.Real: int, float, fractions.Fraction
* numbers.Rational: int, fractions.Fraction
* numbers.Integral: int

int, float, complex methods and attributes:

* ``conjugate()``
* ``imag``
* ``real``

int and Fraction attributes:

* ``denominator``
* ``numerator``


Conversions in Python
=====================

``int(obj)`` and ``float(obj)`` accept:

* ``int``
* ``float``
* ``decimal.Decimal``
* ``fractions.Fraction``
* ``bytes``
* ``str``

``int(obj)`` rounds towards zero (ROUND_DOWN, ex: ``int(0.9) == 0`` and
``int(-0.9) == 0``).

But ``int(obj)`` and ``float(obj)`` reject:

* ``complex``

``complex(obj)`` accepts:

* ``int``
* ``float``
* ``complex``
* ``decimal.Decimal``
* ``fractions.Fraction``
* ``str``

But ``complex(obj)`` rejects:

* ``bytes``

``decimal.Decimal(obj)`` accepts:

* ``int``
* ``float``
* ``decimal.Decimal``
* ``str``

But ``decimal.Decimal(obj)`` rejects:

* ``complex``
* ``fractions.Fraction``
* ``bytes``

``fractions.Fraction(obj)`` accepts:

* ``int``
* ``float``
* ``decimal.Decimal``
* ``fractions.Fraction``
* ``str`` (ex: ``"1"`` or ``"1/2"``)

But ``fractions.Fraction(obj)`` rejects:

* ``complex``
* ``bytes``

int type
========

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

Rounding:

* ``int(float)`` calls ``float.__trunc__()``, so rounds towards zero
  (ROUND_DOWN)

float type
==========

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

Rounding:

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

Convert a Python object to an integer. Type methods:

* ``__int__()``: slot ``type->tp_as_number->nb_int``
* ``__index__()``: slot ``type->tp_as_number->nb_index``
* ``__trunc__()`` (no slot)

``PyNumber_Long(obj)``:

* Call ``obj.__trunc__()`` (Round towards zero, ROUND_DOWN)
* or: If ``obj`` type is bytes or str, parse the string in decimal (base 10)
* or: error!

``PyNumber_Index(x)`` calls the ``__index__()`` method: raises an exception if
the type has no ``__index__()`` method or if method does not return exactly an
int type (*).

``_PyLong_FromNbInt(x)``:

* Call ``type(x).__int__(x)``: the result type must be exactly the int type (*)
* or: error!

``_PyLong_FromNbIndexOrNbInt(x)``: ``__index__()`` or ``__int__()``:

* return ``x`` if ``type(x) == int`` (``PyLong_CheckExact()``)
* call ``type(x).__index__(x)`` if defined: the result type must be exactly
  the int type (*)
* call ``type(x).__int__(x)`` (call ``_PyLong_FromNbInt()``): the result type must
  be exactly the int type (*)
* error if it is not a int subclass, and the type don't define ``__index__()``
  nor ``__int__()`` method
* New in Python 3.8

``PyLong_AsLong()`` converts a Python ``int`` to a C ``long``:

* call ``_PyLong_FromNbIndexOrNbInt()``
* raise OverflowError if the result does not fit into a C long
* Python 3.7 and older only calls ``__int__()``, not ``__index__()``.

``PyLong_AsUnsignedLongMask()`` converts a Python object to a C ``unsigned
long``:

* call ``_PyLong_FromNbIndexOrNbInt(x)`` and then
  ``_PyLong_AsUnsignedLongMask()`` on the result
* error if the object cannot be converted to an int by
  ``_PyLong_FromNbIndexOrNbInt(x)``
* **mask integer overflow**
* Python 3.7 and older only calls ``__int__()``, not ``__index__()``.

(*) Special case: ``__int__()`` or ``__index__()`` return a int subclass. This
feature is deprecated since Python 3.3 (see `commit 6a44f6ee
<https://github.com/python/cpython/commit/6a44f6eef3d0958d88882347190b3e2d1222c2e9>`_).
This feature may be removed from Python 3.9: see `bpo-17576
<https://bugs.python.org/issue17576>`_.

PyArg_ParseTuple and Py_BuildValue
==================================

Reference documentation: `Parsing arguments and building values
<https://docs.python.org/dev/c-api/arg.html>`_.

* PyArg_ParseTuple is implemented in ``Python/getargs.c``, core function:
  ``convertsimple()``.
* Py_BuildValue is implemented in ``Python/modsupport.c``, core function:
  ``do_mkvalue()``.
* Functions behave differently if ``PY_SSIZE_T_CLEAN`` is defined:

    For all ``#`` variants of formats (``s#``, ``y#``, etc.), the type of the
    length argument (int or :c:type:`Py_ssize_t`) is controlled by defining the
    macro :c:macro:`PY_SSIZE_T_CLEAN` before including ``Python.h``.

PyArg_ParseTuple formats:

* ``"i"`` (C ``int``): ``__index__()`` or ``__int__()``; call
  ``PyLong_AsLong(obj)``, but explicitly rejects float using
  ``PyFloat_Check(arg)``.
* ``"l"`` (C ``long``):  ``__index__()`` or ``__int__()``; call ``PyLong_AsLong()``, but
  explicitly rejects float using ``PyFloat_Check(arg)``
* ``"n"`` (C ``ssize_t``): ``__index__()``; call
  ``PyNumber_Index()`` and then ``PyLong_AsSsize_t()``. Exception on overflow.
* ``"k"``: call ``PyLong_AsUnsignedLongMask()`` if it's an int or int subclass,
  error otherwise. **Mask integer overflow**.

Note: In Python 3.7 and older, ``PyLong_AsLong()`` only calls ``__int__()``,
not ``__index__()``.


Script to update this page
==========================

number_tower.py:

.. literalinclude:: number_tower.py
