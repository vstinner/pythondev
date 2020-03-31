+++++++++++++++++++++++
Add a field to PyConfig
+++++++++++++++++++++++

Steps to add a field to PyConfig
================================

* Include/cpython/initconfig.h: Add a new field into ``PyConfig`` structure
* Python/initconfig.c:

  * Initialize the field in ``_PyConfig_InitCompatConfig`` if the default
    is not zero
  * Use COPY_ATTR(field) in ``_PyConfig_Copy()``
  * Use SET_ITEM_INT(field) in ``config_as_dict()``

* Lib/test/test_embed.py: Update unit tests. Maybe add a new test.
* Doc/c-api/init_config.rst: Document the new field.
