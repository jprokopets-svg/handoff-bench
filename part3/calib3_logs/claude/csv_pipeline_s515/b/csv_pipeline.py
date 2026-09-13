def process_csv(text: str) -> str:
    """
    Parse, transform, and format a CSV according to RFC-4180 rules.
    
    PARSE: First row is header. Fields separated by commas. Double-quoted fields
    can contain commas, quotes (escaped as ""), and newlines. Raise ValueError on:
    unterminated quoted field, empty input, row column count mismatch.
    
    TRANSFORM: 
    1. Drop rows where 'status' column equals 'skip' exactly
    2. Sort by 'sort' column if it exists: numeric values first (ascending),
       then non-numeric (lexicographic), stable sort
    
    FORMAT: Re-serialize as CSV with proper quoting, one row per line,
    trailing newline at end.
    """
    if not text:
        raise ValueError("Empty input")
    
    # Parse the CSV
    rows = parse_csv(text)
    
    if not rows:
        raise ValueError("Empty input")
    
    header = rows[0]
    data_rows = rows[1:]
    
    # Find column indices
    status_col_idx = None
    sort_col_idx = None
    
    if 'status' in header:
        status_col_idx = header.index('status')
    
    if 'sort' in header:
        sort_col_idx = header.index('sort')
    
    # Filter: drop rows where status == 'skip'
    if status_col_idx is not None:
        data_rows = [row for row in data_rows if row[status_col_idx] != 'skip']
    
    # Sort by 'sort' column if it exists
    if sort_col_idx is not None:
        def sort_key(row):
            value = row[sort_col_idx]
            try:
                numeric_val = float(value)
                return (0, numeric_val, value)  # numeric first, then by value
            except ValueError:
                return (1, value, value)  # non-numeric second, then lexicographic
        
        data_rows.sort(key=sort_key)
    
    # Format back to CSV
    result_rows = [header] + data_rows
    return format_csv(result_rows)


def parse_csv(text: str) -> list:
    """
    Parse RFC-4180 CSV format.
    Returns list of rows, where each row is a list of fields.
    Raises ValueError on invalid input.
    """
    if not text:
        raise ValueError("Empty input")
    
    rows = []
    current_row = []
    current_field = []
    in_quotes = False
    i = 0
    
    while i < len(text):
        char = text[i]
        
        if in_quotes:
            if char == '"':
                # Check if it's an escaped quote or end of field
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
            # Not in quotes
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
                if current_row or current_field:  # Don't add empty rows at end
                    rows.append(current_row)
                current_row = []
                i += 1
                continue
            else:
                current_field.append(char)
                i += 1
                continue
    
    # Handle end of input
    if in_quotes:
        raise ValueError("Unterminated quoted field")
    
    if current_field or current_row:
        current_row.append(''.join(current_field))
        rows.append(current_row)
    
    # Validate: all rows must have same column count as header
    if rows:
        header_cols = len(rows[0])
        for i, row in enumerate(rows[1:], 1):
            if len(row) != header_cols:
                raise ValueError(f"Row {i} has {len(row)} columns, expected {header_cols}")
    
    return rows


def format_csv(rows: list) -> str:
    """
    Format rows back to RFC-4180 CSV format.
    Quote fields that contain comma, quote, or newline.
    Escape quotes by doubling.
    Add trailing newline.
    """
    lines = []
    
    for row in rows:
        formatted_fields = []
        for field in row:
            # Check if field needs quoting
            needs_quoting = ',' in field or '"' in field or '\n' in field
            
            if needs_quoting:
                # Escape quotes by doubling
                escaped = field.replace('"', '""')
                formatted_fields.append(f'"{escaped}"')
            else:
                formatted_fields.append(field)
        
        lines.append(','.join(formatted_fields))
    
    return '\n'.join(lines) + '\n'
