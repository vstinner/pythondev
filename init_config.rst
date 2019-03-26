+++++++++++++++++++++++++++++++++++
Python Initialization Configuration
+++++++++++++++++++++++++++++++++++

Current design document: `PEP 432 -- Restructuring the CPython startup sequence
<https://www.python.org/dev/peps/pep-0432/>`_ written by Nick Coghlan in 2012.

Python initialization
=====================

* Pre-initialization: encoding and memory allocators
* Core initialization: bare minimum Python runtime
* Main initialization: setup importlib, import site, etc.

Priority and relationship between configuration parameters
==========================================================

General rules, highest priority to lowest:

* ``_PyCoreConfig`` (options set explicitly by the user)
* ``_PyPreConfig`` (options set explicitly by the user)
* Configuration files
* Command line options
* Environment variables
* Global configuration variables

.. note::
   XXX is there a problem between the priority of PYTHONHOME env var and
   ``pybuilddir.txt`` configuration file?

Other rules:

* ``isolated`` sets ``use_environment`` to 0 and ``user_site_directory`` to 0
* ``legacy_windows_fs_encoding`` sets ``utf8_mode`` to 0
* ``dev_mode`` sets allocator to ``"debug"``, ``faulthandler`` to 1 and change
  warning filters. But ``PYTHONMALLOC`` has the priority over dev mode
  (``-X dev`` or ``PYTHONDEVMODE``)

Python Initialization C API
===========================

Official documentation: `Initialization, Finalization, and Threads
<https://docs.python.org/dev/c-api/init.html>`_.

Old APIs
--------

* ``Py_Initialize()``, ``Py_InitializeEx()``: initialize Python
* ``Py_Finalize()``, ``Py_FinalizeEx()``: finalize Python

_PyInitError (Python 3.8 internal API)
--------------------------------------

Return an error or a success:

* ``_Py_INIT_OK()``: success
* ``_Py_INIT_ERR(MSG)``: Python internal error
* ``_Py_INIT_USER_ERR(MSG)``: error caused by user configuration
* ``_Py_INIT_NO_MEMORY()``: out of memory
* ``_Py_INIT_EXIT(EXITCODE)``: exit Python with specified exit code

Read result:

* ``_Py_INIT_FAILED(err)``: Is the result an error or an exit?

_PyPreConfig (Python 3.8 internal API)
--------------------------------------

Pre-initialize Python:

* set memory allocators
* enable the UTF-8 mode if needed
* set the LC_CTYPE locale

If the encoding changes after reading the pre-configuration,
``_PyPreConfig_ReadFromArgv()`` clears the configuration and reads again the
pre-configuration. Two options can trigger this case:

* (PEP 538) If the LC_CTYPE locale is coerced, the locale encoding becomes
  UTF-8.
* (PEP 540) ``-X utf8`` and ``PYTHONUTF8=1`` enable the UTF-8 mode, whereas
  LC_CTYPE locale encoding can be different than UTF-8.

If the memory allocators are changed, a new ``_PyPreConfig`` must be allocated
with the new allocator and the old one should be freed with the old allocator.

API:

* ``_PyPreConfig`` structure
* ``_PyPreConfig_Read(_PyPreConfig*)``
* ``_PyPreConfig_ReadFromArgv(_PyPreConfig*, const _PyArgv*)``
* ``_PyPreConfig_Write(_PyPreConfig*)``: apply pre-configuration
* ``_Py_PreInitialize()``: pre-initialize Python
* ``_Py_PreInitializeFromPreConfig(_PyPreConfig *)``: pre-initialize Python
  with a pre-configuration

_PyPreConfig fields:

* ``allocator``
* ``coerce_c_locale_warn``
* ``coerce_c_locale``
* ``dev_mode``
* ``isolated``
* ``legacy_windows_fs_encoding``
* ``use_environment``
* ``utf8_mode``

_PyCoreConfig (Python 3.8 internal API)
---------------------------------------

Initialize Python:

* pre-initialize Python
* create the interpreter and thread state
* initialize builtin types, exceptions and functions
* import site module
* etc.

API:

* ``_PyCoreConfig`` structure
* ``_PyCoreConfig_Read(_PyCoreConfig *, const _PyPreConfig*)``: read configuration
* ``_PyCoreConfig_ReadFromArgv(_PyCoreConfig*, const _PyArgv*, const _PyPreConfig*)``: read configuration, parse command line arguments
* ``_PyCoreConfig_Write(const _PyCoreConfig*)``: apply configuration
* ``_Py_InitializeFromConfig(_PyCoreConfig)``: initialize Python with a configuration

_PyCoreConfig fields:

