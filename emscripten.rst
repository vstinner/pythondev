++++++++++++++++++++++++++
Run Python with Emscripten
++++++++++++++++++++++++++

Emscripten is a complete compiler toolchain to WebAssembly, using LLVM, with a
special focus on speed, size, and the Web platform.

* `PEP 776 – Emscripten Support <https://peps.python.org/pep-0776/>`_
* `PEP 783 – Emscripten Packaging <https://peps.python.org/pep-0783/>`_

Python on Emscripten
====================

* ``sys.platform`` is ``'emscripten'``
* ``os.name`` is ``'posix'``
* ``platform.machine()`` is ``'wasm32'``
* Example of ``platform.platform()``: ``'Emscripten-1.0-wasm32-32bit'``
* Example ``os.uname()``: ``posix.uname_result(sysname='Emscripten', nodename='emscripten', release='1.0', version='#1', machine='wasm32')``

Build Emscripten
================

Documentation: https://devguide.python.org/getting-started/setup-building/#emscripten

Go to Python source code and remove all untracked files::

    git clean -fdx  # warning: it removes ALL untracked files!

Install nvm (which will install Node.js): https://github.com/nvm-sh/nvm#installing-and-updating

Install Emscripten SDK in ``~/emsdk``::

    mkdir -p ~/emsdk
    export EMSDK_CACHE=~/emsdk
    python3 Platforms/emscripten install-emscripten

Build the build Python (using ``gcc``)::

    python3 Platforms/emscripten build build 2>&1|tee build.log
    # python3 Platforms/emscripten configure-build-python -- --config-cache --with-pydebug
    # python3 Platforms/emscripten make-build-python
    # python3 Platforms/emscripten pythoninfo-build

Make dependencies (libffi and mpdec)::

    python3 Platforms/emscripten make-dependencies

Build the host/Emscripten Python (using ``emcc``)::

    python3 Platforms/emscripten build host 2>&1|tee host.log
    # python3 Platforms/emscripten configure-host --host-runner node -- --config-cache
    # python3 Platforms/emscripten make-host
    # python3 Platforms/emscripten pythoninfo-host

Run Emscripten Python::

    echo 'print("Hello World")' > script.py
    python3 Platforms/emscripten run script.py

Remove all::

    rm -rf ~/emsdk/
    rm -rf ~/.nvm/

See also: https://github.com/python/cpython/blob/main/.github/workflows/reusable-emscripten.yml


Disabled C extensions
=====================

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

Python distribution for the browser and Node.js based on WebAssembly.

* REPL: https://pyodide.org/en/stable/console.html
* https://pyodide.org/
* https://github.com/pyodide/pyodide

Pyodide has more features:

* File system: IDB, Node, ...
* shared extension modules
* PyPI packages
* urllib, asyncio: WebAPI fetch / WebSocket
* support signals

Misc
====

* https://caniuse.com/wasm : browsers support
