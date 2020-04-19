#!/usr/bin/python
#
# tnet.py
#
# Simple serialization format which uses the JSON data model, but is simpler to
# implement in many languages.  Importantly, it supports binary data (not just
# Unicode strings).
#
# Derived from http://tnetstrings.org/ (no license given)
#
# Code Modifications:
#
# - Added unit tests
# - Renamed parse -> load
# - Several small optimizations (5-10% faster for both loads and dumps)
# - Raise ValueError/TypeError instead of assertions; other Error handling:
# - Tweaks to the code style
# - Comments about certain cases
#
# Protocol Modifications
#
# - "\n" is a synonym for , -- in some restricted situations this will give you
#   backward compatibility with unix tools -- records are *lines* in addition to
#   having structure.  Also, if the records are human-readable (i.e. JSON),
#   then a file full of records will be human-readable.
#
# TODO:
#
# - $ for utf-8 unicode string type?  this will work in Python and Go and Node
# JS, and I think R.

# The names of the exposed functions are chosen to match Python's JSON module.
# load() (from a file) has a substantially different implementation than
# loads().  There's no dump() now because that would be trivial.

__all__ = ['dumps', 'dump_line', 'loads', 'load', 'loadfd', 'read', 'readfd']

# %Id%

import os  # for loadfd

#
# SERIALIZATION
#


def dump_line(byte_str):
  """Dump a byte string to a line.

  Normally byte strings are like this: 3:foo,

  Equivalently, they can be written like this: 3:foo\\n (with a newline instead
  of comma).  This function does that.

  See "Protocol Modifications" for the reasoning.
  """
  assert isinstance(byte_str, str), "Can only dump raw byte strings"
  return '%d:%s\n' % (len(byte_str), byte_str)


def dumps(data):
  """Convert a JSON-like object to a serialized TNET string.

  Raises:
    TypeError: if the type of data can't be serialized (this is what the JSON
    module does as well)
  """
  t = type(data)
  if t is long or t is int:
    out = str(data)
    return '%d:%s#' % (len(out), out)
  elif t is float:
    out = '%f' % data
    return '%d:%s^' % (len(out), out)
  elif t is str:
    return '%d:' % len(data) + data + ','
  elif t is unicode:
    data = data.encode('utf-8')
    return '%d:' % len(data) + data + '$'
  elif t is dict:
    return dump_dict(data)
  elif t is list:
    return dump_list(data)
  elif t is tuple:
    return dump_list(data)
  elif data is None:
    return '0:~'
  elif t is bool:
    out = ('f', 't')[data]
    return '%d:%s?' % (len(out), out)
  else:
    raise TypeError(
        "Can't serialize type %r (%r)" % (type(data), str(data)[:20]))


# NOTE: Inlining these functinos didn't seem to make a real difference, although
# I need to test on more data

def dump_dict(data):
  result = []
  for k, v in data.iteritems():
    result.append(dumps(k))
    result.append(dumps(v))

  payload = ''.join(result)
  return '%d:%s}' % (len(payload), payload)


def dump_list(data):
  payload = ''.join([dumps(i) for i in data])
  return '%d:%s]' % (len(payload), payload)


#
# DESERIALIZATION
#


def loads_prefix(data):
  """Parses a string into a Python-like object.

  Raises:
    ValueError if there is an error parsing the serialized form
  """
  if not data:
    raise ValueError("Got empty data to parse")

  left = data.find(':')  # position of ':'
  length = int(data[:left])
  right = left + length + 1  # position of } ] etc

  payload = data[left+1:right]
  try:
    payload_type = data[right]
  except IndexError:
    # This catches the case that len(payload) < length
    raise ValueError(
      "Data was too short: got %s bytes, expected %s" %
      (len(payload), length+1))

  value = parse_value(payload, payload_type)
  return value, data[right+1:]


def loads(data):
  value, extra = loads_prefix(data)
  if extra:
    raise ValueError("Got extra bytes: %r" % extra)
  return value


