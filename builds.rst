.. _python-builds:

+++++++++++++
Python builds
+++++++++++++

See also :ref:`Analysis of CPython binary assembly <assembly>` and :ref:`C
compilers <c-compilers>`.

Build depenencies
=================

Install Python dependencies on Fedora::

    sudo dnf install make gcc openssl-devel \
        readline-devel zlib-devel bzip2-devel xz-devel

Minimum configure Python for Fedora::

    ./configure --prefix /usr --with-platlibdir=lib64 --libdir=/usr/lib64 --enable-shared

Full configure Python for Fedora (check ``CONFIG_ARGS`` in
``/usr/lib64/python3.11/config-3.11-x86_64-linux-gnu/Makefile``)::

    --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu \
    --disable-dependency-tracking --prefix=/usr --exec-prefix=/usr \
    --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc \
    --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 \
    --libexecdir=/usr/libexec --localstatedir=/var --runstatedir=/run \
    --sharedstatedir=/var/lib --mandir=/usr/share/man \
    --infodir=/usr/share/info --with-platlibdir=lib64 --enable-ipv6 \
    --enable-shared --with-computed-gotos=yes \
    --with-dbmliborder=gdbm:ndbm:bdb --with-system-expat --with-system-ffi \
    --with-system-libmpdec --enable-loadable-sqlite-extensions \
    --with-dtrace --with-lto --with-ssl-default-suites=openssl \
    --without-static-libpython --with-wheel-pkg-dir=/usr/share/python-wheels \
    --with-valgrind --without-ensurepip --enable-optimizations \
    build_alias=x86_64-redhat-linux-gnu \
    host_alias=x86_64-redhat-linux-gnu \
    PKG_CONFIG_PATH=':/usr/lib64/pkgconfig:/usr/share/pkgconfig' \
    CC=gcc CFLAGS='-O2  -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS  -fstack-protector-strong   -m64  -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection    -D_GNU_SOURCE -fPIC -fwrapv' \
    LDFLAGS='-Wl,-z,relro -Wl,--as-needed  -Wl,-z,now    -Wl,--build-id=sha1   -g'


.. _release-build:

Release build
=============

In release mode, Python is built with ``-O3 -DNDEBUG`` compiler flags; defining
``NDEBUG`` macro removes assertions.

LTO
---

Use ``gcc -flto``

Maybe also: ``-fuse-linker-plugin -ffat-lto-objects -flto-partition=none``.

Check if Python was built with LTO::

    $ python3 -c "import sysconfig; print('lto' in (sysconfig.get_config_var('PY_CFLAGS') + sysconfig.get_config_var('PY_CFLAGS_NODIST')))"
    True

PGO
---

* Build Python with ``gcc -fprofile-generate``
* Run the test suite: ``make run_profile_task`` uses ``PROFILE_TASK`` variable
  of Makefile. configure uses ``./python -m test --pgo`` by default.
  List of test used with ``--pgo``: see `libregrtest/pgo.py
  <https://github.com/python/cpython/blob/master/Lib/test/libregrtest/pgo.py>`_.
* Rebuild Python with ``gcc -fprofile-use``

Check if Python was built with PGO::

    $ python3 -c "import sysconfig; print('-fprofile-use' in (sysconfig.get_config_var('PY_CFLAGS') + sysconfig.get_config_var('PY_CFLAGS_NODIST')))"
    True

PGO + LTO
---------

Use PGO and add LTO flags.

.. _pydebug:

Debug build
===========

* Fedora: ``dnf install python3-debug`` to get the ``python3-debug`` program:
  run it instead of running ``python3``.
* ``./configure --with-pydebug``
* Python built using ``-Og`` if available, or ``-O0`` otherwise.
* Define the ``Py_DEBUG`` macro which enables many runtime checks to ease
  debug.

Python built in debug mode is very effecient to detect bugs in C extensions.

Effects of the Debug Mode:

* Build Python with assertions (don't set ``NDEBUG`` macro):

  * ``assert(...);``
  * ``_PyObject_ASSERT(...);``
  * etc.

* Install `debug hooks on memory allocators
  <https://docs.python.org/dev/c-api/memory.html#c.PyMem_SetupDebugHooks>`_ to
  detect buffer overflow and other memory errors.
* Add runtime checks, code surroundeded by ``#ifdef Py_DEBUG`` and ``#endif``.
* Unicode and int objects are created with their memory filled with a pattern
  to help detecting uninitialized bytes.
* Many functions ensure that are not called with an exception raised, since
  they can clear or replace the current exception:
  ``assert(!_PyErr_Occurred(tstate));``.

Checks in the GC:

* The GC ``visit_decref()`` function checks if an object was freed using
  ``_PyObject_IsFreed()``. This function is used internally during a GC
  collection on all Python objects tracked by the GC to break reference
  cycles.
* ``PyObject_GC_Track()`` checks if the object was freed using
  ``_PyObject_IsFreed()``.
* GC ``gc_decref()`` function checks if the GC reference count is valid.

Check if Python is built in debug mode
======================================

Py_DEBUG adds ``sys.gettotalrefcount()`` function::

    $ python3 -c "import sys; print('Debug build?', hasattr(sys, 'gettotalrefcount'))"
    Debug build? False
    $ python3-debug -c "import sys; print('Debug build?', hasattr(sys, 'gettotalrefcount'))"
    Debug build? True

or: Check ``sysconfig.get_config_var('Py_DEBUG')`` value::

    $ python3 -c "import sysconfig; print('Debug build?', bool(sysconfig.get_config_var('Py_DEBUG')))"
    Debug build? False
    $ python3-debug -c "import sysconfig; print('Debug build?', bool(sysconfig.get_config_var('Py_DEBUG')))"
    Debug build? True


Extra debug
===========

* ``Objects/dictobject.c``: define DEBUG_PYDICT macro to add
  ``_PyDict_CheckConsistency()`` checks to debug corrupted dictionaries.
* ``Objects/obmalloc.c``: define PYMEM_DEBUG_SERIALNO to store a serial number
  in allocated memory blocks.

Special builds
==============

`Read Misc/SpecialBuilds.txt
<https://github.com/python/cpython/blob/master/Misc/SpecialBuilds.txt>`_.
