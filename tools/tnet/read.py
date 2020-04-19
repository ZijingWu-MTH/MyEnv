#!/usr/bin/python -S
"""
auxiliary function; could go in tnet.py.

Didn't need this for xmap.py.
"""

__author__ = 'Andy Chu'


def read(f):
  """Read a net string from a file handle, but don't decode it."""
  buf = ''
  while True:
    c = f.read(1)
    if not c:
      raise EOFError  # can't use empty string
    if not c.isdigit():
      if buf:
        if c != ':':
          raise ValueError("Expected ':', got %r" % c)
      else:
        raise ValueError("Expected chunk length, got %r" % c)

      break
    buf += c
  length = int(buf)

  # Add back the ':'
  buf += c

  # +1 for the payload type -- not checking it here, since we're just sending it
  # through to the children
  payload = f.read(length + 1)
  return buf + payload


if __name__ == '__main__':
  import sys
  while True:
    try:
      chunk = read(sys.stdin)
    except EOFError:
      break
    print repr(chunk)
