import re


def md_table_to_html(text):
    """
    Parse a GitHub-flavored markdown table and render it as strict HTML.
    """
    # Split into lines and filter out blank lines
    lines = [line for line in text.split('\n') if line.strip()]
    
    # Need at least 2 non-blank lines (header + separator)
    if len(lines) < 2:
        raise ValueError("Need at least header and separator rows")
    
    # Parse header row
    header_cells = parse_row(lines[0])
    header_count = len(header_cells)
    
    # Parse separator row
    separator_cells = parse_row(lines[1])
    
    # Validate separator
    if len(separator_cells) != header_count:
        raise ValueError("Separator column count doesn't match header")
    
    alignments = []
    for cell in separator_cells:
        alignment = validate_separator_cell(cell)
        alignments.append(alignment)
    
    # Parse body rows
    body_rows = []
    for i in range(2, len(lines)):
        row_cells = parse_row(lines[i])
        if len(row_cells) != header_count:
            raise ValueError(f"Body row column count doesn't match header")
        body_rows.append(row_cells)
    
    # Build HTML
    html = '<table>\n'
    
    # Header
    html += '<thead><tr>'
    for i, cell in enumerate(header_cells):
        escaped = escape_html(cell)
        align_attr = get_align_attr(alignments[i])
        html += f'<th{align_attr}>{escaped}</th>'
    html += '</tr></thead>\n'
    
    # Body
    html += '<tbody>'
    for row in body_rows:
        html += '<tr>'
        for i, cell in enumerate(row):
            escaped = escape_html(cell)
            align_attr = get_align_attr(alignments[i])
            html += f'<td{align_attr}>{escaped}</td>'
        html += '</tr>'
    html += '</tbody>\n'
    
    html += '</table>'
    
    return html


def parse_row(line):
    """
    Parse a row line into cells.
    - Remove optional leading and trailing pipes
    - Split by unescaped pipes
    - Handle escaped pipes (\|)
    - Strip whitespace from each cell
    """
    # Remove leading pipe if present
    if line.startswith('|'):
        line = line[1:]
    
    # Remove trailing pipe if present and not escaped
    if line.endswith('|') and not line.endswith('\\|'):
        line = line[:-1]
    
    # Split by unescaped pipes
    cells = split_by_unescaped_pipe(line)
    
    # Strip whitespace and unescape pipes
    cells = [cell.strip().replace('\\|', '|') for cell in cells]
    
    return cells


def split_by_unescaped_pipe(text):
    """
    Split text by unescaped pipe characters.
    """
    cells = []
    current = []
    i = 0
    while i < len(text):
        if i < len(text) - 1 and text[i] == '\\' and text[i + 1] == '|':
            # Escaped pipe
            current.append('\\|')
            i += 2
        elif text[i] == '|':
            # Unescaped pipe - cell separator
            cells.append(''.join(current))
            current = []
            i += 1
        else:
            current.append(text[i])
            i += 1
    
    # Add the last cell
    cells.append(''.join(current))
    
    return cells


def validate_separator_cell(cell):
    """
    Validate a separator cell matches :?-{3,}:?
    Returns the alignment: 'left', 'right', 'center', or None (default)
    """
    pattern = r'^:?-{3,}:?$'
    if not re.match(pattern, cell):
        raise ValueError(f"Invalid separator cell: {cell}")
    
    has_left_colon = cell.startswith(':')
    has_right_colon = cell.endswith(':')
    
    if has_left_colon and has_right_colon:
        return 'center'
    elif has_right_colon:
        return 'right'
    elif has_left_colon:
        return 'left'
    else:
        return None


def get_align_attr(alignment):
    """
    Get the align attribute string for a given alignment.
    """
    if alignment is None:
        return ''
    else:
        return f' align="{alignment}"'


def escape_html(text):
    """
    Escape HTML special characters.
    """
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text
