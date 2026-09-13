def process_csv(text: str) -> str:
    """Parse RFC-4180 CSV, apply transformations, and re-serialize."""
    if not text:
        raise ValueError("Empty input")
    
    # Parse CSV
    rows = []
    i = 0
    n = len(text)
    
    def parse_field() -> str:
        """Parse a single CSV field."""
        nonlocal i
        if i >= n:
            return ""
        
        if text[i] == '"':
            # Quoted field
            i += 1  # Skip opening quote
            field_chars = []
            while i < n:
                if text[i] == '"':
                    if i + 1 < n and text[i + 1] == '"':
                        # Escaped quote
                        field_chars.append('"')
                        i += 2
                    else:
                        # Closing quote
                        i += 1
                        # Skip to comma or newline
                        while i < n and text[i] != ',' and text[i] != '\n':
                            if text[i] == '"':
                                # Should not have unescaped quote after closing
                                raise ValueError("Unescaped quote in field")
                            i += 1
                        break
                else:
                    field_chars.append(text[i])
                    i += 1
            else:
                # Reached end of input without closing quote
                raise ValueError("Unterminated quoted field")
            return ''.join(field_chars)
        else:
            # Unquoted field
            start = i
            while i < n and text[i] != ',' and text[i] != '\n':
                i += 1
            return text[start:i]
    
    def parse_row() -> list[str]:
        """Parse a single CSV row."""
        nonlocal i
        row = []
        while True:
            field = parse_field()
            row.append(field)
            
            if i >= n or text[i] == '\n':
                if i < n and text[i] == '\n':
                    i += 1  # Skip newline
                break
            elif text[i] == ',':
                i += 1  # Skip comma
            else:
                # Should not happen
                break
        return row
    
    # Parse all rows
    while i < n:
        row = parse_row()
        if row:  # Skip empty rows (e.g., trailing newline)
            rows.append(row)
    
    if not rows:
        raise ValueError("No rows found")
    
    # Header is first row
    header = rows[0]
    header_len = len(header)
    
    # Validate all rows have same column count as header
    for idx, row in enumerate(rows):
        if len(row) != header_len:
            raise ValueError(f"Row {idx} has different column count than header")
    
    # Data rows are everything after header
    data_rows = rows[1:]
    
    # TRANSFORMATIONS
    
    # 1. Filter by 'status' column if it exists
    if 'status' in header:
        status_idx = header.index('status')
        filtered_rows = []
        for row in data_rows:
            if row[status_idx] != 'skip':
                filtered_rows.append(row)
        data_rows = filtered_rows
    
    # 2. Sort by 'sort' column if it exists
    if 'sort' in header and data_rows:
        sort_idx = header.index('sort')
        
        def sort_key(row):
            value = row[sort_idx]
            try:
                # Try to parse as float
                return (0, float(value))  # 0 for numeric group
            except ValueError:
                return (1, value)  # 1 for non-numeric group
        
        # Stable sort
        data_rows.sort(key=sort_key)
    
    # FORMAT: Re-serialize as CSV
    result_rows = []
    
    def needs_quoting(field: str) -> bool:
        """Check if a field needs to be quoted."""
        return ',' in field or '"' in field or '\n' in field
    
    def serialize_field(field: str) -> str:
        """Serialize a single field with proper quoting."""
        if needs_quoting(field):
            # Escape quotes by doubling them
            escaped = field.replace('"', '""')
            return f'"{escaped}"'
        return field
    
    # Add header
    result_rows.append(','.join(serialize_field(f) for f in header))
    
    # Add data rows
    for row in data_rows:
        result_rows.append(','.join(serialize_field(f) for f in row))
    
    # Join with newlines and add trailing newline
    return '\n'.join(result_rows) + '\n'