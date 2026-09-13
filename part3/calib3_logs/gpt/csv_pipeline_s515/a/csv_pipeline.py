def process_csv(text: str) -> str:
    if text is None or len(text) == 0:
        raise ValueError('empty input')

    i = 0
    n = len(text)
    rows = []

    while i <= n:
        # If at EOF with nothing to parse, break
        if i == n:
            break
        fields = []
        while True:
            if i < n and text[i] == '"':
                # quoted field
                i += 1
                buf_chars = []
                while True:
                    if i >= n:
                        raise ValueError('unterminated quoted field')
                    ch = text[i]
                    if ch == '"':
                        # escaped quote or end
                        if i + 1 < n and text[i + 1] == '"':
                            buf_chars.append('"')
                            i += 2
                            continue
                        else:
                            i += 1
                            break
                    else:
                        buf_chars.append(ch)
                        i += 1
                field = ''.join(buf_chars)
                # after closing quote, must be comma, newline, or EOF
                if i < n and text[i] not in {',', '\n'}:
                    # could be stray \r before \n; allow \r then \n
                    # if it's a carriage return followed by newline, accept it as part of newline
                    if text[i] == '\r' and (i + 1 < n and text[i + 1] == '\n'):
                        # treat as newline
                        i += 2
                        fields.append(field)
                        break
                    raise ValueError('unexpected character after closing quote')
                # consume separator if present
                if i < n and text[i] == ',':
                    i += 1
                    fields.append(field)
                    # continue to next field in same row
                    continue
                else:
                    # newline or EOF
                    fields.append(field)
                    if i < n and text[i] == '\n':
                        i += 1
                    break

            else:
                # unquoted field
                start = i
                while i < n and text[i] not in {',', '\n'}:
                    i += 1
                field = text[start:i]
                # consume separator or newline
                if i < n and text[i] == ',':
                    i += 1
                    fields.append(field)
                    continue
                else:
                    fields.append(field)
                    if i < n and text[i] == '\n':
                        i += 1
                    break
        rows.append(fields)
        # continue to parse next row

    if not rows:
        raise ValueError('empty input')

    # header is first row
    header = rows[0]
    num_cols = len(header)
    # validate row lengths
    for r in rows:
        if len(r) != num_cols:
            raise ValueError('row has different column count')

    data_rows = rows[1:]

    # TRANSFORM: drop rows where status == 'skip'
    if 'status' in header:
        idx_status = header.index('status')
        data_rows = [r for r in data_rows if r[idx_status] != 'skip']

    # SORT: if 'sort' in header
    if 'sort' in header:
        idx_sort = header.index('sort')

        def sort_key(row):
            val = row[idx_sort]
            try:
                num = float(val)
                return (0, num, None)
            except Exception:
                return (1, None, val)

        # stable sort
        data_rows = sorted(data_rows, key=sort_key)

    # FORMAT: serialize
    def quote_field(s: str) -> str:
        needs = False
        for ch in s:
            if ch in {',', '"', '\n'}:
                needs = True
                break
        if needs:
            # escape quotes
            escaped = s.replace('"', '""')
            return '"' + escaped + '"'
        else:
            return s

    out_lines = []
    # header
    out_lines.append(','.join(quote_field(f) for f in header))
    for r in data_rows:
        out_lines.append(','.join(quote_field(f) for f in r))

    return '\n'.join(out_lines) + '\n'
