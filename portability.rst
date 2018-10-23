++++++++++++++++++++++++
Price of the portability
++++++++++++++++++++++++

Misc
====

* Timers: PEP 418
* Inheritance of file descriptors and handles: PEP 446 (and PEP 433)
* Timezone
* SSL/TLS x509 root certificates
* use recent OS features: detected in configure, detected at runtime
* doc: "Availability: xxx"
* os.confstr(), os.sysconf()
* os.sysconf("SC_PAGESIZE")
* os.cpucount()
* OSError, VMSError, WindowsError, IOError => OSError
* os.closerange()
* os.sendfile(): different API depending on the OS!
* time.strftime()
* tzdata


POSIX vs real world
===================

* Linux adds many new features not part of the POSIX standards
* (Systemd uses new Linux-only features like cgroups, not portable on FreeBSD,
  OpenBSD, etc.)
* _GNU_SOURCE: asprintf(), canonicalize_file_name()
* realpath(NULL)
* "Undefined" parts of POSIX standards: kept for efficiency?
* AIX


Windows
=======

* POSIX API
* POSIX API has fewer features
* Windows console
* Windows ANSI, OEM and console code pages
* Atomic rename file, os.replace()
* One binary for all Windows versions: use LoadLibrary()
* os.fsencode() error handler and Windows versions
* Socket: no file descriptor, SOCKET_T


UNIX
====

* accept4() returns ENOSYS
* open(O_CLOEXEC) and socket(SOCK_CLOEXEC) on old Linux kernels


select, pipes
=============

* test_signal: "OS doesn't report write() error on the read end of a pipe"
* select() limited to sockets on Windows
* select(), poll(), epoll(), devpoll(), kqueue(), etc. => selectors => asyncio
* async I/O operations: no Python API yet?
* select.poll()

  * ifdef HAVE_BROKEN_POLL
  * #ifdef __APPLE__ select_have_broken_poll()


Threads and signals
===================

* Hard

  * low-level OS functions, syscalls
  * threads
  * signals
  * fork, exec

* many tests skipped on old versions of operating systems
* OpenBSD older than 5.2 implemented threads in user-space
* FreeBSD older than 7.0

  * "Issue #12392 and #12469: send a signal to the main thread
    doesn't work before the creation of the first thread on
    FreeBSD 6"

* "Issue #18238: sigwaitinfo() can be interrupted on Linux (raises
  InterruptedError), but not on AIX"

* Signal orders
* HP-UX11
* depending on the OS, a signal sent to the pid is received by the mainthread
  or a random thread
* timeout on locks: drop support for thread APIs different than pthread and nt
* pthread_sigmask()
* pthread_kill()

