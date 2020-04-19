import os
import re
import datetime
import sys
import token
import util
import shelve
from sets import Set

def getIdToken(tokens):
    result = Set()
    for token in tokens:
        if (token.typ == "ID" and (token not in result)):
            result.add(token)
    return result

def check_missed_self_header(filePath):
    selfHeader = util.getHeaderFileBaseOnSource(filePath)
    if (not os.path.isfile(selfHeader)):
        return None
    lines = file(filePath, 'rb').readlines()
    if (not wether_included_header(lines, selfHeader)):
        return "Warning: Not included self file header."
        

def missedHeader(filePath):
    lines = file(filePath, 'rb').readlines()
    selfHeader = util.getHeaderFileBaseOnSource(filePath)
    needIncludeHeaders = []
    str = ""
    for line in lines:
        str = str + line

    tokens = util.tokenize(str)
    tokens = getIdToken(tokens)
    for fileName, keyWordPattern in headerTemplate.iteritems():
        for keyWord in keyWordPattern:
            for token in tokens:
                if (re.match("^" +  keyWord + "$", token.value)):
                    needIncludeHeaders = needIncludeHeaders + [fileName]

    missedHeader = []
    headerLines = []
    if (os.path.isfile(selfHeader)):
        headerLines = file(selfHeader, 'rb').readlines()
    for header in needIncludeHeaders:
        if (not wether_included_header(lines, header) and
            not wether_included_header(headerLines, header)):
            missedHeader = missedHeader + [header]        
    return missedHeader

def wether_included_header(lines, header):
    for line in lines:
        if (line.find("#include") >= 0 and (line.find("<%s>" % header) >= 0 or line.find("\"%s\"" % header) >= 0)):
            return True
    return False

def check_promoted_already(id):
    databaseFile = os.environ.get('ROOT') + "/__fly_check.shelve"
    database = shelve.open(databaseFile)
    if (not database.has_key(id)):
        return False
    return True

def promoted_already(id):
    databaseFile = os.environ.get('ROOT') + "/__fly_check.shelve"
    database = shelve.open(databaseFile)
    database[id] = datetime.datetime.now()

def getMissedHeaderKey(sourceFile, header):
    return sourceFile + ":" + header
    

headerTemplate = {
    "vector":         ["push_back"],
    "functional":     ["bind1st", "bind2nd", "mem_fn", "not1", "not2", "binder1st", "binder2nd"],
    "iostream":       ["cout", "endl"],
    "memory":         ["auto_ptr"],
    "cstdio":         ["s?scanf", "puts", "s?printf", "f?gets"],
    "ssert.h":        ["assert"],
    "cstring":        ["mem(?:cpy|set|n?cmp)", "str(?:len|n?cmp|n?cpy|error)"],
    "cstdlib":        ["system","abs","ato[if]","strto[dflu]+","free","l?abs","s?rand(?:_r|om)?"],
    "cmath":          ["a?(?:sin|cos|tan)[hl]*", "exp[m12fl]*", "fabs[fl]?", "log[210fl]+", "nan[fl]?", "(?:ceil|floor)[fl]?", "l?l?round"],
    "cstrings":       ["b(?:cmp|copy|zero)", "strn?casecmp"],
    "typeinfo":       ["typeid"],
    "new":            ["set_new_handler"],
    "limits":         ["numeric_limits"],
    "algorithm":      ["all_of", "any_of", "none_of", "find", "find_if", "find_end", "find_first_of", "count", "count_if", "mismatch", "equal", "is_permutation", "search", "search_n", "copy", "copy_n", "copy_if", "copy_backward", "move", "move_backward", "swap", "swap_ranges", "iter_swap", "transform", "replace", "replace_if", "replace_copy", "replace_copy_if", "fill", "fill_n", "generate", "generate_n", "remove", "remove_if", "remove_copy", "remove_copy_if", "unique", "unique_copy", "reverse", "reverse_copy", "rotate", "rotate_copy", "random_shuffle", "stable_partition", "stable_sort", "partial_sort", "partial_sort_copy", "nth_element", "lower_bound", "upper_bound", "equal_range", "binary_search", "inplace_merge", "set_union", "set_intersection", "set_difference", "set_symmetric_difference", "push_heap", "pop_heap", "make_heap", "sort_heap", "min_element", "max_element", "lexicographical_compare", "next_permutation", "prev_permutation"],
    "numeric":        ["partial_sum", "accumulate", "adjacent_difference", "inner_product"],
    "iostream":       ["c(?:err|out|in)"],
    "sstream":        ["[io]stringstream"],
    "bitset":         ["bitset"],
    "complex":        ["complex"],
    "deque":          ["deque"],
    "priority_queue": ["priority_queue"],
    "list":           ["list"],
    "map":            ["(?:multi)?map"],
    "set":            ["(?:multi)?set"],
    "vector":         ["vector"],
    "string":         ["string"],
    }


sourceFile = os.path.abspath(sys.argv[1])
missedHeader = missedHeader(sourceFile)

notPromotedMissedHeader = []
for header in missedHeader:
    if (not check_promoted_already(getMissedHeaderKey(sourceFile, header))):
        notPromotedMissedHeader = notPromotedMissedHeader + [header]
    promoted_already(getMissedHeaderKey(sourceFile, header))

if (len(notPromotedMissedHeader) > 0):
    print "Following header are missed:"
    print notPromotedMissedHeader

errorMsg = check_missed_self_header(sourceFile)
if (errorMsg != None):
    print errorMsg
