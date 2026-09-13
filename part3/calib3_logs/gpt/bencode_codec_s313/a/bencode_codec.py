from typing import Tuple, Any


def bencode(obj) -> bytes:
    """Encode obj to bencode bytes."""
    # Reject disallowed types
    if isinstance(obj, bool) or obj is None or isinstance(obj, float) or isinstance(obj, tuple):
        raise ValueError("unsupported type")

    if isinstance(obj, int) and not isinstance(obj, bool):
        return _encode_int(obj)
    if isinstance(obj, bytes):
        return _encode_bytes(obj)
    if isinstance(obj, str):
        return _encode_bytes(obj.encode('utf-8'))
    if isinstance(obj, list):
        return _encode_list(obj)
    if isinstance(obj, dict):
        return _encode_dict(obj)

    raise ValueError("unsupported type")


def _encode_int(i: int) -> bytes:
    # ints must be encoded as i<decimal>e
    return b'i' + str(i).encode('ascii') + b'e'


def _encode_bytes(b: bytes) -> bytes:
    return str(len(b)).encode('ascii') + b':' + b


def _encode_list(lst: list) -> bytes:
    parts = [b'l']
    for item in lst:
        parts.append(bencode(item))
    parts.append(b'e')
    return b''.join(parts)


def _encode_dict(d: dict) -> bytes:
    # keys REQUIRED to be str
    items = []  # list of (key_bytes, value)
    for k, v in d.items():
        if not isinstance(k, str):
            raise ValueError("dict keys must be str")
        kb = k.encode('utf-8')
        items.append((kb, v))
    # sort by raw key bytes
    items.sort(key=lambda kv: kv[0])
    parts = [b'd']
    for kb, v in items:
        parts.append(_encode_bytes(kb))
        parts.append(bencode(v))
    parts.append(b'e')
    return b''.join(parts)


def bdecode(data: bytes) -> Any:
    if not isinstance(data, (bytes, bytearray)):
        raise ValueError("data must be bytes")
    if len(data) == 0:
        raise ValueError("empty input")

    val, idx = _parse_at(data, 0)
    if idx != len(data):
        raise ValueError("trailing data")
    return val


def _parse_at(data: bytes, idx: int) -> Tuple[Any, int]:
    if idx >= len(data):
        raise ValueError("unterminated or empty")
    c = data[idx:idx+1]
    if c == b'i':
        # integer
        end = data.find(b'e', idx+1)
        if end == -1:
            raise ValueError("unterminated integer")
        num_bytes = data[idx+1:end]
        if len(num_bytes) == 0:
            raise ValueError("bare integer")
        # check format
        if num_bytes == b'-':
            raise ValueError("bare minus")
        if num_bytes.startswith(b'-'):
            # negative: must not be -0
            if num_bytes == b'-0':
                raise ValueError("-0 not allowed")
            rest = num_bytes[1:]
            if not rest.isdigit():
                raise ValueError("invalid integer")
        else:
            if not num_bytes.isdigit():
                raise ValueError("invalid integer")
            if len(num_bytes) > 1 and num_bytes.startswith(b'0'):
                raise ValueError("leading zero in integer")
        try:
            val = int(num_bytes.decode('ascii'))
        except Exception:
            raise ValueError("invalid integer")
        return val, end+1
    elif b'0' <= c <= b'9':
        # byte string
        # read digits until ':'
        colon = data.find(b':', idx)
        if colon == -1:
            raise ValueError("missing colon in string")
        len_bytes = data[idx:colon]
        if len(len_bytes) == 0:
            raise ValueError("missing length")
        if not len_bytes.isdigit():
            raise ValueError("invalid length")
        if len(len_bytes) > 1 and len_bytes.startswith(b'0'):
            raise ValueError("leading zero in length")
        length = int(len_bytes.decode('ascii'))
        start = colon+1
        end = start + length
        if end > len(data):
            raise ValueError("string length exceeds data")
        return data[start:end], end
    elif c == b'l':
        lst = []
        idx += 1
        while True:
            if idx >= len(data):
                raise ValueError("unterminated list")
            if data[idx:idx+1] == b'e':
                return lst, idx+1
            val, idx = _parse_at(data, idx)
            lst.append(val)
    elif c == b'd':
        d = {}
        idx += 1
        while True:
            if idx >= len(data):
                raise ValueError("unterminated dict")
            if data[idx:idx+1] == b'e':
                return d, idx+1
            key, idx = _parse_at(data, idx)
            if not isinstance(key, (bytes, bytearray)):
                raise ValueError("dict key must be bytes")
            # ensure key is bytes (not bytearray)
            if isinstance(key, bytearray):
                key = bytes(key)
            val, idx = _parse_at(data, idx)
            d[key] = val
    else:
        raise ValueError("unexpected byte")