def parse_value(payload, payload_type):
  # NOTE: the if-else chain appears to be slightly faster than a dictionary
  # dispatch, at least on Python 2.7/32-bit
  if payload_type == '#':
    return int(payload)
  elif payload_type == '}':
    return parse_dict(payload)
  elif payload_type == ']':
    return parse_list(payload)
  elif payload_type == '?':
    # NOTE: no checking for invalid payloads here
    return payload == 't'
  elif payload_type == '^':
    return float(payload)
  elif payload_type == '~':
    if payload:
      raise ValueError("Can't have non-empty payload for null value")
    return None
  elif payload_type == ',' or payload_type == '\n':
    return payload
  elif payload_type == '$':
    return unicode(payload, 'utf-8')
  elif payload_type == '!':
    # backward compatibility: tnetstrings uses '!'.
    # NOTE: no checking for invalid payloads here
    return payload == 'true'
  else:
    raise ValueError("Invalid payload type: %r" % payload_type)


def parse_list(data):
  result = []
  extra = data
  while True:
    if not extra:
      break
    value, extra = loads_prefix(extra)
    result.append(value)

  return result


def parse_dict(data):
  extra = data
  result = {}
  while True:
    if not extra:
      break
    key, extra = loads_prefix(extra)
    if not isinstance(key, basestring):
      raise ValueError("Keys can only be strings.")
    if not extra:
      raise ValueError("Got an odd number of dictionary items")
    value, extra = loads_prefix(extra)
    result[key] = value

  return result


def read_length(read_func):
  # TODO: We should also prevent the loop from going too many times?
  buf = ''
  while True:
    c = read_func(1)
    if not c:  # EOF
      raise EOFError
    if not c.isdigit():
      if buf:
        if c != ':':
          raise ValueError("Expected ':', got %r" % c)
      else:  # didn't get a number
        raise ValueError("Expected chunk length, got %r" % c)
      break
    buf += c
  return buf


def _read(read_func, max_length):
  """Helper for read and readfd."""
  length_str = read_length(read_func)
  length = int(length_str)
  if max_length and length > max_length:
    raise ValueError("Payload is too large: %s" % length)
  payload1 = read_func(length+1)  # read n+1 bytes
  return length_str + ':' + payload1


def read(f, max_length=0):
  read_func = f.read
  return _read(read_func, max_length)


def readfd(fd, max_length=0):
  read_func = lambda length: os.read(fd, length)
  return _read(read_func, max_length)


def _load(read_func, max_length):
  """Helper for load and loadfd."""
  length_str = read_length(read_func)
  length = int(length_str)
  if max_length and length > max_length:
    raise ValueError("Payload is too large: %s" % length)
  # TODO: If this reads less than the 'length' bytes, should we also raise
  # EOFError?
  payload = read_func(length)
  payload_type = read_func(1)
  return parse_value(payload, payload_type)


def load(f, max_length=0):
  """Load from a file.

  It leaves the file pointer at the end of the record.  NOTE: This would be a
  fragile disk serialization format, because if one byte is corrupted, it's hard
  to "resynchronize" in the middle of the stream.  But it should be fine for
  reading out of pipes.

  Raises:
    EOFError if it encounters EOF on the file
  """
  read_func = f.read
  return _load(read_func, max_length)


def loadfd(fd, max_length=0):
  """Load from a file descriptor.

  This behaves identically to load(), except it bypasses Python's buffered I/O.

  This function is appropriate to use if you want to first load a netstring from
  a file descriptor, and then do select() or some other low-level operation on
  the file descriptor.

  That does NOT work with Python file handles (unless you set
  PYTHONUNBUFFERED=1).  The issue is that Python will buffer internally, and
  select() won't register anything on the file descriptor (because it's in the
  user space buffer).

  Raises:
    EOFError if it encounters EOF on the file
  """
  read_func = lambda length: os.read(fd, length)
  return _load(read_func, max_length)


def main(argv):
  try:
    action = argv[1]
  except IndexError:
    raise RuntimeError("Action should be 'from-json' or 'to-json'.")

  # convert JSON on stdin to TNET
  if action == 'from-json':
    input_data = sys.stdin.read()
    j = json.loads(input_data)
    # make sure there's no extra whitespace
    sys.stdout.write(dumps(j))

  # Print TNET on stdin in a human-readable format
  elif action == 'to-json':
    while True:
      try:
        value = load(sys.stdin)
      except EOFError:
        break
      print json.dumps(value)
  else:
    raise RuntimeError("Action should be 'from-json' or 'to-json'.")


if __name__ == '__main__':
  import json
  import pprint
  import sys
  try:
    sys.exit(main(sys.argv))
  except RuntimeError, e:
    print >> sys.stderr, e.args[0]
  sys.exit(1)
