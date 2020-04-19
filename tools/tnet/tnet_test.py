#!/usr/bin/python -S
"""
tnetstrings_test.py: Tests for tnetstrings.py

Should I use  taste.test for multiplatform tests?
"""

from __future__ import with_statement

__author__ = 'Andy Chu'


import cStringIO
import os
import unittest

import tnet  # module under test


class TnetStringsTest(unittest.TestCase):

  def assertRaises(self, exc, error_substring, func, *args, **kwargs):
    try:
      func(*args, **kwargs)
    except Exception, e:
      if not isinstance(e, exc):
        self.fail("Expected exception type: %s, got %s" % (exc, type(e)))
      if error_substring not in str(e):
        self.fail(
            "Expected %r to be a substring of %r" % (error_substring, str(e)))
    else:
      self.fail("Expected exception type: %s, nothing raise" % exc)

  def testRoundTrip(self):
    cases = [
        None,
        True, False,
        1,
        3.2,
        'hello',
        #u'hello',
        [],
        [1],
        ["hi"],
        ["hi", "byte"],
        ["hi", 1, False],
        ["hi", 1, False, {"byte": 1}],
        {},
        {"hi": 1},
        {"hi": [1,2,3]},
        [{"a": 1, "b": 2}],
        ]

    for o in cases:
      serialized = tnet.dumps(o)
      o2, rest = tnet.loads_prefix(serialized)
      self.assertEqual(o, o2)
      self.assertEqual('', rest)

      # Test the \n synonym
      serialized3 = serialized.replace(',', '\n')
      o3, rest = tnet.loads_prefix(serialized3)
      self.assertEqual(o, o3)
      self.assertEqual('', rest)

      # Test loading from a file
      f = cStringIO.StringIO(serialized)
      o4 = tnet.load(f)
      self.assertEqual(o, o4)

  def testExtraData(self):
    self.assertRaises(
        ValueError, "Got extra bytes: 'extra-bytes'", 
        tnet.loads, '2:ab,extra-bytes')

    value, rest = tnet.loads_prefix('2:ab,extra-bytes')
    self.assertEqual('ab', value)
    self.assertEqual('extra-bytes', rest)

    value = tnet.loads('2:ab,')
    self.assertEqual('ab', value)

  def testOneWay(self):
    # Treat tuple as tnet "array"
    tuple_str = tnet.dumps(('a', 'b'))
    self.assertEqual('8:1:a,1:b,]', tuple_str)
    self.assertEqual(tuple_str, tnet.dumps(['a', 'b']))

  def testBadLoad(self):
    self.assertRaises(
        ValueError, 'non-empty payload', 
        tnet.loads, '1:f~')

    self.assertRaises(
        ValueError, 'Got empty data', 
        tnet.loads, '')

    self.assertRaises(
        ValueError, 'Data was too short', 
        tnet.loads, '2:f,')

    # Too long
    self.assertRaises(
        ValueError, 'Invalid payload type', 
        tnet.loads, '2:ffff,')

    self.assertRaises(
        ValueError, 'Got an odd number', 
        tnet.loads, '4:1:a,}')

    self.assertRaises(
        ValueError, 'Keys can only be strings', 
        tnet.loads, '6:0:~0:~}')  # tring {null: null}

  def testBadDump(self):
    # try to dump an instance objectj
    self.assertRaises(
        TypeError, "Can't serialize type", 
        tnet.dumps, self)

  def testLoad(self):
    f = cStringIO.StringIO('1:1#')
    print tnet.load(f)
    f = cStringIO.StringIO('4:true!')
    print tnet.load(f)
    f = cStringIO.StringIO('5:false!')
    print tnet.load(f)
    f = cStringIO.StringIO('5:false!')
    try:
      tnet.load(f, max_length=4)
    except ValueError:
      pass
    else:
      self.fail("Expected ValueError")

  def testRead(self):
    f = cStringIO.StringIO('1:1#extra')
    s = tnet.read(f)
    self.assertEqual('1:1#', s)

  def testFd(self):
    # NOTE: We don't create _tmp
    with open('../_tmp/testfd.tnet', 'w') as f:
      f.write('1:1#1:2#foo')
    fd = os.open('../_tmp/testfd.tnet', os.O_RDONLY)
    # Load from it
    obj = tnet.loadfd(fd)
    self.assertEqual(1, obj)
    # read from it from it
    s = tnet.readfd(fd)
    self.assertEqual('1:2#', s)

  def testDumpLine(self):
    # Test that you can round trip with dump_line
    s = tnet.dump_line('fo\no\0')
    obj = tnet.loads(s)
    self.assertEqual('fo\no\0', obj)

  def testInstructions(self):
    import dis
    dis.dis(tnet.dump_list)


if __name__ == '__main__':
  unittest.main()
