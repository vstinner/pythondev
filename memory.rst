.. _memory:

+++++++++++++
Python Memory
+++++++++++++

TODO
====

* Compute fragmentation of pymalloc
* Compute fragmentation of the glibc heap
* Tool to visualize the fragmentation?

Benchmarks
==========

Issue #13483:
http://bugs.python.org/file26069/tuples.py


Memory Fragmentation
====================

* Improving Python's Memory Allocator, Evan Jones:
  http://www.evanjones.ca/memoryallocator/
* MemoryError when using highlight in hgweb: http://bz.selenic.com/show_bug.cgi?id=3005


Python Memory Allocators
========================

* PyMem_RawMalloc(), PyMem_RawRealloc(), PyMem_RawFree(): new in Python 3.4
* PyMem_Malloc(), PyMem_Realloc(), PyMem_Free()
* PyObject_Malloc(), PyObject_Realloc(), PyObject_Free()

Current allocators:

* PyMem_RawMalloc(): system malloc()
* PyMem_Malloc(): system malloc()
* PyObject_Malloc(): pymalloc

http://www.python.org/dev/peps/pep-0445/


Windows
=======

* VirtualAlloc
* Windows Low Fragementation Heap (LFH)
* Python: http://bugs.python.org/issue13483

Links:

* http://smallvoid.com/article/winnt-memory-decommit.html

pymalloc
========

* Used by PyObject_Malloc()
* Threshold of 512 bytes
* Arenas of 256 KB

Arena allocator:

* Windows: VirtualAlloc(NULL, size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
* UNIX: mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
* Other: malloc(size);

Linux
=====

/proc/self/statm::

    size       total program size
               (same as VmSize in /proc/[pid]/status)
    resident   resident set size
               (same as VmRSS in /proc/[pid]/status)
    share      shared pages (from shared mappings)
    text       text (code)
    data       data + stack

http://linux-mm.org/Low_On_Memory

/proc, https://www.kernel.org/doc/Documentation/filesystems/proc.txt::

  /proc/buddyinfo
  /proc/pagetypeifo
  /proc/slabinfo => slabtop program
  /proc/meminfo
  /proc/vmallocinfo

