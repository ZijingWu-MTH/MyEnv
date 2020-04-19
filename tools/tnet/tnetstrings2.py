# MODIFICATION 
#
# of the original tnetstrings.py.
#
# This tries to avoid string copies.  Instead it builds up lists of chunks, and
# then flattens it once (recursively) at the end.
#
# But unfortunately it's SLOWER (at least on my testdata), I think because of
# more Python byte codes.  String copies are fast and aren't the bottleneck.
#
# TODO:
# - need to test it with up to 10MB input.  I think we don't care about input
# greater than 10MB, because that should use PGI streaming.
#
# Note this implementation is more strict than necessary to demonstrate
# minimum restrictions on types allowed in dictionaries.
#
# Another implementation option: do it with bytearray?  not sure if that will be
# faster

def dump(data):
  tree = []
  dump_node(data, tree.append)
  # now flatten
  #tokens = []
  tokens = tree
  #flatten(tree, tokens.append)
  return ''.join(tokens)


def flatten(tree, callback):
  for item in tree:
    if isinstance(item, list):
      flatten(item, callback)
    else:
      callback(item)


def dump_chunk(out, tag, callback):
  nbytes = 0
  payload_len = len(out)
  len_str = str(payload_len)

  callback(len_str)
  nbytes += len(len_str)

  callback(':')
  callback(out)
  nbytes += payload_len
  callback(tag)

  return nbytes + 2  # : and tag


def dump_node(data, callback):
  nbytes = 0
  if type(data) is long or type(data) is int:
    out = str(data)
    return dump_chunk(out, '#', callback)
  elif type(data) is float:
    out = '%f' % data
    return dump_chunk(out, '^', callback)
  elif type(data) is str:
    return dump_chunk(data, ',', callback)
  elif type(data) is dict:
    return dump_dict(data, callback)
  elif type(data) is list:
    return dump_list(data, callback)
  elif data == None:
    callback('0:~')
    return 3  # 3 bytes
  elif type(data) is bool:
    out = repr(data).lower()
    return dump_chunk(out, '!', callback)
  else:
    assert False, "Can't serialize stuff that's %s." % type(data)

    
def dump_dict(data, callback):
  # length is first
  tokens = []
  subc = tokens.append
  nbytes = 0
  for k,v in data.items():
    nk = dump_node(str(k), subc)
    nv = dump_node(v, subc)
    nbytes += nk
    nbytes += nv

  len_str = str(nbytes)

  callback(len_str)
  nbytes += len(len_str)

  callback(':')
  #callback(tokens)  # needs to be flattened later
  for t in tokens:
    callback(t)

  callback('}')
  # We have to return the number of bytes we wrote
  return nbytes + 2  # : and }


def dump_list(data, callback):
  tokens = []
  subc = tokens.append
  nbytes = 0
  for i in data:
    nbytes += dump_node(i, subc)

  len_str = str(nbytes)

  callback(len_str)
  nbytes += len(len_str)

  callback(':')
  #callback(tokens)  # needs to be flattened later
  for t in tokens:
    callback(t)

  callback(']')
  # We have to return the number of bytes we wrote
  return nbytes + 2  # : and ]


def parse(data):
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
    value, extra = parse(data)
    result.append(value)

    while extra:
        value, extra = parse(extra)
        result.append(value)

    return result

def parse_pair(data):
    key, extra = parse(data)
    assert extra, "Unbalanced dictionary store."
    value, extra = parse(extra)

    return key, value, extra

def parse_dict(data):
    if len(data) == 0: return {}

    key, value, extra = parse_pair(data)
    assert type(key) is str, "Keys can only be strings."

    result = {key: value}

    while extra:
        key, value, extra = parse_pair(extra)
        result[key] = value
  
    return result
