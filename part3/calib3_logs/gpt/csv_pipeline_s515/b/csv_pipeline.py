def process_csv(text: str) -> str:
    if text is None:
        raise ValueError("empty input")
    if text == "":
        raise ValueError("empty input")

    rows = []
    cur_row = []
    cur_field_chars = []
    in_quotes = False
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]
        if in_quotes:
            if ch == '"':
                # possible escaped quote or end-quote
                if i + 1 < n and text[i + 1] == '"':
                    cur_field_chars.append('"')
                    i += 2
                    continue
                else:
                    in_quotes = False
                    i += 1
                    continue
            else:
                # accept any character including newlines
                cur_field_chars.append(ch)
                i += 1
                continue
        else:
            # not in quotes
            if ch == ',':
                cur_row.append(''.join(cur_field_chars))
                cur_field_chars = []
                i += 1
                continue
            elif ch == '\r':
                # treat CR or CRLF as newline
                cur_row.append(''.join(cur_field_chars))
                cur_field_chars = []
                rows.append(cur_row)
                cur_row = []
                i += 1
                if i < n and text[i] == '\n':
                    i += 1
                continue
            elif ch == '\n':
                cur_row.append(''.join(cur_field_chars))
                cur_field_chars = []
                rows.append(cur_row)
                cur_row = []
                i += 1
                continue
            elif ch == '"':
                # start quoted field only if at start of field
                if len(cur_field_chars) == 0:
                    in_quotes = True
                    i += 1
                    continue
                else:
                    # stray quote inside unquoted field; treat as literal
                    cur_field_chars.append(ch)
                    i += 1
                    continue
            else:
                cur_field_chars.append(ch)
                i += 1
                continue

    # end while
    if in_quotes:
        raise ValueError("unterminated quoted field")

    # append last field and row
    # There are two possibilities: either we ended after a newline which already appended a row,
    # or we have data in current field/row to append
    if cur_field_chars or cur_row:
        cur_row.append(''.join(cur_field_chars))
        rows.append(cur_row)
    else:
        # if nothing was added at all, it means input ended with newline and last row already appended
        pass

    if not rows:
        raise ValueError("empty input")

    # header is first row
    header = rows[0]
    header_len = len(header)

    data_rows = rows[1:]

    # validate row lengths
    for r in data_rows:
        if len(r) != header_len:
            raise ValueError("row has wrong number of columns")

    # find status and sort columns
    status_idx = None
    sort_idx = None
    for idx, name in enumerate(header):
        if name == 'status':
            status_idx = idx
        if name == 'sort':
            sort_idx = idx

    # filter out rows where status == 'skip'
    filtered = []
    for r in data_rows:
        if status_idx is not None and r[status_idx] == 'skip':
            continue
        filtered.append(r)

    # sort if needed
    if sort_idx is not None:
        def sort_key(item):
            val = item[sort_idx]
            try:
                num = float(val)
                return (0, num)
            except Exception:
                return (1, val)

        # stable sort
        filtered = sorted(filtered, key=sort_key)

    # serialize: header + filtered rows
    def quote_field(s: str) -> str:
        need = False
        if '"' in s or ',' in s or '\n' in s or '\r' in s:
            need = True
        if need:
            return '"' + s.replace('"', '""') + '"'
        else:
            return s

    out_lines = []
    # header
    out_lines.append(','.join(quote_field(f) for f in header))
    for r in filtered:
        out_lines.append(','.join(quote_field(f) for f in r))

    result = '\n'.join(out_lines) + '\n'
    return result
