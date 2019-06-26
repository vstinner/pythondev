.. _ci:

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Python Continuous Integration: Travis CI, AppVeyor, VSTS, Buildbots
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The Night's Watch is Fixing the CIs in the Darkness for You
===========================================================

Buildbot Watch: The watchers of CPython's Continuous Integration

.. image:: images/buildbot_watch.png
   :alt: Buildbot Watch

Members:

* Pablo Galindo Salgado
* Victor Stinner

`The Night's Watch is Fixing the CIs in the Darkness for You
<https://pyfound.blogspot.com/2019/06/pablo-galindo-salgado-nights-watch-is.html>`_
by Pablo Galindo Salgado.

Buildbots links
===============

CPython buildbots:

* `Builders <http://buildbot.python.org/all/#/builders>`_
* `buildmaster-config (GitHub)
  <https://github.com/python/buildmaster-config/>`_: Buildbot configuration
* `Devguide: buildbots <https://devguide.python.org/buildbots/>`_

Travis CI
=========

* `Travis CI: Build History
  <https://travis-ci.org/python/cpython/builds>`_
* `CPython: Travis CI configuration (.travis.yml)
  <https://github.com/python/cpython/blob/master/.travis.yml>`_
* https://docs.travis-ci.com/user/running-build-in-debug-mode/
* `Travis CI Status <https://www.traviscistatus.com/>`_

AppVeyor
========

* `AppVeyor: CPython build history
  <https://ci.appveyor.com/project/python/cpython/history>`_
* `CPython: AppVeyor configuration (.github/appveyor.yml)
  <https://github.com/python/cpython/blob/master/.github/appveyor.yml>`_
* `AppVeyor status page <https://appveyor.statuspage.io/>`_

Azure Pipelines PR
==================

* Restart a job: `close/reopen the PR
  <https://mail.python.org/pipermail/python-dev/2019-April/156967.html>`_


Buildbots notifications
=======================

* IRC: #python-dev on Freenode
* Email: `buildbot-status mailing list
  <https://mail.python.org/mm3/mailman3/lists/buildbot-status.python.org/>`_

Articles
========

* `Work on Python buildbots, 2017 Q2
  <https://vstinner.github.io/python-buildbots-2017q2.html>`_

How to watch buildbots?
=======================

Email: `[Python-Dev] How to watch buildbots?
<https://mail.python.org/pipermail/python-dev/2018-May/153754.html>`_.

Report a failure
----------------

When a buildbot fails, I look at tests logs and I try to check if an
issue has already been reported. For example, search for the test
method in title (ex: "test_complex" for test_complex() method). If no
result, search using the test filename (ex: "test_os" for
Lib/test/test_os.py). If there is no result, repeat with full text
searchs ("All Text"). If you cannot find any open bug, create a new
one:

* The title should contain the test name, test method and the buildbot
  name. Example: " test_posix: TestPosixSpawn fails on PPC64 Fedora
  3.x".
* The description should contain the link to the buildbot failure. Try
  to identify useful parts of tests log and copy them in the
  description.
* Fill the Python version field (ex: "3.8" for 3.x buildbots)
* Select at least the "Tests" Component. You may select additional
  Components depending on the bug.

If a bug was already open, you may add a comment to mention that there
is a new failure: add at least a link to buildbot name and a link to
the failure.

And that's all! Simple, isn't it? At this stage, there is no need to
investigate the test failure.

To finish, reply to the failure notification on the mailing list with
a very short email: add a link to the existing or the freshly created
issue, maybe copy one line of the failure and/or the issue title.

Bug example: `issue33630 <https://bugs.python.org/issue33630>`_.

Analyze a failure
-----------------

Later, you may want to analyze these failures, but I consider that
it's a different job (different "maintenance task"). If you don't feel
able to analyze the bug, you may try to find someone who knows more
than you about the failure.

For better bug reports, you can look at the [Changes] tab of a build
failure, and try to identify which recent change introduced the
regression. This task requires to follow recent commits, since
sometimes the failure is old, it's just that the test fails randomly
depending on network issues, system load, or anything else. Sometimes,
previous tests have side effects. Or the buildbot owner made a change
on the system. There are many different explanation, it's hard to
write a complete list. It's really on a case by case basis.

Hopefully, it's now more common that a buildbot failure is obvious and
caused by a very specific recent changes which can be found in the
[Changes] tab.

Revert on fail
==============

* `Policy to revert commits on buildbot failure
  <https://discuss.python.org/t/policy-to-revert-commits-on-buildbot-failure/404>`_
* `[Python-Dev] Keeping an eye on Travis CI, AppVeyor and buildbots: revert on regression
  <https://mail.python.org/pipermail/python-dev/2018-May/153753.html>`_
  (May, 2018)
* `[python-committers] Revert changes which break too many buildbots
  <https://mail.python.org/pipermail/python-committers/2017-June/004588.html>`_
  (June, 2017)

VSTS
====

XXX
