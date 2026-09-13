import re


def process_csv(text):
    """
    Parse, transform, and format a CSV according to RFC-4180 with specific rules.
    
    PARSE: First row is header, fields separated by commas, quoted fields allowed,
           "" escapes quotes inside quoted fields, fields can span newlines.
    TRANSFORM: Drop rows where 'status' column equals 'skip', sort by 'sort' column
               (numeric values first, then lexicographic).
    FORMAT: Re-serialize as CSV with trailing newline.
    """
    
    # Validate input
    if not text:
        raise ValueError("Empty input")
    
    # Parse CSV
    rows = parse_csv(text)
    
    if not rows:
        raise ValueError("Empty input")
    
    header = rows[0]
    data_rows = rows[1:]
    
    # Validate all rows have same column count as header
    for row in data_rows:
        if len(row) != len(header):
            raise ValueError(f"Row has {len(row)} columns, expected {len(header)}")
    
    # Transform: drop rows where status == 'skip'
    status_idx = None
    if 'status' in header:
        status_idx = header.index('status')
        data_rows = [row for row in data_rows if row[status_idx] != 'skip']
    
    # Transform: sort by 'sort' column if it exists
    if 'sort' in header:
        sort_idx = header.index('sort')
        
        def sort_key(row):
            value = row[sort_idx]
            try:
                numeric_value = float(value)
                # Numeric values sort first (group 0), then by numeric value
                return (0, numeric_value, "")
            except ValueError:
                # Non-numeric values sort second (group 1), then lexicographically
                return (1, float('inf'), value)
        
        data_rows.sort(key=sort_key)
    
    # Format: re-serialize as CSV
    output_rows = [header] + data_rows
    result = format_csv(output_rows)
    
    return result


def parse_csv(text):
    """
    Parse RFC-4180 CSV format.
    Returns list of rows, where each row is a list of fields.
    Raises ValueError on invalid input.
    """
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
                    # Escaped quote
                    current_field.append('"')
                    i += 2
                    continue
                else:
                    # End of quoted field
                    in_quotes = False
                    i += 1
                    continue
            else:
                # Regular character inside quotes
                current_field.append(char)
                i += 1
                continue
        else:
            # Not in quotes
            if char == '"':
                # Start of quoted field
                in_quotes = True
                i += 1
                continue
            elif char == ',':
                # Field separator
                current_row.append(''.join(current_field))
                current_field = []
                i += 1
                continue
            elif char == '\n':
                # Row separator
                current_row.append(''.join(current_field))
                current_field = []
                if current_row:  # Only add non-empty rows
                    rows.append(current_row)
                current_row = []
                i += 1
                continue
            else:
                # Regular character
                current_field.append(char)
                i += 1
                continue
    
    # Handle end of input
    if in_quotes:
        raise ValueError("Unterminated quoted field")
    
    # Add final field and row if any
    current_row.append(''.join(current_field))
    if current_row and current_row != ['']:
        rows.append(current_row)
    elif current_row == [''] and rows:  # Empty field at end
        rows.append(current_row)
    
    return rows


def format_csv(rows):
    """
    Format rows as RFC-4180 CSV.
    Quote fields that contain comma, quote, or newline.
    Escape quotes by doubling.
    """
    lines = []
    
    for row in rows:
        formatted_fields = []
        for field in row:
            # Check if field needs quoting
            needs_quoting = ',' in field or '"' in field or '\n' in field
            
            if needs_quoting:
                # Escape quotes by doubling
                escaped_field = field.replace('"', '""')
                formatted_fields.append(f'"{escaped_field}"')
            else:
                formatted_fields.append(field)
        
        lines.append(','.join(formatted_fields))
    
    # Join with newlines and add trailing newline
    return '\n'.join(lines) + '\n'
