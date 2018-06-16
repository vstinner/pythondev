.. _cpython:

+++++++
CPython
+++++++

See also:

* :ref:`CPython buildbots <ci>`
* :ref:`Compile CPython on Windows <windows>`

Python developer mode
=====================

https://mail.python.org/pipermail/python-ideas/2016-March/039314.html

Strict developer mode::

    PYTHONMALLOC=debug python3.6 -Werror -bb -X faulthandler script.py

Developer mode::

    PYTHONMALLOC=debug python3.6 -Wd -b -X faulthandler script.py

* Show ``DeprecationWarning`` and ``ResourceWarning warnings``: ``python -Wd``
* Show ``BytesWarning`` warning: ``python -b``
* Enable ``faulthandler`` to get a Python traceback on segfault and fatal
  errors: ``python -X faulthandler``
* Debug hooks on Python memory allocators: ``PYTHONMALLOC=debug``
* Enable Python assertions (assert) and set ``__debug__`` to ``True``: remove
  (or just ignore) -O or -OO command line arguments

See also ``PYTHONASYNCIODEBUG=1`` for asyncio.

=> implementated in Python 3.7 as: "python3 -X dev" or PYTHONDEVMODE=1 !


CPython infra
=============

Python infrastructure
---------------------

* http://infra.psf.io/
* https://status.python.org/ Status of services maintained by the Python infra
  team
* https://github.com/python/psf-chef/

  - `doc/nodes.rst
    <https://github.com/python/psf-chef/blob/master/doc/nodes.rst>`_
  - `doc/roles.rst
    <https://github.com/python/psf-chef/blob/master/doc/roles.rst>`_

* https://github.com/python/psf-salt/
* PSF pays a full-time sysadmin to maintain the Python infra: XXX
* https://www.python.org/psf/league/
* Managed services: http://infra.psf.io/overview/#details-of-various-services
* http://www.pythontest.net/ used by the test suite, see
  https://github.com/python/pythontestdotnet/

Services used by unit tests
---------------------------

* pythontest.net services:

  * `pythontestdotnet <https://github.com/python/pythontestdotnet>`_: source of
    pythontest.net (resources used for Python test suite).
  * test_urllib2net: http://www.pythontest.net/index.html#frag, tcp/80 (HTTP)
  * FTP: ftp://www.pythontest.net/README
  * Copies of unicode text files like http://www.pythontest.net/unicode/EUC-CN.TXT
  * test_hashlib test files like http://www.pythontest.net/hashlib/blake2b.txt
  * test_httplib: self-signed.pythontest.net, tcp/443 (HTTPS)
  * test_robotparser: http://www.pythontest.net/elsewhere/robots.txt
  * test_socket: испытание.pythontest.net

* snakebite.net::

    # Testing connect timeout is tricky: we need to have IP connectivity
    # to a host that silently drops our packets.  We can't simulate this
    # from Python because it's a function of the underlying TCP/IP stack.
    # So, the following Snakebite host has been defined:
    blackhole = resolve_address('blackhole.snakebite.net', 56666)

    # Blackhole has been configured to silently drop any incoming packets.
    # No RSTs (for TCP) or ICMP UNREACH (for UDP/ICMP) will be sent back
    # to hosts that attempt to connect to this address: which is exactly
    # what we need to confidently test connect timeout.

    # However, we want to prevent false positives.  It's not unreasonable
    # to expect certain hosts may not be able to reach the blackhole, due
    # to firewalling or general network configuration.  In order to improve
    # our confidence in testing the blackhole, a corresponding 'whitehole'
    # has also been set up using one port higher:
    whitehole = resolve_address('whitehole.snakebite.net', 56667)

* news.trigofacile.com:

  * Used by test_nntplib
  * NNTP (tcp/119) and and NNTP/SSL (tcp/563)
  * Server administrator: julien@trigofacile.com

* ipv6.google.com:

  * test_ssl uses it to test IPv6: HTTP (tcp/80) and HTTPS (tcp/443)

* sha256.tbs-internet.com:

  * test_ssl uses it to test x509 certificate signed by SHA256: HTTPS (tcp/443)

python.org
----------

* https://github.com/python/pythondotorg/ Source code of python.org
* wiki.python.org runs MoinMoin

Package Index (PyPI)
--------------------

* https://pypi.org/ "Warehouse", the new Python Package Index,

  - https://github.com/pypa/warehouse

* https://pypi.python.org/ "Python Cheeseshop", the old Python Package Index
* Python CDN: http://infra.psf.io/services/cdn/

cpython GitHub project
----------------------

