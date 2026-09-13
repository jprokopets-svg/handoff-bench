def process_csv(text: str) -> str:
    """Parse CSV, transform, and re-serialize."""
    if not text:
        raise ValueError("empty input")
    
    # Parse CSV
    rows = []
    i = 0
    n = len(text)
    
    def parse_field():
        nonlocal i
        if i >= n:
            return None
        if text[i] == '"':
            # Quoted field
            i += 1  # skip opening quote
            field_parts = []
            while i < n:
                if text[i] == '"':
                    if i + 1 < n and text[i + 1] == '"':
                        # Escaped quote
                        field_parts.append('"')
                        i += 2
                    else:
                        # Closing quote
                        i += 1
                        # Check for comma or newline or end
                        if i >= n or text[i] == '\n' or text[i] == ',':
                            break
                        else:
                            # Malformed: quote not followed by comma/newline/end
                            raise ValueError("unterminated quoted field")
                else:
                    field_parts.append(text[i])
                    i += 1
            else:
                # Reached end of text without closing quote
                raise ValueError("unterminated quoted field")
            return ''.join(field_parts)
        else:
            # Unquoted field
            start = i
            while i < n and text[i] != ',' and text[i] != '\n':
                i += 1
            return text[start:i]
    
    # Parse all rows
    while i < n:
        row = []
        while True:
            field = parse_field()
            if field is None:
                break
            row.append(field)
            if i >= n:
                break
            if text[i] == ',':
                i += 1
                continue
            elif text[i] == '\n':
                i += 1
                break
        if row:  # skip empty lines (though CSV shouldn't have them)
            rows.append(row)
    
    if not rows:
        raise ValueError("no rows")
    
    # Check column counts
    header = rows[0]
    col_count = len(header)
    for idx, row in enumerate(rows[1:], start=1):
        if len(row) != col_count:
            raise ValueError(f"row {idx} has different column count")
    
    # Transform
    data_rows = rows[1:] if len(rows) > 1 else []
    
    # Find column indices
    header_lower = [col.lower() for col in header]
    status_idx = None
    sort_idx = None
    for idx, col in enumerate(header_lower):
        if col == 'status':
            status_idx = idx
        if col == 'sort':
            sort_idx = idx
    
    # Drop rows where status == 'skip'
    if status_idx is not None and data_rows:
        filtered_rows = []
        for row in data_rows:
            if row[status_idx] != 'skip':
                filtered_rows.append(row)
        data_rows = filtered_rows
    
    # Sort rows if sort column exists
    if sort_idx is not None and data_rows:
        def sort_key(row):
            val = row[sort_idx]
            try:
                # Try to parse as float
                return (0, float(val), '')  # numeric group first
            except ValueError:
                return (1, '', val)  # non-numeric group second
        
        # Stable sort
        data_rows.sort(key=sort_key)
    
    # Format CSV
    def needs_quoting(field):
        if not field:
            return False
        if ',' in field or '"' in field or '\n' in field:
            return True
        # Also quote if field starts/ends with space? Not required by spec
        return False
    
    def escape_field(field):
        if '"' in field:
            field = field.replace('"', '""')
        return field
    
    output_rows = []
    # Header
    header_fields = []
    for field in header:
        field = escape_field(field)
        if needs_quoting(field):
            header_fields.append(f'"{field}"')
        else:
            header_fields.append(field)
    output_rows.append(','.join(header_fields))
    
    # Data rows
    for row in data_rows:
        row_fields = []
        for field in row:
            field = escape_field(field)
            if needs_quoting(field):
                row_fields.append(f'"{field}"')
            else:
                row_fields.append(field)
        output_rows.append(','.join(row_fields))
    
    result = '\n'.join(output_rows) + '\n'
    return result