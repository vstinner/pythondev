++++++++++++++++++++++++++++++++++++
Compile Python to WebAssembly (WASM)
++++++++++++++++++++++++++++++++++++

Python documentation: `Tools/wasm/README.md <https://github.com/python/cpython/blob/main/Tools/wasm/README.md>`_.

April 2022: There is a work-in-progress to support WASM targets in Python 3.11
which is still at the alpha stage (release scheduled in October 2022).

Targets
=======

Status in April 2022 (from Christian Heimes' slides at Pycon DE):

========================  ==================  ==================  =========================
Features                  CPython Emscripten  CPython Emscripten  Pyodide
                          browser             node
========================  ==================  ==================  =========================
subprocess (fork, exec)   no                  no                  no
threads                   no                  YES                 WIP
file system               no (only MEMFS)     YES (Node raw FS)   YES (IDB, Node, ...)
shared extension modules  WIP                 WIP                 YES
PyPI packages             no                  no                  YES
sockets                   ?                   ?                   ?
urllib, asyncio           no                  no                  WebAPI fetch / WebSocket
signals                   no                  WIP                 YES
========================  ==================  ==================  =========================

CPython on WebAssembly
======================

Status
------

* **WARNING**: WASM support is highly experimental! Lots of features are not working yet.
* April 2022: Christian Heime's talk at Pycon DE:
  `Python 3.11 in the web browser - A journey
  <https://speakerdeck.com/tiran/python-3-dot-11-in-the-web-browser-a-journey-pycon-de-2022-keynote>`_
* April 2022: WASM binary is ~4.5 MB compressed with static, reduced stdlib.
  4.6 MB wasm (compressed 1.5 MB), 2.7 MB stdlib bytecode, some JS.

Python on wasm32-emscripten
---------------------------

* ``sys.platform`` is ``'emscripten'``
* ``os.name`` is ``'posix'``
* ``platform.machine()`` is ``'wasm32'``
* Example of ``platform.platform()``: ``'Emscripten-1.0-wasm32-32bit'``
* Example ``os.uname()``: ``posix.uname_result(sysname='Emscripten', nodename='emscripten', release='1.0', version='#1', machine='wasm32')``

Python on wasm32-wasi
---------------------

* ``sys.platform`` is ``'wasi'``
* ``os.name`` is ``'posix'``
* ``platform.machine()`` is ``'wasm32'``
* Example of ``platform.platform()``: ``'wasi-0.0.0-wasm32-32bit'``
* Example ``os.uname()``: ``posix.uname_result(sysname='wasi', nodename='(none)', release='0.0.0', version='0.0.0', machine='wasm32')``

Build
-----

Cross-build CPython to WASM:

* `Tools/wasm/README.md <https://github.com/python/cpython/blob/main/Tools/wasm/README.md>`_
* Python: Tools/wasm/ directory: scripts to build Python for WASM.
* `configure \-\-with-emscripten-target=[browser|node]
  <https://docs.python.org/dev/using/configure.html#cmdoption-with-emscripten-target>`_
* `configure \-\-enable-wasm-dynamic-linking
  <https://docs.python.org/dev/using/configure.html#cmdoption-enable-wasm-dynamic-linking>`_
* By default, ``configure --with-suffix`` (``EXE`` Makefile variable) is set to
  ``.js`` for Emscripten and ``.wasm`` for WASI.

In short, on Fedora, commands to type in the Python source code directory::

    git clean -fdx  # warning: it removes ALL untracked files!
    podman run --rm -ti -v $(pwd):/python-wasm/cpython:Z -w /python-wasm/cpython quay.io/tiran/cpythonbuild:emsdk3

In the emsdk3 container::

    # python3 -u ./Tools/wasm/wasm_build.py wasi build -v 2>&1|tee log
    ./Tools/wasm/wasm_build.py wasi build # -v
    cd builddir/wasi/
    make pythoninfo
    make buildbottest TESTOPTS=""

Build 2
-------

Documentation: https://devguide.python.org/getting-started/setup-building/#wasi

Create a container from "devcontainer" cpython-dev (container based on Fedora)::

    podman build .devcontainer --tag cpython-dev

In a CPython checkout, start by removing all local files not tracked by Git::

    git clean -fdx

In the clean CPython checkout, run the container::

    podman run -it --rm -v $PWD:/workspace:O -w/workspace cpython-dev

Now inside the container, build Python for WASI::

    python3 Tools/wasm/wasi.py build -- --config-cache --with-pydebug

Run Python::

    cross-build/wasm32-wasi/python.sh

Run the test suite::

    cross-build/wasm32-wasi/python.sh -m test


Python WASM browser REPL
========================

Christian Heimes' REPL:

* April 2022: Python 3.11 alpha 6
* https://cheimes.fedorapeople.org/python-wasm/

Ethan Smith's REPL

* April 2022: Python 3.11 alpha 7
* https://repl.ethanhs.me/
* https://github.com/ethanhs/python-wasm

Python WASM detailed status
===========================

Disabled C extensions
---------------------

C extensions disabled on Emscripten/browser, Emscripten/node and WASI targets:

* ``_ctypes``, ``_ctypes_test``
* ``_curses``, ``_curses_panel``
* ``_dbm``, ``_gdbm``
* ``_scproxy``
* ``_tkinter``
* ``_xxsubinterpreters``
* ``grp``
* ``nis``
* ``ossaudiodev``
* ``pwd``, ``spwd``
* ``syslog``

C extensions disabled on Emscripten/browser, Emscripten/node targets:

* ``_multiprocessing``
* ``_posixshmem``
* ``_posixsubprocess``

C extensions disabled on the Emscripten/browser target:

* ``fcntl``
* ``readline``
* ``resource``
* ``termios``

Pyodide
=======

Python distribution for the browser and Node.js based on WebAssembly:

* REPL: https://pyodide.org/en/stable/console.html

  * April 2022: Python 3.10.2

* https://pyodide.org/
* https://github.com/pyodide/pyodide

WASI
====

* April 2022: WASI is not supported: it will likely be supported eventually.
* No browser or Javascript
* sandboxed, small runtime (wasmtime 18 MB Rust binary)
* https://github.com/bytecodealliance/wasmtime-py

pygame and WASM
===============

* https://pygame-web.github.io/
* Examples: https://pmp-p.itch.io/

Misc
====

* https://caniuse.com/wasm
* `CPython WebAssembly nightly tests & unofficial builds
  <https://github.com/tiran/cpython-wasm-test>`_
  by Christian Heimes
* https://quay.io/repository/tiran/cpythonbuild?tab=tags&tag=emsdk3
* https://github.com/tiran/cpython_builddep/
* https://github.com/tiran/cpython_builddep/blob/main/wasm/Dockerfile.emsdk3
* ``.github/workflows/reusable-wasi.yml``
