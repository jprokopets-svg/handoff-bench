
import csv
import io

def process_csv(text: str):
    """
    Parses RFC-4180-style CSV, applies a fixed transform, and returns the
    re-serialized CSV with a trailing newline.
    """
    if not text:
        raise ValueError("Empty input")

    f = io.StringIO(text)
    
    # Use strict=True to enforce RFC-4180 for parsing errors.
    reader = csv.reader(f, strict=True)
    
    try:
        try:
            header = next(reader)
        except StopIteration:
            # This handles empty input or input with only newlines
            raise ValueError("Empty input: no header row")

        data = []
        # The row number for error reporting should start from 2 for data rows.
        for i, row in enumerate(reader, start=2):
            if len(row) != len(header):
                raise ValueError(f"Row {i} has a different number of columns than the header")
            data.append(row)

    except csv.Error as e:
        # This will now catch parsing errors like unterminated quotes because of strict=True
        raise ValueError(f"CSV parsing error: {e}")

    # --- Transformation ---

    # (1) Drop rows where 'status' is 'skip'
    try:
        status_col_index = header.index('status')
        data = [row for row in data if row[status_col_index] != 'skip']
    except ValueError:
        # 'status' column not found, do nothing.
        pass

    # (2) Sort by 'sort' column if it exists
    try:
        sort_col_index = header.index('sort')

        def sort_key(row):
            value = row[sort_col_index]
            try:
                # Attempt to convert to float for numeric sorting
                return (0, float(value))
            except (ValueError, TypeError):
                # Fallback to string sorting
                return (1, value)

        # Python's sort is stable
        data.sort(key=sort_key)
    except ValueError:
        # 'sort' column not found, do nothing.
        pass

    # --- Formatting ---
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    
    writer.writerow(header)
    writer.writerows(data)

    return output.getvalue()
