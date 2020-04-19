#!/usr/bin/python
"""
benchmark.py

NOTE: Python 2.6 stdlib json doesn't have C speedups, but Python 2.7 does.
This makes a huge difference (8-10x faster with C).

On Python 2.6, here is an example, using testdata/test.json (which is probably
not representative, more cases would be better).

- tnet.py is faster than the original tnetstrings module (some simple Python
optimizations).

- We're almost exactly the as fast on encoding as Python json, and >3x faster
on decoding.

- tnet is slightly smaller, but not much.


tnetstrings serialized size 12946

tnet.py dumps:
        per run: 3.007278 ms

tnetstrings.py dump:
        per run: 3.413620 ms

tnet.py parse:
        per run: 3.928602 ms

tnetstrings.py parse:
        per run: 4.722099 ms

JSON serialized size 13578

json.dumps:
        per run: 3.048642 ms

json.loads:
        per run: 11.046679 ms
"""

__author__ = 'Andy Chu'


try:
  import json
except ImportError:
  # for Python 2.5
  import simplejson as json
  print 'Using SIMPLEJSON'

import cProfile
import pstats  # wtf, on ubuntu this requires package 'python-profiler'
import sys
import time

import tnet
import tnetstrings
import tnetstrings2


class Error(Exception):
  pass


def timeit(func, d):
  start = time.time()
  n = 100
  for i in xrange(n):
    s = func(d)
  elapsed = time.time() - start
  print '\telapsed: %f ms' % (elapsed*1000)
  print '\tper run: %f ms' % (elapsed*1000/n)
  print


# Oops: json is using a C extension.  That's why it's 10x faster for some cases.
# Doh.
#
# homer python2.7$ python
# Python 2.7.1+ (r271:86832, Apr 11 2011, 18:05:24) 
# [GCC 4.5.2] on linux2
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import _json
# >>> _json
# <module '_json' from '/usr/lib/python2.7/lib-dynload/_json.so'>


def Profile(d):
  j = json.dumps(d)
  t = tnetstrings.dump(d)
  ctx = {
      'd': d,
      't': t,
      'j': j,
      'json': json,
      'tnet': tnet,
      'tnetstrings': tnetstrings,
      }


  print 'profiling json'
  cProfile.runctx('json.dumps(d)', ctx, ctx, 'json_dump.prof',)
  cProfile.runctx('json.loads(j)', ctx, ctx, 'json_load.prof',)
  print 'profiling tnet'
  cProfile.runctx('for i in xrange(100): tnet.dumps(d)', ctx, ctx, 'tnet_dump.prof')
  cProfile.runctx('for i in xrange(100): tnet.loads(t)', ctx, ctx, 'tnet_load.prof')
  print 'profiling tnetstrings'
  cProfile.runctx('for i in xrange(100): tnetstrings.dump(d)', ctx, ctx,
      'tnetstrings_dump.prof')
  cProfile.runctx('for i in xrange(100): tnetstrings.parse(t)', ctx, ctx,
      'tnetstrings_load.prof')


def Stats():
  for filename in ['json_dump', 'json_load', 'tnet_dump', 'tnet_load',
      'tnetstrings_dump', 'tnetstrings_load']:
    s = pstats.Stats(filename + '.prof')
    s.sort_stats('time').print_stats()


def RunAll(d):
  s = tnetstrings.dump(d)

  s2 = tnetstrings2.dump(d)

  print 'rows', len(d)
  print 'tnetstrings serialized size', len(s)
  print 'tnetstrings2 serialized size', len(s2)

  assert s == s2

  print 'tnet.py dumps:'
  timeit(tnet.dumps, d)
  print 'tnetstrings.py dump:'
  timeit(tnetstrings.dump, d)
  print 'tnetstrings2.py dump:'
  timeit(tnetstrings2.dump, d)

  print '--'

  print 'tnet.py parse:'
  timeit(tnet.parse, s)
  print 'tnetstrings.py parse:'
  timeit(tnetstrings.parse, s)

  print '--'

  j = json.dumps(d)
  print 'JSON serialized size', len(j)

  print 'json.dumps:'
  timeit(json.dumps, d)

  print 'json.loads:'
  timeit(json.loads, j)


def main(argv):
  """Returns an exit code."""
  d = json.load(open(argv[1]))
  action = argv[2]
  if action == 'all':
    RunAll(d)
  elif action == 'profile':
    Profile(d)
  elif action == 'stats':
    Stats()


if __name__ == '__main__':
  try:
    sys.exit(main(sys.argv))
  except Error, e:
    print >> sys.stderr, e.args[0]
    sys.exit(1)
