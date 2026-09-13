import re


def md_table_to_html(text: str) -> str:
    if text is None:
        raise ValueError
    # Split into lines and ignore blank lines
    lines = [line.rstrip('\n') for line in text.splitlines()]
    nonblank = [ln for ln in lines if ln.strip() != '']
    if len(nonblank) < 2:
        raise ValueError('need at least header and separator')

    header_line = nonblank[0]
    sep_line = nonblank[1]
    body_lines = nonblank[2:]

    def count_preceding_bs(s, pos):
        # count consecutive backslashes immediately before position pos (pos is index of char)
        i = pos - 1
        cnt = 0
        while i >= 0 and s[i] == '\\':
            cnt += 1
            i -= 1
        return cnt

    def remove_unescaped_leading_trailing_pipe(s: str) -> str:
        # remove leading unescaped '|' if present
        if s.startswith('|'):
            # at start, cannot be escaped
            s = s[1:]
        # remove trailing unescaped '|'
        if s.endswith('|'):
            # check if escaped by odd number of backslashes
            if count_preceding_bs(s, len(s)-1) % 2 == 0:
                s = s[:-1]
        return s

    def split_cells(s: str):
        # Do not modify original escaping except \| -> | (remove backslash)
        s2 = remove_unescaped_leading_trailing_pipe(s)
        cells = []
        cur = []
        i = 0
        L = len(s2)
        while i < L:
            ch = s2[i]
            if ch == '\\':
                # if next is '|', treat as escaped pipe
                if i+1 < L and s2[i+1] == '|':
                    cur.append('|')
                    i += 2
                    continue
                else:
                    # keep backslash as literal
                    cur.append('\\')
                    i += 1
                    continue
            if ch == '|':
                # unescaped separator
                cells.append(''.join(cur))
                cur = []
                i += 1
                continue
            else:
                cur.append(ch)
                i += 1
        # append last cell
        cells.append(''.join(cur))
        # Strip whitespace around each cell
        cells = [c.strip() for c in cells]
        return cells

    header_cells = split_cells(header_line)
    sep_cells = split_cells(sep_line)

    # separator must have same number of cells as header
    if len(sep_cells) != len(header_cells):
        raise ValueError('separator column count mismatch')

    # validate separator pattern and compute alignments
    alignments = []  # 'left','right','center', or None
    sep_re = re.compile(r'^:?-{3,}:?$')
    for sc in sep_cells:
        if not sep_re.match(sc):
            raise ValueError('invalid separator cell: %r' % sc)
        left = sc.startswith(':')
        right = sc.endswith(':')
        if left and right:
            alignments.append('center')
        elif left:
            alignments.append('left')
        elif right:
            alignments.append('right')
        else:
            alignments.append(None)

    # parse body rows
    body_rows = []
    for bl in body_lines:
        cells = split_cells(bl)
        if len(cells) != len(header_cells):
            raise ValueError('body row column count mismatch')
        body_rows.append(cells)

    # escape HTML in cell contents: replace & < >
    def escape_html(s: str) -> str:
        s = s.replace('&', '&amp;')
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
        return s

    # build HTML
    def cell_html(tag: str, content: str, align: str):
        esc = escape_html(content)
        if align is None:
            return f'<{tag}>{esc}</{tag}>'
        else:
            return f'<{tag} align="{align}">{esc}</{tag}>'

    # header
    header_cells_html = ''.join(cell_html('th', header_cells[i], alignments[i]) for i in range(len(header_cells)))
    thead = f'<thead><tr>{header_cells_html}</tr></thead>'
    # body
    tbody_rows = []
    for row in body_rows:
        cells_html = ''.join(cell_html('td', row[i], alignments[i]) for i in range(len(row)))
        tbody_rows.append(f'<tr>{cells_html}</tr>')
    tbody = '<tbody>' + ''.join(tbody_rows) + '</tbody>'

    html = '<table>\n' + thead + '\n' + tbody + '\n</table>'
    return html
