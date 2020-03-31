+++++++++++++++++++++++
Add a field to PyConfig
+++++++++++++++++++++++

Documentation
=============

* https://docs.python.org/dev/c-api/init_config.html
* https://www.python.org/dev/peps/pep-0587/


Main files
==========

* ``Python/preconfig.c``: _PyPreConfig_Read()
* ``Python/initconfig.c``: PyConfig_Read()
* ``Include/cpython/initconfig.h``: PyConfig structure
* ``Include/internal/pycore_initconfig.h``

Python initialization and finalization:

* ``Modules/main.c``:

  * pymain_main()
  * pymain_free()
  * Py_BytesMain()
  * Py_RunMain()

* ``Python/pylifecycle.c``:

  * Py_InitializeFromConfig()
  * Py_PreInitialize()
  * Py_FinalizeEx()

Add a field to PyConfig
=======================

* ``Include/cpython/initconfig.h``: Add a new field into ``PyConfig`` structure
* ``Python/initconfig.c``:

  * Initialize the field in ``_PyConfig_InitCompatConfig()`` if the default
    is not zero
  * ``_PyConfig_Copy()``: add ``COPY_ATTR(field)``
  * ``config_as_dict()``: add ``SET_ITEM_INT(field)``
  * ``PyConfig_Read()``: if needed, add an assertion at the function exit
    to validate that the field is valid.

* ``Lib/test/test_embed.py``: Add field default value
  to ``InitConfigTests.CONFIG_COMPAT``
* ``Doc/c-api/init_config.rst``: Document the new field.

Add a field to PyPreConfig
==========================

* ``Include/cpython/initconfig.h``: Add a new field into ``PyPreConfig`` structure
* ``Python/preconfig.c``:

  * Initialize the field in ``_PyPreConfig_InitCompatConfig()`` if the default
    is not zero
  * ``preconfig_copy()``: add ``COPY_ATTR(field)``
  * ``_PyPreConfig_AsDict()``: add ``SET_ITEM_INT(field)``
  * ``preconfig_read()``: if needed, add an assertion at the function exit
    to validate that the field is valid.

* ``Lib/test/test_embed.py``: Add field default value
  to ``InitConfigTests.PRE_CONFIG_COMPAT``
* ``Doc/c-api/init_config.rst``: Document the new field.


Add an unit test for new PyPreConfig or PyConfig field
======================================================

* ``Programs/_testembed.c``, ``test_init_from_config()``: Set the field to
  a value different than the default.
* ``Lib/test/test_embed.py``: Update ``test_init_from_config()``
  of ``InitConfigTests``.


Add a new command line option
=============================

* ``Python/getopt.c``: Update ``SHORT_OPTS`` or ``_PyOS_LongOption``
* ``Python/initconfig.c``: Modify config_parse_cmdline()
* Document the new env option

  * ``Python/initconfig.c``: Update one of the ``usage_xxx`` variables
  * ``Doc/using/cmdline.rst``
  * ``Misc/python.man``

Example of ``Python/initconfig.c`` usage::

    -B     : don't write .pyc files on import; also PYTHONDONTWRITEBYTECODE=x\n\

Example of ``Doc/using/cmdline.rst`` entry::

    .. cmdoption:: -d

       Turn on parser debugging output (for expert only, depending on compilation
       options).  See also :envvar:`PYTHONDEBUG`.

* Add an unit test. ``Lib/test/test_cmd_line.py``, ``Lib/test/test_embed.py``
  (``InitConfigTests``) or another test depending on how the value is exposed
  in Python.


Add an environment variable
===========================

* ``Python/initconfig.c``:

  * Modify the appropriate helper function of ``PyConfig_Read()`` to read
    the environment variable.
  * Update ``usage_xxx`` to document the new env var

Example::

    _Py_get_env_flag(use_env, &config->parser_debug, "PYTHONDEBUG");

* ``Doc/using/cmdline.rst``: Document the new env var
* ``Misc/python.man``: Document the new env var
* ``Programs/_testembed.c``: Update ``test_init_from_config()``
  and ``set_most_env_vars()`` to set the env var,
  ``PyConfig`` must have the priority.
* ``Lib/test/test_embed.py``: Update ``InitConfigTests``.

Note: environment variable with a name starting with ``PYTHON`` are ignored
when using ``-E`` or ``-I`` command line options.
