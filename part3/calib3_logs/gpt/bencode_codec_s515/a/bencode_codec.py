def bencode(obj):
    """Encode Python object to bencode bytes."""
    # Helper
    def encode(o):
        # Reject bool explicitly (bool is subclass of int)
        if isinstance(o, bool):
            raise ValueError('bool not allowed')
        if isinstance(o, int):
            # ints allowed
            return b'i' + str(o).encode('ascii') + b'e'
        if isinstance(o, bytes):
            return str(len(o)).encode('ascii') + b':' + o
        if isinstance(o, str):
            b = o.encode('utf-8')
            return str(len(b)).encode('ascii') + b':' + b
        if isinstance(o, list):
            parts = [b'l']
            for item in o:
                parts.append(encode(item))
            parts.append(b'e')
            return b''.join(parts)
        if isinstance(o, dict):
            # keys must be str
            items = []
            for k, v in o.items():
                if not isinstance(k, str):
                    raise ValueError('dict keys must be str')
                kb = k.encode('utf-8')
                items.append((kb, v))
            # sort by raw encoded key bytes
            items.sort(key=lambda kv: kv[0])
            parts = [b'd']
            for kb, v in items:
                parts.append(str(len(kb)).encode('ascii') + b':' + kb)
                parts.append(encode(v))
            parts.append(b'e')
            return b''.join(parts)
        # reject other types
        raise ValueError('unsupported type: %r' % (type(o),))

    return encode(obj)


def bdecode(data):
    """Decode bencode bytes to Python object. Returns int, bytes, list, or dict (with bytes keys).
    Raises ValueError on malformed input.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise ValueError('data must be bytes')
    data = bytes(data)
    n = len(data)
    if n == 0:
        raise ValueError('empty input')

    def parse_at(i):
        if i >= n:
            raise ValueError('unexpected end')
        c = data[i:i+1]
        # integer
        if c == b'i':
            # find 'e'
            epos = data.find(b'e', i+1)
            if epos == -1:
                raise ValueError('unterminated integer')
            numb = data[i+1:epos]
            if len(numb) == 0:
                raise ValueError('empty integer')
            # check sign and digits
            if numb[0:1] == b'-':
                if len(numb) == 1:
                    raise ValueError('bare -')
                # -0 is invalid
                if numb[1:2] == b'0':
                    raise ValueError('negative zero')
                if not all(48 <= b <= 57 for b in numb[1:]):
                    raise ValueError('invalid integer digits')
            else:
                # leading zeros not allowed except single '0'
                if numb[0:1] == b'0' and len(numb) > 1:
                    raise ValueError('leading zero')
                if not all(48 <= b <= 57 for b in numb):
                    raise ValueError('invalid integer digits')
            try:
                val = int(numb.decode('ascii'))
            except Exception:
                raise ValueError('invalid integer')
            return val, epos + 1
        # byte string: starts with digit
        if b'0' <= c <= b'9':
            # find ':'
            colon = data.find(b':', i)
            if colon == -1:
                raise ValueError('no colon')
            lenbytes = data[i:colon]
            if len(lenbytes) == 0:
                raise ValueError('empty length')
            # leading zero rule
            if lenbytes[0:1] == b'0' and len(lenbytes) > 1:
                raise ValueError('leading zero in length')
            if not all(48 <= b <= 57 for b in lenbytes):
                raise ValueError('non-digit in length')
            length = int(lenbytes.decode('ascii'))
            start = colon + 1
            end = start + length
            if end > n:
                raise ValueError('string length too long')
            return data[start:end], end
        if c == b'l':
            i2 = i + 1
            res = []
            while True:
                if i2 >= n:
                    raise ValueError('unterminated list')
                if data[i2:i2+1] == b'e':
                    return res, i2 + 1
                val, i2 = parse_at(i2)
                res.append(val)
        if c == b'd':
            i2 = i + 1
            res = {}
            while True:
                if i2 >= n:
                    raise ValueError('unterminated dict')
                if data[i2:i2+1] == b'e':
                    return res, i2 + 1
                key, i2 = parse_at(i2)
                # keys must be bytes
                if not isinstance(key, (bytes, bytearray)):
                    raise ValueError('dict keys must be bytes')
                # ensure key is bytes
                key = bytes(key)
                val, i2 = parse_at(i2)
                res[key] = val
            # unreachable
        # unexpected
        raise ValueError('unexpected byte: %r' % (c,))

    val, pos = parse_at(0)
    if pos != n:
        raise ValueError('trailing data')
    return val
