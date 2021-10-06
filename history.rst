.. _python:

+++++++++++++++++
History of Python
+++++++++++++++++

Guido van Rossum started to write Python in December 1989.

History of Python releases
==========================

See also `Status of Python branches
<https://docs.python.org/devguide/#status-of-python-branches>`_.

* Python 3.9: October 2020
* Python 3.8: October 2019
* Python 3.7: June 2018
* Python 3.6: December 2016
* Python 3.5: September 2015
* Python 3.4: March 2014
* Python 3.3: September 2012
* Python 3.2: February 2011
* Python 2.7: July 2010
* Python 3.1: June 2009
* Python 3.0: December 2008
* Python 2.6: October 2008
* Python 2.5: September 2006
* Python 2.4: March 2005
* Python 2.3: July 2003
* Python 2.2: December 2001
* Python 2.1: April 2001
* Python 2.0: October 2000
* Python 1.5: April 1999
* Python 0.9.1: `February 20, 1991
  <https://www.tuhs.org/Usenet/alt.sources/1991-February/001749.html>`_
  (date commonly used at the birth of the Python project)



History of the Python language (syntax)
=======================================

* Python 3.8: ``x := 1`` assignment expression (PEP 572) and ``/`` in function
  for positional-only parameters (PEP 570)
* Python 3.7: ``async`` and ``await`` become keywords
* Python 3.6: f-strings (`PEP 498 "Literal String Interpolation"
  <https://www.python.org/dev/peps/pep-0498/>`_)
* Python 3.5:

  * Add ``async`` and ``await`` (not really keywords yet)
  * The ``@`` operator (`PEP 465 "A dedicated infix operator for matrix multiplication"
    <https://www.python.org/dev/peps/pep-0465/>`_)
  * `PEP 448 "Additional Unpacking Generalization" <https://www.python.org/dev/peps/pep-0448/>`_

* *(Python 3.4: no change)*
* Python 3.3:

  * ``yield from``: `PEP 380 "Syntax for Delegating to a Subgenerator"
    <http://legacy.python.org/dev/peps/pep-0380/>`_
  * ``u'unicode'`` syntax is back: `PEP 414 "Explicit Unicode literals"
    <http://legacy.python.org/dev/peps/pep-0414/>`_

* *(Python 3.2: no change)*
* Python 2.7:

  * all changes of Python 3.1

* Python 3.1:

  * dict/set comprehension
  * set literals
  * multiple context managers in a single with statement

* Python 3.0:

  * all changes of Python 2.6
  * new ``nonlocal`` keyword
  * ``raise exc from exc2``: `PEP 3134 "Exception Chaining and Embedded
    Tracebacks" <http://legacy.python.org/dev/peps/pep-3134/>`_
  * ``print`` and ``exec`` become a function
  * ``True``, ``False``, ``None``, ``as``, ``with`` are reserved words
  * Change from ``except exc, var`` to ``except exc as var``:
    `PEP 3110 "Catching Exceptions in Python 3000"
    <http://legacy.python.org/dev/peps/pep-3110/>`_
  * Removed syntax: ``a <> b``, ```a```, ``123l``, ``123L``, ``u'unicode'``,
    ``U'unicode'`` and ``def func(a, (b, c)): pass``
  * `PEP 3132 "Extended Iterable Unpacking" <https://www.python.org/dev/peps/pep-3132/>`_

* Python 2.6:

  * with: `PEP 343 "The "with" Statement"
    <http://legacy.python.org/dev/peps/pep-0343/>`_
  * ``b'bytes'`` syntax: `PEP 3112 "Bytes literals in Python 3000" <http://legacy.python.org/dev/peps/pep-3112/>`_

Old Python Versions
===================

* `Python 0.9.1 <https://www.python.org/download/releases/early/>`_
* `Python 1.5.2 <https://www.python.org/download/releases/1.5/>`_
* `Python 0.9.1 .. 2.0 source tarballs
  <https://www.python.org/ftp/python/src/>`_
* `David Beazley tests in 2017 (tweets)
  <https://twitter.com/dabeaz/status/934604333425004544>`_
* `neopythonic <http://neopythonic.blogspot.fr/>`_ by Guido van Rossum:
  Ramblings through technology, politics, culture and philosophy by the creator
  of the Python programming language.
* `History of Python (Wikipedia article)
  <https://en.wikipedia.org/wiki/History_of_Python>`_
* `The History of Python
  <http://python-history.blogspot.com/>`_ by Guido van Rossum:
  A series of articles on the history of the Python programming language and
  its community.

Development before GitHub
=========================

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

Python 3000
===========

* https://mail.python.org/pipermail/python-3000/
* https://www.python.org/dev/peps/pep-3000/
* https://www.python.org/dev/peps/pep-3100/

CVS, Subversion, Mercurial
==========================

* CVS: Initially hosted on cvs.python.org, it migrated to Sourceforge
* Subversion: https://svn.python.org/projects/python/
* Mercurial: https://hg.python.org/cpython/

  * Map Subversion revision to Mercurial commit: Misc/svnmap.txt file
    in the Python code base.

* Lookup service. Examples:

  * Subversion revision 68121: https://hg.python.org/lookup/r68121
    redirects to http://svn.python.org/view?view=revision&revision=68121 but
    sadly this service is down (tested in September 2020)
