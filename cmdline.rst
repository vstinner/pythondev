+++++++++++++++++++
Python Command Line
+++++++++++++++++++

Add a new command line option or new environment variable
=========================================================

Modify Python/initconfig.c to read the new environment variable. Example::

    _Py_get_env_flag(use_env, &config->parser_debug, "PYTHONDEBUG");

Note: environment variable with a name starting with ``PYTHON`` are ignored
when using ``-E`` or ``-I`` command line options.

Document the option in ``Doc/using/cmdline.rst``. Example::

    .. cmdoption:: -d

       Turn on parser debugging output (for expert only, depending on compilation
       options).  See also :envvar:`PYTHONDEBUG`.

Document the option in ``Python/initconfig.c`` usage string. Example::

    -B     : don't write .pyc files on import; also PYTHONDONTWRITEBYTECODE=x\n\

Document the new option the in the manual page ``Misc/python.man``.

Add a test in ``Lib/test/test_cmd_line.py``.
