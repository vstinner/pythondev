++++++++++++++++++
Run Python on WASI
++++++++++++++++++

Python on WASI
==============

* ``sys.platform`` is ``'wasi'``
* ``os.name`` is ``'posix'``
* ``platform.machine()`` is ``'wasm32'``
* Example of ``platform.platform()``: ``'wasi-0.0.0-wasm32-32bit'``
* Example ``os.uname()``: ``posix.uname_result(sysname='wasi', nodename='(none)', release='0.0.0', version='0.0.0', machine='wasm32')``

Build Python for WASI
=====================

Documentation: https://devguide.python.org/getting-started/setup-building/#wasi

Create a container from "wasicontainer" cpython-dev (container based on Fedora)::

    git clone https://github.com/python/cpython-devcontainers
    cd cpython-devcontainers
    podman build wasicontainer --tag wasi-cpython-dev

In a CPython checkout, start by removing all local files not tracked by Git::

    git clean -fdx

In the clean CPython checkout, run the container::

    podman run -it --rm -v $PWD:/workspace:O -w/workspace wasi-cpython-dev

Now inside the container, build Python for WASI (in debug mode)::

    python3 Platforms/WASI build -- --config-cache --with-pydebug

Run Python::

    cross-build/wasm32-wasip1/python.sh

Run the test suite::

    cross-build/wasm32-wasip1/python.sh -m test

See also: https://github.com/python/cpython/blob/main/.github/workflows/reusable-wasi.yml


Misc
====

* https://github.com/bytecodealliance/wasmtime-py
