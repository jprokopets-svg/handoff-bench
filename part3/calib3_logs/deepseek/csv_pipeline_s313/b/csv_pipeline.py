def process_csv(text: str) -> str:
    if not text:
        raise ValueError("empty input")
    
    # Parse CSV
    lines = text.splitlines(keepends=False)
    if not lines:
        raise ValueError("empty input")
    
    # Parse header
    header, pos = parse_row(text, 0)
    if not header:
        raise ValueError("no header")
    
    # Parse all rows
    rows = []
    while pos < len(text):
        # Skip newline
        if text[pos] == '\n':
            pos += 1
            continue
        row, pos = parse_row(text, pos)
        rows.append(row)
    
    # Check column counts
    col_count = len(header)
    for i, row in enumerate(rows):
        if len(row) != col_count:
            raise ValueError(f"row {i+1} has different column count")
    
    # Build dict for each row
    data = []
    for row in rows:
        data.append(dict(zip(header, row)))
    
    # Filter by status column
    if 'status' in header:
        data = [row for row in data if row.get('status') != 'skip']
    
    # Sort by sort column if present
    if 'sort' in header and data:
        def sort_key(row):
            val = row.get('sort', '')
            try:
                # Try to parse as float
                return (0, float(val), '')  # numeric group first
            except ValueError:
                return (1, 0, val)  # non-numeric group second
        
        # Stable sort
        data.sort(key=sort_key)
    
    # Reconstruct rows
    output_rows = [header]
    for row_dict in data:
        output_rows.append([row_dict.get(col, '') for col in header])
    
    # Format CSV
    result = []
    for row in output_rows:
        formatted_fields = []
        for field in row:
            # Check if field needs quoting
            needs_quote = False
            if isinstance(field, str):
                if ',' in field or '"' in field or '\n' in field:
                    needs_quote = True
                # RFC 4180: fields with leading/trailing spaces may be quoted
                # but not required. We'll quote if contains spaces at edges?
                # Simpler: quote if contains comma, quote, or newline.
            if needs_quote:
                # Escape quotes by doubling
                escaped = field.replace('"', '""')
                formatted_fields.append(f'"{escaped}"')
            else:
                formatted_fields.append(field)
        result.append(','.join(formatted_fields))
    
    return '\n'.join(result) + '\n'


def parse_row(text: str, start: int):
    """Parse a CSV row starting at position start.
    Returns (list of fields, next_position).
    """
    fields = []
    pos = start
    length = len(text)
    
    while pos < length:
        # Skip whitespace? RFC says spaces are part of field unless quoted.
        # We'll not skip.
        
        if text[pos] == '"':
            # Quoted field
            pos += 1
            field_chars = []
            while pos < length:
                if text[pos] == '"':
                    # Could be escaped quote or end of field
                    if pos + 1 < length and text[pos + 1] == '"':
                        # Escaped quote
                        field_chars.append('"')
                        pos += 2
                    else:
                        # End of quoted field
                        pos += 1
                        break
                else:
                    field_chars.append(text[pos])
                    pos += 1
            else:
                # Reached end of text without closing quote
                raise ValueError("unterminated quoted field")
            
            fields.append(''.join(field_chars))
            
            # Skip to comma or newline
            while pos < length and text[pos] != ',' and text[pos] != '\n':
                pos += 1
        else:
            # Unquoted field
            field_chars = []
            while pos < length and text[pos] != ',' and text[pos] != '\n':
                field_chars.append(text[pos])
                pos += 1
            fields.append(''.join(field_chars))
        
        # Check for separator
        if pos < length and text[pos] == ',':
            pos += 1
            continue
        elif pos < length and text[pos] == '\n':
            # Row ends at newline
            pos += 1
            break
        elif pos >= length:
            # End of text
            break
    
    return fields, pos