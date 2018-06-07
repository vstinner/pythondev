++++++++++++++
Python Numbers
++++++++++++++

Types
=====

* int
* float: IEEE 754 (64 bits, base 2)
* complex: implemented as two floats
* decimal.Decimal: base 10, arbitrary precision
* fractions.Fraction: rational, numerator/denominator; automatically
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

* ``__int__()``
* ``__index__()``
* ``__trunc__()``

``PyNumber_Long()``:

* Call ``obj.__trunc__()``
* or: If obj is a Unicode or bytes string, decode from base 10
* or: error!

``PyNumber_Index()``:

* Call ``obj.__index__()`` which must return a Python int (exact int type).
  Internal: ``obj->ob_type->tp_as_number->nb_index`` field.
* or: error!

``_PyLong_FromNbInt()``:

* Call ``obj.__int__()`` which must return a Python int (exact int type).
  Interal: ``obj->ob_type->tp_as_number->nb_int`` field.

getargs.c formats:

* ``l``: ``PyLong_AsLong()`` which uses ``obj.__int__()``, error if float
* ``n``: ``PyNumber_Index()``

XXX behaviour of undefined formats as ``k`` on integer overflow?
