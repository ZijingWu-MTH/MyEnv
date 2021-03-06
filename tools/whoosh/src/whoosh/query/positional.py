# Copyright 2007 Matt Chaput. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY MATT CHAPUT ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL MATT CHAPUT OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Matt Chaput.

from __future__ import division
import copy

from whoosh import matching
from whoosh.analysis import Token
from whoosh.compat import u
from whoosh.query import qcore, terms, nary


class Phrase(qcore.Query):
    """Matches documents containing a given phrase."""

    def __init__(self, fieldname, words, slop=1, boost=1.0, char_ranges=None):
        """
        :param fieldname: the field to search.
        :param words: a list of words (unicode strings) in the phrase.
        :param slop: the number of words allowed between each "word" in the
            phrase; the default of 1 means the phrase must match exactly.
        :param boost: a boost factor that to apply to the raw score of
            documents matched by this query.
        :param char_ranges: if a Phrase object is created by the query parser,
            it will set this attribute to a list of (startchar, endchar) pairs
            corresponding to the words in the phrase
        """

        self.fieldname = fieldname
        self.words = words
        self.slop = slop
        self.boost = boost
        self.char_ranges = char_ranges

    def __eq__(self, other):
        return (other and self.__class__ is other.__class__ and
                self.fieldname == other.fieldname and self.words == other.words
                and self.slop == other.slop and self.boost == other.boost)

    def __repr__(self):
        return "%s(%r, %r, slop=%s, boost=%f)" % (self.__class__.__name__,
                                                  self.fieldname, self.words,
                                                  self.slop, self.boost)

    def __unicode__(self):
        return u('%s:"%s"') % (self.fieldname, u(" ").join(self.words))
    __str__ = __unicode__

    def __hash__(self):
        h = hash(self.fieldname) ^ hash(self.slop) ^ hash(self.boost)
        for w in self.words:
            h ^= hash(w)
        return h

    def has_terms(self):
        return True

    def tokens(self, boost=1.0):
        char_ranges = self.char_ranges
        startchar = endchar = None
        for i, word in enumerate(self.words):
            if char_ranges:
                startchar, endchar = char_ranges[i]

            yield Token(fieldname=self.fieldname, text=word,
                        boost=boost * self.boost, startchar=startchar,
                        endchar=endchar, chars=True)

    def normalize(self):
        if not self.words:
            return qcore.NullQuery
        if len(self.words) == 1:
            t = terms.Term(self.fieldname, self.words[0])
            if self.char_ranges:
                t.startchar, t.endchar = self.char_ranges[0]
            return t

        words = [w for w in self.words if w is not None]
        return self.__class__(self.fieldname, words, slop=self.slop,
                              boost=self.boost, char_ranges=self.char_ranges)

    def replace(self, fieldname, oldtext, newtext):
        q = copy.copy(self)
        if q.fieldname == fieldname:
            for i, word in enumerate(q.words):
                if word == oldtext:
                    q.words[i] = newtext
        return q

    def _and_query(self):
        return nary.And([terms.Term(self.fieldname, word)
                         for word in self.words])

    def estimate_size(self, ixreader):
        return self._and_query().estimate_size(ixreader)

    def estimate_min_size(self, ixreader):
        return self._and_query().estimate_min_size(ixreader)

    def matcher(self, searcher, weighting=None):
        fieldname = self.fieldname
        reader = searcher.reader()

        # Shortcut the query if one of the words doesn't exist.
        for word in self.words:
            if (fieldname, word) not in reader:
                return matching.NullMatcher()

        field = searcher.schema[fieldname]
        if not field.format or not field.format.supports("positions"):
            raise qcore.QueryError("Phrase search: %r field has no positions"
                                  % self.fieldname)

        # Construct a tree of SpanNear queries representing the words in the
        # phrase and return its matcher
        from whoosh.spans import SpanNear
        q = SpanNear.phrase(fieldname, self.words, slop=self.slop)
        m = q.matcher(searcher, weighting=weighting)
        if self.boost != 1.0:
            m = matching.WrappingMatcher(m, boost=self.boost)
        return m


class Ordered(nary.And):
    """Matches documents containing a list of sub-queries in the given order.
    """

    JOINT = " BEFORE "

    def matcher(self, searcher, weighting=None):
        from whoosh.spans import SpanBefore

        return self._matcher(SpanBefore._Matcher, None, searcher,
                             weighting=weighting)



