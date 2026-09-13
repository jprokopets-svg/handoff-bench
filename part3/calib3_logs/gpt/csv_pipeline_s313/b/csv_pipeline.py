from typing import List


def process_csv(text: str) -> str:
    if text is None or text == "":
        raise ValueError("empty input")

    i = 0
    n = len(text)
    rows: List[List[str]] = []
    current_row: List[str] = []
    current_field_chars: List[str] = []
    in_quotes = False

    while i < n:
        c = text[i]
        if in_quotes:
            if c == '"':
                # either escaped quote or closing quote
                if i + 1 < n and text[i + 1] == '"':
                    current_field_chars.append('"')
                    i += 2
                else:
                    # closing quote
                    i += 1
                    in_quotes = False
                    # after closing quote, next char must be comma, newline, or EOF
                    if i < n and text[i] not in (',', '\n'):
                        raise ValueError("invalid character after closing quote")
                continue
            else:
                current_field_chars.append(c)
                i += 1
                continue
        else:
            if c == '"':
                # start quoted field
                # if field already has characters, it's an error in strict mode
                if current_field_chars:
                    # treat it as normal char (be permissive), but spec is strict; raise
                    raise ValueError("unexpected quote in unquoted field")
                in_quotes = True
                i += 1
                continue
            elif c == ',':
                current_row.append(''.join(current_field_chars))
                current_field_chars = []
                i += 1
                continue
            elif c == '\n':
                current_row.append(''.join(current_field_chars))
                current_field_chars = []
                rows.append(current_row)
                current_row = []
                i += 1
                continue
            else:
                current_field_chars.append(c)
                i += 1
                continue

    # end while
    if in_quotes:
        raise ValueError("unterminated quoted field")

    # if there is remaining data (either fields collected or partial row), append final field/row
    if current_field_chars or current_row:
        current_row.append(''.join(current_field_chars))
        rows.append(current_row)

    if not rows:
        raise ValueError("empty input")

    # header
    header = rows[0]
    ncols = len(header)
    for r in rows[1:]:
        if len(r) != ncols:
            raise ValueError("row has different column count")

    # transform: filter status == 'skip'
    status_idx = None
    sort_idx = None
    for idx, name in enumerate(header):
        if name == 'status':
            status_idx = idx
        if name == 'sort':
            sort_idx = idx

    data_rows = rows[1:]
    if status_idx is not None:
        filtered = [r for r in data_rows if r[status_idx] != 'skip']
    else:
        filtered = list(data_rows)

    # sorting
    if sort_idx is not None:
        def sort_key(row):
            val = row[sort_idx]
            try:
                num = float(val)
                return (0, num)
            except Exception:
                return (1, val)

        # stable sort
        filtered = sorted(filtered, key=sort_key)

    # serialization
    def serialize_field(f: str) -> str:
        need_quote = (',' in f) or ('"' in f) or ('\n' in f)
        if '"' in f:
            f_escaped = f.replace('"', '""')
        else:
            f_escaped = f
        if need_quote:
            return '"' + f_escaped + '"'
        else:
            return f_escaped

    out_lines: List[str] = []
    out_lines.append(','.join(serialize_field(x) for x in header))
    for r in filtered:
        out_lines.append(','.join(serialize_field(x) for x in r))

    return '\n'.join(out_lines) + '\n'
