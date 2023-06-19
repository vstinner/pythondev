.. _import:

+++++++++++++
Python Import
+++++++++++++

See also :ref:`Python importtime <importtime>` and :ref:`Python standard library <stdlib>`.

Implementation
==============

In short, the built-in ``__import__`` function (``builtins.__import__``) calls
the C function ``PyImport_ImportModuleLevelObject()`` which calls
``importlib._bootstrap._find_and_load()`` if the module is not cached in
``sys.modules``.

The implementation is splitted in multiple files in C and Python code. Main
files:

* ``Lib/importlib/_bootstrap.py``: frozen as ``_frozen_importlib``
* ``Lib/importlib/_bootstrap_external.py``: frozen as ``_frozen_importlib_external``
* ``Python/import.c``

The API is splitted in multiple parts:

* ``importlib.machinery``: internals
* ``importlib.util``: public helper functions
* private ``_imp`` extension
* C API like ``PyImport_ImportModuleLevelObject()``

The importlib package was added to Python 3.1. In Python 3.3, the import
machinery was rewritten based on the importlib package.

importlib concepts
------------------

* Module finder (*finder*) with a ``find_spec()`` method.
  ``sys.meta_path`` is a list of importlib finders.
* Path hooks used by PathFinder: ``sys.path_hooks`` list.
  Usually: ``[zipimport.zipimporter, importlib._bootstrap_external.FileFinder]``.
  To be exact, the second one is a function which creates a FileFinder instance
  if a path a directory.
* Module loader (*loader*) with ``create_module()`` and ``exec_module()`` methods.
  Example: ``importlib.machinery.SourceFileLoader``.
* Module specification (*spec*): ``importlib.machinery.ModuleSpec`` which has a
  loader.
* ``sys.path_importer_cache`` used by ``PathFinder``

IMPORT_NAME bytecode
--------------------

In Python 3.13, ``import <name>`` is implemented in ``Python/bytecodes.c`` with
the ``IMPORT_NAME(name, fromlist, level)`` bytecode: it has a ``name`` argument
and two stack arguments: ``fromlist`` and ``level``. Usually, ``fromlist`` is
``None`` and ``level`` is equal to ``0``.  The ``IMPORT_NAME`` bytecode calls
the ``ceval.c`` ``import_name()`` function:

* Get ``__import__`` function of the ``builtins`` name (usually the
  ``builtins`` module dictionary)
* Call ``__import__(name, frame_globals, frame_locals, fromlist, level)``.
  There is a fast-path when ``__import__`` in the frame builtins is the
  built-in ``__import__`` function (if the function was not overriden):
  call ``PyImport_ImportModuleLevelObject(name, frame_globals, frame_locals, fromlist, level)`` directly.

Example::

    >>> def f():
    ...     import name
    ...     return name
    ...
    >>> dis.dis(f)
      1           0 RESUME                   0

      2           2 LOAD_CONST               1 (0)
                  4 LOAD_CONST               0 (None)
                  6 IMPORT_NAME              0 (name)
                  8 STORE_FAST               0 (name)

      3          10 LOAD_FAST                0 (name)
                 12 RETURN_VALUE

Built-in __import__() function
------------------------------

``builtins.__import__()`` is implemented in ``Python/bltinmodule.c``. It just
calls ``PyImport_ImportModuleLevelObject(name, globals, locals, fromlist, level)``.

PyImport_ImportModuleLevelObject(name, globals, locals, fromlist, level)
------------------------------------------------------------------------

In short, call ``importlib._bootstrap._find_and_load(name)`` if the module is
not cached in ``sys.modules``.

Function implemented in ``Python/import.c``. Simplified explanation (look at
the implementation for details):

* Get the module from ``sys.modules``. If the module is already cached: return
  it.
