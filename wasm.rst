++++++++++++++++++++++++++++++++++++
Compile Python to WebAssembly (WASM)
++++++++++++++++++++++++++++++++++++

Python documentation: `Tools/wasm/README.md <https://github.com/python/cpython/blob/main/Tools/wasm/README.md>`_.

Targets
=======

Status in April 2022 (from Christian Heimes' slides at Pycon DE):

========================  ==============  =================  =========================
Features                  Browser         Node               Pyodide
========================  ==============  =================  =========================
subprocess (fork, exec)   X               X                  X
threads                   X               yes                WIP
file system               X (only MEMFS)  yes (Node raw FS)  yes (IDB, Node, ...)
shared extension modules  WIP             WIP                yes
PyPI packages             X               X                  yes
sockets                   ?               ?                  ?
urllib, asyncio           X               X                  WebAPI fetch / WebSocket
signals                   X               WIP                yes
========================  ==============  =================  =========================

Node supports threads using ``--experimental-wasm-threads`` command line option.


CPython with WASM
=================

Status
------

* **WARNING**: WASM support is highly experimental! Lots of features are not working yet.
* April 2022: Christian Heime's talk at Pycon DE:
  `Python 3.11 in the web browser - A journey
  <https://speakerdeck.com/tiran/python-3-dot-11-in-the-web-browser-a-journey-pycon-de-2022-keynote>`_
* April 2022: WASM binary is ~4.5 MB compressed with staic, reduced stdlib.
  4.6 MB wasm (compressed 1.5 MB), 2.7 MB stdlib bytecode, some JS.
* January 2022, browser target: almost 10 MB (6.5 MB WASM, 2.9 MB stdlib, some JS)

Python on WASM
--------------

Browser, Node and Pyodide targets:

* ``sys.platform`` is ``'emscripten'``
* ``os.name`` is ``'posix'``
* ``platform.machine()`` is ``'wasm32'`` or ``'wasm64'``
* ``platform.release()``: ``'1.0'``
* ``platform.version()``: ``'#1'``
* Example of ``platform.platform()``: ``'Emscripten-1.0-wasm32-32bit'``
* Example ``os.uname()``: ``posix.uname_result(sysname='Emscripten', nodename='emscripten', release='1.0', version='#1', machine='wasm32')``

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

Python WASM browser REPL
========================

Christian Heimes' REPL:

* April 2022: Python 3.11 alpha 6
* https://cheimes.fedorapeople.org/python-wasm/
* Networking, subprocesses, and threading are not available

Ethan Smith's REPL

* April 2022: Python 3.11 alpha 7
* https://repl.ethanhs.me/
* https://github.com/ethanhs/python-wasm

Python WASM detailed status
===========================

Disabled C extensions
---------------------

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

Tests skipped in a browser
--------------------------

Result of `pmp-p's Python build
<https://pmp-p.github.io/python-wasm-plus/python311.html?org.python3.11.0>`_ on
Firefox 99::

    == Tests result: SUCCESS ==

    283 tests OK.

    95 tests skipped:
        test__xxsubinterpreters test_asdl_parser test_asyncgen
        test_asynchat test_asyncio test_asyncore test_check_c_globals
        test_clinic test_cmd_line test_concurrent_futures
        test_contextlib_async test_curses test_dbm_gnu test_dbm_ndbm
        test_devpoll test_doctest test_docxmlrpc test_embed test_epoll
        test_faulthandler test_fcntl test_file_eintr test_fork1
        test_ftplib test_gdb test_grp test_httplib test_httpservers
        test_idle test_imaplib test_interpreters test_ioctl test_kqueue
        test_launcher test_lzma test_mmap test_msilib
        test_multiprocessing_fork test_multiprocessing_forkserver
        test_multiprocessing_main_handling test_multiprocessing_spawn
        test_nis test_openpty test_ossaudiodev test_pdb test_pipes
        test_poll test_poplib test_pty test_pwd test_readline
        test_regrtest test_repl test_resource test_select test_selectors
        test_smtplib test_smtpnet test_socket test_socketserver test_spwd
        test_ssl test_startfile test_subprocess test_sys_settrace
        test_syslog test_tcl test_telnetlib test_thread
        test_threadedtempfile test_threading test_threading_local test_tix
        test_tk test_tools test_ttk_guionly test_ttk_textonly test_turtle
        test_urllib2 test_urllib2_localnet test_urllib2net test_urllibnet
        test_venv test_wait3 test_wait4 test_webbrowser test_winconsoleio
        test_winreg test_winsound test_wsgiref test_xmlrpc test_xmlrpc_net
        test_zipfile64 test_zipimport_support test_zoneinfo

    1 test run no tests:
        test_dtrace

    Total duration: 2 hour 8 min
    Tests result: SUCCESS

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

Misc
====

* https://caniuse.com/wasm
