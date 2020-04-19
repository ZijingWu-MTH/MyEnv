from __future__ import with_statement

from nose.tools import assert_equal, assert_raises  #@UnresolvedImport

import random
from array import array

from whoosh.compat import b, u, xrange, array_tobytes
from whoosh.filedb.filestore import RamStorage
from whoosh.support import dawg
from whoosh.support.testing import TempStorage


def gwrite(keys, st=None):
    st = st or RamStorage()
    f = st.create_file("test")
    gw = dawg.GraphWriter(f)
    gw.start_field("_")
    for key in keys:
        gw.insert(key)
    gw.finish_field()
    gw.close()
    return st


def greader(st):
    return dawg.GraphReader(st.open_file("test"))


def enlist(string):
    return string.split()


#

def test_empty_fieldname():
    gw = dawg.GraphWriter(RamStorage().create_file("test"))
    assert_raises(ValueError, gw.start_field, "")
    assert_raises(ValueError, gw.start_field, None)
    assert_raises(ValueError, gw.start_field, 0)


def test_empty_key():
    gw = dawg.GraphWriter(RamStorage().create_file("test"))
    gw.start_field("_")
    assert_raises(KeyError, gw.insert, b(""))
    assert_raises(KeyError, gw.insert, "")
    assert_raises(KeyError, gw.insert, u(""))
    assert_raises(KeyError, gw.insert, [])


def test_keys_out_of_order():
    f = RamStorage().create_file("test")
    gw = dawg.GraphWriter(f)
    gw.start_field("test")
    gw.insert("alfa")
    assert_raises(KeyError, gw.insert, "abba")


def test_duplicate_keys():
    st = gwrite(enlist("alfa bravo bravo bravo charlie"))
    cur = dawg.Cursor(greader(st))
    assert_equal(list(cur.flatten_strings()), ["alfa", "bravo", "charlie"])


def test_inactive_raise():
    st = gwrite(enlist("alfa bravo charlie"))
    cur = dawg.Cursor(greader(st))
    while cur.is_active():
        cur.next_arc()
    assert_raises(dawg.InactiveCursor, cur.label)
    assert_raises(dawg.InactiveCursor, cur.prefix)
    assert_raises(dawg.InactiveCursor, cur.prefix_bytes)
    assert_raises(dawg.InactiveCursor, list, cur.peek_key())
    assert_raises(dawg.InactiveCursor, cur.peek_key_bytes)
    assert_raises(dawg.InactiveCursor, cur.stopped)
    assert_raises(dawg.InactiveCursor, cur.value)
    assert_raises(dawg.InactiveCursor, cur.accept)
    assert_raises(dawg.InactiveCursor, cur.at_last_arc)
    assert_raises(dawg.InactiveCursor, cur.next_arc)
    assert_raises(dawg.InactiveCursor, cur.follow)
    assert_raises(dawg.InactiveCursor, cur.switch_to, b("a"))
    assert_raises(dawg.InactiveCursor, cur.skip_to, b("a"))
    assert_raises(dawg.InactiveCursor, list, cur.flatten())
    assert_raises(dawg.InactiveCursor, list, cur.flatten_v())
    assert_raises(dawg.InactiveCursor, list, cur.flatten_strings())
    assert_raises(dawg.InactiveCursor, cur.find_path, b("a"))