* Call ``importlib._bootstrap._find_and_load(name)``.
* If ``fromlist`` is a non-empty list (if it's true),
  call ``importlib._handle_fromlist(module, fromlist, import_func)``
  where ``import_func`` is ``builtins.__import__``.

importlib _find_and_load()
--------------------------

In short:

* Call the ``find_spec()`` method of each ``sys.meta_path`` finder. Use the
  first matching *spec* (not ``None``).
* ``module = loader.create_module(spec)``.
* ``sys.modules[name] = module``
* ``loader.exec_module(module)``

``importlib._bootstrap._find_and_load(name, import_func)`` pseudo-code:

* Call ``spec = _find_spec(name, path)`` where *path* is ``None``
  or ``parent_module.__path__``.
* Call ``module = module_from_spec(spec)``
* Cache the module in ``sys.modules``
* Call ``spec.loader.exec_module(module)``, except for namespace packages which
  have no loader

``importlib._bootstrap._find_spec(name, path, target=None)`` pseudo-code:

* For each finder of ``sys.meta_path``,
  call ``finder.find_spec(name, path, target)``.
* If a ``find_spec()`` method result is not ``None``, return *spec*.

``importlib._bootstrap.module_from_spec(spec)`` pseudo-code:

* Call ``spec.loader.create_module(spec)``
* Call ``_init_module_attrs(spec, module)`` which sets module attributes:

  * ``__cached__``
  * ``__file__``
  * ``__loader__``
  * ``__name__``
  * ``__package__``
  * ``__path__``
  * ``__spec__``

importlib.import_module(name, package=None)
-------------------------------------------

Implemented in ``Lib/importlib/__init__.py``, call
``importlib._bootstrap._gcd_import(name[level:], package, level)`` which calls
``importlib._bootstrap._find_and_load()``. Similar to ``builtins.__import__()``
function.

Load a namespace package
------------------------

A namespace package has no ``__init__.py`` file.

Implemented in ``Lib/importlib/_bootstrap_external.py`` with ``PathFinder``.
``sys.meta_path[2]`` is an ``_frozen_importlib_external.PathFinder`` instance

Call ``PathFinder.find_spec(name, path=None, target=None)``:

* Call ``PathFinder._get_spec(name, sys.path, target=None)``:

  * For each ``sys.path`` entry, get
    ``PathFinder._path_importer_cache(entry)``: ``FileFinder`` instance.
    Call ``FileFinder.find_spec(name, target)`` method.
  * If there is a match, store ``spec.submodule_search_locations``
  * If there was at least one match, combine all ``spec.submodule_search_locations``
    as a *namespace_path* and create a ``ModuleSpec`` with it which has no
    loader (``None``).

``PathFinder._path_importer_cache(entry)`` uses ``sys.path_importer_cache``.



Python startup
==============

* ``_PyBuiltin_Init()`` creates the ``builtins`` module.
  The ``builtins`` module dictionary is stored in ``interp->builtins``.
* ``_PyImport_InitCore()`` in ``Python/import.c``:

  * Imports the ``_frozen_importlib`` frozen module, known as "importlib"
  * Call ``bootstrap_imp()``: create the ``_imp`` extension

    * Mock a ``ModuleSpec`` object as ``spec``
    * Call ``create_builtin(tstate, name, spec)``:
      internal function of ``_imp.create_builtin()``. It calls
      ``PyInit__imp()`` of ``_PyRuntime.imports.inittab`` (as the ``"_imp"`` entry).
    * Call ``exec_builtin_or_dynamic(mod)`` (``_imp.exec_builtin()``):
      call ``PyModule_ExecDef(mod)`` which calls ``imp_module_exec(mod)``:
      the ``Py_mod_exec`` slot of ``imp_module.m_slots``.

  * Store the ``_imp`` extension in ``sys.modules``
  * Call ``_frozen_importlib._install(sys, _imp)``

    * Set up the spec for existing builtin/frozen modules
    * Add ``BuiltinImporter`` and ``FrozenImporter`` to ``sys.meta_path``

* Call ``_PyImport_InitExternal()``:

  * Call ``_frozen_importlib._install_external_importers()``:

    * Import ``_frozen_importlib_external``
    * Call ``_frozen_importlib_external._install(_frozen_importlib)``

      * Add FileFinder path hook to ``sys.path_hook``
      * Add FileFinder to ``sys.meta_path``

  * Import ``zipimport.zipimporter`` and prepends it to ``sys.path_hooks``


Frozen modules
==============

* ``Modules/config.c`` implements ``_PyImport_Inittab``:
  file generated from ``Modules/config.c.in`` by ``Modules/makesetup``.
* Example of an entry: ``{"_imp", PyInit__imp}``.
* ``PyImport_Inittab`` is initialized to ``_PyImport_Inittab``
* ``PyImport_ExtendInittab()`` copies ``PyImport_Inittab`` to ``inittab_copy``
* ``_PyRuntime.imports.inittab``


Links
=====

* `Python importlib documentation
  <https://docs.python.org/dev/library/importlib.html>`_
* `PEP 451 – A ModuleSpec Type for the Import System
  <https://peps.python.org/pep-0451/>`_ (2013, Python 3.4) by Eric Snow
* `Unravelling the import statement
  <https://snarky.ca/unravelling-the-import-statement/>`_
  (January 2021) by Brett Cannon
* `If I were designing Python's import from scratch
  <https://snarky.ca/if-i-were-designing-imort-from-scratch/>`_
  (December 2015) by Brett Cannon
