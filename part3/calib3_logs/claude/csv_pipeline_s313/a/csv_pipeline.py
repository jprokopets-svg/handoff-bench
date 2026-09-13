def process_csv(text):
    """
    Parse, transform, and format a CSV according to RFC-4180 with specific rules.
    
    PARSE: First row is header, fields separated by commas, quoted fields allowed,
           "" escapes quotes, fields can span newlines.
    TRANSFORM: Drop rows where 'status' column equals 'skip', sort by 'sort' column
               (numeric values first, then lexicographic).
    FORMAT: Re-serialize as CSV with trailing newline.
    """
    
    # Check for empty input
    if not text:
        raise ValueError("Empty input")
    
    # Parse CSV
    rows = _parse_csv(text)
    
    if not rows:
        raise ValueError("Empty input")
    
    header = rows[0]
    data_rows = rows[1:]
    
    # Validate all rows have same column count as header
    for row in data_rows:
        if len(row) != len(header):
            raise ValueError(f"Row has {len(row)} columns, expected {len(header)}")
    
    # Find column indices
    status_idx = None
    sort_idx = None
    
    for i, col in enumerate(header):
        if col == 'status':
            status_idx = i
        elif col == 'sort':
            sort_idx = i
    
    # Transform: drop rows where status == 'skip'
    if status_idx is not None:
        data_rows = [row for row in data_rows if row[status_idx] != 'skip']
    
    # Transform: sort by 'sort' column if it exists
    if sort_idx is not None:
        data_rows = _sort_rows(data_rows, sort_idx)
    
    # Format: re-serialize
    result = _format_csv([header] + data_rows)
    
    return result


def _parse_csv(text):
    """Parse CSV text into a list of rows (each row is a list of fields)."""
    rows = []
    current_row = []
    current_field = []
    in_quotes = False
    i = 0
    
    while i < len(text):
        char = text[i]
        
        if in_quotes:
            if char == '"':
                # Check if it's an escaped quote
                if i + 1 < len(text) and text[i + 1] == '"':
                    current_field.append('"')
                    i += 2
                    continue
                else:
                    # End of quoted field
                    in_quotes = False
                    i += 1
                    continue
            else:
                current_field.append(char)
                i += 1
                continue
        else:
            if char == '"':
                in_quotes = True
                i += 1
                continue
            elif char == ',':
                current_row.append(''.join(current_field))
                current_field = []
                i += 1
                continue
            elif char == '\n':
                current_row.append(''.join(current_field))
                current_field = []
                if current_row or current_field:  # Only add non-empty rows
                    rows.append(current_row)
                current_row = []
                i += 1
                continue
            else:
                current_field.append(char)
                i += 1
                continue
    
    # Handle unterminated quoted field
    if in_quotes:
        raise ValueError("Unterminated quoted field")
    
    # Add final field and row if exists
    if current_field or current_row or i > 0:
        current_row.append(''.join(current_field))
        if current_row:
            rows.append(current_row)
    
    return rows


def _sort_rows(rows, sort_idx):
    """Sort rows by the column at sort_idx, with numeric values first."""
    def sort_key(row):
        value = row[sort_idx]
        try:
            num_val = float(value)
            return (0, num_val)  # Numeric values sort first
        except ValueError:
            return (1, value)  # Non-numeric values sort second, lexicographically
    
    return sorted(rows, key=sort_key)


def _format_csv(rows):
    """Format rows back into CSV text."""
    lines = []
    
    for row in rows:
        formatted_fields = []
        for field in row:
            formatted_fields.append(_quote_field(field))
        lines.append(','.join(formatted_fields))
    
    return '\n'.join(lines) + '\n'


def _quote_field(field):
    """Quote a field if necessary (contains comma, quote, or newline)."""
    if ',' in field or '"' in field or '\n' in field:
        # Escape quotes by doubling
        escaped = field.replace('"', '""')
        return f'"{escaped}"'
    return field
