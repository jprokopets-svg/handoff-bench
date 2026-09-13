import re

def md_table_to_html(text: str) -> str:
    # Split into lines and ignore blank lines
    lines = [line.rstrip('\n') for line in text.splitlines()]
    non_blank = [line for line in lines if line.strip() != '']
    
    # Need at least two non-blank lines (header and separator)
    if len(non_blank) < 2:
        raise ValueError("Fewer than two non-blank lines")
    
    header_line = non_blank[0]
    separator_line = non_blank[1]
    body_lines = non_blank[2:]
    
    # Parse a row: handle optional leading/trailing pipes, escaped pipes
    def parse_row(line):
        # Remove optional leading pipe
        if line.startswith('|'):
            line = line[1:]
        # Remove optional trailing pipe (unless escaped)
        if line.endswith('|') and not line.endswith('\\|'):
            line = line[:-1]
        # Split by unescaped pipes
        # We need to split by '|' but not '\|'
        # Replace escaped pipes with a temporary marker
        line = line.replace('\\|', '\x00')
        cells = [cell.strip() for cell in line.split('|')]
        # Restore escaped pipes
        cells = [cell.replace('\x00', '|') for cell in cells]
        return cells
    
    header_cells = parse_row(header_line)
    separator_cells = parse_row(separator_line)
    
    # Check separator column count matches header
    if len(separator_cells) != len(header_cells):
        raise ValueError("Separator column count mismatch")
    
    # Validate separator pattern: each cell must match ':?-{3,}:?'
    sep_pattern = re.compile(r'^:?-{3,}:?$')
    alignments = []
    for cell in separator_cells:
        if not sep_pattern.match(cell):
            raise ValueError(f"Invalid separator cell: {cell}")
        # Determine alignment
        left_colon = cell.startswith(':')
        right_colon = cell.endswith(':')
        if left_colon and right_colon:
            align = 'center'
        elif left_colon:
            align = 'left'
        elif right_colon:
            align = 'right'
        else:
            align = None  # default, no align attribute
        alignments.append(align)
    
    # Parse body rows
    body_rows = []
    for line in body_lines:
        cells = parse_row(line)
        if len(cells) != len(header_cells):
            raise ValueError("Body row column count mismatch")
        body_rows.append(cells)
    
    # HTML escaping
    def escape(text):
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text
    
    # Build HTML
    parts = ['<table>']
    
    # Header
    header_html = ['<thead><tr>']
    for i, cell in enumerate(header_cells):
        align = alignments[i]
        if align:
            header_html.append(f'<th align="{align}">{escape(cell)}</th>')
        else:
            header_html.append(f'<th>{escape(cell)}</th>')
    header_html.append('</tr></thead>')
    parts.append(''.join(header_html))
    
    # Body
    if body_rows:
        body_html = ['<tbody>']
        for row in body_rows:
            body_html.append('<tr>')
            for i, cell in enumerate(row):
                align = alignments[i]
                if align:
                    body_html.append(f'<td align="{align}">{escape(cell)}</td>')
                else:
                    body_html.append(f'<td>{escape(cell)}</td>')
            body_html.append('</tr>')
        body_html.append('</tbody>')
        parts.append(''.join(body_html))
    else:
        parts.append('<tbody></tbody>')
    
    parts.append('</table>')
    return '\n'.join(parts)