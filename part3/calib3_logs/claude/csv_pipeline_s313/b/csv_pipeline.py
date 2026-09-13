def process_csv(text: str) -> str:
    """
    Parse, transform, and format a CSV string.
    
    PARSE: RFC-4180 style CSV with quoted fields and escaped quotes.
    TRANSFORM: Filter rows where status=='skip', sort by 'sort' column if present.
    FORMAT: Re-serialize with proper quoting and trailing newline.
    """
    if not text:
        raise ValueError("Empty input")
    
    # Parse CSV
    rows = _parse_csv(text)
    
    if not rows:
        raise ValueError("Empty input")
    
    header = rows[0]
    data_rows = rows[1:]
    
    # Find column indices
    status_col = None
    sort_col = None
    try:
        status_col = header.index('status')
    except ValueError:
        pass
    try:
        sort_col = header.index('sort')
    except ValueError:
        pass
    
    # Filter: drop rows where status == 'skip'
    if status_col is not None:
        data_rows = [row for row in data_rows if row[status_col] != 'skip']
    
    # Sort: by sort column if present
    if sort_col is not None:
        data_rows = _sort_rows(data_rows, sort_col)
    
    # Format and return
    return _format_csv([header] + data_rows)


def _parse_csv(text: str) -> list:
    """
    Parse RFC-4180 CSV text into a list of rows (each row is a list of fields).
    Raises ValueError on unterminated quotes or column count mismatch.
    """
    rows = []
    i = 0
    n = len(text)
    
    while i < n:
        row = []
        # Parse one row
        while i < n:
            # Parse one field
            if i < n and text[i] == '"':
                # Quoted field
                i += 1
                field = []
                while i < n:
                    if text[i] == '"':
                        i += 1
                        if i < n and text[i] == '"':
                            # Escaped quote
                            field.append('"')
                            i += 1
                        else:
                            # End of quoted field
                            break
                    else:
                        field.append(text[i])
                        i += 1
                else:
                    # Reached end of text without closing quote
                    raise ValueError("Unterminated quoted field")
                
                row.append(''.join(field))
            else:
                # Unquoted field
                field = []
                while i < n and text[i] not in ',\n':
                    field.append(text[i])
                    i += 1
                row.append(''.join(field))
            
            # Check what comes next
            if i < n and text[i] == ',':
                i += 1
                # Continue to next field
            elif i < n and text[i] == '\n':
                i += 1
                # End of row
                break
            elif i >= n:
                # End of text
                break
            else:
                # Should not happen
                break
        
        if row or i < n:  # Add row if it has content or we haven't reached end
            rows.append(row)
    
    # Validate column counts
    if rows:
        header_cols = len(rows[0])
        for row in rows[1:]:
            if len(row) != header_cols:
                raise ValueError(f"Row has {len(row)} columns, expected {header_cols}")
    
    return rows


def _sort_rows(rows: list, sort_col: int) -> list:
    """
    Sort rows by the column at sort_col index.
    Numeric values sort before non-numeric values.
    Within each group, sort ascending (numeric ascending, then lexicographic).
    """
    def sort_key(row):
        value = row[sort_col]
        try:
            num = float(value)
            return (0, num)  # Numeric: group 0, then by numeric value
        except ValueError:
            return (1, value)  # Non-numeric: group 1, then by string value
    
    return sorted(rows, key=sort_key)


def _format_csv(rows: list) -> str:
    """
    Format rows back into CSV text with proper quoting and trailing newline.
    """
    lines = []
    for row in rows:
        formatted_fields = [_quote_field(field) for field in row]
        lines.append(','.join(formatted_fields))
    
    return '\n'.join(lines) + '\n'


def _quote_field(field: str) -> str:
    """
    Quote a field if it contains comma, quote, or newline.
    Escape internal quotes by doubling them.
    """
    if ',' in field or '"' in field or '\n' in field:
        # Need to quote
        escaped = field.replace('"', '""')
        return f'"{escaped}"'
    else:
        return field
