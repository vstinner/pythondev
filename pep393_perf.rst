********************
PEP 393 performances
********************

Writing efficient code manipulating Unicode is harder since the PEP 393.  The
problem is to respect the canonical form.

If you preallocate an ASCII buffer but you need to write a Latin1 character,
you have to convert the ASCII string to Latin1 which means copying all already
written characters. It is inefficient especially if the Latin1 characters
occurs at the end. If you preallocate an UCS4 buffer, but the result is UCS2,
you have to "shrink" the buffer from UCS4 to UCS2, which means copying all
characters.

To not having to widen or shrink your buffer, you can scan your input to
compute the maximum character before allocating the buffer. In practice,
processing the input twice may be slower.

Another problem is the length of the result. Getting the length of str%args and
str.format(args) require to do the work twice: once to get the length, once to
write characters. Both approaches were tested (*), and processing the output
twice is too slow.

For efficient code, you should be optimistic and enlarge or widen the buffer on
demand. When the output length is unknown, it is better to overallocate the
buffer.

The _PyUnicodeWriter API helps to implement such function:

 * Widen the buffer on demand
 * Enlarge the buffer on demand
 * Minimum length and overallocation of the buffer can be configured
 * Avoid completly the need of a buffer when the output is only composed
   of one string
 * Delay allocation of the buffer until the first write. It helps to compute
   the length and kind of the buffer, because the length and kind cannot always
   be computed before the first write. It avoids also allocating a buffer is
   no write is done at all (ex: error before writing the first characters).
 * Give a direct access to the buffer for best performances

