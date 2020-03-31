+++++++++++++++++++++++
Add a field to PyConfig
+++++++++++++++++++++++

Add a field to PyConfig
=======================

* ``Include/cpython/initconfig.h``: Add a new field into ``PyConfig`` structure
* ``Python/initconfig.c``:

  * Initialize the field in ``_PyConfig_InitCompatConfig`` if the default
    is not zero
  * Use COPY_ATTR(field) in ``_PyConfig_Copy()``
  * Use SET_ITEM_INT(field) in ``config_as_dict()``
  * PyConfig_Read(): if needed, add an assertion at the function exit
    to validate that the field is valid.

* ``Lib/test/test_embed.py``: Update unit tests. Maybe add a new test.
* ``Doc/c-api/init_config.rst``: Document the new field.

Add a new command line option
=============================

* ``Python/getopt.c``: Update ``SHORT_OPTS`` or ``_PyOS_LongOption``
* ``Python/initconfig.c``:

  * Update ``usage_xxx`` variables to document the new option
  * Modify the appropriate helper function of ``PyConfig_Read()`` to parse
    the option

* ``Doc/using/cmdline.rst``: Document the new option
* ``Misc/python.man``: Document the new env option
* Add an unit test. ``Lib/test/test_cmd_line.py``, ``Lib/test/test_embed.py``
  (``InitConfigTests``) or another test depending on how the value is exposed
  in Python.

Add an environment variable
===========================

* ``Python/initconfig.c``:

  * Modify the appropriate helper function of ``PyConfig_Read()`` to read
    the environment variable.
  * Update ``usage_xxx`` to document the new env var

* ``Doc/using/cmdline.rst``: Document the new env var
* ``Misc/python.man``: Document the new env var
* ``Programs/_testembed.c``: Update test_init_from_config() and set_most_env_vars()
  to set the env var, PyConfig must have the priority.
* ``Lib/test/test_embed.py``: Update InitConfigTests if needed.
