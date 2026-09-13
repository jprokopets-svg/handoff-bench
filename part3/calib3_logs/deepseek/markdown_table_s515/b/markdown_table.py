def md_table_to_html(text: str) -> str:
    # Split text into lines and ignore blank lines
    lines = [line.rstrip('\n') for line in text.splitlines()]
    non_blank_lines = [line for line in lines if line.strip() != '']
    
    # Check if we have at least two non-blank lines
    if len(non_blank_lines) < 2:
        raise ValueError("Fewer than two non-blank lines")
    
    # First non-blank line is header row
    header_line = non_blank_lines[0]
    # Second non-blank line is separator row
    separator_line = non_blank_lines[1]
    # Remaining lines are body rows
    body_lines = non_blank_lines[2:]
    
    # Helper function to parse a row into cells
    def parse_row(line: str) -> list[str]:
        # Remove optional leading and trailing '|'
        line = line.strip()
        if line.startswith('|'):
            line = line[1:]
        if line.endswith('|') and not line.endswith('\\|'):
            line = line[:-1]
        
        # Split by unescaped '|' characters
        cells = []
        current = []
        i = 0
        while i < len(line):
            if line[i] == '\\' and i + 1 < len(line) and line[i + 1] == '|':
                # Escaped pipe
                current.append('|')
                i += 2
            elif line[i] == '|':
                # Cell separator
                cells.append(''.join(current).strip())
                current = []
                i += 1
            else:
                current.append(line[i])
                i += 1
        
        # Add the last cell
        cells.append(''.join(current).strip())
        return cells
    
    # Parse header row
    header_cells = parse_row(header_line)
    num_columns = len(header_cells)
    
    # Parse separator row
    separator_cells = parse_row(separator_line)
    
    # Check separator column count matches header
    if len(separator_cells) != num_columns:
        raise ValueError("Separator column count mismatch")
    
    # Determine alignment for each column
    alignments = []
    for cell in separator_cells:
        cell = cell.strip()
        # Check pattern: :?-{3,}:?
        if not cell or len(cell) < 3:
            raise ValueError("Invalid separator cell")
        
        # Check if it's all dashes with optional colons
        dashes_only = True
        for i, ch in enumerate(cell):
            if ch == ':':
                if i != 0 and i != len(cell) - 1:
                    raise ValueError("Invalid separator cell")
            elif ch != '-':
                dashes_only = False
        
        if not dashes_only:
            raise ValueError("Invalid separator cell")
        
        # Count dashes (must be at least 3)
        dash_count = sum(1 for ch in cell if ch == '-')
        if dash_count < 3:
            raise ValueError("Invalid separator cell")
        
        # Determine alignment
        left_colon = cell.startswith(':')
        right_colon = cell.endswith(':')
        
        if left_colon and right_colon:
            alignments.append('center')
        elif left_colon:
            alignments.append('left')
        elif right_colon:
            alignments.append('right')
        else:
            alignments.append(None)  # No alignment attribute
    
    # Parse body rows
    body_rows = []
    for line in body_lines:
        cells = parse_row(line)
        if len(cells) != num_columns:
            raise ValueError("Body row column count mismatch")
        body_rows.append(cells)
    
    # Helper function to escape HTML entities
    def escape_html(text: str) -> str:
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text
    
    # Build HTML
    html_parts = ['<table>']
    
    # Build header
    header_html = ['<thead><tr>']
    for i, cell in enumerate(header_cells):
        escaped_cell = escape_html(cell)
        if alignments[i] is not None:
            header_html.append(f'<th align="{alignments[i]}">{escaped_cell}</th>')
        else:
            header_html.append(f'<th>{escaped_cell}</th>')
    header_html.append('</tr></thead>')
    html_parts.append(''.join(header_html))
    
    # Build body
    if body_rows:
        body_html = ['<tbody>']
        for row in body_rows:
            body_html.append('<tr>')
            for i, cell in enumerate(row):
                escaped_cell = escape_html(cell)
                if alignments[i] is not None:
                    body_html.append(f'<td align="{alignments[i]}">{escaped_cell}</td>')
                else:
                    body_html.append(f'<td>{escaped_cell}</td>')
            body_html.append('</tr>')
        body_html.append('</tbody>')
        html_parts.append(''.join(body_html))
    else:
        html_parts.append('<tbody></tbody>')
    
    html_parts.append('</table>')
    
    return '\n'.join(html_parts)