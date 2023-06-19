.. _import:

+++++++++++++
Python Import
+++++++++++++

See also :ref:`Python importtime <importtime>` and :ref:`Python standard library <stdlib>`.

Implementation
==============

In short, the built-in ``__import__`` function (``builtins.__import__``) calls
``PyImport_ImportModuleLevelObject()`` which calls
``importlib._find_and_load()`` if the module is not cached in ``sys.modules``.

The implementation is splitted in multiple files in C and Python code. Main
files:

* ``Lib/importlib/_bootstrap.py``
* ``Lib/importlib/_bootstrap_external.py``
* ``Python/import.c``

The importlib package was added to Python 3.1. In Python 3.3, the import
machinery was rewritten based on the importlib package.

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

In short, call ``importlib._find_and_load(name)`` if the module is not cached
in ``sys.modules``.

Function implemented in ``Python/import.c``. Simplified explanation (look at
the implementation for details):

* Get the module from ``sys.modules``. If the module is already cached: return
  it.
* Call ``importlib._find_and_load(name)``.
* If ``fromlist`` is a non-empty list (if it's true),
  call ``importlib._handle_fromlist(module, fromlist, import_func)``
  where ``import_func`` is ``builtins.__import__``.

Python startup
--------------

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

  * Call ``_frozen_importlib._install(sys, _imp)``

Frozen modules
--------------

* ``Modules/config.c`` implements ``_PyImport_Inittab``:
  file generated from ``Modules/config.c.in`` by ``Modules/makesetup``.
* Example of an entry: ``{"_imp", PyInit__imp}``.
* ``PyImport_Inittab`` is initialized to ``_PyImport_Inittab``
* ``PyImport_ExtendInittab()`` copies ``PyImport_Inittab`` to ``inittab_copy``
* ``_PyRuntime.imports.inittab``