* https://github.com/python/cpython/
* GitHub uses mention-bot: https://github.com/facebook/mention-bot

  * https://github.com/mention-bot/how-to-unsubscribe
  * userBlacklist, userBlacklistForPR in `CPython .mention-bot
    <https://github.com/python/cpython/blob/master/.mention-bot>`_
  * Adding you GitHub login to userBlacklistForPR stops the mention bot from
    mentioning anyone on your PRs.

* https://github.com/python/core-workflow/tree/master/cherry_picker/

Misc
----

* http://bugs.python.org/ Bug tracker (modified instance of Roundup)

  * https://pypi.python.org/pypi/roundup
  * Meta bug tracker: http://psf.upfronthosting.co.za/roundup/meta/
    (bug in the bug tracker software)

* Mailing lists: https://mail.python.org/mailman/listinfo

  - python-dev
  - python-ideas
  - python-list
  - lot of Special Interest Groups (SIG)
  - etc.

* http://buildbot.python.org/

  * `CPython 3.6
    <http://buildbot.python.org/all/waterfall?category=3.6.stable&category=3.6.unstable>`_
  * `CPython 3.x (master)
    <http://buildbot.python.org/all/waterfall?category=3.x.stable&category=3.x.unstable>`_
  * `Custom builders
    <https://docs.python.org/devguide/buildbots.html#custom-builders>`_
  * `buildmaster-config
    <https://github.com/python/buildmaster-config/tree/master/master>`_
    (configuration)
  * `Fork of BuildBot running on buildbot.python.org
    <https://github.com/python/buildbot/>`_

* GitHub CLA bot: XXX

Documentation
-------------

* https://docs.python.org/ Python online documentation
* https://github.com/python/docsbuild-scripts/
* Mirror: http://python.readthedocs.io/en/latest/ Still use the old Mercurial repository.
* https://www.python.org/dev/peps/pep-0545/ i18n doc

.. _vendored-libs:

Vendored external libraries
===========================

Update dependencies: https://github.com/python/cpython-source-deps/blob/master/README.rst

See my `external_versions.py
<https://github.com/vstinner/misc/blob/master/cpython/external_versions.py>`_
script: external version of embedded libraries from CPython source code
(locally).

On security branches, some dependencies are outdated because no more macOS nor
Windows installer is built. It was decided to not upgrade outdated zlib 1.2.5
in Python 3.3.7, since it's specific to Windows, and no Windows user is
expected to build his/her own Python 3.3 anymore.

* ``Modules/_ctypes/libffi/``: copy of `libffi <https://sourceware.org/libffi/>`_

  * Removed from Python 3.7: https://bugs.python.org/issue27979

* ``Modules/_ctypes/libffi_osx/``: `libffi <https://sourceware.org/libffi/>`_ for macOS?

  * Version: ``grep PACKAGE_VERSION Modules/_ctypes/libffi_osx/include/fficonfig.h``
  * Python 2.7-3.6 uses libffi 2.1

* ``Modules/_ctypes/libffi_msvc/``: `libffi <https://sourceware.org/libffi/>`_
  for Windows (for Microsoft Visual Studio)?

  * Version: second line of ``Modules/_ctypes/libffi_msvc/ffi.h``
  * Python 2.7-3.6 use libffi 2.0 beta, copied from ctypes-0.9.9.4 in 2006

* ``Modules/expat/``: copy of `libexpat <https://github.com/libexpat/libexpat/>`_

  * ``./configure --with-system-expat``
  * Rationale: https://mail.python.org/pipermail/python-dev/2017-June/148287.html
  * Used on Windows and macOS, Linux distributions use system libexpat
  * Version: search for ``XML_MAJOR_VERSION`` in ``Modules/expat/expat.h``
  * Script to update it: see attached script to https://bugs.python.org/issue30947
  * Recent update: https://bugs.python.org/issue30947
  * Python 2.7, 3.3-3.6 use libexpat 2.2.1

* ``Modules/zlib/``: copy of `zlib <https://zlib.net/>`_

  * Version: ``ZLIB_VERSION`` in ``Modules/zlib/zlib.h``
  * Only used on Windows (system zlib is used on macOS and Linux)
  * Python zlib module not built if system zlib is older than 1.1.3
  * Script to update it: XXX
  * Recent update: https://bugs.python.org/issue29169
  * Python 2.7, 3.4 and 3.5, 3.6 use zlib 1.2.11
  * Python 3.3 uses zlib 1.2.5: https://github.com/python/cpython/pull/3108

