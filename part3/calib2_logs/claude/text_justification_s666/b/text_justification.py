def full_justify(words: list[str], max_width: int) -> list[str]:
    """
    Format a list of words into fully-justified lines of exactly max_width characters.
    
    - Greedy packing: add words to the current line while they fit
    - Non-last lines: fully justified with extra spaces distributed left-to-right
    - Last line: left-justified with trailing spaces
    - Single word lines: left-justified with trailing padding
    """
    if not words:
        return []
    
    result = []
    current_line = []
    current_length = 0
    
    for word in words:
        # Check if adding this word would exceed max_width
        # current_length is the sum of word lengths
        # We need at least len(current_line) spaces (one between each pair of words)
        # So total would be: current_length + len(word) + len(current_line)
        if current_length + len(word) + len(current_line) <= max_width:
            current_line.append(word)
            current_length += len(word)
        else:
            # Current line is full, justify it and start a new line
            result.append(justify_line(current_line, max_width, False))
            current_line = [word]
            current_length = len(word)
    
    # Handle the last line (left-justified)
    if current_line:
        result.append(justify_line(current_line, max_width, True))
    
    return result


def justify_line(words: list[str], max_width: int, is_last: bool) -> str:
    """
    Justify a single line of words.
    
    - If is_last is True: left-justify with trailing spaces
    - If single word: left-justify with trailing spaces
    - Otherwise: fully justify with extra spaces distributed left-to-right
    """
    if is_last or len(words) == 1:
        # Left-justify: single spaces between words, pad with trailing spaces
        line = ' '.join(words)
        return line + ' ' * (max_width - len(line))
    
    # Multiple words, not last line: fully justify
    total_word_length = sum(len(word) for word in words)
    total_spaces = max_width - total_word_length
    gaps = len(words) - 1
    
    spaces_per_gap = total_spaces // gaps
    extra_spaces = total_spaces % gaps
    
    line = ''
    for i, word in enumerate(words[:-1]):
        line += word
        # Add base spaces plus one extra if this gap gets an extra space
        line += ' ' * (spaces_per_gap + (1 if i < extra_spaces else 0))
    
    line += words[-1]
    return line
