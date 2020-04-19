#!/usr/bin/python -S
"""
tnetstrings2_test.py: Tests for tnetstrings2.py
"""

__author__ = 'Andy Chu'


import sys
import unittest

import tnetstrings2  # module under test


class FooTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testFoo(self):
    print tnetstrings2.dump(1)
    print tnetstrings2.dump(None)
    print tnetstrings2.dump(True)
    print tnetstrings2.dump(1.234)
    print tnetstrings2.dump('foo')
    print tnetstrings2.dump({'one': 'two'})
    print tnetstrings2.dump(['one', 'two', 'three'])
    print tnetstrings2.dump({'yo': ['one', 'two', 'three']})


if __name__ == '__main__':
  unittest.main()
