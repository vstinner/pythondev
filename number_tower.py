from __future__ import print_function
import numbers
import warnings
import fractions
import decimal

warnings.simplefilter("error", DeprecationWarning)

VALUES = (
    ("int", 123),
    ("float", 1.5),
    ("complex", complex(0, 1.5)),
    ("decimal.Decimal", decimal.Decimal("1.1")),
    ("fractions.Fraction", fractions.Fraction(1, 7)),
    ("bytes", b"123"),
    ("str", "123"),
)

TYPES = (
    ("int", int),
    ("float", float),
    ("complex", complex),
    ("decimal.Decimal", decimal.Decimal),
    ("fractions.Fraction", fractions.Fraction),
)

for type_descr, num_type in TYPES:
    accepted = []
    rejected = []
    for value_descr, value in VALUES:
        try:
            num_type(value)
        except TypeError:
            rejected.append(value_descr)
        else:
            accepted.append(value_descr)
    if accepted:
        print("``%s(obj)`` accept:" % type_descr)
        print()
        for name in accepted:
            print("* ``%s``" % name)
        print()
    if rejected:
        print("``%s(obj)`` reject:" % type_descr)
        print()
        for name in rejected:
            print("* ``%s``" % name)
        print()
print()

for tower_name, tower_type in (
    ("Number", numbers.Number),
    ("Complex", numbers.Complex),
    ("Real", numbers.Real),
    ("Rational", numbers.Rational),
    ("Integral", numbers.Integral),
):
    subclasses = []
    for type_descr, num_type in TYPES:
        if issubclass(num_type, tower_type):
            subclasses.append(type_descr)
    print("%s subclasses: %s" % (tower_name, ", ".join(subclasses)))
