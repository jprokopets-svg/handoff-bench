import re

def md_table_to_html(text: str) -> str:
    # Split text into lines and ignore blank lines
    lines = [line.rstrip('\n') for line in text.splitlines()]
    non_blank_lines = [line for line in lines if line.strip() != '']
    
    # Check we have at least 2 non-blank lines (header and separator)
    if len(non_blank_lines) < 2:
        raise ValueError("Fewer than two non-blank lines")
    
    # Parse rows
    header_line = non_blank_lines[0]
    separator_line = non_blank_lines[1]
    body_lines = non_blank_lines[2:]
    
    # Helper function to parse a row into cells
    def parse_row(line: str):
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
                current.append('|')
                i += 2
            elif line[i] == '|':
                cells.append(''.join(current).strip())
                current = []
                i += 1
            else:
                current.append(line[i])
                i += 1
        cells.append(''.join(current).strip())
        
        return cells
    
    # Parse header, separator, and body rows
    header_cells = parse_row(header_line)
    separator_cells = parse_row(separator_line)
    body_rows = [parse_row(line) for line in body_lines]
    
    # Validate separator has same number of cells as header
    if len(separator_cells) != len(header_cells):
        raise ValueError("Column-count mismatch in separator")
    
    # Validate each separator cell matches the pattern
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
            alignments.append(None)
    
    # Validate body rows have correct number of cells
    for row in body_rows:
        if len(row) != len(header_cells):
            raise ValueError("Column-count mismatch in body row")
    
    # Helper function to escape HTML special characters
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
        escaped = escape_html(cell)
        if alignments[i]:
            header_html.append(f'<th align="{alignments[i]}">{escaped}</th>')
        else:
            header_html.append(f'<th>{escaped}</th>')
    header_html.append('</tr></thead>')
    html_parts.append(''.join(header_html))
    
    # Build body
    if body_rows:
        body_html = ['<tbody>']
        for row in body_rows:
            body_html.append('<tr>')
            for i, cell in enumerate(row):
                escaped = escape_html(cell)
                if alignments[i]:
                    body_html.append(f'<td align="{alignments[i]}">{escaped}</td>')
                else:
                    body_html.append(f'<td>{escaped}</td>')
            body_html.append('</tr>')
        body_html.append('</tbody>')
        html_parts.append(''.join(body_html))
    else:
        html_parts.append('<tbody></tbody>')
    
    html_parts.append('</table>')
    
    return '\n'.join(html_parts)