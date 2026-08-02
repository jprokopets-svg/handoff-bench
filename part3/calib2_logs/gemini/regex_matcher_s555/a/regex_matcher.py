import re

def full_match(pattern, text):
    try:
        compiled_pattern = re.compile(pattern)
    except re.error as e:
        raise ValueError(str(e))
    
    match = compiled_pattern.fullmatch(text)
    return match is not None
