++++++++++++++++++++++++++++++++++++
Compile Python to WebAssembly (WASM)
++++++++++++++++++++++++++++++++++++

CPython with WASM
=================

Status
------

* January 2022: almost 10 MB (6.5 MB WASM, 2.9 MB stdlib, some JS)
* WASI is not supported: it will likely be supported eventually.

Python on WASM
--------------

* ``sys.platform`` is ``emscripten``
* ``os.name`` is ``'posix'``

Build
-----

Cross-build Python to WASM:

* `configure --with-emscripten-target=[browser|node]
  <https://docs.python.org/dev/using/configure.html#cmdoption-with-emscripten-target>`_
* `configure --enable-wasm-dynamic-linking
  <https://docs.python.org/dev/using/configure.html#cmdoption-enable-wasm-dynamic-linking>`_
* ``configure --with-suffix`` is set to ``.wasm`` by default:
  the ``EXE`` variable in Makefile.

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

WASM limitations
================

* No socket (yet): use Pyodide for that
* No subprocess
* threads are currently not supported in browsers, but are supported
  in Node.JS using ``--experimental-wasm-threads`` command line option.

Pyodide
=======

Python distribution for the browser and Node.js based on WebAssembly:

* https://github.com/pyodide/pyodide
* https://pyodide.org/

Ethan Smith's REPL
==================

* https://repl.ethanhs.me/
* https://github.com/ethanhs/python-wasm

Misc
====

* https://caniuse.com/wasm