* ``Modules/_decimal/libmpdec/``: copy of `libmpdec <http://www.bytereef.org/mpdecimal/>`_

  * Option: ``./configure --with-system-libmpdec``
  * Included since Python 3.3 for _decimal
  * Maintained by Stefan Krah
  * Version: ``MPD_VERSION`` in ``Modules/_decimal/libmpdec/mpdecimal.h``
  * Used on all platforms
  * Script to update: XXX
  * Recent update: https://bugs.python.org/issue26621
  * Python 3.6 uses libmpdec 2.4.2 (released at february 2016)
  * Python 3.4 and 3.5 uses libmpdec 2.4.1
  * Python 3.3 uses libmpdec 2.4.0

* Windows and macOS installers include OpenSSL (binary library)

  * Windows version: search for ``openssl-`` in ``PCbuild/get_externals.bat``
  * macOS version: search for ``openssl-`` in ``Mac/BuildScript/build-installer.py``
  * See: http://python-security.readthedocs.io/ssl.html#openssl-versions
  * See: https://www.python.org/dev/peps/pep-0543/

* Windows and macOS installers include `SQLite <https://www.sqlite.org/>`_

  * Recent update: https://bugs.python.org/issue28791
  * macOS: search for ``SQLite`` in ``Mac/BuildScript/build-installer.py``
  * Windows: search for ``sqlite-`` in ``PCbuild/get_externals.bat``

See also `cpython-bin-deps <https://github.com/python/cpython-bin-deps>`_
and `cpython-source-deps <https://github.com/python/cpython-source-deps>`_.


Supported architectures
=======================

* Intel x86 and x86_64 (aka AMD64)
* PPC64
* ARMv7

Maybe some others?

Supported platforms
===================

PEP 11 lists removal of supported platforms:

* MS-DOS: 2014:
  `bpo-22591: Drop support of MS-DOS (DJGPP compiler)
  <https://bugs.python.org/issue22591>`_,
  `commit b71c7dc9 <https://github.com/python/cpython/commit/b71c7dc9ddd6997be49ed6aaabf99a067e2c0388>`_
* Python 3.4: VMS, OS/2, Windows 2000

  * VMS:
    `bpo-16136: Removal of VMS support <https://bugs.python.org/issue16136>`_,
    `main removal commit <https://github.com/python/cpython/commit/af01f668173d4061893148b54a0f01b91c7716c2>`_
    (`remove VMSError doc commit
    <https://github.com/python/cpython/commit/b2788fe854173b6b213010a7462c05594d703c06>`_)

* Python 3.7: IRIX

PEP 11 on Windows:

    CPython's Windows support now follows [Microsoft product support
    lifecycle]. A new feature release X.Y.0 will support all Windows releases
    whose extended support phase is not yet expired. Subsequent bug fix
    releases will support the same Windows releases as the original feature
    release (even if the extended support phase has ended).

Windows:

* `Windows Supported Versions in Python
  <https://docs.python.org/dev/using/windows.html#supported-versions>`_
  (in the Python development ``master`` branch)
* Windows Vista support dropped in Python 3.7
* Windows XP support dropped in Python 3.5
* Windows 2000 support dropped in Python 3.4
* `bpo-23451 <https://bugs.python.org/issue23451>`_, 2015-03: "Python 3.5 now
  requires Windows Vista or newer". See `change1
  <https://hg.python.org/cpython/rev/57e2549cc9a6>`_ and `change2
  <https://hg.python.org/cpython/rev/f64d0b99d405>`_.
* Python 2.7 supports Windows XP and newer

FreeBSD:

* Python 3.7 dropped support for FreeBSD 9 and older.
* FreeBSD 9 buildbot wokers have been removed in 2017

macOS:

* 2018-05-28: macOS Leopard (macOS 10.6, 2008) is `currently
  <https://mail.python.org/pipermail/python-dev/2018-May/153725.html>`_ the
  minimum officially supported macOS version.
* February 2018: Tiger (macOS 10.4, 2004) buildbots removed, which indirectly
  means that Tiger is no longer officially supported.

Well supported platforms on Python 3.6 and 2.7:

* Linux
* Windows: Vista and newer for Python 3.6, XP and newer for Python 2.7
* FreeBSD

Tested by Travis CI and buildbots.

Supported platform with best effort support:

* Android API 24
* OpenBSD
* NetBSD
* Solaris, OpenIndiana
* AIX

Platforms not supported officially:

* Cygwin
* MinGW
* HP-UX

Unofficial projects:

* `Python for OpenVMS <https://www.vmspython.org/>`_
* `PythonD <http://www.caddit.net/pythond/>`_:  PythonD is a 32-bit,
  multi-threaded, networking- and OpenGL-enabled Python interpreter for DOS and
  Windows.