def test_types():
    st = RamStorage()

    types = ((dawg.IntValues, 100, 0),
             (dawg.BytesValues, b('abc'), b('')),
             (dawg.ArrayValues("i"), array("i", [0, 123, 42]), array("i")),
             (dawg.IntListValues, [0, 6, 97], []))

    for t, v, z in types:
        assert_equal(t.common(None, v), None)
        assert_equal(t.common(v, None), None)
        assert_equal(t.common(None, None), None)
        assert_equal(t.subtract(v, None), v)
        assert_equal(t.subtract(None, v), None)
        assert_equal(t.subtract(None, None), None)
        assert_equal(t.add(v, None), v)
        assert_equal(t.add(None, v), v)
        assert_equal(t.add(None, None), None)
        f = st.create_file("test")
        t.write(f, v)
        t.write(f, z)
        f.close()
        f = st.open_file("test")
        assert_equal(t.read(f), v)
        assert_equal(t.read(f), z)

    assert_equal(dawg.IntValues.common(100, 20), 20)
    assert_equal(dawg.IntValues.add(20, 80), 100)
    assert_equal(dawg.IntValues.subtract(100, 80), 20)

    assert_equal(dawg.BytesValues.common(b("abc"), b("abc")), b("abc"))
    assert_equal(dawg.BytesValues.common(b("abcde"), b("abfgh")), b("ab"))
    assert_equal(dawg.BytesValues.common(b("abcde"), b("ab")), b("ab"))
    assert_equal(dawg.BytesValues.common(b("ab"), b("abcde")), b("ab"))
    assert_equal(dawg.BytesValues.common(None, b("abcde")), None)
    assert_equal(dawg.BytesValues.common(b("ab"), None), None)

    a1 = array("i", [0, 12, 123, 42])
    a2 = array("i", [0, 12, 420])
    cm = array("i", [0, 12])
    assert_equal(dawg.ArrayValues.common(a1, a1), a1)
    assert_equal(dawg.ArrayValues.common(a1, a2), cm)
    assert_equal(dawg.ArrayValues.common(a2, a1), cm)
    assert_equal(dawg.ArrayValues.common(None, a1), None)
    assert_equal(dawg.ArrayValues.common(a2, None), None)


def _fst_roundtrip(domain, t):
    with TempStorage() as st:
        f = st.create_file("test")
        gw = dawg.GraphWriter(f, vtype=t)
        gw.start_field("_")
        for key, value in domain:
            gw.insert(key, value)
        gw.finish_field()
        gw.close()

        f = st.open_file("test")
        gr = dawg.GraphReader(f, vtype=t)
        cur = dawg.Cursor(gr)
        assert_equal(list(cur.flatten_v()), domain)
        f.close()


def test_fst_int():
    domain = [(b("aaab"), 0), (b("aabc"), 12), (b("abcc"), 23),
              (b("bcab"), 30), (b("bcbc"), 31), (b("caaa"), 70),
              (b("cbba"), 80), (b("ccca"), 101)]
    _fst_roundtrip(domain, dawg.IntValues)


def test_fst_bytes():
    domain = [(b("aaab"), b("000")), (b("aabc"), b("001")),
              (b("abcc"), b("010")), (b("bcab"), b("011")),
              (b("bcbc"), b("100")), (b("caaa"), b("101")),
              (b("cbba"), b("110")), (b("ccca"), b("111"))]
    _fst_roundtrip(domain, dawg.BytesValues)


def test_fst_array():
    domain = [(b("000"), array("i", [10, 231, 36, 40])),
              (b("001"), array("i", [1, 22, 12, 15])),
              (b("010"), array("i", [18, 16, 18, 20])),
              (b("011"), array("i", [52, 3, 4, 5])),
              (b("100"), array("i", [353, 4, 56, 62])),
              (b("101"), array("i", [3, 42, 5, 6])),
              (b("110"), array("i", [894, 9, 101, 11])),
              (b("111"), array("i", [1030, 200, 1000, 2000])),
              ]
    _fst_roundtrip(domain, dawg.ArrayValues("i"))


def test_fst_intlist():
    domain = [(b("000"), [1, 2, 3, 4]),
              (b("001"), [1, 2, 12, 15]),
              (b("010"), [1, 16, 18, 20]),
              (b("011"), [2, 3, 4, 5]),
              (b("100"), [3, 4, 5, 6]),
              (b("101"), [3, 4, 5, 6]),
              (b("110"), [8, 9, 10, 11]),
              (b("111"), [100, 200, 1000, 2000]),
              ]
    _fst_roundtrip(domain, dawg.IntListValues)


