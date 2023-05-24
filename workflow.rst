https://mail.python.org/pipermail/python-committers/2017-March/004307.html

.. _workflow:

+++++++++++++++++++++++++++
Python Development Workflow
+++++++++++++++++++++++++++

See also :ref:`CPython infrastructure <infra>` and :ref:`History of
Python <history>`.

Source Code
===========

* 2017-current: Git

  * `PEP 512 <https://www.python.org/dev/peps/pep-0512/>`_:
    Migrating from hg.python.org to GitHub
  * `We are now live on GitHub!
    <https://mail.python.org/pipermail/python-committers/2017-February/004220.html>`_
    (Feb 2017)
  * `4 weeks with the new workflow: what needs changing?
    <https://mail.python.org/pipermail/python-committers/2017-March/004307.html>`_
  * `Pull request #1
    <https://github.com/python/cpython/pull/1>`_ (Feb 2017)

* 2011-2017: Mercurial

  * `PEP 385 <https://www.python.org/dev/peps/pep-0385/>`_: Migrating from
    Subversion to Mercurial. "2011-03-05: final conversion (tentative)"
  * `PEP 374 <https://peps.python.org/pep-0374/>`_: Choosing a distributed VCS
    for the Python project
  * https://hg.python.org/cpython/
  * Mapping of Subversion revision to Mercurial commit:
    ``Misc/svnmap.txt`` file in the Python code base.
  * Example with Subversion revision 68121:
    https://hg.python.org/lookup/r68121
    redirects to
    http://svn.python.org/view?view=revision&revision=68121
    but sadly this service is down (tested in September 2020)

* 2005-2011: Subversion (SVN)

  * `PEP 347 <https://peps.python.org/pep-0347/>`_
  * 2005-10-27: `[Python-Dev] Conversion to Subversion is complete
    <https://mail.python.org/pipermail/python-dev/2005-October/057690.html>`_
  * Subversion: https://svn.python.org/projects/python/

* 1990-2005: CVS

  * Python migrated to Subversion to 2005, but I don't when CVS started to be
    used. 1989 is the year when Guido created Python.
  * Initially hosted on ``cvs.python.org``, it migrated to Sourceforge
  * The first CVS commit was made at Aug 9, 1990.
    (converted as a `Git commit
    <https://github.com/python/cpython/commit/7f777ed95a19224294949e1b4ce56bbffcb1fe9f>`_)

Python Forge and Bug Tracker
============================

* 2022-current: GitHub

  * 2018-2022
  * Migration completed in April 2022
  * `PEP 588 <https://www.python.org/dev/peps/pep-0588/>`_:
    GitHub Issues Migration Plan
  * `PEP 581 <https://www.python.org/dev/peps/pep-0581/>`_:
    Using GitHub Issues for CPython

* 2007-2022: Roundup with Rietveld

  * https://wiki.python.org/moin/CallForTrackers
  * http://bugs.python.org/
  * CPython instance: https://github.com/psf/bpo-tracker-cpython
  * https://pypi.python.org/pypi/roundup
  * Modified instance of Roundup
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
    (`email <https://mail.python.org/archives/list/python-dev@python.org/message/7B4KAXNWJUYC4SYL53CSQ35LLXPL3X5Y/>`__)
  * The `first commit mentioning SF patch
    <https://github.com/python/cpython/commit/ef82cd72341158ec791406215da198e8a5508357>`_
    was made at June 20, 2000
  * Redirection URLs like: ``http://python.org/sf/1615275``

Rietveld (2008-2017)
====================

`Rietveld <https://github.com/rietveld-codereview/rietveld>`_ was used for code
reviews:

* Based on patch files
* bugs.python.org had a tool to create a review from a Mercurial
  repository
* Support multiple "versions" of a patch
* People who comment cannot unsubscribe: new comments are sent by emails
* User database disconnected from bugs.python.org database
* The server was not reliable and failed often
* In 2008/2009, Rietveld was an external service where to upload patches
  using an ``upload.py`` script
* Example: https://codereview.appspot.com/14105
* `Python-ideas: Yield-from patches on Rietveld
  <https://mail.python.org/pipermail/python-ideas/2009-March/003209.html>`_
  (March 2009):
  "I have uploaded the patches for my yield-from implementation to Rietveld if
  anyone wants to take a look at them: http://codereview.appspot.com/20101/show"
* https://mail.python.org/archives/list/python-dev@python.org/message/Q6LHYBYDLBJ5HKR35KH6L7I6D5HXOLA5/

History (2009-2010):

* `Tracker-discuss: Adding a "Rietveld this" button?
  <https://mail.python.org/pipermail/tracker-discuss/2009-March/001875.html>`_
  (march 2009) about roundup/rietveld integration
* `python-dev: Define a place for code review in Python workflow
  <https://mail.python.org/archives/list/python-dev@python.org/thread/VONLJONZYVKRCFQZEQMJR5TRK4PBMAPW/>`_
  (Jul 2010, same idea proposed again),
* `Python-Dev: View tracker patches with ViewVC?
  <https://mail.python.org/archives/list/python-dev@python.org/message/O4B7YB5OTCXUTOVG3UCP7SGVAPF3U23B/>`_
  (Jul 2010, early discussions about the actual implementation),
* `python-checkins, tracker: Import rietveld
  <https://mail.python.org/pipermail/python-checkins/2010-September/097989.html>`_
  (30 Sep 2010): Rietveld integration added, with a few more commits in October.
* `Python-Dev: Rietveld integration into Roundup
  <https://mail.python.org/archives/list/python-dev@python.org/message/JTPR4IP3UU2MHOBJ4LCAYPR73ZPFJSXR/>`_
  (October 2010) by Martin von Loewis

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
