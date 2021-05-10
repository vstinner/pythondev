.. _assembly:

+++++++++++++++++++++++++++++++++++
Analysis of CPython binary assembly
+++++++++++++++++++++++++++++++++++

Usually, you should not care how the C compiler optimizes Python. Analyzing the
assembly code helps to check if the C compiler is able to optimize Python as
you might expect.

See also :ref:`Python builds <python-builds>` and `Assembly Intel x86
<https://vstinner.readthedocs.io/assembly_x86.html>`_.

Inline libpython function calls and LTO
=======================================

Link Time Optimization (LTO) helps a lot to inline function calls.

If Python is configured with ``--enable-shared`` (Python executable is linked
to ``libpythonX.Y.so``), the ``-fno-semantic-interposition`` compiler flag is
needed by GCC to inline libpython function calls. This flag is now enabled by
``--enable-optimizations`` since Python 3.10. Clang disables semantic
interposition by default and so doesn't need this flag.

See `Red Hat Enterprise Linux 8.2 brings faster Python 3.8 run speeds
<https://developers.redhat.com/blog/2020/06/25/red-hat-enterprise-linux-8-2-brings-faster-python-3-8-run-speeds/>`_
for a concrete analysis of Python 3.8 performance on RHEL 8 with
``--enable-shared`` and ``-fno-semantic-interposition``.

macOS doesn't use LTO
=====================

The official Python macOS binaries are **not** built with LTO to keep support
of old clang versions of macOS 10.6: see `bpo-41181
<https://bugs.python.org/issue41181>`_.  See also `bpo-42235: [macOS] Use
--enable-optimizations in build-installer.py
<https://bugs.python.org/issue42235>`_.

Concrete example of performance issue with the lack of LTO on macOS: `bpo-39542
<https://bugs.python.org/issue39542#msg373230>`_. Converting ``PyTuple_Check()``
macro to a function call introduced a performance slowndown on macOS beause
clang was unable to inline the PyTuple_Check() function call. The change
was reverted to restore performance on macOS.

In Python 3.10, LTO is used on macOS but on macOS 10.15 and newer
(`bpo-42235 <https://bugs.python.org/issue42235>`_).

Security compiler flags
=======================

Position Independent Code (-fPIC)
---------------------------------

On Fedora, Python is built with ``-fPIC`` for security. See `Wikipedia:
Position-independent code
<https://en.wikipedia.org/wiki/Position-independent_code>`_.

Control flow Enforcement Technology (CET) hardening
---------------------------------------------------

GCC has a ``-fcf-protection=branch`` flag which emits ``ENDBR64`` ("End Branch
64 bit") instructions at functions entry point. It is used on Fedora.

Compiler and linker flags
=========================

Get compiler (CFLAGS) and linker (LDFLAGS) flags::

    $ python3
    Python 3.9.1 (default, Jan 20 2021, 00:00:00)
    >>> import sysconfig
    >>> cflags = sysconfig.get_config_var('PY_CFLAGS') + sysconfig.get_config_var('PY_CFLAGS_NODIST')
    >>> ldflags = sysconfig.get_config_var('PY_LDFLAGS') + sysconfig.get_config_var('PY_LDFLAGS_NODIST')
    >>> '-fPIC' in cflags
    True
    >>> '-fno-semantic-interposition' in cflags
    True
    >>> '-flto' in ldflags
    True

Python thread state (tstate)
============================

Since Python 3.8, there is an on-going effect to pass explicitly the current
Python thread state ("tstate") to internal functions:

* It avoids having to read an atomic variable: ``_PyThreadState_GET()`` reads
  ``_PyRuntime.gilstate.tstate_current`` atomic variable with
  ``_Py_atomic_load_relaxed()``.
* It should help the C compiler to inline more code.

See `Pass the Python thread state explicitly
<https://vstinner.github.io/cpython-pass-tstate.html>`_.

PyErr_Occurred()
----------------

Simplified C code of ``PyErr_Occurred()``::

    PyObject* PyErr_Occurred(void)
    {
        _PyRuntimeState *runtime = &_PyRuntime;
        _Py_atomic_address *ptstate = &runtime->gilstate.tstate_current;
        PyThreadState *tstate = (PyThreadState*)_Py_atomic_load_relaxed(ptstate)
        return tstate->curexc_type;
    }

``PyErr_Occurred()`` of Fedora Python 3.9 (built with ``-fPIC``)::

    endbr64

    # rax = &_PyRuntime = *(void **)0x7ffff7f45d38
    mov rax, QWORD PTR [rip+0x1fef9d]  # 0x7ffff7f45d38

    # offsetof(_PyRuntimeState, gilstate.tstate_current) = 0x238
    # rdx = tstate = *(_PyRuntime.gilstate.tstate_current) = *(void **)($rax + 0x238)
    mov rdx, QWORD PTR [rax+0x238]

    # offsetof(PyThreadState, curexc_type) = 0x58
    # rax = tstate->curexc_type = *(void **)($rdx + 0x58)
    mov rax, QWORD PTR [rdx+0x58]

    ret

Getting tstate requires two pointer deferences (two ``MOV``):

* ``runtime = *($rip + 0x1fef9d)`` (``&_PyRuntime``)
* ``tstate = runtime->gilstate.tstate``

``PyErr_Occurred()`` requires 3 pointer deferences.

Note: the ``$rip`` indirection is needed by ``-fPIC`` flag and ``endbr64``
instruction is related to CET hardening flag.

_PyErr_Occurred()
-----------------

C code::

    static inline PyObject* _PyErr_Occurred(PyThreadState *tstate)
    {
        assert(tstate != NULL);
        return tstate->curexc_type;
    }

``_PyErr_Occurred()`` of Fedora Python 3.9 (built with ``-fPIC``), inlined in
``_Py_CheckFunctionResult+12()``:::

    # $rdi = tstate argument
    # offsetof(PyThreadState, curexc_type) = 0x58
    mov rax, QWORD PTR [rdi+0x58]                                                                           │

The function calls becomes a single pointer deference (one ``MOV``):

* ``result = (*tstate).curexc_type``

On Fedora, calling ``PyErr_Occurred()`` requires 6 instructions (CALL, ENDBR64,
3 MOV, RET), whereas inlined ``_PyErr_Occurred`` is a single MOV instruction.
