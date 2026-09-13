
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
    
    try:
        reader = csv.reader(f, strict=False)
        
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("Empty input: no header row")

        data = []
        for i, row in enumerate(reader):
            if len(row) != len(header):
                raise ValueError(f"Row {i+2} has a different number of columns than the header")
            data.append(row)

    except csv.Error as e:
        raise ValueError(f"CSV parsing error: {e}")

    try:
        status_col_index = header.index('status')
        data = [row for row in data if row[status_col_index] != 'skip']
    except ValueError:
        pass

    try:
        sort_col_index = header.index('sort')

        def sort_key(row):
            value = row[sort_col_index]
            try:
                return (0, float(value))
            except (ValueError, TypeError):
                return (1, value)

        data.sort(key=sort_key)
    except ValueError:
        pass

    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    
    writer.writerow(header)
    writer.writerows(data)

    return output.getvalue()
