import re


def md_table_to_html(text: str) -> str:
    # Split into non-blank lines
    lines = [ln for ln in text.splitlines() if ln.strip() != ""]
    if len(lines) < 2:
        raise ValueError("Not enough lines")

    def split_row(line: str):
        # Remove optional leading '|' if present and not escaped (start can't be escaped)
        if line.startswith('|'):
            line = line[1:]
        # Remove optional trailing '|' if present and not escaped
        if line.endswith('|'):
            # determine if escaped by counting preceding backslashes
            i = len(line) - 1
            # count backslashes immediately before the final '|' in original line
            # but since we've possibly removed first char, operate on current line
            # count backslashes before this last char (which was '|' before slicing)
            # Actually here last char of current line is '|' char; check preceding backslashes
            bs_count = 0
            j = i - 1
            while j >= 0 and line[j] == '\\':
                bs_count += 1
                j -= 1
            if bs_count % 2 == 0:
                # not escaped
                line = line[:-1]
        # Now split on unescaped '|'
        cells = []
        cur = []
        i = 0
        n = len(line)
        while i < n:
            ch = line[i]
            if ch == '\\' and i + 1 < n and line[i+1] == '|':
                # escaped pipe, include literal '|'
                cur.append('|')
                i += 2
                continue
            if ch == '|':
                cells.append(''.join(cur))
                cur = []
                i += 1
                continue
            # otherwise just add char
            cur.append(ch)
            i += 1
        # append last cell
        cells.append(''.join(cur))
        # strip surrounding whitespace from each cell
        return [c.strip() for c in cells]

    header_line = lines[0]
    sep_line = lines[1]
    body_lines = lines[2:]

    header_cells = split_row(header_line)
    sep_cells = split_row(sep_line)

    if len(sep_cells) != len(header_cells):
        raise ValueError("Separator column count mismatch")

    alignments = []
    for cell in sep_cells:
        # cell pattern: optional leading ':', at least 3 dashes, optional trailing ':'
        if not re.fullmatch(r':?-{3,}:?', cell):
            raise ValueError("Invalid separator cell")
        left = cell.startswith(':')
        right = cell.endswith(':')
        if left and right:
            alignments.append('center')
        elif left:
            alignments.append('left')
        elif right:
            alignments.append('right')
        else:
            alignments.append(None)

    # parse body rows
    body_cells = []
    for bl in body_lines:
        cells = split_row(bl)
        if len(cells) != len(header_cells):
            raise ValueError("Body row column count mismatch")
        body_cells.append(cells)

    def escape_html(s: str) -> str:
        # replace & first
        s = s.replace('&', '&amp;')
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
        return s

    # Build HTML
    def make_cell(tag: str, content: str, align: str):
        esc = escape_html(content)
        if align:
            return f"<{tag} align=\"{align}\">{esc}</{tag}>"
        else:
            return f"<{tag}>{esc}</{tag}>"

    # header
    ths = ''.join(make_cell('th', header_cells[i], alignments[i]) for i in range(len(header_cells)))
    thead = f"<thead><tr>{ths}</tr></thead>"
    # body
    trs = []
    for row in body_cells:
        tds = ''.join(make_cell('td', row[i], alignments[i]) for i in range(len(row)))
        trs.append(f"<tr>{tds}</tr>")
    tbody = f"<tbody>{''.join(trs)}</tbody>"

    return '<table>\n' + thead + '\n' + tbody + '\n</table>'
