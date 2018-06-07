.. _python3:

++++++++
Python 3
++++++++

Python 3.0 was released in December 2008. Python 2.7 was released in July 2010.

Python 2 or Python 3?
=====================

* `pythonclock.org <https://pythonclock.org/>`_: "Python 2.7 will retire in..."
* `Python 3 Statement <https://python3statement.github.io/>`_

My article `Why should OpenStack move to Python 3 right now?
<http://techs.enovance.com/6521/openstack_python3>`_ explains why you should
move to Python 3 right now.

Python 2 will reach its end of life in 2020: see `Python 2.7 Release Schedule
<https://www.python.org/dev/peps/pep-0373/>`_. At Pycon US 2014, the support
`was extended from 2015 to 2020
<https://hg.python.org/peps/rev/76d43e52d978>`_ to give more time to companies
to port their applications to Python 3.


Port Python 2 code to Python 3
==============================

* `six module <http://pythonhosted.org/six/>`_
* `2to6 <https://github.com/limodou/2to6>`_
* `Language differences and workarounds <http://python3porting.com/differences.html>`_ (python3porting book)
* `Porting Python 2 Code to Python 3 <http://docs.python.org/dev/howto/pyporting.html>`_ (docs.python.org)
* `python-porting mailing list <http://mail.python.org/mailman/listinfo/python-porting>`_
* `getpython3.com <http://getpython3.com/>`_
* `Porting code to Python 3 <http://wiki.python.org/moin/PortingToPy3k/>`_ (Python.org wiki)
* `python-incompatibility <http://code.google.com/p/python-incompatibility/>`_
* `2to3c <https://fedorahosted.org/2to3c/>`_
* `py3to2 <https://pypi.python.org/pypi/py3to2>`_
* `Python 3 Wall of Superpowers <https://python3wos.appspot.com/>`_
* `Can I Use Python 3? <https://github.com/brettcannon/caniusepython3>`_


Python 3 is better than Python 2
================================

* `10 awesome features of Python that you can't use because you refuse to
  upgrade to Python 3
  <http://asmeurer.github.io/python3-presentation/slides.html>`_

Comparison on unequal types compares the type names
---------------------------------------------------

Python 2 implements a strange comparison operator. For the instruction ``a <
b``, if ``a.__cmp__(b)`` and ``b.__cmp__(a)`` raise ``NotImplementedError`` or
return ``NotImplemented``, Python 2 compares the *name* of the types.
Basically, ``a < b`` becomes ``type(a).__name__ < type(b).__name__``.
It's more complex than that, if a type is a number, the comparison uses an
empty string as the type name.

Extract of the ``default_3way_compare()`` function of Python 2 ``Objects/object.c``::

    /* different type: compare type names; numbers are smaller */
    if (PyNumber_Check(v))
        vname = "";
    else
        vname = v->ob_type->tp_name;
    if (PyNumber_Check(w))
        wname = "";
    else
        wname = w->ob_type->tp_name;
    c = strcmp(vname, wname);

Example in Python 2::

    >>> [1, 2, 3] < "abc"
    True
    >>> type([1, 2, 3]).__name__, type("abc").__name__
    ('list', 'str')
    >>> type([1, 2, 3]).__name__ < type("abc").__name__
    True

As a proof of the behaviour, it's possible to use type subclasses to modify the
type names::


    >>> class z(list): pass
    ...
    >>> class a(str): pass
    ...
    >>> [1, 2, 3] < "abc"
    True
    >>> z([1, 2, 3]) < a("abc")
    False
    >>> type(z([1, 2, 3])).__name__, type(a("abc")).__name__
    ('z', 'a')
    >>> type(z([1, 2, 3])).__name__ < type(a("abc")).__name__
    False

Python 3 doesn't have this strange fallback in comparison. It now raises
TypeError on this case::

    >>> [1, 2, 3] < "abc"
    TypeError: unorderable types: list() < str()

As a consequence, the builtin ``cmp()`` function was removed from Python 3. To
sort a list, the ``key`` parameter of ``list.sort()`` must be used. By the way,
on Python 2, using a *key* function (``list.sort(key=func)``) is more efficient
than using a *cmp* function (``list.sort(cmp=func)``).

On Python 2.7, it's possible to enable Python 3 comparison using ``-3 -Werror``
command line options::

    $ python2 -3 -Werror
    >>> [1, 2, 3] < "abc"
    DeprecationWarning: comparing unequal types not supported in 3.x

Bugs already fixed in Python 3
------------------------------

