import re


def md_table_to_html(text: str) -> str:
    """Convert GitHub-flavored markdown table to strict HTML."""
    
    # Parse lines, ignoring blank lines
    lines = [line for line in text.split('\n') if line.strip()]
    
    # Must have at least header + separator
    if len(lines) < 2:
        raise ValueError("Table must have at least a header and separator row")
    
    # Parse header row
    header_cells = parse_row(lines[0])
    
    # Parse and validate separator row
    separator_cells = parse_row(lines[1])
    
    if len(separator_cells) != len(header_cells):
        raise ValueError("Separator row must have same number of cells as header")
    
    # Validate separator cells and extract alignment
    alignments = []
    for cell in separator_cells:
        alignment = validate_separator_cell(cell)
        alignments.append(alignment)
    
    # Parse body rows
    body_rows = []
    for i in range(2, len(lines)):
        row_cells = parse_row(lines[i])
        if len(row_cells) != len(header_cells):
            raise ValueError(f"Body row {i-1} has {len(row_cells)} cells, expected {len(header_cells)}")
        body_rows.append(row_cells)
    
    # Generate HTML
    html_parts = ['<table>']
    
    # Header
    header_html = '<thead><tr>'
    for i, cell in enumerate(header_cells):
        escaped = escape_html(cell)
        align = alignments[i]
        if align:
            header_html += f'<th align="{align}">{escaped}</th>'
        else:
            header_html += f'<th>{escaped}</th>'
    header_html += '</tr></thead>'
    html_parts.append(header_html)
    
    # Body
    body_html = '<tbody>'
    for row in body_rows:
        body_html += '<tr>'
        for i, cell in enumerate(row):
            escaped = escape_html(cell)
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


def parse_row(line: str) -> list:
    """Parse a markdown table row into cells.
    
    Handles:
    - Optional leading and trailing pipes
    - Escaped pipes (\|) within cells
    - Whitespace trimming
    """
    # Remove leading pipe if present
    if line.startswith('|'):
        line = line[1:]
    
    # Remove trailing pipe if present (but not if escaped)
    if line.endswith('|') and not line.endswith('\\|'):
        line = line[:-1]
    
    # Split by unescaped pipes
    cells = []
    current_cell = []
    i = 0
    while i < len(line):
        if i < len(line) - 1 and line[i] == '\\' and line[i+1] == '|':
            # Escaped pipe - add literal pipe to current cell
            current_cell.append('|')
            i += 2
        elif line[i] == '|':
            # Unescaped pipe - cell separator
            cell_text = ''.join(current_cell).strip()
            cells.append(cell_text)
            current_cell = []
            i += 1
        else:
            current_cell.append(line[i])
            i += 1
    
    # Add the last cell
    cell_text = ''.join(current_cell).strip()
    cells.append(cell_text)
    
    return cells


def validate_separator_cell(cell: str) -> str:
    """Validate a separator cell and return alignment.
    
    Pattern: :?-{3,}:?
    - No colons: default (no alignment)
    - Left colon only: left align
    - Right colon only: right align
    - Both colons: center align
    
    Returns: 'left', 'right', 'center', or None (default)
    """
    pattern = r'^:?-{3,}:?$'
    if not re.match(pattern, cell):
        raise ValueError(f"Invalid separator cell: '{cell}'")
    
    has_left = cell.startswith(':')
    has_right = cell.endswith(':')
    
    if has_left and has_right:
        return 'center'
    elif has_left:
        return 'left'
    elif has_right:
        return 'right'
    else:
        return None


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text
