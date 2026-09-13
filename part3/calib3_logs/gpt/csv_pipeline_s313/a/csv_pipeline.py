def process_csv(text):
    # Parse CSV according to RFC-4180-like rules
    if text == "":
        raise ValueError("empty input")

    i = 0
    n = len(text)
    rows = []
    cur_field = []  # list of chars
    cur_row = []
    in_quotes = False
    expect_sep_after_quote = False

    while i < n:
        ch = text[i]
        if in_quotes:
            if ch == '"':
                # could be end or escaped
                if i+1 < n and text[i+1] == '"':
                    cur_field.append('"')
                    i += 2
                else:
                    in_quotes = False
                    expect_sep_after_quote = True
                    i += 1
            else:
                cur_field.append(ch)
                i += 1
        else:
            if expect_sep_after_quote:
                # After a closing quote, only comma or newline or EOF allowed
                if ch == ',':
                    cur_row.append(''.join(cur_field))
                    cur_field = []
                    expect_sep_after_quote = False
                    i += 1
                elif ch == '\n':
                    cur_row.append(''.join(cur_field))
                    rows.append(cur_row)
                    cur_row = []
                    cur_field = []
                    expect_sep_after_quote = False
                    i += 1
                else:
                    # any other character invalid
                    raise ValueError('invalid character after closing quote')
            else:
                if ch == ',':
                    cur_row.append(''.join(cur_field))
                    cur_field = []
                    i += 1
                elif ch == '\n':
                    cur_row.append(''.join(cur_field))
                    rows.append(cur_row)
                    cur_row = []
                    cur_field = []
                    i += 1
                elif ch == '"':
                    # start of quoted field only allowed at field start
                    if len(cur_field) != 0:
                        # quote in middle of unquoted field
                        raise ValueError('unexpected quote')
                    in_quotes = True
                    i += 1
                else:
                    cur_field.append(ch)
                    i += 1

    # End of input
    if in_quotes:
        raise ValueError('unterminated quoted field')

    if expect_sep_after_quote:
        # closed quote at EOF -> finish field
        cur_row.append(''.join(cur_field))
        cur_field = []
        expect_sep_after_quote = False
    elif cur_field or cur_row:
        # Append remaining field/row if any characters were read
        # If both empty and no rows, that means empty input which we handled earlier
        cur_row.append(''.join(cur_field))
    # If cur_row not empty, append
    if cur_row:
        rows.append(cur_row)

    if not rows:
        # no rows parsed
        raise ValueError('empty input')

    # All rows parsed. Validate columns count
    header = rows[0]
    ncols = len(header)
    data_rows = rows[1:]
    for r in data_rows:
        if len(r) != ncols:
            raise ValueError('row has wrong number of columns')

    # Transform: drop rows with status == 'skip'
    status_idx = None
    sort_idx = None
    for idx, name in enumerate(header):
        if name == 'status':
            status_idx = idx
        if name == 'sort':
            sort_idx = idx

    if status_idx is not None:
        filtered = [r for r in data_rows if r[status_idx] != 'skip']
    else:
        filtered = list(data_rows)

    # Sorting: stable sort if sort column exists
    if sort_idx is not None:
        def sort_key(row):
            val = row[sort_idx]
            try:
                num = float(val)
                return (0, num, '')
            except Exception:
                return (1, 0.0, val)
        # Use stable sorted
        filtered = sorted(filtered, key=sort_key)

    # Reconstruct rows: header + filtered
    out_rows = [header] + filtered

    # Format back to CSV
    def quote_field(s):
        # Quote only if contains comma, double-quote, or newline
        if any(c in s for c in [',', '"', '\n']):
            # escape quotes by doubling
            esc = s.replace('"', '""')
            return '"' + esc + '"'
        else:
            return s

    lines = []
    for r in out_rows:
        line = ','.join(quote_field(f) for f in r)
        lines.append(line)
    return '\n'.join(lines) + '\n'