def test_fst_nones():
    domain = [(b("000"), [1, 2, 3, 4]),
              (b("001"), None),
              (b("010"), [1, 16, 18, 20]),
              (b("011"), None),
              (b("100"), [3, 4, 5, 6]),
              (b("101"), None),
              (b("110"), [8, 9, 10, 11]),
              (b("111"), None),
              ]
    _fst_roundtrip(domain, dawg.IntListValues)


def test_fst_accept():
    domain = [(b("a"), [1, 2, 3, 4]),
              (b("aa"), [1, 2, 12, 15]),
              (b("aaa"), [1, 16, 18, 20]),
              (b("aaaa"), [2, 3, 4, 5]),
              (b("b"), [3, 4, 5, 6]),
              (b("bb"), [3, 4, 5, 6]),
              (b("bbb"), [8, 9, 10, 11]),
              (b("bbbb"), [100, 200, 1000, 2000]),
              ]
    _fst_roundtrip(domain, dawg.IntListValues)


def test_words():
    words = enlist("alfa alpaca amtrak bellow fellow fiona zebulon")
    with TempStorage() as st:
        gwrite(words, st)
        gr = greader(st)
        cur = dawg.Cursor(gr)
        assert_equal(list(cur.flatten_strings()), words)
        gr.close()


def test_random():
    def randstring():
        length = random.randint(1, 10)
        a = array("B", (random.randint(0, 255) for _ in xrange(length)))
        return array_tobytes(a)
    keys = sorted(randstring() for _ in xrange(1000))

    with TempStorage() as st:
        gwrite(keys, st)
        gr = greader(st)
        cur = dawg.Cursor(gr)
        s1 = cur.flatten()
        s2 = sorted(set(keys))
        for i, (k1, k2) in enumerate(zip(s1, s2)):
            assert k1 == k2, "%s: %r != %r" % (i, k1, k2)

        sample = list(keys)
        random.shuffle(sample)
        for key in sample:
            cur.reset()
            cur.find_path(key)
            assert_equal(cur.prefix_bytes(), key)
        gr.close()


def test_shared_suffix():
    st = gwrite(enlist("blowing blue glowing"))

    gr = greader(st)
    cur1 = dawg.Cursor(gr)
    cur2 = dawg.Cursor(gr)

    cur1.find_path(b("blo"))
    cur2.find_path(b("glo"))
    assert_equal(cur1.stack[-1].target, cur2.stack[-1].target)


def test_fields():
    with TempStorage() as st:
        f = st.create_file("test")
        gw = dawg.GraphWriter(f)
        gw.start_field("f1")
        gw.insert("a")
        gw.insert("aa")
        gw.insert("ab")
        gw.finish_field()
        gw.start_field("f2")
        gw.insert("ba")
        gw.insert("baa")
        gw.insert("bab")
        gw.close()

        gr = dawg.GraphReader(st.open_file("test"))
        cur1 = dawg.Cursor(gr, gr.root("f1"))
        cur2 = dawg.Cursor(gr, gr.root("f2"))
        assert_equal(list(cur1.flatten_strings()), ["a", "aa", "ab"])
        assert_equal(list(cur2.flatten_strings()), ["ba", "baa", "bab"])
        gr.close()


def test_within():
    with TempStorage() as st:
        gwrite(enlist("0 00 000 001 01 010 011 1 10 100 101 11 110 111"), st)
        gr = greader(st)
        s = set(dawg.within(gr, "01", k=1))
        gr.close()
    assert_equal(s, set(["0", "00", "01", "011", "010",
                         "001", "10", "101", "1", "11"]))


def test_within_match():
    st = gwrite(enlist("abc def ghi"))
    gr = greader(st)
    assert_equal(set(dawg.within(gr, "def")), set(["def"]))


