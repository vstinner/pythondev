.. _workflow:

+++++++++++++++++++++++++++
Python Development Workflow
+++++++++++++++++++++++++++

See also :ref:`CPython infrastructure <infra>`.

Source Code
===========

* Git (current)

  * 2015-2016: https://www.python.org/dev/peps/pep-0512/
  * https://www.python.org/dev/peps/pep-0512/

* OLD: Mercurial

  * 2009: https://www.python.org/dev/peps/pep-0385/
  * https://hg.python.org/cpython/

* OLD: Subversion

  * 2005-10-27: `[Python-Dev] Conversion to Subversion is complete
    <https://mail.python.org/pipermail/python-dev/2005-October/057690.html>`_
  * https://svn.python.org/

* OLD: CVS

  * SourceForge

Code Review
===========

* GitHub (current)
* OLD: `Rietveld <https://github.com/rietveld-codereview/rietveld>`_

  * Based on patch files
  * bugs.python.org had a tool to create a review from a Mercurial
    repository
  * Support multiple "versions" of a patch
  * People who comment cannot unsubscribe: new comments are sent by emails
  * User database disconnected from bugs.python.org database
  * The server was not reliable and failed often

Python Bug Tracker
==================

* GitHub (current)

  * 2018-2022: Migration completed in April 2022
  * https://www.python.org/dev/peps/pep-0588/
  * https://www.python.org/dev/peps/pep-0581/

* 2007-2022: Roundup

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
  * https://github.com/python/bugs.python.org/
  * OLD: https://hg.python.org/tracker/roundup/
  * OLD: https://hg.python.org/tracker/python-dev/

* Before 2007: SourceForge

  * Redirection URLs like: ``http://python.org/sf/1615275``


GitHub bots
===========

cherry-pick for backports
-------------------------

* https://github.com/python/core-workflow/tree/master/cherry_picker/
* `Check Python CLA <https://check-python-cla.herokuapp.com/>`_ (service run
  by Mariatta Wyjaya)

miss-islington
--------------

* Bug reports: https://github.com/python/miss-islington/issues
* Code: https://github.com/python/miss-islington
* https://github.com/miss-islington

Mariatta is the primary maintainer. The bot runs in Heroku.

The bot runs `cherry-picker <https://pypi.org/project/cherry-picker/>`_
to backport changes in CPython.

GitHub CLA bot
--------------

* https://github.com/ambv/cla-bot is forked from https://github.com/edgedb/cla-bot
* https://discuss.python.org/t/https-github-com-python-is-now-using-a-new-cla-bot/14961
