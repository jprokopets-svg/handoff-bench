import re
from typing import List, Tuple, Optional

def process_csv(text: str) -> str:
    """
    Parse RFC-4180 CSV, apply transformations, and re-serialize.
    
    Transformations:
    1. Drop rows where column 'status' equals 'skip' exactly
    2. If column 'sort' exists, sort rows stably by that column:
       - Rows whose value parses as float sort numerically (ascending)
       - Then rows whose value doesn't parse as float sort lexicographically (ascending)
    
    Returns CSV string with trailing newline.
    """
    if not text:
        raise ValueError("Empty input")
    
    # Parse CSV
    rows = parse_csv(text)
    if not rows:
        raise ValueError("No rows parsed")
    
    # First row is header
    header = rows[0]
    data_rows = rows[1:]
    
    # Validate column counts
    expected_cols = len(header)
    for i, row in enumerate(data_rows):
        if len(row) != expected_cols:
            raise ValueError(f"Row {i+1} has different column count")
    
    # Transform: drop rows where 'status' column equals 'skip'
    if 'status' in header:
        status_idx = header.index('status')
        data_rows = [row for row in data_rows if row[status_idx] != 'skip']
    
    # Transform: sort by 'sort' column if present
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
    
    # Format: serialize back to CSV
    result_rows = [header] + data_rows
    return serialize_csv(result_rows) + '\n'


def parse_csv(text: str) -> List[List[str]]:
    """
    Parse RFC-4180 CSV string into list of rows (list of fields).
    Handles quoted fields, escaped quotes, and newlines in quoted fields.
    """
    rows = []
    pos = 0
    length = len(text)
    
    while pos < length:
        row = []
        while True:
            # Parse a field
            field, pos = parse_field(text, pos)
            row.append(field)
            
            # Check for comma or end of row
            if pos >= length:
                # End of text
                rows.append(row)
                return rows
            elif text[pos] == ',':
                pos += 1  # Skip comma
                continue
            elif text[pos] == '\n':
                pos += 1  # Skip newline
                rows.append(row)
                break
            else:
                # Should not happen with proper CSV
                raise ValueError(f"Unexpected character at position {pos}")
    
    return rows


def parse_field(text: str, pos: int) -> Tuple[str, int]:
    """
    Parse a single CSV field starting at position pos.
    Returns (field_value, new_position).
    """
    length = len(text)
    
    if pos >= length:
        return "", pos
    
    if text[pos] == '"':
        # Quoted field
        pos += 1  # Skip opening quote
        field_parts = []
        
        while pos < length:
            if text[pos] == '"':
                # Could be escaped quote or end of field
                if pos + 1 < length and text[pos + 1] == '"':
                    # Escaped quote
                    field_parts.append('"')
                    pos += 2
                else:
                    # End of field
                    pos += 1
                    # Skip to comma or newline or end
                    while pos < length and text[pos] not in (',', '\n'):
                        pos += 1
                    return ''.join(field_parts), pos
            else:
                field_parts.append(text[pos])
                pos += 1
        
        # If we get here, we reached end of text without closing quote
        raise ValueError("Unterminated quoted field")
    else:
        # Unquoted field
        start = pos
        while pos < length and text[pos] not in (',', '\n'):
            pos += 1
        field = text[start:pos]
        return field, pos


def serialize_csv(rows: List[List[str]]) -> str:
    """
    Serialize rows to CSV string.
    Quotes fields only when necessary.
    """
    result_rows = []
    for row in rows:
        result_fields = []
        for field in row:
            # Check if field needs quoting
            needs_quote = False
            if field is None:
                field = ""
            if any(c in field for c in (',', '"', '\n', '\r')):
                needs_quote = True
            
            if needs_quote:
                # Escape quotes by doubling
                escaped = field.replace('"', '""')
                result_fields.append(f'"{escaped}"')
            else:
                result_fields.append(field)
        
        result_rows.append(','.join(result_fields))
    
    return '\n'.join(result_rows)