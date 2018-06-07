+++++++++++++++++
Python on Android
+++++++++++++++++

Summary:

* Python 2.7 and 3.5 can be used on Android using CrystaX NDK. It uses
  patches on Python.
* Python 3.6 (from python.org) mostly work on Android API 24 without further
  patches, but need recipes to be build and these recipes are not standardized
  yet.
* The goal is to get a full Android API 24 support for Python 3.7 using a
  standard build recipe; Android buildbot using qemu.

Xavier's "Android support" document (Decembre 2017):
https://github.com/xdegaye/cagibi/blob/master/doc/android_support.rst

Android CI for Python
=====================

* https://mail.python.org/pipermail/python-dev/2017-December/151171.html
* Guido wants a PEP?
* https://bugs.python.org/issue30386
* https://github.com/python/cpython/pull/1629

pmpp's plan: "Test on VMs with Android 4.4 (arm/i386) and Android 7 or 8 (all
platforms)".


People
======

* Xavier de Gaye: was given push privileges on June 3, 2016 on the
  recommendation of Victor Stinner to pursue its work on porting Python on
  Android.
* Chih-Hsuan Yen aka *yan12125*
* Paul Peny aka *pmpp*: Panda3D contributor, wants to "port" Panda3D on Android
  (especially Python binding of Panda3D)

Android?
========

Android is not the common "Linux" system, only the Linux kernel is shared,
everything else is different:

* Kernel: Linux
* libc: Bionic
* SDK: "NDK"
* Different filesystem:

  * /system/bin/sh
  * /system/lib/libc.so

The Android API version combines Linux kernel and bionic versions.

Bionic
======

* https://en.wikipedia.org/wiki/Bionic_(software)
* Broken locales
* No shmem -- see https://github.com/pelya/android-shmem

C++ stdlib has a working localeconv()!? Example::

    #include <locale>

    using namespace std;

    static char decimal_point;
    static char thousands_sep;
    static lconv lc_cache ;

    extern "C" {
        struct lconv *localeconv(void){
            decimal_point = std::use_facet<std::numpunct<char> >(std::locale(std::setlocale(LC_ALL, NULL))).decimal_point();
            lc_cache.decimal_point = &decimal_point;

            thousands_sep = std::use_facet<std::numpunct<char> >(std::locale(std::setlocale(LC_ALL, NULL))).thousands_sep();
            lc_cache.thousands_sep = &thousands_sep ;

            return &lc_cache;
        }
    }

Android, NDK and API versions
=============================

Android versions
----------------

https://en.wikipedia.org/wiki/Android_version_history :

========================  =======  ============
Android version           Release  API versions
========================  =======  ============
Android 7 (Nougat)        2016-08  24-25
Android 6 (Marshmallow)   2015-10  23
Android 5 (Lollipop)      2014-11  21-22
Android 4.4 (Kitkat)      2013-10  19-20
========================  =======  ============

Supported API
-------------

* Python 3.7 currently targets API 21+
  (but may have a partial support of API 19+)
* Unity supports API 16+
* Kivy supports API 19+

Cheap devices only support old versions of Android. Cheap devices allow
developers to work on Android without having to buy expensive devices just for
this platforms.

XXX Python 3.7 should have a basic API 19+ support: fix compilation, but it's
ok if some tests fail. Just push upstream existing patches for API 19.

API 19
------

* Basically, the full locale API is broken
* mmap() works but is not exported in libc headers

NDK
---

XXX what is NDK? :-)

NDK 14b is the first release to use "Unified headers".

Python on Android
=================

* A lot of changes merged since 2016
* Python uses UTF-8 as its "filesystem encoding" and uses directly Python's
  codec rather than mbstowcs() and wcstombs()
* Python 3.7 added `sys.getandroidapilevel()
  <https://docs.python.org/dev/library/sys.html#sys.getandroidapilevel>`_: API
  level used to *build* Python, not the runtime API version.
  ``sys.getandroidapilevel()`` mostly exists to implement the test "is Python
  running on Android?".

XXX should we change sys.platform from "linux" to "android" on Android?

Patches for API 19:

* https://github.com/pmp-p/droid-pydk/tree/master/sources.32

Build system and patches for API 21:

* https://github.com/yan12125/python3-android


Build Python for Android
========================

Stdlib packed into a ZIP file.

Cross-compilation
-----------------

Xavier's favorite option.

Drawback: pip cannot be used to install C extensions (see :ref:`pip
<android-pip>`).

Build Python on Android
-----------------------

pmpp's favorite option.

Hackish option
--------------

pmpp's second choice.

* Link Python to a static libc on Linux using Android linker
* Extract object files from libpython.a and link again on Android

Drawback: broken DNS resolution.


Devices to develop Python on Android?
=====================================

Devices:

* Raspberry PI 3: arm64

Software (Android):

* Lineage (ex-cyanogen)
* Android TV

TTY on Android?
===============

* Python REPL
* ncurses

See `Terminal Emulator for Android
<https://play.google.com/store/apps/details?id=jackpal.androidterm>`_ (Google
Play).

dlopen() RTLD_BIND_NOW
======================

Bionic dlopen() doesn't support RTDL_LAZY. Dependencies must be loaded
explicitly!

.. _android-pip:

pip, MACHDEP, sysconfig
=======================

* https://bugs.python.org/issue32637 proposes to change sys.platform from
  "linux" to "android", but keep MACHDEP="linux".
* sysconfig: sysconfig data filename generated by Makefile using MACHDEP.
  Issue on cross-compilation. sysconfig uses sys.platform to recreate
  the module name at runtime.

If Python was cross-compiled, pip fails to build C extensions. The C compiler
fails to locate Python header files.

SELinux
=======

SELinux is enforced on arm64 since Android 5 (Lollipop).

CrystaX NDK
===========

In short, `CrystaX NDK <https://www.crystax.net/>`_ is closer to a regular
Linux glibc.

CrystaX NDK is a drop-in replacement for Google's NDK. Following are the main
goals of CrystaX NDK:

* Better standard compatibility
* Easy porting of existing code to Android
* New features for Android native development

It provides Python 2.7 and Python 3.5, Python compiled with patches to support
Android.

The Kivy project uses the Python of CrystaX. Kivy updated CrystaX Python get to
Python 3.6:

* `python-for-android <https://python-for-android.readthedocs.io/>`_ (aka
  "p4a"): Turn your Python application into an Android APK.  (`GitHub
  python-for-android <https://github.com/kivy/python-for-android/>`_)
* `buildozer <https://github.com/kivy/buildozer>`_, Generic Python packager for
  Android and iOS.