Some race conditions are already fixed in Python 3. The fix may be backported
to Python 2, but it takes more time because the Python 3 branch diverged from
the Python 2 branch, and Python core developer focus on Python 3.

* `python RLock implementation unsafe with signals
  <http://bugs.python.org/issue13697>`_
* Locks cannot be interrupted by signals in Python 2:
  `Condition.wait() doesn't raise KeyboardInterrupt
  <http://bugs.python.org/issue8844>`_
* subprocess is not thread-safe in Python 2:

  - file descriptor issue (see above)
  - `subprocess.Popen hangs when child writes to stderr
    <http://bugs.python.org/issue1336>`_
  - `Doc: subprocess should warn uses on race conditions when multiple threads
    spawn child processes <http://bugs.python.org/issue19809>`_

In Python 2, file descriptors are inherited by default in the subprocess
module, close_fds must be set explicitly to True. A race condition causes two
child processes to inherit a file descriptor, whereas only one specific child
process was supposed to inherit it. Python 3.2 fixed this issue by closing all
file descriptors by default.  Python 3.4 is even better: now all file
descriptors are not inheritable by default (`PEP 446: Make newly created file
descriptors non-inheritable <http://www.python.org/dev/peps/pep-0446/>`_).


Bugs that won't be fixed in Python 2 anymore
============================================

Unicode
-------

The Unicode support of Python 3 is much much better than in Python 2. Many
Unicode issues were closed as "won't fix" in Python 2, especially issues opened
after the release of Python 3.0. Some examples:

* `Outputting unicode crushes when printing to file on Linux
  <http://bugs.python.org/issue6832>`_
* `stdout.encoding not set when redirecting windows command line output
  <http://bugs.python.org/issue14192>`_

Bugs in the C stdio (used by the Python I/O)
--------------------------------------------

Python 2 uses the buffer API of the C standard library: ``fopen()``,
``fread()``, ``fseek()``, etcThis API has many bugs. Python works around some
bugs, but some others cannot be fixed (in Python). Examples:

* `Issue #20866: Crash in the libc fwrite() on SIGPIPE (segfault with os.popen and SIGPIPE)
  <http://bugs.python.org/issue20866>`_
* `Issue #21638: Seeking to EOF is too inefficient!
  <http://bugs.python.org/issue21638>`_
* `Issue #1744752: end-of-line issue on Windows on file larger than 4 GB
  <http://bugs.python.org/issue1744752>`_
* `Issue #683160: Reading while writing-only permissions on Windows
  <http://bugs.python.org/issue683160>`_
* `Issue #2730: file readline w+ memory dumps
  <http://bugs.python.org/issue2730>`_
* `Issue #22651: Open file in a+ mode reads from end of file in Python 3.4
  <http://bugs.python.org/issue22651>`_
* `Issue #228210: Threads using same stream blow up (Windows)
  <http://bugs.python.org/issue228210>`_

Python 3 has a much better I/O library: the ``io`` module which uses directly
system calls like ``open()``, ``read()`` and  ``lseek()``.


Hash DoS
--------

The hash function of Python 2 has a "worst complexity" issue which can be
exploited for a denial of service (DoS). It's called the "hash DoS"
vulnerability. Python 3.3 randomizes the hash function by default, Python 2.7
can use randomized hash if enabled explicitly. But the real fix is in Python
3.4 with the `PEP 456 <http://www.python.org/dev/peps/pep-0456/>`_ which now
uses the new SipHash hash function which is much safer.


subprocess
----------

The subprocess module is written in pure Python in Python 2.7. There are
complex race conditions. The correct fix was to reimplement the critical part
in C, fix implemented in Python 3.

* `subprocess.Popen hangs when child writes to stderr
  <http://bugs.python.org/issue1336>`_

See also the `PEP 446: Make newly created file descriptors non-inheritable
<http://www.python.org/dev/peps/pep-0446/>`_ which also fixes a complex issues
related to subprocesses, PEP implemented in Python 3.4.

Workaround: install the subprocess32 module from PyPI (and use it instead of
subprocess).


No more polling (busy loop) in Lock.acquire(timeout)
----------------------------------------------------

In Python 3.2, locks got a new optional timeout parameter which uses the
native OS function.

