.. _android:

+++++++++++++++++
Python on Android
+++++++++++++++++

Summary:

* Python 2.7 and 3.5 can be used on Android using CrystaX NDK. It uses
  patches on Python.
* Python 3.6 (from python.org) mostly work on Android API 24 without further
  patches, but need recipes to be built and these recipes are not standardized
  yet.
* The goal is to get a full Android API 24 support for Python 3.7 using a
  standard build recipe; Android buildbot using qemu.

In 2019, BeeWare was awarded by the PSF a $50,000 grant to help improve cPython
on Android. Check out their blog and call for contractors here:
https://beeware.org/news/buzz/beeware-project-awarded-a-psf-education-grant/.

BeeWare VOC
===========

A transpiler that converts Python bytecode into Java bytecode.

* http://beeware.org/voc
* https://github.com/beeware/voc

See also https://github.com/beeware/ouroboros/


Android CI for Python
=====================

* https://mail.python.org/pipermail/python-dev/2017-December/151171.html
* Guido wants a PEP?
* https://bugs.python.org/issue30386
* https://github.com/python/cpython/pull/1629

Test CI: 
  - Test on headless qemu VMs with Android 4.4 (arm/i386) and Android 7 or 8 (all
platforms)" : very slow
  - physically usb attached devices : need hosting.
  - network attached devices : need rooted devices to restart adb in network mode.


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
* Different filesystem layout and device mapper:

  * /system/bin/sh
  * /system/lib/libc.so

The Android API version combines Linux kernel and bionic versions.

Bionic
======

* https://en.wikipedia.org/wiki/Bionic_(software)
* Broken locales in libc but not in libstdc++
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
https://developer.android.com/about/dashboards

========================  =======  ============ ================
Android version           Release  API versions  market coverage
========================  =======  ============ ================
Android 7 (Nougat)        2016-08  24-25        57.9 %
Android 6 (Marshmallow)   2015-10  23           74.8 %
Android 5 (Lollipop)      2014-11  21-22        86.3 %
Android 4.4 (Kitkat)      2013-10  19-20        96.2 %
========================  =======  ============ ================



Supported API
-------------

* Python 3.7 currently targets API 21+
  (but may have a partial support of API 19+)
* Unity supports API 16+
* Kivy supports API 19+
* Termux layer support python3.6+ and API 21+

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


Cross-compilation
=================

* Documentation:
  `yan12125's comment on issue28833 <https://bugs.python.org/msg282141>`_
* Xavier's abandonned PR:
  `bpo-28833: Fix cross-compilation of third-party extension modules
  <https://github.com/python/cpython/pull/17420>`_
  
Problem to solve for adb shell / ssh shell / Termux use (with repl):

None left, except that most people may never use python app started in those ways.

So it raises the question : Could that be bad for Python future ?

  https://www.youtube.com/watch?v=22EI9uQE_ZM
  
  https://www.pythonpodcast.com/python-potential-black-swans-episode-221/



Problem to solve for in apk use ( standard android application , main is java based but embed libpython via Java native interface and a thread):

- libpython3.x.so must be unversionned and be located in <apkroot>/lib
- for cross-compiling and linking against libpython3.x.so,  its soname must be set 
or set(IMPORTED_NO_SONAME ON) must be used in cmake, not ndk-build, linking would be broken.
 
 possible fix, apply patchelf after compilation: https://github.com/pmp-p/pydk/blob/3e87331d62fb80549b61cff561d192a594efec70/sources.aosp/python3.aosp.sh#L409
 
 
Python stdlib C modules are by default cross compiled dynamic but they can't be garanteed to load because:
--

 - their filenames don't start by "lib".
 - their soname is not set.
 - their default location is not <apkroot>/lib/ ( only location allowed for most android api )  but is instead  <prefix>/lib/python3.x/lib-dynload/
 - on earlier python they were not linked to libpython (fixed since 3.7).

  LD_LIBRARY_PATH / LD_PRELOAD are not allowed from java user space.

see https://android.googlesource.com/platform/bionic/+/master/android-changes-for-ndk-developers.md
  
  
Third party C modules have the same problem :
--
  
possible fix, apply patchelf after compilation, change filenames (avoiding collisions!), set correct soname, move files in same folder for android sdk builder (gradle) to pick libpython.so.

 note that cross compiling third party with setuptools/pip may need to set _PYTHON_SYSCONFIGDATA_NAME which is an internal.


Cross-compilation is used to target:

* Android on ARM and ARM64
* Android x86 and amd64.
* Android mips, but deprecated on newer toolchains.
* Intel 32-bit for Ubuntu multiarch: compilation done from x86-64 (64 bit) to x86 (32 bit)
* can be used for WASM (emscripten), and could be used for WASI (clang) targets.


