from bencode_codec import *


def _raises(fn):
    try:
        fn()
        return False
    except ValueError:
        return True

assert bencode(42) == b'i42e'

assert bencode(-7) == b'i-7e'

assert bencode(0) == b'i0e'

assert bencode(b'') == b'0:'

assert bencode(b'spam') == b'4:spam'

assert bencode('hello') == b'5:hello'

assert bencode([1, 2]) == b'li1ei2ee'

assert bencode([]) == b'le'

assert bencode({}) == b'de'

assert bencode({'b': 2, 'a': 1}) == b'd1:ai1e1:bi2ee'

assert bencode([1, b'a', [b'x']]) == b'li1e1:al1:xee'

assert bdecode(b'i42e') == 42

assert bdecode(b'i-7e') == -7

assert bdecode(b'4:spam') == b'spam'

assert bdecode(b'0:') == b''

assert bdecode(b'le') == []

assert bdecode(b'd1:ai1e1:bi2ee') == {b'a': 1, b'b': 2}

assert bdecode(bencode([1, 3, b'x', {'k': 'v'}])) == [1, 3, b'x', {b'k': b'v'}]

assert bdecode(bencode({'x': [1, b'y', {'z': 3}]})) == {b'x': [1, b'y', {b'z': 3}]}

assert bdecode(bencode('héllo wörld')) == b'h\xc3\xa9llo w\xc3\xb6rld'

assert bdecode(bencode(42)) == 42 and bdecode(bencode(b'bytes')) == b'bytes'

assert _raises(lambda: bdecode(b''))

assert _raises(lambda: bdecode(b'i1'))

assert _raises(lambda: bdecode(b'i01e'))

assert _raises(lambda: bdecode(b'i-0e'))

assert _raises(lambda: bdecode(b'i-'))

assert _raises(lambda: bdecode(b'3:ab'))

assert _raises(lambda: bdecode(b'03:abc'))

assert _raises(lambda: bdecode(b'4:ab'))

assert _raises(lambda: bdecode(b'l1:ai1e'))

assert _raises(lambda: bdecode(b'd1:a'))

assert _raises(lambda: bdecode(b'di1e1:e'))

assert _raises(lambda: bdecode(b'x'))

assert _raises(lambda: bdecode(b'i1ei2e'))

assert _raises(lambda: bencode(1.5))

assert _raises(lambda: bencode(True))

assert _raises(lambda: bencode(None))

assert _raises(lambda: bencode({1: 'x'}))