Extract of ``threading._Condition.wait(timeout)`` of Python 2.7::

    def wait(self, timeout=None):
        ...
        # Balancing act:  We can't afford a pure busy loop, so we
        # have to sleep; but if we sleep the whole timeout time,
        # we'll be unresponsive.  The scheme here sleeps very
        # little at first, longer as time goes on, but never longer
        # than 20 times per second (or the timeout time remaining).
        endtime = _time() + timeout
        delay = 0.0005 # 500 us -> initial delay of 1 ms
        while True:
            gotit = waiter.acquire(0)
            if gotit:
                break
            remaining = endtime - _time()
            if remaining <= 0:
                break
            delay = min(delay * 2, remaining, .05)
            _sleep(delay)
        ...

Moreover, ``subprocess.Popen.communicate()`` also got a timeout parameter.


Monotonic clocks
----------------

Timeouts must not use the system clocks but a monotonic clock. It is explained
in the `PEP 418 <http://legacy.python.org/dev/peps/pep-0418/>`_ which has been
implemented in Python 3.3.

Example of issue with system clock changes: `threading.Timer/timeouts break on
change of win32 local time <http://bugs.python.org/issue1508864>`_.

See also the PEP 418 for a list of issues related to the system clock.

Other bugs
----------

Misc bugs:

* `Destructor of ElementTree.Element is recursive
  <http://bugs.python.org/issue28871>`_
* `Ctrl-C doesn't interrupt simple loop
  <http://bugs.python.org/issue21870>`_: require the new GIL
  introduced in Python 3.2

Python 2 is slower
==================

* The C code base doesn't respect strict aliasing and so must be compiled with
  ``-fno-strict-aliasing`` (to avoid bugs when the compiler optimizes the code)
  which is inefficient. The structure of Python C type has been deeply
  rewritten to fix the root cause.
* Python 3 uses less memory for Unicode text thanks to the `PEP 393: Flexible
  String Representation <https://www.python.org/dev/peps/pep-0393/>`_. Many
  operations on "ASCII" strings are faster on Python 3 than Python 2.


Port Python 3 code to Python 2
==============================

Notes based on my experience of porting Tulip to Python 2 (Trollius project).

* Remove keyword-only parameter: replace ``def func(*, loop=None): ...``
  with ``def func(loop=None): ...``
* ``super()`` requires the class and self, *and* the class must inherit from object
* A class must inherit explicitly from object to use properties and ``super()``,
  otherwise ``super()`` fails with a cryptic "TypeError: must be type, not
  classobj" message.
* Python 2.6: ``str.format()`` doesn't support ``{}``. For example,
  ``"{} {}".format("Hello", "World")`` must be written
  ``"{0} {1}".format("Hello", "World")``.
* Replace ``list.clear()`` with ``del list[:]``
* Replace ``list2 = list.copy()`` with ``list2 = list[:]``
* Python 3.3 has new specialized ``OSError`` exceptions: ``BlockingIOError``,
  ``InterruptedError``, ``TimeoutError``, etc. Python 2 has ``IOError``,
  ``OSError``, ``EnvironmentError``, ``WindowsError``, ``VMSError``,
  ``mmap.error``, ``select.error``, etc.
* ``raise ValueError("error") from None`` should be replaced with
  ``raise ValueError("error")``
* ``memoryview`` should be replaced with ``buffer``

Major changes in between Python 2.6 and 3.3:

* ``threading.Lock.acquire()`` and ``subprocess.Popen.communicate()`` support
  timeout.  A busy loop can be used for ``threading.Lock.acquire()``
  (non-blocking call + sleep) in Python 2.
* ``time.monotonic()`` (3.3)
* set and dict literals
* ``memoryview`` object
* ``collections.OrderedDict`` (2.7, 3.1)
* ``weakref.WeakSet`` (2.7, 3.0)
* ``argparse``
* Python 2 doesn't support ``ssl.SSLContext`` nor certificate validation
* ``ssl`` module: ``SSLContext``, ``SSLWantReadError``, ``SSLWantWriteError``,
  ``SSLError``
* Python 2 does not support ``yield from`` and does not support ``return`` in
  generators (3.3)
* Python 2 doesn't support the ``nonlocal`` keyword: use mutable types like
  list or dict instead (3.0)

New modules in the standard library between Python 2.6 and Python 3.3:

* concurrent.futures (3.2)
* faulthandler (3.3)
* importlib (3.1)
* ipaddress (3.3)
* lzma (3.3)
* tkinter.ttk (3.1)
* unittest.mock (3.3)
* venv (3.3)

Python 3.4 has even more modules:

* asyncio
* enum
* ensurepip
* pathlib
* selectors
* statistics
* tracemalloc


