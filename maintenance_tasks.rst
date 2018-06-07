+++++++++++++
CPython tasks
+++++++++++++

CPython is a big project. Maintaining CPython require to frequently do
different tasks. This page tries to list all "tasks" required to maintain
Python. The goal is to make sure that each task has at least two maintainers,
so one maintainer can easily take holiday or stop working on this task.

For the background, see Vicky's talk `Passing the Baton: Succession planning
for FOSS leadership
<https://fosdem.org/2018/schedule/event/community_passing_the_batton_foss_leadership/>`_.

Tasks
=====

* `Review and merge pull requests <https://github.com/python/cpython/pulls>`_:
  done by around 34 core developers (Stephane Wirtel's stats at Pycon Italy
  2018). The merge action is restricted to core developers.
  Maintainers: active core developers (June 2018: around 34 core devs).
* `Bug triage <https://bugs.python.org/>`_: closing a bug needs the bug triage permission
* `Check for buildbot failures
  <https://mail.python.org/mm3/mailman3/lists/buildbot-status.python.org/>`_:
  Read logs of each buildbot failure, check if the failure is known. If the
  failure is known, maybe mention the new failure in the existing bug.
  Otherwise, open a new bug. Then reply to the email with a link to the bug.
  Maintainers: Victor Stinner.
* Run bugs.python.org: fix bugs, deploy new version. See the
  `meta bug tracker <http://psf.upfronthosting.co.za/roundup/meta/>`_ for bugs
  of bugs.python.org itself (not for Python bugs). Roundup is going to be
  deployed in a Docker container on OpenShift. Maintainers:
  Ezio Melotti, Brett Cannon, Maciej Szulik.
* `Run pythontest.net <http://www.pythontest.net/>`_. Maintainers: ?
* Run GitHub bots. Maintainers: Brett Cannon and Mariatta Wijaya.
* Update external dependencies
* Update unicodedata on new Unicode release. Latest update (Unicode 11.0):
  https://bugs.python.org/issue33778. Maintainer: Benajamin Peterson.
