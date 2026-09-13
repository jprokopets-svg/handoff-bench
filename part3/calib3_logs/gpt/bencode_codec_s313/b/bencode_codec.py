def bencode(obj: object) -> bytes:
    """Encode a Python object to bencode bytes.

    Supported types: int (but not bool), bytes, str (UTF-8), list, dict (keys must be str).
    """
    def enc(o):
        # Reject booleans explicitly (they are instances of int)
        if isinstance(o, bool):
            raise ValueError("bool is not supported")
        if isinstance(o, int):
            # integer encoding
            return b'i' + str(o).encode('ascii') + b'e'
        if isinstance(o, bytes):
            return str(len(o)).encode('ascii') + b':' + o
        if isinstance(o, str):
            b = o.encode('utf-8')
            return str(len(b)).encode('ascii') + b':' + b
        if isinstance(o, list):
            parts = [b'l']
            for item in o:
                parts.append(enc(item))
            parts.append(b'e')
            return b''.join(parts)
        if isinstance(o, dict):
            # keys must be str
            # convert keys to UTF-8 bytes and sort by raw bytes
            items = []
            for k, v in o.items():
                if not isinstance(k, str):
                    raise ValueError('dict keys must be str')
                kb = k.encode('utf-8')
                items.append((kb, v))
            # sort by raw bytes of key
            items.sort(key=lambda kv: kv[0])
            parts = [b'd']
            for kb, v in items:
                parts.append(str(len(kb)).encode('ascii') + b':' + kb)
                parts.append(enc(v))
            parts.append(b'e')
            return b''.join(parts)
        raise ValueError(f'Unsupported type: {type(o)!r}')

    return enc(obj)


def bdecode(data: bytes) -> object:
    """Decode bencoded bytes to Python objects.

    Returns int, bytes, list, dict (dict keys are bytes).
    """
    if isinstance(data, bytearray):
        data = bytes(data)
    if not isinstance(data, (bytes,)):
        raise ValueError('data must be bytes')
    n = len(data)
    if n == 0:
        raise ValueError('empty input')

    def parse_int(i):
        # data[i] == ord('i')
        j = data.find(b'e', i+1)
        if j == -1:
            raise ValueError('unterminated integer')
        num_bytes = data[i+1:j]
        if len(num_bytes) == 0:
            raise ValueError('empty integer')
        # negative?
        if num_bytes == b'-':
            raise ValueError('bare - is not valid integer')
        if num_bytes[0:1] == b'-':
            if num_bytes == b'-0':
                raise ValueError("-0 is not allowed")
            # ok otherwise
        else:
            # positive: prohibit leading zeros unless exactly '0'
            if len(num_bytes) > 1 and num_bytes[0:1] == b'0':
                raise ValueError('leading zero in integer')
        try:
            val = int(num_bytes.decode('ascii'))
        except Exception:
            raise ValueError('invalid integer')
        return val, j+1

    def parse_bytes(i):
        # parse length prefix until ':'
        j = i
        if j >= n or not (48 <= data[j] <= 57):  # not digit
            raise ValueError('invalid string length')
        # gather digits
        while j < n and 48 <= data[j] <= 57:
            j += 1
        if j >= n or data[j] != ord(':'):
            raise ValueError('missing colon in string')
        len_bytes = data[i:j]
        if len(len_bytes) > 1 and len_bytes[0:1] == b'0':
            raise ValueError('leading zero in string length')
        try:
            length = int(len_bytes.decode('ascii'))
        except Exception:
            raise ValueError('invalid string length')
        start = j+1
        end = start + length
        if end > n:
            raise ValueError('string length exceeds data')
        return data[start:end], end

    def parse_value(i):
        if i >= n:
            raise ValueError('unexpected end')
        c = data[i:i+1]
        if c == b'i':
            return parse_int(i)
        if c == b'l':
            lst = []
            idx = i+1
            while True:
                if idx >= n:
                    raise ValueError('unterminated list')
                if data[idx:idx+1] == b'e':
                    return lst, idx+1
                val, idx = parse_value(idx)
                lst.append(val)
        if c == b'd':
            d = {}
            idx = i+1
            while True:
                if idx >= n:
                    raise ValueError('unterminated dict')
                if data[idx:idx+1] == b'e':
                    return d, idx+1
                key, idx = parse_value(idx)
                # keys must be bytes
                if not isinstance(key, (bytes, bytearray)):
                    raise ValueError('dict keys must be bytes')
                # ensure key is bytes (convert bytearray)
                if isinstance(key, bytearray):
                    key = bytes(key)
                val, idx = parse_value(idx)
                d[key] = val
            # unreachable
        # otherwise it's a byte string (length-prefixed)
        return parse_bytes(i)

    val, idx = parse_value(0)
    if idx != n:
        raise ValueError('trailing data')
    return val
