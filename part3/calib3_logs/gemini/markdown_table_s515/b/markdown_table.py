
import re

def md_table_to_html(text: str) -> str:
    """
    Parses a GitHub-flavored markdown table and renders it as strict HTML.
    """
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    if len(lines) < 2:
        raise ValueError("Markdown table must have at least two lines (header and separator).")

    header_line = lines[0]
    separator_line = lines[1]
    body_lines = lines[2:]

    def escape_html(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def parse_row(row_str):
        # Handle optional leading/trailing pipes
        if row_str.startswith('|'):
            row_str = row_str[1:]
        # The logic for removing a trailing pipe is more complex than a simple check,
        # as it should not be removed if it's the only character or part of an escaped sequence.
        # A simple split handles most cases correctly if we clean up the cells later.
        # Let's use a negative lookbehind regex split to handle escaped pipes.
        cells = re.split(r'(?<!\\)\|', row_str)
        # If the original string ended with a non-escaped pipe, the split will produce an empty string at the end.
        if row_str.endswith('|') and not row_str.endswith('\\|'):
             cells = cells[:-1]

        return [cell.strip().replace('\\|', '|') for cell in cells]


    header_cells = parse_row(header_line)
    separator_cells = parse_row(separator_line)

    if len(header_cells) != len(separator_cells):
        raise ValueError("Column count mismatch between header and separator.")

    alignments = []
    for cell in separator_cells:
        match = re.fullmatch(r':?-{3,}:?', cell)
        if not match:
            raise ValueError(f"Invalid separator cell format: '{cell}'")
        
        align = ''
        if cell.startswith(':') and cell.endswith(':'):
            align = 'center'
        elif cell.startswith(':'):
            align = 'left'
        elif cell.endswith(':'):
            align = 'right'
        alignments.append(align)

    # Header HTML
    header_html = '<thead><tr>'
    for i, cell in enumerate(header_cells):
        align_attr = f' align="{alignments[i]}"' if alignments[i] else ''
        header_html += f'<th{align_attr}>{escape_html(cell)}</th>'
    header_html += '</tr></thead>'

    # Body HTML
    body_html = '<tbody>'
    for line in body_lines:
        body_cells = parse_row(line)
        if len(body_cells) != len(header_cells):
            raise ValueError("Column count mismatch in a body row.")
        
        body_html += '<tr>'
        for i, cell in enumerate(body_cells):
            align_attr = f' align="{alignments[i]}"' if alignments[i] else ''
            body_html += f'<td{align_attr}>{escape_html(cell)}</td>'
        body_html += '</tr>'
    body_html += '</tbody>'

    return f'<table>\n{header_html}\n{body_html}\n</table>'
