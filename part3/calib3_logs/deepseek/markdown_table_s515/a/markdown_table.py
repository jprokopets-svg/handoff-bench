import re

def md_table_to_html(text: str) -> str:
    # Split into lines and ignore blank lines
    lines = [line.rstrip('\n') for line in text.splitlines()]
    non_blank = [line for line in lines if line.strip() != '']
    
    # Need at least 2 non-blank lines (header and separator)
    if len(non_blank) < 2:
        raise ValueError("Fewer than two non-blank lines")
    
    # Parse header row (first non-blank line)
    header_line = non_blank[0]
    # Parse separator row (second non-blank line)
    separator_line = non_blank[1]
    # Body rows (remaining lines)
    body_lines = non_blank[2:]
    
    # Helper to parse a row into cells
    def parse_row(line: str):
        # Remove optional leading/trailing pipe
        # But trailing pipe removed unless escaped
        # We'll handle escaped pipes during cell splitting
        line = line.strip()
        if line.startswith('|'):
            line = line[1:]
        # Check for trailing pipe that's not escaped
        if line.endswith('|') and not line.endswith('\\|'):
            line = line[:-1]
        elif line.endswith('\\|'):
            # Replace escaped trailing pipe with literal pipe
            line = line[:-2] + '|'
        
        # Split by unescaped '|'
        # We'll manually parse to handle escaped pipes
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
        # Add last cell
        if current:
            cells.append(''.join(current).strip())
        return cells
    
    # Parse header cells
    header_cells = parse_row(header_line)
    if not header_cells:
        raise ValueError("Header row has no cells")
    
    # Parse separator cells
    separator_cells = parse_row(separator_line)
    
    # Check separator cell count matches header
    if len(separator_cells) != len(header_cells):
        raise ValueError("Separator column count mismatch")
    
    # Validate separator pattern for each cell
    alignments = []
    pattern = re.compile(r'^:?-{3,}:?$')
    for cell in separator_cells:
        if not pattern.match(cell):
            raise ValueError("Separator cell does not match pattern")
        # Determine alignment
        if cell.startswith(':') and cell.endswith(':'):
            alignments.append('center')
        elif cell.startswith(':'):
            alignments.append('left')
        elif cell.endswith(':'):
            alignments.append('right')
        else:
            alignments.append(None)  # default, no align attribute
    
    # Parse body rows
    body_rows = []
    for line in body_lines:
        cells = parse_row(line)
        if len(cells) != len(header_cells):
            raise ValueError("Body row column count mismatch")
        body_rows.append(cells)
    
    # HTML escaping
    def escape_html(text: str) -> str:
        return (text.replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;'))
    
    # Build HTML
    parts = ['<table>\n<thead><tr>']
    
    # Header row
    for i, cell in enumerate(header_cells):
        escaped = escape_html(cell)
        if alignments[i] is not None:
            parts.append(f'<th align="{alignments[i]}">{escaped}</th>')
        else:
            parts.append(f'<th>{escaped}</th>')
    
    parts.append('</tr></thead>\n<tbody>')
    
    # Body rows
    for row in body_rows:
        parts.append('<tr>')
        for i, cell in enumerate(row):
            escaped = escape_html(cell)
            if alignments[i] is not None:
                parts.append(f'<td align="{alignments[i]}">{escaped}</td>')
            else:
                parts.append(f'<td>{escaped}</td>')
        parts.append('</tr>')
    
    parts.append('</tbody>\n</table>')
    
    return ''.join(parts)