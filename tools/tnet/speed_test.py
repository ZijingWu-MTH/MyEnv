#!/usr/bin/python

# http://librelist.com/browser//mongrel2/2011/3/21/tnetstrings-speed-test/
# http://codepad.org/Uj42SuMo

import sys
import json
import simplejson

def parse_payload(data):
    assert data, "Invalid data to parse, it's empty."
    length, extra = data.split(':', 1)
    length = int(length)

    payload, extra = extra[:length], extra[length:]
    assert extra, "No payload type: %r, %r" % (payload, extra)
    payload_type, remain = extra[0], extra[1:]

    assert len(payload) == length, "Data is wrong length %d vs %d" % (length, len(payload))
    return payload, payload_type, remain

def parse_list(data):
    if len(data) == 0: return []

    result = []
    value, extra = parse_tnetstring(data)
    result.append(value)

    while extra:
        value, extra = parse_tnetstring(extra)
        result.append(value)

    return result

def parse_pair(data):
    key, extra = parse_tnetstring(data)
    assert extra, "Unbalanced dictionary store."
    value, extra = parse_tnetstring(extra)
    #assert value, "Got an invalid value, null not allowed."

    return key, value, extra

def parse_dict(data):
    if len(data) == 0: return {}

    key, value, extra = parse_pair(data)
    result = {key: value}

    while extra:
        key, value, extra = parse_pair(extra)
        result[key] = value
  
    return result
    
def parse_tnetstring(data):
    payload, payload_type, remain = parse_payload(data)

    if payload_type == '#':
        value = int(payload)
    elif payload_type == '}':
        value = parse_dict(payload)
    elif payload_type == ']':
        value = parse_list(payload)
    elif payload_type == '!':
        value = payload == 'true'
    elif payload_type == '^':
        value = float(payload)
    elif payload_type == '~':
        assert len(payload) == 0, "Payload must be 0 length for null."
        value = None
    elif payload_type == ',':
        value = payload
    else:
        assert False, "Invalid payload type: %r" % payload_type

    return value, remain


def dump_dict(data):
    result = []
    for k,v in data.items():
        result.append(dump_tnetstring(str(k)))
        result.append(dump_tnetstring(v))

    payload = ''.join(result)
    return '%d:' % len(payload) + payload + '}'


def dump_list(data):
    result = []
    for i in data:
        result.append(dump_tnetstring(i))

    payload = ''.join(result)
    return '%d:' % len(payload) + payload + ']'


def dump_tnetstring(data):
    if type(data) is long or type(data) is int:
        out = str(data)
        return '%d:%s#' % (len(out), out)
    if type(data) is float:
        out = '%f' % data
        return '%d:%s^' % (len(out), out)
    elif type(data) is str:
        return '%d:' % len(data) + data + ',' 
    elif type(data) is dict:
        return dump_dict(data)
    elif type(data) is list:
        return dump_list(data)
    elif data == None:
        return '0:~'
    elif type(data) is bool:
        out = repr(data).lower()
        return '%d:%s!' % (len(out), out)
    else:
        assert False, "Can't serialize stuff that's %s." % type(data)


TESTS = {
    '0:}': {},
    '0:]': [],
    '51:5:hello,39:11:12345678901#4:this,4:true!0:~4:\x00\x00\x00\x00,]}': 
            {'hello': [12345678901, 'this', True, None, '\x00\x00\x00\x00']},
    '5:12345#': 12345,
    '12:this is cool,': "this is cool",
    '0:,': "",
    '0:~': None,
    '4:true!': True,
    '5:false!': False,
    '10:\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00,': "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    '24:5:12345#5:67890#5:xxxxx,]': [12345, 67890, 'xxxxx'],
}

BIG_TEST = 1
# Overwrite with our bad test case
if BIG_TEST:
  TESTS = {}
  testdata = json.load(open('testdata/test.json'))
  from pprint import pprint
  #pprint(testdata)
  TESTS[dump_tnetstring(testdata)] = testdata


JSON_TESTS = {}

for k,v in TESTS.items():
    JSON_TESTS[json.dumps(v)] = v



def thrash_tnetstrings(count):
    for i in xrange(0,count):
        for data, expect in TESTS.items():
            payload, remain = parse_tnetstring(data)
            again = dump_tnetstring(payload)
            back, extra = parse_tnetstring(again)

def thrash_simplejson(count):
    for i in xrange(0,count):
        for data, expect in JSON_TESTS.items():
            payload = simplejson.loads(data)
            again = simplejson.dumps(payload)
            back = simplejson.loads(again)

def thrash_json(count):
    for i in xrange(0,count):
        for data, expect in JSON_TESTS.items():
            payload = json.loads(data)
            again = json.dumps(payload)
            back = json.loads(again)
    

if sys.argv[1] == 'json':
    print 'json'
    thrash_json(int(sys.argv[2]))
elif sys.argv[1] == 'simplejson':
    print 'simplejson'
    thrash_simplejson(int(sys.argv[2]))
else:
    print 'tnet'
    thrash_tnetstrings(int(sys.argv[2]))

