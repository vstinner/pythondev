.. _infra:

++++++++++++++++++++++
CPython infrastructure
++++++++++++++++++++++

See also :ref:`Python Development Workflow <workflow>`.

* `Current organization owners
  <https://devguide.python.org/devcycle/?highlight=github%20administrators#current-owners>`_
* `Current repository administrators
  <https://devguide.python.org/devcycle/?highlight=github%20administrators#current-administrators>`_

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

python.org
==========

* https://github.com/python/pythondotorg/ Source code of python.org
* wiki.python.org runs MoinMoin
* https://peps.python.org/ source: https://github.com/python/peps

  * Deploy job: https://github.com/python/peps/actions

Source Code
===========

* Git

  * 2015-2016: https://www.python.org/dev/peps/pep-0512/
  * https://www.python.org/dev/peps/pep-0512/

* Mercurial

  * 2009: https://www.python.org/dev/peps/pep-0385/
  * https://hg.python.org/cpython/

* Subversion

  * 2005-10-27: `[Python-Dev] Conversion to Subversion is complete
    <https://mail.python.org/pipermail/python-dev/2005-October/057690.html>`_
  * https://svn.python.org/

* CVS

  * SourceForge

Python Bug Tracker
==================

* WIP: GitHub

  * 2018-2022
  * https://www.python.org/dev/peps/pep-0588/
  * https://www.python.org/dev/peps/pep-0581/

* Roundup

  * Migration from SourceForge to Roundup in 2007
  * `Status of new issue tracker <https://mail.python.org/archives/list/python-dev@python.org/thread/6P4HUPKUU45FGG64LHSWCQBKPZRC2ND4/>`_ (29 Oct 2006) by Brett Cannon
  * `Re: [Python-Dev] PEP 581: Using GitHub Issues for CPython
    <https://mail.python.org/archives/list/python-dev@python.org/message/7B4KAXNWJUYC4SYL53CSQ35LLXPL3X5Y/>`_
    (8 Mar 2019) by Barry Warsaw
  * tracker-discuss mailing list
  * Weekly "Summary of Tracker Issues" sent to python-dev since May 13, 2007.
    First email: `Summary of Tracker Issues
    <https://mail.python.org/archives/list/python-dev@python.org/thread/ZAAW7AOB6UYROEU3ACB5XT4TB7F24X27/#HRHFCQ5XB35O4G7MCLD7JRVXFWD3L2NE>`_:
    "ACTIVITY SUMMARY (05/06/07 - 05/13/07)" (May 2007).

* SourceForge

  * Redirection URLs like: ``http://python.org/sf/1615275``

Package Index (PyPI)
====================

* https://pypi.org/ "Warehouse", the new Python Package Index,

  - https://github.com/pypa/warehouse

* https://pypi.python.org/ "Python Cheeseshop", the old Python Package Index
* Python CDN: http://infra.psf.io/services/cdn/

cpython GitHub project
======================

* https://github.com/python/cpython/
* GitHub uses mention-bot: https://github.com/facebook/mention-bot

  * https://github.com/mention-bot/how-to-unsubscribe
  * userBlacklist, userBlacklistForPR in `CPython .mention-bot
    <https://github.com/python/cpython/blob/master/.mention-bot>`_
  * Adding you GitHub login to userBlacklistForPR stops the mention bot from
    mentioning anyone on your PRs.

* https://github.com/python/core-workflow/tree/master/cherry_picker/
* `Check Python CLA <https://check-python-cla.herokuapp.com/>`_ (service run
  by Mariatta Wyjaya)
* IRC notifications: http://n.tkte.ch/ --
  see: https://discuss.python.org/t/replacement-for-irc-github-service/805


Misc
====

* http://bugs.python.org/ Bug tracker (modified instance of Roundup)

  * https://pypi.python.org/pypi/roundup
  * Report Tracker Problem: https://github.com/python/psf-infra-meta/issues
  * CPython instance: https://github.com/psf/bpo-tracker-cpython
  * Special links:

    * `edit Components <https://bugs.python.org/component>`_
    * `edit Versions <https://bugs.python.org/version>`_
    * `Test issue <https://bugs.python.org/issue2771>`_
    * Bot for IRC notification, ``irker`` bot:
      `pillar/base/bugs.sls in psf-salt
      <https://github.com/python/psf-salt/commit/3cb5b90376c49ba2e296362384df10ee687c8a00>`_

  * Weekly summary by email: https://github.com/psf/bpo-tracker-cpython/blob/master/scripts/roundup-summary

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
    <https://github.com/python/buildmaster-config/tree/master/master>`__
    (configuration)
  * `Fork of BuildBot running on buildbot.python.org
    <https://github.com/python/buildbot/>`_

* GitHub CLA bot: XXX

Documentation
=============

* https://docs.python.org/ Python online documentation
* https://github.com/python/docsbuild-scripts/
* Mirror: http://python.readthedocs.io/en/latest/ Still use the old Mercurial repository.
* https://www.python.org/dev/peps/pep-0545/ i18n doc

.. _vendored-libs:


IRC bots
========

IRC bots on #python-dev:

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


Roundup: bugs.python.org
========================

* https://github.com/python/bugs.python.org/
* https://hg.python.org/tracker/roundup/
* https://hg.python.org/tracker/python-dev/
