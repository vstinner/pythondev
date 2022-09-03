.. _workflow:

+++++++++++++++++++++++++++
Python Development Workflow
+++++++++++++++++++++++++++

See also :ref:`CPython infrastructure <infra>` and :ref:`History of
Python <python>`.

Source Code
===========

* 2015-current: Git

  * 2015-2016: https://www.python.org/dev/peps/pep-0512/
  * https://www.python.org/dev/peps/pep-0512/

* 2011-2015: Mercurial

  * `PEP 385 <https://www.python.org/dev/peps/pep-0385/>`_:
    "2011-03-05: final conversion (tentative)"
  * https://hg.python.org/cpython/
  * Mapping of Subversion revision to Mercurial commit:
    ``Misc/svnmap.txt`` file in the Python code base.
  * Example with Subversion revision 68121:
    https://hg.python.org/lookup/r68121
    redirects to
    http://svn.python.org/view?view=revision&revision=68121
    but sadly this service is down (tested in September 2020)

* 2005-2011: Subversion

  * 2005-10-27: `[Python-Dev] Conversion to Subversion is complete
    <https://mail.python.org/pipermail/python-dev/2005-October/057690.html>`_
  * Subversion: https://svn.python.org/projects/python/

* 1990-2005: CVS

  * Python migrated to Subversion to 2005, but I don't when CVS started to be
    used. 1989 is the year when Guido created Python.
  * Initially hosted on ``cvs.python.org``, it migrated to Sourceforge
  * The first CVS commit was made at Aug 9, 1990.

Python Bug Tracker
==================

* 2022-current: GitHub

  * 2018-2022: Migration completed in April 2022
  * https://www.python.org/dev/peps/pep-0588/
  * https://www.python.org/dev/peps/pep-0581/

* 2007-2022: Roundup

  * http://bugs.python.org/ Bug tracker (modified instance of Roundup)
  * https://pypi.python.org/pypi/roundup
  * CPython instance: https://github.com/psf/bpo-tracker-cpython
  * Report Tracker Problem: https://github.com/python/psf-infra-meta/issues
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

* 2000-2007: SourceForge

  * May 2000: "We move all development (CVS at the time, and bug tracking) to
    SourceForge. This roughly coincided with PythonLabs leaving CNRI, so
    clearly we couldn’t continue running infra off of their systems."
    (`source <https://mail.python.org/archives/list/python-dev@python.org/message/7B4KAXNWJUYC4SYL53CSQ35LLXPL3X5Y/>`__)
  * The `first commit mentioning SF patch
    <https://github.com/python/cpython/commit/ef82cd72341158ec791406215da198e8a5508357>`_
    was made at June 20, 2000
  * Redirection URLs like: ``http://python.org/sf/1615275``

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

Workflow in 2010-2018 (before GitHub, buildbots testing code once merged)
=========================================================================

Buildbot was only running after changes were pushed upstream. It was common that
a change broke the Windows support, and so core devs pushed an "attempt to fix
Windows" commit, and then a second one, etc.

To propose a change, a contributor had to open an issue in the bug tracker
(Roundup at bugs.python.org), and attach a patch file. A core developer had to

* Download the patch locally
* Apply the patch file
* Fix conflicts: when the day was older than 1 day, conflicts were very likely

Misc/NEWS was basically always in conflict, especially on merges.

Changes were first fixed in the oldest supported branch, and then
forward-ported to newer branches. For example, fixed in 2.6, and ported to
2.7, 3.0 and 3.1.

When Subversion was used, a Subversion "property" (in practice, a text file
tracked by Subversion) listed the revision number of all "merged" changes.  For
example, when a change made in the 2.6 branch was merged into the 2.7 branch,
it was added to this list. It was likely that this property file was in
conflict. Sadly, it was a text file made of a single line with thousands of
revision numbers. Text editors are not convenient to edit such file. It was
barely possible to fix a conflict in this property.

A new tool to review (comment) patches was linked to Roundup: Rietveld.
It was possible to generate a patch from a fork the Mercurial repository,
and then get a review page. Rietveld supported multiple revisions of the same
change. Drawback: the tool was not well integrated with Roundup. For example,
there was no way to unsubscribe from a review.


GitHub Python organization
==========================

* https://github.com/python/
* `Current organization owners
  <https://devguide.python.org/devcycle/?highlight=github%20administrators#current-owners>`_
* `Current repository administrators
  <https://devguide.python.org/devcycle/?highlight=github%20administrators#current-administrators>`_

GitHub CPython project
======================

* https://github.com/python/cpython/
* GitHub cpython administrators:

  * Brett Cannon
  * Release managers (ex: Ned Deily)

* GitHub uses mention-bot: https://github.com/facebook/mention-bot

  * https://github.com/mention-bot/how-to-unsubscribe
  * userBlacklist, userBlacklistForPR in `CPython .mention-bot
    <https://github.com/python/cpython/blob/master/.mention-bot>`_
  * Adding you GitHub login to userBlacklistForPR stops the mention bot from
    mentioning anyone on your PRs.

* IRC notifications: http://n.tkte.ch/ --
  see: https://discuss.python.org/t/replacement-for-irc-github-service/805


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
