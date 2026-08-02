import re

def parse_json(text):
    text = text.strip()
    if not text:
        raise ValueError("Empty input")

    value, end_index = _parse_value(text, 0)
    remaining = text[end_index:].strip()
    if remaining:
        raise ValueError("Trailing content after JSON value")
    return value

def _parse_value(text, index):
    text_len = len(text)
    while index < text_len and text[index].isspace():
        index += 1

    if index >= text_len:
        raise ValueError("Unexpected end of input")

    if text[index:].startswith('null'):
        return None, index + 4
    elif text[index:].startswith('true'):
        return True, index + 4
    elif text[index:].startswith('false'):
        return False, index + 5
    elif text[index] == '"':
        return _parse_string(text, index)
    elif text[index] == '[':
        return _parse_array(text, index)
    elif text[index] == '{':
        return _parse_object(text, index)
    elif text[index] == '-' or text[index].isdigit():
        return _parse_number(text, index)
    else:
        raise ValueError(f"Unexpected character at index {index}: {text[index]}")

def _parse_string(text, index):
    start = index + 1
    end = start
    while end < len(text) and text[end] != '"':
        if text[end] == '\\' and end + 1 < len(text):
            end += 2
        else:
            end += 1
    if end >= len(text) or text[end] != '"':
        raise ValueError("Unclosed string")
    
    s = text[start:end]
    
    # Validate escapes and control characters
    if re.search(r'[\x00-\x1f]', s):
        raise ValueError("Raw control characters in string")
    if re.search(r'\\u[0-9a-fA-F]{0,3}[^0-9a-fA-F]', s) or re.search(r'\\u[0-9a-fA-F]{5,}', s):
        raise ValueError("Invalid unicode escape sequence")
    if re.search(r'\\(?!["\\/bfnrtu])', s):
        raise ValueError("Invalid escape sequence")

    s = s.encode('utf-8').decode('unicode_escape')
    return s, end + 1

def _parse_array(text, index):
    arr = []
    index += 1  # Skip '['

    while True:
        while index < len(text) and text[index].isspace():
            index += 1

        if index >= len(text):
            raise ValueError("Unclosed array")

        if text[index] == ']':
            return arr, index + 1
        
        if arr:
            if text[index] != ',':
                raise ValueError("Missing comma in array")
            index += 1
            while index < len(text) and text[index].isspace():
                index += 1
            if index >= len(text) or text[index] == ']':
                raise ValueError("Trailing comma in array")

        value, new_index = _parse_value(text, index)
        arr.append(value)
        index = new_index

def _parse_object(text, index):
    obj = {}
    index += 1  # Skip '{'

    while True:
        while index < len(text) and text[index].isspace():
            index += 1

        if index >= len(text):
            raise ValueError("Unclosed object")

        if text[index] == '}':
            return obj, index + 1

        if obj:
            if text[index] != ',':
                raise ValueError("Missing comma in object")
            index += 1
            while index < len(text) and text[index].isspace():
                index += 1
            if index >= len(text) or text[index] == '}':
                raise ValueError("Trailing comma in object")

        key, new_index = _parse_string(text, index)
        index = new_index

        while index < len(text) and text[index].isspace():
            index += 1

        if index >= len(text) or text[index] != ':':
            raise ValueError("Missing colon in object")
        
        index += 1 # Skip ':'

        value, new_index = _parse_value(text, index)
        obj[key] = value
        index = new_index

def _parse_number(text, index):
    match = re.match(r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?', text[index:])
    if not match:
        raise ValueError("Invalid number format")
    
    num_str = match.group(0)
    if num_str.startswith('0') and len(num_str) > 1 and num_str[1].isdigit():
        raise ValueError("Numbers with leading zeros are not allowed")
    if num_str.endswith('.'):
        raise ValueError("Numbers cannot end with a decimal point")
    
    try:
        if '.' in num_str or 'e' in num_str or 'E' in num_str:
            return float(num_str), index + match.end()
        else:
            return int(num_str), index + match.end()
    except ValueError:
        raise ValueError("Invalid number format")
