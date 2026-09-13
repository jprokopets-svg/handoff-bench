
import csv
import io

def process_csv(text: str) -> str:
    if not text:
        raise ValueError("Empty input")

    try:
        reader = csv.reader(io.StringIO(text))
        header = next(reader)
        data = list(reader)
    except (csv.Error, StopIteration) as e:
        raise ValueError("CSV parsing error") from e

    if any(len(row) != len(header) for row in data):
        raise ValueError("Inconsistent row length")

    if 'status' in header:
        status_index = header.index('status')
        data = [row for row in data if row[status_index] != 'skip']

    if 'sort' in header:
        sort_index = header.index('sort')
        def sort_key(row):
            value = row[sort_index]
            try:
                return (0, float(value))
            except ValueError:
                return (1, value)
        data.sort(key=sort_key)

    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(data)

    result = output.getvalue()
    if not result.endswith('\n'):
        result += '\n'
        
    return result
