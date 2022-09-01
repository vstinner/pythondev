.. _infra:

++++++++++++++++++++++
CPython infrastructure
++++++++++++++++++++++

See also :ref:`Python Development Workflow <workflow>`.

Python infrastructure
=====================

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
===========================

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

python.org website
==================

* https://github.com/python/pythondotorg/ Source code of python.org
* wiki.python.org runs MoinMoin
* https://peps.python.org/ source: https://github.com/python/peps

  * Deploy job: https://github.com/python/peps/actions

Package Index (PyPI)
====================

* https://pypi.org/ "Warehouse", the new Python Package Index,

  - https://github.com/pypa/warehouse

* https://pypi.python.org/ "Python Cheeseshop", the old Python Package Index
* Python CDN: http://infra.psf.io/services/cdn/

Mailing lists
=============

* https://mail.python.org/mailman/listinfo
* Main lists:

  * python-dev
  * python-committers
  * python-ideas
  * python-list

* Maintainer: "postmaster".

Documentation
=============

* https://docs.python.org/ Python online documentation
* https://github.com/python/docsbuild-scripts/
* Mirror: http://python.readthedocs.io/en/latest/ Still use the old Mercurial repository.
* https://www.python.org/dev/peps/pep-0545/ i18n doc

.. _vendored-libs:


IRC bots
========

IRC bots on Libera Chat #python-dev:

* ``github``: bot run by GitHub. Source code:
  `github-services: lib/services/irc.rb
  <https://github.com/github/github-services/blob/master/lib/services/irc.rb>`_.
  GitHub services are `deprecated since April 2018
  <https://developer.github.com/changes/2018-04-25-github-services-deprecation/>`_.
* ``py-bb``: buildbot IRC bot, see `buildmaster-config
  <https://github.com/python/buildmaster-config>`__ (buildbot configuration).
* ``irker007``: Roundup bot.

  * https://hg.python.org/tracker/python-dev/file/tip/detectors/irker.py
  * http://www.catb.org/esr/irker/


Misc
====

* https://github.com/python/release-tools/ : Scripts for making (C)Python releases
