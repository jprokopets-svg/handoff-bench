def md_table_to_html(text: str) -> str:
    """
    Parse a GitHub-flavored markdown table and render it as strict HTML.
    
    Returns a string of the form:
    '<table>\n<thead><tr>...rows...</tr></thead>\n<tbody>...rows...</tbody>\n</table>'
    """
    
    # Split into lines and filter out blank lines
    lines = [line for line in text.split('\n') if line.strip()]
    
    # Must have at least 2 non-blank lines (header + separator)
    if len(lines) < 2:
        raise ValueError("Table must have at least a header row and separator row")
    
    # Parse header row
    header_cells = parse_row(lines[0])
    header_count = len(header_cells)
    
    # Parse separator row
    separator_cells = parse_row(lines[1])
    
    # Validate separator row
    if len(separator_cells) != header_count:
        raise ValueError("Separator row must have same number of cells as header")
    
    # Extract alignment from separator
    alignments = []
    for cell in separator_cells:
        alignment = parse_alignment(cell)
        alignments.append(alignment)
    
    # Build header HTML
    header_html = '<tr>'
    for i, cell in enumerate(header_cells):
        escaped = html_escape(cell)
        align = alignments[i]
        if align:
            header_html += f'<th align="{align}">{escaped}</th>'
        else:
            header_html += f'<th>{escaped}</th>'
    header_html += '</tr>'
    
    # Parse body rows
    body_html = ''
    for line in lines[2:]:
        body_cells = parse_row(line)
        
        # Validate column count
        if len(body_cells) != header_count:
            raise ValueError(f"Body row has {len(body_cells)} cells, expected {header_count}")
        
        body_html += '<tr>'
        for i, cell in enumerate(body_cells):
            escaped = html_escape(cell)
            align = alignments[i]
            if align:
                body_html += f'<td align="{align}">{escaped}</td>'
            else:
                body_html += f'<td>{escaped}</td>'
        body_html += '</tr>'
    
    return f'<table>\n<thead>{header_html}</thead>\n<tbody>{body_html}</tbody>\n</table>'


def parse_row(line: str) -> list:
    """
    Parse a markdown table row into cells.
    
    - Remove optional leading and trailing pipes
    - Split by unescaped pipes
    - Handle escaped pipes (\|) as literal pipes
    - Strip whitespace from each cell
    """
    # Remove leading pipe if present
    if line.startswith('|'):
        line = line[1:]
    
    # Remove trailing pipe if present (but not if escaped)
    if line.endswith('|') and not line.endswith('\\|'):
        line = line[:-1]
    
    # Split by unescaped pipes
    cells = []
    current_cell = ''
    i = 0
    while i < len(line):
        if i < len(line) - 1 and line[i] == '\\' and line[i + 1] == '|':
            # Escaped pipe - add literal pipe
            current_cell += '|'
            i += 2
        elif line[i] == '|':
            # Unescaped pipe - cell separator
            cells.append(current_cell.strip())
            current_cell = ''
            i += 1
        else:
            current_cell += line[i]
            i += 1
    
    # Add the last cell
    cells.append(current_cell.strip())
    
    return cells


def parse_alignment(cell: str) -> str:
    """
    Parse alignment from a separator cell.
    
    Pattern: :?-{3,}:?
    - :--- = left
    - ---: = right
    - :---: = center
    - --- = default (no align attribute)
    
    Raises ValueError if cell doesn't match pattern.
    """
    cell = cell.strip()
    
    # Check if it matches the pattern: :?-{3,}:?
    if not cell:
        raise ValueError("Separator cell cannot be empty")
    
    # Count leading and trailing colons
    has_left_colon = cell.startswith(':')
    has_right_colon = cell.endswith(':')
    
    # Extract the dashes part
    dashes_part = cell
    if has_left_colon:
        dashes_part = dashes_part[1:]
    if has_right_colon:
        dashes_part = dashes_part[:-1]
    
    # Check if remaining part is all dashes and at least 3
    if not dashes_part or not all(c == '-' for c in dashes_part) or len(dashes_part) < 3:
        raise ValueError(f"Invalid separator cell: {cell}")
    
    # Determine alignment
    if has_left_colon and has_right_colon:
        return 'center'
    elif has_right_colon:
        return 'right'
    elif has_left_colon:
        return 'left'
    else:
        return None  # default, no align attribute


def html_escape(text: str) -> str:
    """
    Escape HTML special characters.
    
    - & -> &amp;
    - < -> &lt;
    - > -> &gt;
    """
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text
