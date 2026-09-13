def bencode(obj: object) -> bytes:
    """Encode a Python object to bencode bytes.
    Supported types: int, bytes, str, list, dict (with str keys).
    """
    def enc(o):
        # Reject bool explicitly
        if isinstance(o, bool):
            raise ValueError("bool is not supported")
        if isinstance(o, int):
            return b"i" + str(o).encode("ascii") + b"e"
        if isinstance(o, bytes):
            return str(len(o)).encode("ascii") + b":" + o
        if isinstance(o, str):
            bts = o.encode("utf-8")
            return str(len(bts)).encode("ascii") + b":" + bts
        if isinstance(o, list):
            parts = [b"l"]
            for item in o:
                parts.append(enc(item))
            parts.append(b"e")
            return b"".join(parts)
        if isinstance(o, dict):
            # keys must be str
            items = []
            for k, v in o.items():
                if not isinstance(k, str):
                    raise ValueError("dict keys must be str")
                kb = k.encode("utf-8")
                items.append((kb, v))
            # sort by raw key bytes
            items.sort(key=lambda kv: kv[0])
            parts = [b"d"]
            for kb, v in items:
                parts.append(str(len(kb)).encode("ascii") + b":" + kb)
                parts.append(enc(v))
            parts.append(b"e")
            return b"".join(parts)
        raise ValueError(f"Unsupported type: {type(o)!r}")

    return enc(obj)


def bdecode(data: bytes) -> object:
    """Decode bencode bytes to Python object.
    Returns int, bytes, list, dict (with bytes keys).
    """
    if isinstance(data, bytearray):
        data = bytes(data)
    if not isinstance(data, (bytes,)):
        raise ValueError("data must be bytes-like")
    if len(data) == 0:
        raise ValueError("empty input")

    n = len(data)

    def parse_int(start):
        # start points at 'i'
        if data[start:start+1] != b'i':
            raise ValueError("not an int")
        end = data.find(b'e', start+1)
        if end == -1:
            raise ValueError("unterminated integer")
        num_bytes = data[start+1:end]
        if len(num_bytes) == 0:
            raise ValueError("empty integer")
        # reject leading + sign; only optional leading -
        if num_bytes[0:1] == b'-':
            if len(num_bytes) == 1:
                raise ValueError("bare - in integer")
            if num_bytes[1:2] == b'0':
                raise ValueError("-0 is not allowed")
            if not num_bytes[1:].isdigit():
                raise ValueError("invalid integer")
        else:
            if num_bytes[0:1] == b'0' and len(num_bytes) > 1:
                raise ValueError("leading zero in integer")
            if not num_bytes.isdigit():
                raise ValueError("invalid integer")
        try:
            val = int(num_bytes.decode('ascii'))
        except Exception:
            raise ValueError("invalid integer")
        return val, end+1

    def parse_str(start):
        # start points at first digit of length
        colon = data.find(b':', start)
        if colon == -1:
            raise ValueError("missing ':' in string")
        len_bytes = data[start:colon]
        if len(len_bytes) == 0:
            raise ValueError("empty length")
        if not len_bytes.isdigit():
            raise ValueError("non-digit in length")
        if len(len_bytes) > 1 and len_bytes[0:1] == b'0':
            raise ValueError("leading zero in length")
        length = int(len_bytes.decode('ascii'))
        start_content = colon + 1
        end_content = start_content + length
        if end_content > n:
            raise ValueError("string length longer than available data")
        return data[start_content:end_content], end_content

    def parse_any(start):
        if start >= n:
            raise ValueError("unexpected end")
        c = data[start:start+1]
        if c == b'i':
            return parse_int(start)
        if c.isdigit():
            return parse_str(start)
        if c == b'l':
            idx = start + 1
            lst = []
            while True:
                if idx >= n:
                    raise ValueError("unterminated list")
                if data[idx:idx+1] == b'e':
                    return lst, idx+1
                val, idx = parse_any(idx)
                lst.append(val)
        if c == b'd':
            idx = start + 1
            d = {}
            while True:
                if idx >= n:
                    raise ValueError("unterminated dict")
                if data[idx:idx+1] == b'e':
                    return d, idx+1
                # keys must be byte strings
                key, idx2 = parse_str(idx)
                if not isinstance(key, (bytes,)):
                    raise ValueError("dict key must be bytes")
                val, idx3 = parse_any(idx2)
                d[key] = val
                idx = idx3
        raise ValueError("invalid start byte")

    val, endpos = parse_any(0)
    if endpos != n:
        raise ValueError("trailing data")
    return val
