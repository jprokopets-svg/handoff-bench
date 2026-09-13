import re


def md_table_to_html(text: str) -> str:
    # Split into non-blank lines
    lines = [ln for ln in text.splitlines() if ln.strip() != ""]
    if len(lines) < 2:
        raise ValueError("Insufficient non-blank lines for a markdown table")

    header_line = lines[0]
    sep_line = lines[1]
    body_lines = lines[2:]

    def remove_outer_unescaped_pipes(line: str) -> str:
        # remove leading '|' if present and unescaped (at start it's always unescaped)
        if line.startswith('|'):
            line = line[1:]
        # remove trailing '|' if present and not escaped (odd number of backslashes before it means escaped)
        if line.endswith('|'):
            # count consecutive backslashes before last char
            i = len(line) - 2
            backslashes = 0
            while i >= 0 and line[i] == '\\':
                backslashes += 1
                i -= 1
            if backslashes % 2 == 0:
                line = line[:-1]
        return line

    def split_row(line: str) -> list:
        # Handle optional outer pipes
        line = remove_outer_unescaped_pipes(line)
        cells = []
        buf = []
        i = 0
        L = len(line)
        while i < L:
            ch = line[i]
            if ch == '\\' and i + 1 < L and line[i + 1] == '|':
                # escaped pipe -> literal pipe in cell
                buf.append('|')
                i += 2
            elif ch == '|':
                # separator
                cell = ''.join(buf).strip()
                cells.append(cell)
                buf = []
                i += 1
            else:
                buf.append(ch)
                i += 1
        # append last cell
        cell = ''.join(buf).strip()
        cells.append(cell)
        return cells

    header_cells = split_row(header_line)
    sep_cells = split_row(sep_line)

    if len(sep_cells) != len(header_cells):
        raise ValueError("Separator row must have the same number of cells as the header")

    # parse separator cells for alignment
    aligns = []
    sep_re = re.compile(r'^:?-{3,}:?$')
    for sc in sep_cells:
        if not sep_re.fullmatch(sc):
            raise ValueError(f"Invalid separator cell: {sc}")
        left = sc.startswith(':')
        right = sc.endswith(':')
        if left and right:
            aligns.append('center')
        elif left:
            aligns.append('left')
        elif right:
            aligns.append('right')
        else:
            aligns.append(None)

    # helper to escape html
    def escape_html(s: str) -> str:
        s = s.replace('&', '&amp;')
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
        return s

    # build header
    ths = []
    for idx, cell in enumerate(header_cells):
        content = escape_html(cell)
        align = aligns[idx]
        if align:
            ths.append(f"<th align=\"{align}\">{content}</th>")
        else:
            ths.append(f"<th>{content}</th>")
    thead = '<thead><tr>' + ''.join(ths) + '</tr></thead>'

    # build body
    tds_rows = []
    for line in body_lines:
        cells = split_row(line)
        if len(cells) != len(header_cells):
            raise ValueError("Row has a different number of cells than header")
        tds = []
        for idx, cell in enumerate(cells):
            content = escape_html(cell)
            align = aligns[idx]
            if align:
                tds.append(f"<td align=\"{align}\">{content}</td>")
            else:
                tds.append(f"<td>{content}</td>")
        tds_rows.append('<tr>' + ''.join(tds) + '</tr>')

    tbody = '<tbody>' + ''.join(tds_rows) + '</tbody>'

    return '<table>\n' + thead + '\n' + tbody + '\n</table>'
