import re


def md_table_to_html(text):
    """Parse a GitHub-flavored markdown table and render it as strict HTML."""
    
    # Split into lines and filter out blank lines
    lines = [line for line in text.split('\n') if line.strip()]
    
    # Need at least 2 non-blank lines (header + separator)
    if len(lines) < 2:
        raise ValueError("Need at least header and separator rows")
    
    # Parse header row
    header_cells = _parse_row(lines[0])
    header_count = len(header_cells)
    
    # Parse separator row
    separator_cells = _parse_row(lines[1])
    
    # Validate separator
    if len(separator_cells) != header_count:
        raise ValueError("Separator column count doesn't match header")
    
    alignments = []
    for cell in separator_cells:
        alignment = _parse_alignment(cell)
        alignments.append(alignment)
    
    # Parse body rows
    body_rows = []
    for i in range(2, len(lines)):
        row_cells = _parse_row(lines[i])
        if len(row_cells) != header_count:
            raise ValueError(f"Row {i} column count doesn't match header")
        body_rows.append(row_cells)
    
    # Build HTML
    html_parts = ['<table>']
    
    # Build header
    header_html = '<thead><tr>'
    for i, cell in enumerate(header_cells):
        escaped = _escape_html(cell)
        align = alignments[i]
        if align:
            header_html += f'<th align="{align}">{escaped}</th>'
        else:
            header_html += f'<th>{escaped}</th>'
    header_html += '</tr></thead>'
    html_parts.append(header_html)
    
    # Build body
    body_html = '<tbody>'
    for row in body_rows:
        body_html += '<tr>'
        for i, cell in enumerate(row):
            escaped = _escape_html(cell)
            align = alignments[i]
            if align:
                body_html += f'<td align="{align}">{escaped}</td>'
            else:
                body_html += f'<td>{escaped}</td>'
        body_html += '</tr>'
    body_html += '</tbody>'
    html_parts.append(body_html)
    
    html_parts.append('</table>')
    
    return '\n'.join(html_parts)


def _parse_row(line):
    """Parse a row, handling escaped pipes and optional leading/trailing pipes."""
    # Remove optional leading pipe
    if line.startswith('|'):
        line = line[1:]
    
    # Remove optional trailing pipe (unless escaped)
    if line.endswith('|') and not line.endswith('\\|'):
        line = line[:-1]
    
    # Split by unescaped pipes
    cells = []
    current_cell = []
    i = 0
    while i < len(line):
        if i < len(line) - 1 and line[i] == '\\' and line[i + 1] == '|':
            # Escaped pipe - add literal pipe
            current_cell.append('|')
            i += 2
        elif line[i] == '|':
            # Unescaped pipe - cell separator
            cells.append(''.join(current_cell).strip())
            current_cell = []
            i += 1
        else:
            current_cell.append(line[i])
            i += 1
    
    # Add the last cell
    cells.append(''.join(current_cell).strip())
    
    return cells


def _parse_alignment(cell):
    """Parse alignment from separator cell. Returns 'left', 'right', 'center', or None."""
    cell = cell.strip()
    
    # Pattern: :?-{3,}:?
    if not re.match(r'^:?-{3,}:?$', cell):
        raise ValueError(f"Invalid separator cell: {cell}")
    
    has_left_colon = cell.startswith(':')
    has_right_colon = cell.endswith(':')
    
    if has_left_colon and has_right_colon:
        return 'center'
    elif has_left_colon:
        return 'left'
    elif has_right_colon:
        return 'right'
    else:
        return None


def _escape_html(text):
    """Escape HTML special characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text
