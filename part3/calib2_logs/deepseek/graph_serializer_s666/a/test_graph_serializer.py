from graph_serializer import *


assert decode(encode([1, 2.5, True, None, 'x', {'a': [1]}])) == [1, 2.5, True, None, 'x', {'a': [1]}]

assert decode(encode([])) == []

assert decode(encode({})) == {}

assert decode(encode('')) == ''

assert decode(encode('h\u00e9llo\u2192\u4e16\u754c')) == 'h\u00e9llo\u2192\u4e16\u754c'

inner = [1, 2]; obj = [inner, inner]; out = decode(encode(obj)); assert out[0] is out[1]

lst = [1]; lst.append(lst); out = decode(encode(lst)); assert out[0] == 1 and out[1] is out

d = {}; d['self'] = d; out = decode(encode(d)); assert out['self'] is out

v = [1]; d = {'a': v, 'b': v}; out = decode(encode(d)); assert out['a'] is out['b']