from json_parser import *


def _raises(fn):
    try:
        fn()
        return False
    except ValueError:
        return True

assert parse_json('123') == 123

assert parse_json('-0.5') == -0.5

assert parse_json('123.456') == 123.456

assert parse_json('[-0.5, 1e10, 1.5E-3, 0, -7]') == [-0.5, 1e10, 1.5E-3, 0, -7]

assert parse_json('{"a": 1, "b": [true, null, "x"]}') == {'a': 1, 'b': [True, None, 'x']}

assert parse_json('{"a":{"b":[1,[2,3],{"c":null}]}}') == {'a': {'b': [1, [2, 3], {'c': None}]}}

assert parse_json('"\\u0041\\n\\t\\\""') == 'A\n\t\"'

assert _raises(lambda: parse_json(''))

assert _raises(lambda: parse_json('{"a": 1} extra'))

assert _raises(lambda: parse_json('01'))

assert _raises(lambda: parse_json('[1,]'))

assert _raises(lambda: parse_json('{"a":1,}'))

assert _raises(lambda: parse_json("'x'"))

assert _raises(lambda: parse_json('1.'))

assert _raises(lambda: parse_json('.5'))

assert _raises(lambda: parse_json('+1'))

assert _raises(lambda: parse_json('"unclosed'))