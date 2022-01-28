++++++++++++++++++++++++++++++++++++
Compile Python to WebAssembly (WASM)
++++++++++++++++++++++++++++++++++++

* CPython status

  * January 2022: almost 10 MB (6.5 MB WASM, 2.9 MB stdlib, some JS)
  * Cross-build Python to WASM
  * WASI is not support: it will likely be supported eventually.
  * ``sys.platform`` is ``emscripten`` and os.name is ``'posix'``
  * Disabled C extensions:

    * _ctypes
    * _curses
    * _curses_panel
    * _dbm
    * _gdbm
    * _multiprocessing
    * _posixshmem
    * _posixsubprocess
    * _scproxy
    * _tkinter
    * _xxsubinterpreters
    * fcntl
    * grp
    * nis
    * ossaudiodev
    * resource
    * readline
    * spwd
    * syslog
    * termios

* WASM limitations

  * No threads
  * No subprocess
  * No socket (yet)

* Pyodide: Python distribution for the browser and Node.js based on
  WebAssembly.

  * https://github.com/pyodide/pyodide
  * https://pyodide.org/

* Ethan Smith's REPL

  * https://repl.ethanhs.me/
  * https://github.com/ethanhs/python-wasm

* https://caniuse.com/wasm