def test_within_insert():
    st = gwrite(enlist("00 01 10 11"))
    gr = greader(st)
    s = set(dawg.within(gr, "0"))
    assert_equal(s, set(["00", "01", "10"]))


def test_within_delete():
    st = gwrite(enlist("abc def ghi"))
    gr = greader(st)
    assert_equal(set(dawg.within(gr, "df")), set(["def"]))

    st = gwrite(enlist("0"))
    gr = greader(st)
    assert_equal(list(dawg.within(gr, "01")), ["0"])


def test_within_replace():
    st = gwrite(enlist("abc def ghi"))
    gr = greader(st)
    assert_equal(set(dawg.within(gr, "dez")), set(["def"]))

    st = gwrite(enlist("00 01 10 11"))
    gr = greader(st)
    s = set(dawg.within(gr, "00"))
    assert_equal(s, set(["00", "10", "01"]), s)


def test_within_transpose():
    st = gwrite(enlist("abc def ghi"))
    gr = greader(st)
    s = set(dawg.within(gr, "dfe"))
    assert_equal(s, set(["def"]))


def test_within_k2():
    st = gwrite(enlist("abc bac cba"))
    gr = greader(st)
    s = set(dawg.within(gr, "cb", k=2))
    assert_equal(s, set(["abc", "cba"]))


def test_within_prefix():
    st = gwrite(enlist("aabc aadc babc badc"))
    gr = greader(st)
    s = set(dawg.within(gr, "aaxc", prefix=2))
    assert_equal(s, set(["aabc", "aadc"]))


def test_skip():
    st = gwrite(enlist("abcd abfg cdqr1 cdqr12 cdxy wxyz"))
    gr = greader(st)
    cur = gr.cursor()
    while not cur.stopped(): cur.follow()
    assert_equal(cur.prefix_bytes(), b("abcd"))
    assert cur.accept()

    cur = gr.cursor()
    while not cur.stopped(): cur.follow()
    assert_equal(cur.prefix_bytes(), b("abcd"))
    cur.skip_to(b("cdaa"))
    assert_equal(cur.peek_key_bytes(), b("cdqr1"))
    assert_equal(cur.prefix_bytes(), b("cdq"))

    cur = gr.cursor()
    while not cur.stopped(): cur.follow()
    cur.skip_to(b("z"))
    assert not cur.is_active()


def test_insert_bytes():
    # This test is only meaningful on Python 3
    domain = [b("alfa"), b("bravo"), b("charlie")]

    st = RamStorage()
    gw = dawg.GraphWriter(st.create_file("test"))
    gw.start_field("test")
    for key in domain:
        gw.insert(key)
    gw.close()

    cur = dawg.GraphReader(st.open_file("test")).cursor()
    assert_equal(list(cur.flatten()), domain)


def test_insert_unicode():
    domain = [u("\u280b\u2817\u2801\u281d\u2809\u2811"),
              u("\u65e5\u672c"),
              u("\uc774\uc124\ud76c"),
              ]

    st = RamStorage()
    gw = dawg.GraphWriter(st.create_file("test"))
    gw.start_field("test")
    for key in domain:
        gw.insert(key)
    gw.close()

    cur = dawg.GraphReader(st.open_file("test")).cursor()
    assert_equal(list(cur.flatten_strings()), domain)


def test_within_unicode():
    domain = [u("\u280b\u2817\u2801\u281d\u2809\u2811"),
              u("\u65e5\u672c"),
              u("\uc774\uc124\ud76c"),
              ]

    st = RamStorage()
    gw = dawg.GraphWriter(st.create_file("test"))
    gw.start_field("test")
    for key in domain:
        gw.insert(key)
    gw.close()

    gr = dawg.GraphReader(st.open_file("test"))
    s = list(dawg.within(gr, u("\uc774.\ud76c")))
    assert_equal(s, [u("\uc774\uc124\ud76c")])