* ``argv``
* ``base_exec_prefix``
* ``base_prefix``
* ``buffered_stdio``
* ``bytes_warning``
* ``dll_path``
* ``dump_refs``
* ``exec_prefix``
* ``executable``
* ``faulthandler``
* ``filesystem_encoding``
* ``filesystem_errors``
* ``hash_seed``
* ``home``
* ``import_time``
* ``inspect``
* ``install_signal_handlers``
* ``interactive``
* ``legacy_windows_stdio``
* ``malloc_stats``
* ``module_search_path_env``
* ``module_search_paths``
* ``optimization_level``
* ``parser_debug``
* ``preconfig``
* ``prefix``
* ``program_name``
* ``program``
* ``pycache_prefix``
* ``quiet``
* ``run_command``
* ``run_filename``
* ``run_module``
* ``show_alloc_count``
* ``show_ref_count``
* ``site_import``
* ``skip_source_first_line``
* ``stdio_encoding``
* ``stdio_errors``
* ``tracemalloc``
* ``use_hash_seed``
* ``use_module_search_paths``
* ``user_site_directory``
* ``verbose``
* ``warnoptions``
* ``write_bytecode``
* ``xoptions``

_PyCoreConfig private fields:

* ``_check_hash_pycs_mode``
* ``_frozen``
* ``_install_importlib``

Configuration files
===================

* ``pyvenv.cfg``
* ``python._pth`` (Windows only)
* ``pybuilddir.txt`` (Unix only)

Global configuration variables
==============================

Variables:

* ``Py_BytesWarningFlag``
* ``Py_DebugFlag``
* ``Py_DontWriteBytecodeFlag``
* ``Py_FileSystemDefaultEncodeErrors``
* ``Py_FileSystemDefaultEncoding``
* ``Py_FrozenFlag``
* ``Py_HasFileSystemDefaultEncoding``
* ``Py_HashRandomizationFlag``
* ``Py_IgnoreEnvironmentFlag``
* ``Py_InspectFlag``
* ``Py_InteractiveFlag``
* ``Py_IsolatedFlag``
* ``Py_LegacyWindowsFSEncodingFlag`` (Windows only)
* ``Py_LegacyWindowsStdioFlag`` (Windows only)
* ``Py_NoSiteFlag``
* ``Py_NoUserSiteDirectory``
* ``Py_OptimizeFlag``
* ``Py_QuietFlag``
* ``Py_UTF8Mode``
* ``Py_UnbufferedStdioFlag``
* ``Py_VerboseFlag``
* ``_Py_HasFileSystemDefaultEncodeErrors``

Note: ``Py_HasFileSystemDefaultEncoding`` and
``_Py_HasFileSystemDefaultEncodeErrors`` are bad API to manage memory
allocations.

Command line options
====================

Usage::

    python3 [options]
    python3 [options] -c COMMAND
    python3 [options] -m MODULE
    python3 [options] SCRIPT

Options:

* ``-b``
* ``-B``
* ``-c COMMAND``
* ``--check-hash-based-pycs``
* ``-d``
* ``-E``
* ``-h``
* ``-i``
* ``-I``
* ``-J``
* ``-m MODULE``
* ``-O``
* ``-q``
* ``-R``
* ``-s``
* ``-S``
* ``-t``
* ``-u``
* ``-v``
* ``-V``
* ``-W WARNING``
* ``-x``
* ``-X XOPTION``
* ``-?``

Environment variables
=====================

* ``PYTHONCOERCECLOCALE``
* ``PYTHONDEBUG``
* ``PYTHONDEVMODE``
* ``PYTHONDONTWRITEBYTECODE``
* ``PYTHONDUMPREFS``
* ``PYTHONEXECUTABLE``
* ``PYTHONFAULTHANDLER``
* ``PYTHONHASHSEED``
* ``PYTHONHOME``
* ``PYTHONINSPECT``
* ``PYTHONIOENCODING``
* ``PYTHONLEGACYWINDOWSFSENCODING``
* ``PYTHONLEGACYWINDOWSSTDIO``
* ``PYTHONMALLOC``
* ``PYTHONMALLOCSTATS``
* ``PYTHONNOUSERSITE``
* ``PYTHONOPTIMIZE``
* ``PYTHONPATH``
* ``PYTHONPROFILEIMPORTTIME``
* ``PYTHONPYCACHEPREFIX,``
* ``PYTHONTRACEMALLOC``
* ``PYTHONUNBUFFERED``
* ``PYTHONUTF8``
* ``PYTHONVERBOSE``
* ``PYTHONWARNINGS``
* ``PYTHONWARNINGS``

Python issues
=============

* https://bugs.python.org/issue22257
* https://bugs.python.org/issue32030
* https://bugs.python.org/issue32124
* https://bugs.python.org/issue33932
* https://bugs.python.org/issue34008
* https://bugs.python.org/issue34170
* https://bugs.python.org/issue34589
* https://bugs.python.org/issue34639
* https://bugs.python.org/issue36142
* https://bugs.python.org/issue36202
* https://bugs.python.org/issue36204
* https://bugs.python.org/issue36301
